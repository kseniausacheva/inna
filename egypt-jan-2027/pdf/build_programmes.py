#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Приложение к презентации флота: четыре программы по дням с подробным таймингом
и расшифровкой каждой строки. Источник — programmes.json (результат редактуры),
выход — programmes.html → PDF (A4 портрет, фирменный стиль).

Запуск:  python3 build_programmes.py            # собирает programmes.html
         затем рендер Chromium (см. CLAUDE.md), выход — ../Программы_ПО_ДНЯМ_La_Royal_Event.pdf
"""
import html, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'programmes.json')
OUT = os.path.join(HERE, 'programmes.html')

NBSP = ' '

def esc(t):
    t = html.escape(str(t or ''))
    # неразрывные пробелы в числах и перед тире
    t = re.sub(r'(\d) (\d{3})\b', r'\1' + NBSP + r'\2', t)
    t = t.replace(' —', NBSP + '—')
    return t

CSS = '''
h2.prog{font-size:22pt; color:var(--ink); border:0; margin:0 0 2pt; padding:0}
.sub{margin-bottom:6pt}
.intro{font-size:10.2pt; line-height:1.55; max-width:165mm; margin:6pt 0 8pt}
.day{page-break-inside:auto; margin:10pt 0 4pt}
.day h3{font-size:11.5pt; font-weight:800; margin:0 0 1pt; color:var(--violet-d)}
.day .lbl{font-family:Unbounded,sans-serif; font-weight:600; font-size:7pt; letter-spacing:.18em;
  text-transform:uppercase; color:var(--muted); margin:0 0 2pt}
.day .sum{font-size:9.2pt; color:var(--ink2); margin:2pt 0 4pt; max-width:165mm}
.day .hd{break-after:avoid; page-break-after:avoid; break-inside:avoid}
table.tt thead{display:table-header-group}
table.tt tr.first{break-after:avoid; page-break-after:avoid}
table.tt{page-break-inside:auto; margin:2pt 0 4pt; font-size:8.8pt}
table.tt tr{page-break-inside:avoid}
table.tt th{font-size:7pt; letter-spacing:.08em; text-transform:uppercase; padding:3pt 6pt}
table.tt td{padding:3.6pt 6pt; line-height:1.42}
table.tt td.t{width:17mm; white-space:nowrap; font-variant-numeric:tabular-nums; font-weight:700; color:var(--ink)}
table.tt td.w{width:46mm; font-weight:600}
table.tt td.y{color:var(--ink2)}
table.tt tr.opt td{background:var(--soft)}
table.tt tr.opt td.w::after{content:"по желанию"; display:block; font-family:Unbounded,sans-serif;
  font-weight:600; font-size:6.3pt; letter-spacing:.12em; text-transform:uppercase; color:var(--violet-d); margin-top:1.5pt}
.night{font-size:8.6pt; color:var(--muted); margin:0 0 2pt}
.night b{color:var(--ink2); font-weight:600}
.two{display:grid; grid-template-columns:1fr 1fr; gap:6mm; margin-top:6pt; page-break-inside:avoid}
.two h4{margin:0 0 3pt}
.two ul{margin:0; padding-left:0; list-style:none}
.two li{padding-left:5mm; position:relative; margin-bottom:2.2pt; font-size:9pt; line-height:1.4}
.two li::before{content:""; position:absolute; left:0; top:5.5pt; width:2.6mm; height:2.6mm; border-radius:50%; background:var(--lime)}
.two .x li::before{background:var(--pink)}
.know{page-break-inside:avoid; margin-top:8pt}
.know ol{margin:3pt 0 0; padding-left:5mm}
.know li{margin-bottom:2.4pt; font-size:9pt; line-height:1.42}
.pb{page-break-before:always}
.toc{margin:6pt 0 0}
.toc td{padding:4pt 6pt; font-size:9.6pt}
.toc td.n{width:9mm; font-family:Unbounded,sans-serif; font-weight:800; color:var(--violet-d)}
.toc td.s{color:var(--ink2); font-size:8.8pt}
'''

HEAD = '''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Программы по дням · La Royal Event</title>
<link rel="stylesheet" href="brand-print-full.css"><style>%s</style></head><body>
<div class="cover">
  <img src="img/logo1.png" alt="La Royal Event">
  <p class="eyebrow">Нил · три судна · приложение к презентации</p>
  <h1>Четыре программы<br>по дням и по часам</h1>
  <p class="sub">Что происходит, когда и почему именно так. Для тех, кто будет собирать группу и отвечать на её вопросы.</p>
  <div class="band">
    <span style="background:var(--violet); width:62mm"></span>
    <span style="background:var(--lime); width:22mm"></span>
    <span style="background:var(--pink); width:12mm"></span>
  </div>
</div>
''' % CSS

FOOT = '''<footer>La Royal Event · программы по дням · время указано как ориентир по сетке операторов
и расписанию рейсов текущего сезона; точные часы фиксируются договором под дату</footer></body></html>'''


def render(progs):
    out = [HEAD]
    # оглавление
    out.append('<p class="eyebrow" style="margin-top:4mm">Что внутри</p><table class="toc">')
    for i, p in enumerate(progs, 1):
        out.append('<tr><td class="n">%d</td><td><b>%s</b></td><td class="s">%s</td></tr>'
                   % (i, esc(p['title']), esc(p['subtitle'])))
    out.append('</table>')
    out.append('<div class="note" style="margin-top:6mm"><div class="t">Как читать</div>'
               '<p style="margin:0">Левая колонка — время, средняя — что происходит, правая — зачем это так устроено '
               'и что нужно знать. Строки на сером фоне — по желанию: решаются отдельно, под них держим время в программе. '
               'Суда идут по сетке операторов: понедельник из Луксора, пятница из Асуана; Lumière — в любой день под группу.</p></div>')

    for i, p in enumerate(progs, 1):
        out.append('<div class="pb"></div>')
        out.append('<p class="eyebrow">Программа %d</p>' % i)
        out.append('<h2 class="prog">%s</h2>' % esc(p['title']))
        out.append('<p class="sub">%s</p>' % esc(p['subtitle']))
        out.append('<p class="intro">%s</p>' % esc(p['intro']))
        for d in p['days']:
            out.append('<div class="day">')
            out.append('<div class="hd"><p class="lbl">%s</p><h3>%s</h3>' % (esc(d['label']), esc(d['heading'])))
            if d.get('summary'):
                out.append('<p class="sum">%s</p>' % esc(d['summary']))
            out.append('</div>')
            out.append('<table class="tt"><thead><tr><th style="width:17mm">Время</th><th style="width:46mm">Что происходит</th><th>Пояснение</th></tr></thead>')
            for j, r in enumerate(d['rows']):
                cls = ' class="%s"' % ' '.join(c for c in ('opt' if r.get('optional') else '', 'first' if j == 0 else '') if c) if (r.get('optional') or j == 0) else ''
                out.append('<tr%s><td class="t">%s</td><td class="w">%s</td><td class="y">%s</td></tr>'
                           % (cls, esc(r['time']), esc(r['what']), esc(r['why'])))
            out.append('</table>')
            if d.get('night'):
                out.append('<p class="night"><b>Ночь:</b> %s</p>' % esc(d['night']))
            out.append('</div>')
        if p.get('need_to_know'):
            out.append('<div class="note know"><div class="t">Что надо знать заранее</div><ol>')
            out.extend('<li>%s</li>' % esc(x) for x in p['need_to_know'])
            out.append('</ol></div>')
        if p.get('included') or p.get('extra'):
            out.append('<div class="two"><div><h4>В программе</h4><ul>')
            out.extend('<li>%s</li>' % esc(x) for x in p.get('included', []))
            out.append('</ul></div><div class="x"><h4>Отдельно, по запросу</h4><ul>')
            out.extend('<li>%s</li>' % esc(x) for x in p.get('extra', []))
            out.append('</ul></div></div>')
    out.append(FOOT)
    return '\n'.join(out)


if __name__ == '__main__':
    progs = json.load(io.open(SRC, encoding='utf-8'))
    io.open(OUT, 'w', encoding='utf-8').write(render(progs))
    print('programmes.html собран:', sum(len(p['days']) for p in progs), 'дней,',
          sum(len(r) for p in progs for d in p['days'] for r in [d['rows']]), 'строк')
