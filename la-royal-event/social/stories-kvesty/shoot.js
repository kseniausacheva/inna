const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'stories.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (let i = 1; i <= 8; i++) {
    const el = page.locator('#s' + i);
    await el.screenshot({ path: path.join(__dirname, `story-0${i}.png`) });
    console.log('ok: story-0' + i);
  }
  await browser.close();
})();
