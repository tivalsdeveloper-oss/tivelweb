const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { getPool } = require('./_db');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };
  try {
    if (!process.env.JWT_SECRET) throw new Error('JWT_SECRET is not configured');
    const { identifier, password } = JSON.parse(event.body || '{}');
    const db = getPool();
    const result = await db.query('SELECT id,email,username,password_hash,email_verified FROM store_builder.users WHERE lower(email)=lower($1) OR lower(username)=lower($1) LIMIT 1', [identifier || '']);
    if (!result.rowCount || !(await bcrypt.compare(password || '', result.rows[0].password_hash))) return { statusCode: 401, body: JSON.stringify({ error: 'Invalid login details.' }) };
    const user = result.rows[0];
    if (!user.email_verified) return { statusCode: 403, body: JSON.stringify({ error: 'Verify your email first.', needsVerification: true, email: user.email }) };
    const token = jwt.sign({ sub: user.id, email: user.email, username: user.username }, process.env.JWT_SECRET, { expiresIn: '7d' });
    return { statusCode: 200, body: JSON.stringify({ token, user: { id: user.id, email: user.email, username: user.username } }) };
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: JSON.stringify({ error: 'Login failed.' }) };
  }
};