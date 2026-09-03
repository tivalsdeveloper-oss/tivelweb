const { getPool } = require('./_db');

exports.handler = async () => {
  try {
    const db = getPool();
    const result = await db.query('SELECT id,slug,name,price_cents,currency,description,features FROM store_builder.packages WHERE active=TRUE ORDER BY price_cents');
    return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(result.rows) };
  } catch (e) {
    console.error(e);
    return { statusCode: 500, body: JSON.stringify({ error: 'Could not load packages.' }) };
  }
};