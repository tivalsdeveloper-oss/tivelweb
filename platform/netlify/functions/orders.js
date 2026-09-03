const jwt = require('jsonwebtoken');
const { getPool } = require('./_db');

function auth(event) {
  const header = event.headers.authorization || event.headers.Authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : '';
  return jwt.verify(token, process.env.JWT_SECRET);
}

exports.handler = async (event) => {
  try {
    if (!process.env.JWT_SECRET) throw new Error('JWT_SECRET is not configured');
    const claims = auth(event);
    const db = getPool();
    if (event.httpMethod === 'GET') {
      const result = await db.query(`SELECT o.id,o.business_name,o.business_type,o.status,o.payment_status,o.total_cents,o.currency,o.created_at,p.name AS package_name FROM store_builder.orders o JOIN store_builder.packages p ON p.id=o.package_id WHERE o.user_id=$1 ORDER BY o.created_at DESC`, [claims.sub]);
      return { statusCode: 200, body: JSON.stringify(result.rows) };
    }
    if (event.httpMethod === 'POST') {
      const { packageId, businessName, businessType, contactPhone, requirements } = JSON.parse(event.body || '{}');
      if (!packageId || !businessName) return { statusCode: 400, body: JSON.stringify({ error: 'Package and business name are required.' }) };
      const pkg = await db.query('SELECT id,price_cents,currency FROM store_builder.packages WHERE id=$1 AND active=TRUE', [packageId]);
      if (!pkg.rowCount) return { statusCode: 404, body: JSON.stringify({ error: 'Package not found.' }) };
      const p = pkg.rows[0];
      const result = await db.query(`INSERT INTO store_builder.orders(user_id,package_id,business_name,business_type,contact_phone,requirements,total_cents,currency) VALUES($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id,status,payment_status,created_at`, [claims.sub,p.id,businessName,businessType||null,contactPhone||null,requirements||null,p.price_cents,p.currency]);
      return { statusCode: 201, body: JSON.stringify(result.rows[0]) };
    }
    return { statusCode: 405, body: 'Method not allowed' };
  } catch (e) {
    console.error(e);
    return { statusCode: e.name === 'JsonWebTokenError' ? 401 : 500, body: JSON.stringify({ error: e.name === 'JsonWebTokenError' ? 'Please sign in again.' : 'Order request failed.' }) };
  }
};