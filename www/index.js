const CC = 'https://live-command-center-production-31ed.up.railway.app';

const SOURCES = {
  usgs: 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson',
  eonet: 'https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100',
  nws: 'https://api.weather.gov/alerts/active'
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'no-store'
    }
  });
}

async function upstream(url) {
  try {
    const headers = { 'accept': 'application/json' };
    if (url.includes('api.weather.gov')) {
      headers['accept'] = 'application/geo+json';
      headers['user-agent'] = 'Eagle-Eyes-World-Data-Edge/1.0';
    }
    const r = await fetch(url, { headers });
    const body = await r.text();
    return new Response(body, {
      status: r.status,
      headers: {
        'content-type': r.headers.get('content-type') || 'application/json',
        'cache-control': 'no-store'
      }
    });
  } catch (e) {
    return json({ ok: false, error: 'upstream_unavailable', detail: String(e) }, 503);
  }
}

export default {
  async fetch(req) {
    const u = new URL(req.url);
    if (req.method !== 'GET') return json({ ok: false, error: 'method_not_allowed' }, 405);
    if (u.pathname === '/') return new Response('EAGLE EYES WORLD DATA EDGE ONLINE', { headers: { 'content-type': 'text/plain' } });
    if (u.pathname === '/healthz') return json({ ok: true, status: 'healthy', runtime: 'cloudflare-workers', timestamp: new Date().toISOString() });
    if (u.pathname === '/api/metrics') return upstream(`${CC}/api/metrics`);
    if (u.pathname === '/api/sources') return json({ ok: true, sources: Object.keys(SOURCES), commandCenter: CC, timestamp: new Date().toISOString() });
    if (u.pathname === '/api/events') {
      const key = (u.searchParams.get('source') || 'usgs').toLowerCase();
      if (!SOURCES[key]) return json({ ok: false, error: 'unknown_source', allowed: Object.keys(SOURCES) }, 400);
      return upstream(SOURCES[key]);
    }
    return json({ ok: false, error: 'not_found' }, 404);
  }
};
