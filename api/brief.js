'use strict';
// Vercel Serverless Function: POST /api/brief
const { handleBrief, clientIp } = require('../lib/brief');

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method Not Allowed' });
  }
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  const { status, body: out } = await handleBrief(body, { ip: clientIp(req) });
  res.status(status).json(out);
};
