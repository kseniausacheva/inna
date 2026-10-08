# Сторис «Наши квесты»

Серия из 8 карточек 1080×1920 для Instagram: обложка, «как устроено», 5 программ (Код пирамид, Последняя страница, Ладья идёт за солнцем, Путь к звёздам, Фараон), CTA с контактами.

Стиль: ночной режим бренда (STYLE.md) + стекломорфизм: полупрозрачные карточки с размытием над светящимися пятнами лилового, лайма и розового. Шрифты Prata / Golos Text / JetBrains Mono. Тексты — дословно из `client-package/katalog-teksty.md`.

Как пересобрать PNG:

1. В `assets/` положить: `logo-src.png` (фирменный логотип на прозрачном фоне), `prata.ttf`, `golos.ttf` (GolosText[wght]), `jbmono.ttf` (JetBrainsMono[wght]) — все с Google Fonts.
2. `NODE_PATH=$(npm root -g) node shoot.js` — скриншоты через Playwright/Chromium, получатся `story-01.png` … `story-08.png`.

Готовые PNG отправлены в чат 2026-10-08.
