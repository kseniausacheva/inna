// Рендер книжки «Дневник Камаля» и вклейки в блокнот курьера.
// Запуск: NODE_PATH=$(npm root -g) node render-dnevnik.js
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const dir = __dirname;

  for (const [src, out] of [
    ['dnevnik-kamalya.html', 'dnevnik-kamalya-pechat.pdf'],
    ['vkleika-bloknot.html', 'vkleika-bloknot-kuryera.pdf'],
  ]) {
    await page.goto('file://' + path.join(dir, src), { waitUntil: 'networkidle' });
    await page.pdf({ path: path.join(dir, out), preferCSSPageSize: true, printBackground: true });
    console.log('ok:', out);
  }
  await browser.close();
})();
