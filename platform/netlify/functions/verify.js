const crypto = require('crypto');
const { getPool } = require('./_db');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };
  try {
    const { email, code } = JSON.parse(event.body || '{}');
    const codeHash = crypto.createHash('sha256').update(String(code || '')).digest('hex');
    const db = getPool();
    const result = await db.query("UPDATE store_builder.users SET email_verified=TRUE, verification_code_hash=NULL, verification_expires_at=NULL, updated_at=NOW() WHERE lower(email)=lower($1) AND verification_code_hash=$2 AND verification_expires_at>NOW() RETURNING id", [email, codeHash]);
    if (!result.rowCount) return { statusCode: 400, body: JSON.stringify({ error: 'Invalid or expired verification code.' }) };
    return { statusCode: 200, body: JSON.stringify({ ok: true }) };
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: JSON.stringify({ error: 'Verification failed.' }) };
  }
};