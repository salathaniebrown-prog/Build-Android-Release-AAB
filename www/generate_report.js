const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

const logFilePath = path.join(__dirname, 'transactions.log');
const configPath = path.join(__dirname, 'config.json');

if (!fs.existsSync(configPath)) {
  console.log('Error: config.json missing from active directory.');
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const ENCRYPTION_KEY = crypto.scryptSync('SovereignSecretKey2026', 'salt', 32); 

if (!fs.existsSync(logFilePath)) {
  console.log('No historical transaction logs found yet in this workspace. Staging clean container.');
  fs.writeFileSync(logFilePath, '', 'utf8');
  process.exit(0);
}

const lines = fs.readFileSync(logFilePath, 'utf8').split('\n');

console.log('==================================================');
console.log('      UPGRADED HIGH-TIER ORCHESTRATION REPORT     ');
console.log(` Active Model Profile: ${config.ORCHESTRATION_MODEL} `);
console.log(` Max Pool Threshold:  ${config.MAX_CREDIT_POINTS.toLocaleString()} Points `);
console.log('==================================================\n');

lines.forEach(line => {
  if (!line.trim()) return;
  try {
    const logEntry = JSON.parse(line);
    const parts = logEntry.protected_payload.split(':');
    
    const iv = Buffer.from(parts[0], 'hex');
    const authTag = Buffer.from(parts[1], 'hex');
    const encryptedText = Buffer.from(parts[2], 'hex');
    
    const decipher = crypto.createDecipheriv('aes-256-gcm', ENCRYPTION_KEY, iv);
    decipher.setAuthTag(authTag);
    
    let decrypted = decipher.update(encryptedText, 'hex', 'utf8') + decipher.final('utf8');
    const parsedData = JSON.parse(decrypted);
    
    console.log(`[ORCHESTRATOR PACKET VERIFIED]`);
    console.log(`- Timestamp:       ${logEntry.timestamp}`);
    console.log(`- Client Origin:   ${parsedData.ip}`);
    console.log(`- Core Directive:  ${parsedData.transaction.action}`);
    console.log(`- Points Assigned: ${parsedData.transaction.credits_applied.toLocaleString()}`);
    console.log(`- Monitored Asset: ${parsedData.transaction.target_asset}`);
    console.log('--------------------------------------------------');
  } catch (err) {}
});
