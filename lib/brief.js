'use strict';
/*
  Общая логика обработки брифа. Используется и в Vercel-функции (api/brief.js),
  и в локальном/VPS-сервере (server.js). Внешних зависимостей нет (Node 18+).

  Уведомления (задаются переменными окружения, см. .env.example):
    - Telegram: TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID
    - Email через Resend: RESEND_API_KEY + BRIEF_TO_EMAIL (+ BRIEF_FROM_EMAIL)
  Можно включить оба канала. Если ни один не настроен, в production вернётся
  ошибка 503, а в разработке бриф просто печатается в консоль.
*/

const LIMITS = { name: 120, contact: 200, type: 60, about: 4000, budget: 120 };
const REQUIRED = ['name', 'contact', 'about'];

class BriefError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

function clean(v, max) {
  if (v === undefined || v === null) return '';
  return String(v).replace(/\r\n?/g, '\n').replace(/[^\S\n]+/g, ' ').trim().slice(0, max);
}

function validate(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) throw new BriefError(400, 'Некорректный запрос.');
  // honeypot: боты заполняют скрытое поле — отвечаем «ок», но ничего не шлём
  if (body.website) return null;

  const brief = {};
  for (const k of Object.keys(LIMITS)) brief[k] = clean(body[k], LIMITS[k]);
  const missing = REQUIRED.filter((k) => !brief[k]);
  if (missing.length) throw new BriefError(400, 'Заполните имя, контакт и описание проекта.');
  if (brief.about.length < 5) throw new BriefError(400, 'Расскажите о проекте чуть подробнее.');
  brief.page = clean(body.page, 300);
  return brief;
}

// ---- простой in-memory rate limit (best-effort; на serverless живёт в тёплом инстансе)
const hits = new Map();
const WINDOW_MS = 10 * 60 * 1000, MAX_PER_WINDOW = 5;
function rateLimit(ip) {
  const now = Date.now();
  const list = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  if (list.length >= MAX_PER_WINDOW) throw new BriefError(429, 'Слишком много запросов. Попробуйте через несколько минут.');
  list.push(now); hits.set(ip, list);
  if (hits.size > 5000) for (const [k, v] of hits) if (!v.some((t) => now - t < WINDOW_MS)) hits.delete(k);
}

// ---- форматирование
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function fmtDate(d) {
  return new Intl.DateTimeFormat('ru-RU', { dateStyle: 'short', timeStyle: 'short', timeZone: process.env.BRIEF_TZ || 'Europe/Moscow' }).format(d);
}

function telegramText(b, meta) {
  const lines = [
    '🎨 <b>Новый бриф с сайта</b>',
    '',
    `<b>Имя:</b> ${esc(b.name)}`,
    `<b>Контакт:</b> ${esc(b.contact)}`,
    b.type ? `<b>Тип проекта:</b> ${esc(b.type)}` : null,
    b.budget ? `<b>Бюджет:</b> ${esc(b.budget)}` : null,
    '',
    `<b>О проекте:</b>`,
    esc(b.about),
    '',
    `<i>${esc(fmtDate(meta.date))}${meta.ip ? ' · ' + esc(meta.ip) : ''}</i>`,
  ];
  return lines.filter((l) => l !== null).join('\n');
}

function emailHtml(b, meta) {
  const row = (k, v) => v ? `<tr><td style="padding:6px 12px 6px 0;color:#6E6157;white-space:nowrap;vertical-align:top">${k}</td><td style="padding:6px 0">${esc(v).replace(/\n/g, '<br>')}</td></tr>` : '';
  return `<div style="font-family:system-ui,sans-serif;font-size:15px;line-height:1.5;color:#17120F;max-width:640px">
<h2 style="font-weight:600;margin:0 0 16px">Новый бриф с сайта</h2>
<table style="border-collapse:collapse">${row('Имя', b.name)}${row('Контакт', b.contact)}${row('Тип проекта', b.type)}${row('Бюджет', b.budget)}</table>
<h3 style="font-weight:600;margin:20px 0 8px">О проекте</h3>
<p style="white-space:pre-wrap;margin:0">${esc(b.about)}</p>
<p style="color:#6E6157;font-size:13px;margin-top:24px">${esc(fmtDate(meta.date))}${meta.ip ? ' · ' + esc(meta.ip) : ''}${b.page ? ' · ' + esc(b.page) : ''}</p>
</div>`;
}

function emailText(b, meta) {
  return [`Новый бриф с сайта`, ``, `Имя: ${b.name}`, `Контакт: ${b.contact}`, b.type && `Тип проекта: ${b.type}`, b.budget && `Бюджет: ${b.budget}`, ``, `О проекте:`, b.about, ``, fmtDate(meta.date)].filter(Boolean).join('\n');
}

// ---- каналы уведомлений
async function fetchJson(url, init, timeoutMs = 10000) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...init, signal: ctrl.signal });
    const text = await res.text();
    if (!res.ok) throw new Error(`${res.status} ${text.slice(0, 300)}`);
    return text;
  } finally { clearTimeout(t); }
}

async function sendTelegram(b, meta, env) {
  const token = env.TELEGRAM_BOT_TOKEN, chatId = env.TELEGRAM_CHAT_ID;
  await fetchJson(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text: telegramText(b, meta), parse_mode: 'HTML', disable_web_page_preview: true }),
  });
}

async function sendEmail(b, meta, env) {
  const to = env.BRIEF_TO_EMAIL.split(',').map((s) => s.trim()).filter(Boolean);
  const from = env.BRIEF_FROM_EMAIL || 'Бриф с сайта <onboarding@resend.dev>';
  const replyTo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(b.contact) ? b.contact : undefined;
  await fetchJson('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${env.RESEND_API_KEY}` },
    body: JSON.stringify({ from, to, reply_to: replyTo, subject: `Бриф: ${b.name}${b.type ? ' · ' + b.type : ''}`, html: emailHtml(b, meta), text: emailText(b, meta) }),
  });
}

function channels(env) {
  const list = [];
  if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) list.push(['telegram', sendTelegram]);
  if (env.RESEND_API_KEY && env.BRIEF_TO_EMAIL) list.push(['email', sendEmail]);
  return list;
}

/**
 * Обрабатывает бриф. Возвращает { status, body } для HTTP-ответа.
 * @param {object} rawBody распарсенный JSON тела запроса
 * @param {{ ip?: string, env?: object, log?: function }} meta
 */
async function handleBrief(rawBody, meta = {}) {
  const env = meta.env || process.env;
  const log = meta.log || console;
  try {
    if (meta.ip) rateLimit(meta.ip);
    const brief = validate(rawBody);
    if (!brief) return { status: 200, body: { ok: true } }; // honeypot

    const ctx = { date: new Date(), ip: meta.ip };
    const list = channels(env);
    if (!list.length) {
      if (env.NODE_ENV === 'production' || env.VERCEL) {
        log.error('[brief] no notification channel configured (TELEGRAM_* or RESEND_API_KEY + BRIEF_TO_EMAIL)');
        return { status: 503, body: { ok: false, error: 'Приём брифов временно не настроен.' } };
      }
      log.log('[brief] DEV — уведомления не настроены, бриф:\n' + emailText(brief, ctx));
      return { status: 200, body: { ok: true, dev: true } };
    }

    const results = await Promise.allSettled(list.map(([, fn]) => fn(brief, ctx, env)));
    const failed = results.map((r, i) => [list[i][0], r]).filter(([, r]) => r.status === 'rejected');
    failed.forEach(([name, r]) => log.error(`[brief] ${name} failed:`, r.reason && r.reason.message));
    if (failed.length === results.length) {
      return { status: 502, body: { ok: false, error: 'Не удалось доставить уведомление.' } };
    }
    return { status: 200, body: { ok: true } };
  } catch (err) {
    if (err instanceof BriefError) return { status: err.status, body: { ok: false, error: err.message } };
    log.error('[brief] unexpected:', err);
    return { status: 500, body: { ok: false, error: 'Внутренняя ошибка сервера.' } };
  }
}

function clientIp(req) {
  const xf = req.headers['x-forwarded-for'];
  if (xf) return String(xf).split(',')[0].trim();
  return (req.socket && req.socket.remoteAddress) || '';
}

module.exports = { handleBrief, validate, clientIp, BriefError, _internal: { telegramText, emailHtml, emailText, rateLimit } };
