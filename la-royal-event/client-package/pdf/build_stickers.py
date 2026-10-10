# -*- coding: utf-8 -*-
# Собирает giza-stikery-komand.html из эмблем карточек команд (giza-kartochki-komand.html):
# 6 страниц А4, на каждой 12 круглых стикеров (58 мм) одной команды.
# PDF рендерится через render.js (Playwright, preferCSSPageSize).
import re

src = open('giza-kartochki-komand.html', encoding='utf-8').read()
svgs = re.findall(r'<div class="emblem">(<svg.*?</svg>)</div>', src, re.S)
names = re.findall(r'<div class="team">КОМАНДА «(.+?)»</div>', src)
assert len(svgs) == 6 and len(names) == 6, (len(svgs), len(names))

head = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Стикеры команд</title><link rel="stylesheet" href="fonts/local.css"><style>
/* Круглые стикеры команд, 58 мм. 6 страниц А4 — по одной на команду, на странице 12 штук.
   Печать на самоклеящейся бумаге А4, резать по контуру круга.
   Команды 1–5 — игровые, страница «Веер» — запасная. */
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Golos Text",Arial,sans-serif;color:#4a2014}
.sheet{width:210mm;height:297mm;overflow:hidden;padding:13mm 12mm;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(4,1fr);justify-items:center;align-items:center;page-break-after:always;background:#fff}
.sheet:last-child{page-break-after:auto}
.circle{width:58mm;height:58mm;border-radius:50%;border:0.5mm solid #8d2f23;background:#fdf6e6;display:flex;align-items:center;justify-content:center}
.ring{width:53mm;height:53mm;border-radius:50%;border:0.25mm solid #c08a2d;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:3mm;background:radial-gradient(closest-side, rgba(192,138,45,.10), transparent 70%)}
.eyebrow{font-size:6.5pt;letter-spacing:.16em;color:#8d2f23}
.emblem{width:22mm;height:22mm;margin:1.6mm 0 1.2mm}
.team{font-family:"Spectral",Georgia,serif;font-weight:600;font-size:13pt;letter-spacing:.08em;color:#4a2014}
.foot{font-size:5.6pt;letter-spacing:.14em;color:#8d2f23;margin-top:1.4mm}
</style></head><body>
'''

cells = []
for name, svg in zip(names, svgs):
    sticker = ('<div class="circle"><div class="ring">'
               '<div class="eyebrow">КОД ПИРАМИД</div>'
               f'<div class="emblem">{svg}</div>'
               f'<div class="team">{name}</div>'
               '<div class="foot">LA ROYAL EVENT</div>'
               '</div></div>')
    cells.append('<div class="sheet">' + sticker * 12 + '</div>')

open('giza-stikery-komand.html', 'w', encoding='utf-8').write(head + '\n'.join(cells) + '\n</body></html>\n')
print('ok:', names)
