# Handoff: Сайт-портфолио иллюстратора «Инна»

## Overview
Одностраничный сайт-визитка креатора (иллюстрации, сториборды, вертикальные/горизонтальные сериалы, аватары). Цель посетителя — заполнить бриф. Аудитория: продюсеры и студии, бренды и агентства, частные заказчики, издательства. Язык — русский. Тон — тёплый, ручной, авторский; тёмная «студийная» тема.

## About the Design Files
`inna-studio.dc.html` (+ `image-slot.js`, `support.js`) — **дизайн-референс в HTML**, прототип внешнего вида и поведения, а не production-код. Задача: воссоздать его в целевом стеке (Next.js/React, Astro, Vue и т. д. — если стек не выбран, рекомендуем Next.js + Tailwind или plain CSS) и подключить бэкенд для формы брифа. Файл можно открыть в браузере и инспектировать — все стили инлайновые, разметка семантичная.

Логика (данные работ, отзывов, цен, состояние формы) — в `<script data-dc-script>` внизу файла, класс `Component` с методом `renderVals()`. Список работ по категориям — массив `rows`.

## Fidelity
**High-fidelity.** Цвета, типографика, отступы и состояния — финальные. Воссоздать pixel-perfect. Контент (имена клиентов, отзывы, цены, контакты) — **плейсхолдеры**, заменяются владельцем.

## Screens / Views (одна страница, секции сверху вниз)

### Nav (sticky)
- `position:sticky; top:0; z-index:10`, `display:flex; justify-content:space-between`, padding `20px clamp(20px,5vw,72px)`.
- Фон `rgba(23,18,15,.85)`, `backdrop-filter:blur(10px)`, `border-bottom:1px solid #2A221D`.
- Лого: «ИННА» Piazzolla 22px/600 + « — студия» italic 300, цвет `#E0A23A`.
- Ссылки: Golos Text 13px, `letter-spacing:.06em`, uppercase, `#B9AA98`; «Бриф ↗» — `#E0A23A`. Hover — `#E0A23A`.

### Hero (`#top`)
- Padding `clamp(40px,7vw,96px) clamp(20px,5vw,72px) 0`.
- Строка категорий: 13px uppercase `.16em` `#B9AA98`, разделители «/» `#E0A23A`.
- H1: Piazzolla 300, `clamp(56px,11.5vw,200px)`, `line-height:.88`, `letter-spacing:-.035em`. Текст «Истории / *кадр за кадром*», вторая строка italic `#E0A23A` со сдвигом `padding-left:clamp(20px,12vw,220px)`.
- Ниже 12-колоночная сетка: лид (кол. 1–5, 17–20px `#B9AA98`, max 44ch) и кнопки справа (кол. 7–12): primary `#E0A23A` текст `#17120F`, padding `16px 28px`, radius 4px, hover → фон `#F1E6D6`; secondary — border `1px #3A302A`, hover border `#F1E6D6`.
- Декор: радиальное свечение справа сверху `radial-gradient(circle, rgba(224,162,58,.35), transparent 60%)`, blur 40px, анимация `glow` 9s (opacity .55↔.85). Поверх всей страницы — шумовая текстура (SVG feTurbulence), `opacity:.09; mix-blend-mode:screen; pointer-events:none`.
- Анимация появления `rise` (.7–.9s, задержки 0/.1/.2/.3s): `translateY(24px)→0`, opacity 0→1.

### Hero reel
- Горизонтальный скролл, `gap:16px`, `scroll-snap-type:x mandatory`, 5 плейсхолдеров разных пропорций: 9:16 (`clamp(200px,22vw,300px)`), 16:9 (`clamp(320px,40vw,540px)`, align-self:end), 4:5, 1:1 (align-self:center), 16:9. Radius 6px.

### Обо мне (`#about`)
- 12 колонок, `border-top:1px solid #2A221D`, padding `clamp(72px,10vw,160px)` по вертикали.
- Кол. 1–3: индекс «01 / Обо мне» (13px uppercase `#E0A23A`).
- Кол. 4–9: H2 Piazzolla 300 `clamp(32px,3.6vw,56px)` `line-height:1.08`; два абзаца 18px `#B9AA98`; сетка фактов `repeat(auto-fit,minmax(140px,1fr))` с 1px-разделителями `#2A221D` (ячейки фон `#17120F`, padding 20px, число Piazzolla 40px `#E0A23A`, подпись 13px `#B9AA98`).
- Кол. 10–12: портрет 3:4, radius 6.

### Работы (`#works`) — 5 строк (02–06)
Каждая строка: сетка 12 кол., padding `clamp(40px,5vw,72px)`, `border-bottom:1px #2A221D`.
- Кол. 1–3 (`position:sticky; top:90px`): индекс, H3 Piazzolla 300 `clamp(28px,2.8vw,44px)`, описание 15px `#B9AA98` max 26ch.
- Кол. 4–12: горизонтальная лента карточек, `gap:14px`, snap. Подпись 13px `#B9AA98`, мета `#6E6157`.
- Категории и пропорции карточек: Иллюстрации 4:5 (`clamp(200px,22vw,300px)`), Сториборды 16:9 (`clamp(300px,36vw,480px)`), Вертикальные сериалы 9:16 (`clamp(180px,18vw,240px)`), Горизонтальные сериалы 16:9, Аватары 1:1 (`clamp(160px,16vw,220px)`).

### Отзывы (`#reviews`, 07)
- Кол. 4–12: список цитат, каждая `grid 2fr 1fr`, `padding:32px 0`, `border-top:1px #2A221D`. Цитата Piazzolla italic 300 `clamp(22px,2vw,30px)`, автор 14px (`имя #F1E6D6/500`, роль `#B9AA98`).
- Список клиентов: 14px uppercase `.06em` `#6E6157`.

### Цены (`#prices`, 08) — скрывается флагом `showPrices`
- Строки `grid 1fr auto`, `padding:22px 0`, `border-top:1px #2A221D`. Название Piazzolla 26px, описание 14px `#B9AA98`, цена Piazzolla `clamp(22px,2vw,30px)` `#E0A23A`.

### Бриф (`#brief`, 09) — инвертированная светлая секция
- Фон `#F1E6D6`, текст `#17120F`, padding `clamp(64px,9vw,140px)`, `z-index:6` (поверх шума).
- Кол. 1–5: индекс `#B0651C`, H2 Piazzolla 300 `clamp(38px,4.8vw,76px)` «Расскажите, что *нарисовать*», подзаголовок 17px `#5A4C40`, контакты (email, Telegram).
- Кол. 7–12: форма — поля без фона, только `border-bottom:1px solid #17120F`, padding `16px 0`, 17px, focus → `border-bottom-color:#B0651C`. Поля: name*, contact*, тип проекта (чипы-toggle: border 1px `#17120F`, radius 4, активный — фон `#17120F` текст `#F1E6D6`), about* (textarea), budget. Кнопка «Отправить бриф →»: фон `#17120F`, текст `#F1E6D6`, padding `18px 28px`, radius 4, hover фон `#B0651C`.
- После отправки форма заменяется блоком «Спасибо! Бриф получен…» (border 1px `#17120F`, padding 40px, Piazzolla 30px 300).

### Footer
- 13px uppercase `.06em` `#6E6157`, копирайт слева, ссылки (Behance, Telegram, Instagram) справа.

## Interactions & Behavior
- Якорная навигация по секциям.
- Чипы типа проекта — single-select toggle (повторный клик снимает).
- Submit формы: `preventDefault`, валидация HTML5 `required` на name/contact/about; state `sent=true` → показ благодарности. **Бэкенд**: POST `{name, contact, type, about, budget}` (например `/api/brief`) → письмо/Telegram-уведомление владельцу; показать ошибку при неудаче (в прототипе нет).
- Горизонтальные ленты — нативный скролл со snap; скроллбар тонкий: `scrollbar-color:#3A302A transparent`, track прозрачный, thumb `#3A302A`.
- Плейсхолдеры `<image-slot>` — заменить на `<img>`/`<video>` (для сериалов уместны muted autoplay-превью).
- Адаптив: все размеры через `clamp()`, сетки 12 колонок — на мобильных (<720px) секции с `grid-column` следует свернуть в одну колонку (в прототипе не реализовано media-query, добавить).
- Motion: `rise` и `glow` keyframes — см. выше; уважать `prefers-reduced-motion`.

## State Management
- `type: string|null` — выбранный тип проекта.
- `sent: boolean` — статус отправки брифа (добавить `loading`, `error`).
- `showPrices: boolean` — флаг показа раздела «Цены» (конфиг/CMS).
- Данные `rows`, `reviews`, `prices` — статичные, кандидаты на CMS/MDX.

## Design Tokens
Цвета:
- `--bg` `#17120F` (фон), `--bg-2` `#2A221D` (разделители), `--bg-3` `#3A302A` (бордеры кнопок, скроллбар)
- `--ink` `#F1E6D6` (основной текст, фон секции брифа), `--muted` `#B9AA98`, `--dim` `#6E6157`, `--placeholder` `#7E7064`
- `--accent` `#E0A23A` (охра), `--accent-dark` `#B0651C` (на светлом), `--ink-2` `#5A4C40`

Типографика:
- Display: **Piazzolla** (Google Fonts, opsz 8..30, weights 300/400/600, italic 300/400) — заголовки, цифры, цитаты, цены.
- Body: **Golos Text** 400/500/600 — всё остальное. Base 16px / 1.5.
- Микро-лейблы: 13px, uppercase, `letter-spacing:.16em` (индексы) или `.06em` (nav/footer).

Отступы: горизонтальные поля `clamp(20px,5vw,72px)`; вертикальные секции `clamp(72px,10vw,160px)`; сетка 12 кол., `gap:24px`; ленты `gap:14–16px`.
Радиусы: 4px (кнопки, чипы), 6px (изображения). Тени не используются (кроме свечения).

## Assets
- Шрифты — Google Fonts (`Piazzolla`, `Golos+Text`).
- Изображения — отсутствуют, плейсхолдеры `<image-slot>`; владелец предоставит работы, портрет, кадры сериалов.
- Шум — инлайн SVG data-URI с `feTurbulence baseFrequency=.85`.

## Files
- `inna-studio.dc.html` — сам дизайн (разметка + данные + логика).
- `image-slot.js` — компонент плейсхолдера изображений (только для прототипа).
- `support.js` — рантайм прототипа (только для просмотра, не переносить).
