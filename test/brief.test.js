'use strict';
// Запуск: npm test
const assert = require('assert');
const { handleBrief } = require('../lib/brief');

const quiet = { log() {}, error() {} };
const good = { name: 'Тест', contact: '@test', about: 'Нужен сториборд на 20 кадров', type: 'Сториборд', budget: '50 000' };

(async () => {
  // 1. валидация
  let r = await handleBrief({ name: '', contact: '', about: '' }, { env: {}, log: quiet });
  assert.strictEqual(r.status, 400); assert.strictEqual(r.body.ok, false);
  r = await handleBrief('nope', { env: {}, log: quiet });
  assert.strictEqual(r.status, 400);

  // 2. honeypot → ok, но канал не вызывается
  let calls = [];
  global.fetch = async (url, init) => { calls.push({ url, init }); return { ok: true, text: async () => '{}' }; };
  r = await handleBrief({ ...good, website: 'spam' }, { env: { TELEGRAM_BOT_TOKEN: 't', TELEGRAM_CHAT_ID: '1' }, log: quiet });
  assert.strictEqual(r.status, 200); assert.strictEqual(calls.length, 0);

  // 3. dev без каналов → ok + dev
  r = await handleBrief(good, { env: {}, log: quiet });
  assert.deepStrictEqual(r.body, { ok: true, dev: true });

  // 4. production без каналов → 503
  r = await handleBrief(good, { env: { NODE_ENV: 'production' }, log: quiet });
  assert.strictEqual(r.status, 503);

  // 5. telegram + email вызываются, текст содержит поля
  calls = [];
  r = await handleBrief(good, { env: { TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '42', RESEND_API_KEY: 'k', BRIEF_TO_EMAIL: 'a@b.c' }, log: quiet });
  assert.strictEqual(r.status, 200);
  assert.strictEqual(calls.length, 2);
  const tg = JSON.parse(calls.find((c) => c.url.includes('telegram')).init.body);
  assert.strictEqual(tg.chat_id, '42');
  assert.ok(tg.text.includes('Сториборд') && tg.text.includes('@test'));
  const em = JSON.parse(calls.find((c) => c.url.includes('resend')).init.body);
  assert.deepStrictEqual(em.to, ['a@b.c']);
  assert.ok(em.subject.includes('Тест'));

  // 6. HTML экранируется
  calls = [];
  await handleBrief({ ...good, about: '<script>alert(1)</script> и ещё' }, { env: { TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '42' }, log: quiet });
  assert.ok(!JSON.parse(calls[0].init.body).text.includes('<script>'));

  // 7. все каналы упали → 502
  global.fetch = async () => ({ ok: false, status: 500, text: async () => 'boom' });
  r = await handleBrief(good, { env: { TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '42' }, log: quiet });
  assert.strictEqual(r.status, 502);

  // 8. один канал упал, другой ок → 200
  global.fetch = async (url) => url.includes('telegram') ? { ok: false, status: 500, text: async () => 'x' } : { ok: true, text: async () => '{}' };
  r = await handleBrief(good, { env: { TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '42', RESEND_API_KEY: 'k', BRIEF_TO_EMAIL: 'a@b.c' }, log: quiet });
  assert.strictEqual(r.status, 200);

  // 9. rate limit: 6-й запрос с одного IP → 429
  global.fetch = async () => ({ ok: true, text: async () => '{}' });
  const env = { TELEGRAM_BOT_TOKEN: 'tok', TELEGRAM_CHAT_ID: '42' };
  for (let i = 0; i < 5; i++) assert.strictEqual((await handleBrief(good, { env, ip: '9.9.9.9', log: quiet })).status, 200);
  assert.strictEqual((await handleBrief(good, { env, ip: '9.9.9.9', log: quiet })).status, 429);

  console.log('✓ brief handler: all tests passed');
})().catch((e) => { console.error('✗', e); process.exit(1); });
