'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { spawn } = require('node:child_process');
const MODEL = 'tinyllama:latest';
const BASE = 'http://127.0.0.1:11434';
const LOGDIR = path.join(__dirname, 'logs');
const clean = s => String(s).replace(/[\x00-\x08\x0b-\x1f\x7f-\x9f]/g, '');
let previousCPU = process.cpuUsage();
let previousTime = process.hrtime.bigint();

function metrics() {
  let total = 'unavailable', available = 'unavailable', storage = 'unavailable';
  try {
    const text = fs.readFileSync('/proc/meminfo', 'utf8');
    const value = name => {
      const match = text.match(new RegExp('^' + name + ':\\s+(\\d+)\\s+kB', 'm'));
      return match ? (Number(match[1]) / 1024).toFixed(0) + ' MiB' : 'unavailable';
    };
    total = value('MemTotal'); available = value('MemAvailable');
  } catch {}
  try {
    const stat = fs.statfsSync(__dirname);
    storage = (stat.bavail * stat.bsize / 1024 ** 3).toFixed(1) + ' GiB';
  } catch {}
  const now = process.hrtime.bigint(), cpu = process.cpuUsage();
  const elapsed = Number(now - previousTime) / 1000;
  const percent = 100 * (cpu.user + cpu.system - previousCPU.user - previousCPU.system) / elapsed;
  previousCPU = cpu; previousTime = now;
  return { time: new Date().toISOString(), total, available, storage,
    processCPU: Number.isFinite(percent) ? percent.toFixed(1) + '%' : 'unavailable',
    processRAM: (process.memoryUsage().rss / 1024 ** 2).toFixed(1) + ' MiB' };
}

async function api(route, body, timeout = 3000) {
  const response = await fetch(BASE + route, {
    method: body ? 'POST' : 'GET', redirect: 'error',
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(timeout)
  });
  if (!response.ok) throw new Error('Ollama HTTP ' + response.status);
  const data = await response.json();
  if (data.error) throw new Error(clean(data.error));
  return data;
}

async function tags() {
  const data = await api('/api/tags');
  if (!Array.isArray(data.models)) throw new Error('Unexpected Ollama response');
  return data;
}

async function ensureServer() {
  try { return await tags(); }
  catch (error) {
    if (error.cause?.code !== 'ECONNREFUSED') throw error;
  }
  const output = fs.openSync(path.join(LOGDIR, 'ollama-local.log'), 'a', 0o600);
  let child;
  try {
    child = spawn('ollama', ['serve'], { detached: true,
      stdio: ['ignore', output, output], env: { ...process.env,
        OLLAMA_HOST: '127.0.0.1:11434', OLLAMA_NUM_PARALLEL: '1',
        OLLAMA_MAX_LOADED_MODELS: '1', OLLAMA_CONTEXT_LENGTH: '512' } });
    await new Promise((resolve, reject) => {
      child.once('spawn', resolve); child.once('error', reject);
    });
    child.unref();
  } finally { fs.closeSync(output); }
  for (let attempt = 0; attempt < 10; attempt++) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    try { return await tags(); } catch {}
  }
  throw new Error('Server unavailable; inspect logs/ollama-local.log');
}

async function answer(prompt) {
  if (!prompt.trim() || prompt.length > 500) throw new Error('Use a question of 1-500 characters.');
  const data = await api('/api/generate', { model: MODEL, prompt,
    system: 'Give a brief answer. You have no live telemetry or tools. Do not invent measurements or claim you performed actions.',
    stream: false, keep_alive: 0,
    options: { num_ctx: 512, num_predict: 128, num_thread: 2, num_batch: 32, temperature: 0.2 }
  }, 180000);
  if (data.done !== true || typeof data.response !== 'string' || !data.response.trim()) {
    throw new Error('No complete answer received.');
  }
  return clean(data.response);
}

async function main() {
  const blessed = require('blessed');
  if (process.argv.includes('--check-deps')) return;
  fs.mkdirSync(LOGDIR, { recursive: true, mode: 0o700 });
  const sessionName = 'eagle-eyes-chat-' + new Date().toISOString().replace(/[:.]/g, '-') + '-' + process.pid + '.ndjson';
  const session = fs.openSync(path.join(LOGDIR, sessionName), 'ax', 0o600);
  const screen = blessed.screen({ smartCSR: true, title: 'Eagle Eyes Local', fullUnicode: true });
  const box = (label, top, left, width, height, color) => blessed.box({ parent: screen,
    label, top, left, width, height, tags: false, border: { type: 'line' },
    style: { border: { fg: color } } });
  const header = box(' EAGLE EYES / ALSTRA ', 0, 0, '100%', 3, 'cyan');
  header.setContent('Local status + TinyLlama | /status /reconnect /quit');
  const hardware = box(' LOCAL MEASUREMENTS ', 3, 0, '50%', 10, 'cyan');
  const services = box(' CONNECTIONS ', 3, '50%', '50%', 10, 'yellow');
  const transcript = blessed.log({ parent: screen, top: 13, bottom: 3, width: '100%',
    label: ' AI ANSWERS ARE UNVERIFIED | PGUP/PGDN ', border: { type: 'line' },
    tags: false, scrollback: 250, mouse: true, keys: true, scrollOnInput: true });
  const input = blessed.textbox({ parent: screen, bottom: 0, height: 3, width: '100%',
    label: ' Ask TinyLlama (max 500 characters) ', border: { type: 'line' },
    inputOnFocus: true, tags: false });
  let connection = 'Checking...', checked = 'not yet', busy = false, checking = false, closed = false;
  let statusTimer, healthTimer;
  function message(role, text) {
    const safe = clean(text);
    transcript.log('[' + role + '] ' + safe);
    try {
      fs.writeSync(session, JSON.stringify({ at: new Date().toISOString(), role, text: safe }) + '\n');
      fs.fsyncSync(session);
    } catch (error) { transcript.log('[SAVE ERROR] ' + clean(error.message)); }
    screen.render();
  }
  function draw() {
    if (closed) return;
    const m = metrics();
    hardware.setContent('UTC ' + m.time.slice(11, 19) + '\nRAM total: ' + m.total +
      '\nRAM available: ' + m.available + '\nDisk available: ' + m.storage +
      '\nDashboard RAM: ' + m.processRAM + '\nDashboard CPU: ' + m.processCPU +
      '\nCPU 100% = one core; RAM: /proc/meminfo');
    services.setContent('Ollama: ' + connection + '\nChecked UTC: ' + checked +
      '\nModel: tinyllama\nRequest: ' + (busy ? 'working' : 'idle') +
      '\nGPU temp / power: unavailable\nRemote telemetry: not connected');
    screen.render();
  }
  async function refresh(start = false) {
    if (checking || closed) return;
    checking = true;
    try {
      const data = await (start ? ensureServer() : tags());
      const present = data.models.some(m => m.name === MODEL || m.name === 'tinyllama');
      connection = present ? 'responding; model installed' : 'responding; model missing';
      if (start && !present) message('SETUP', 'Run ollama pull tinyllama in a separate Termux session.');
    } catch (error) { connection = 'unavailable'; if (start && !closed) message('ERROR', error.message); }
    finally { checked = new Date().toISOString().slice(11, 19); checking = false; draw(); }
  }
  function quit() {
    if (closed) return;
    closed = true; clearInterval(statusTimer); clearInterval(healthTimer);
    fs.closeSync(session); screen.destroy();
    console.log('Chat saved: ' + path.join(LOGDIR, sessionName));
    process.exit(0);
  }
  async function submit(raw) {
    const text = String(raw || '').trim();
    input.clearValue(); setImmediate(() => { if (!closed) input.focus(); });
    if (!text) return;
    if (text === '/quit') return quit();
    if (busy || checking) return message('STATUS', 'Please wait for the current operation.');
    if (text === '/status') { await refresh(); return message('STATUS', JSON.stringify(metrics())); }
    if (text === '/reconnect') return refresh(true);
    if (text.length > 500) return message('STATUS', 'Please shorten the question to 500 characters.');
    busy = true; message('YOU', text); draw();
    try { const reply = await answer(text); if (!closed) message('AI UNVERIFIED', reply); }
    catch (error) { if (!closed) message('ERROR', error.message + ' Try /reconnect if Ollama stopped.'); }
    finally { busy = false; draw(); }
  }
  input.on('submit', text => { submit(text).catch(error => message('ERROR', error.message)); });
  input.on('cancel', () => setImmediate(() => { if (!closed) input.focus(); }));
  screen.key(['C-c'], quit);
  screen.key(['pageup'], () => { transcript.scroll(-5); screen.render(); });
  screen.key(['pagedown'], () => { transcript.scroll(5); screen.render(); });
  process.on('SIGTERM', quit); process.on('SIGINT', quit);
  message('SAVED SESSION', 'logs/' + sessionName);
  message('INFO', 'Measurements come from this device/process. AI answers are text only and run no commands.');
  input.focus(); draw();
  statusTimer = setInterval(draw, 5000);
  healthTimer = setInterval(() => { if (!busy) void refresh(); }, 30000);
  await refresh(true);
}

module.exports = { metrics, answer, tags, ensureServer, clean };
if (require.main === module) main().catch(error => { console.error(clean(error.message)); process.exitCode = 1; });
