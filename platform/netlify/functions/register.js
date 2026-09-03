const bcrypt = require('bcryptjs');
const crypto = require('crypto');
const nodemailer = require('nodemailer');
const { getPool } = require('./_db');

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };
  try {
    const { email, username, password } = JSON.parse(event.body || '{}');
    if (!email || !username || !password || password.length < 8) return { statusCode: 400, body: JSON.stringify({ error: 'Email, username and password (8+ characters) are required.' }) };
    const db = getPool();
    const exists = await db.query('SELECT 1 FROM store_builder.users WHERE lower(email)=lower($1) OR lower(username)=lower($2)', [email, username]);
    if (exists.rowCount) return { statusCode: 409, body: JSON.stringify({ error: 'Email or username already exists.' }) };
    const passwordHash = await bcrypt.hash(password, 12);
    const code = String(crypto.randomInt(100000, 1000000));
    const codeHash = crypto.createHash('sha256').update(code).digest('hex');
    await db.query("INSERT INTO store_builder.users(email,username,password_hash,verification_code_hash,verification_expires_at) VALUES($1,$2,$3,$4,NOW()+INTERVAL '15 minutes')", [email.trim(), username.trim(), passwordHash, codeHash]);
    if (process.env.GMAIL_USER && process.env.GMAIL_APP_PASSWORD) {
      const transporter = nodemailer.createTransport({ service: 'gmail', auth: { user: process.env.GMAIL_USER, pass: process.env.GMAIL_APP_PASSWORD } });
      await transporter.sendMail({ from: `tivalsdeveloper <${process.env.GMAIL_USER}>`, to: email, subject: 'Verify your tivalsdeveloper account', text: `Your verification code is ${code}. It expires in 15 minutes.` });
    }
    return { statusCode: 201, body: JSON.stringify({ ok: true, emailSent: Boolean(process.env.GMAIL_USER && process.env.GMAIL_APP_PASSWORD) }) };
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: JSON.stringify({ error: 'Could not create account.' }) };
  }
};