#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Приложение к презентации флота «Программы по дням»: модуль «Каир» + четыре модуля «Нил»
и таблица готовых комбинаций. Источник — modules.json (собирается make_modules.py),
выход — programmes.html → PDF (A4 портрет, фирменный стиль).

Запуск:  python3 make_modules.py && python3 build_programmes.py
         затем рендер Chromium (см. CLAUDE.md), выход — ../Программы_ПО_ДНЯМ_La_Royal_Event.pdf
"""
import html, io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'modules.json')
OUT = os.path.join(HERE, 'programmes.html')
NBSP = ' '

def esc(t):
    t = html.escape(str(t or ''), quote=False)
    t = re.sub(r'(\d) (\d{3})\b', r'\1' + NBSP + r'\2', t)
    t = t.replace(' —', NBSP + '—')
    return t

CSS = '''
h2.prog{font-size:20pt; color:var(--ink); border:0; margin:0 0 2pt; padding:0}
.sub{margin-bottom:6pt}
.intro{font-size:10.2pt; line-height:1.55; max-width:165mm; margin:6pt 0 8pt}
.day{page-break-inside:auto; margin:10pt 0 4pt}
.day .hd{break-after:avoid; page-break-after:avoid; break-inside:avoid}
.day h3{font-size:11.5pt; font-weight:800; margin:0 0 1pt; color:var(--violet-d)}
.day .lbl{font-family:Unbounded,sans-serif; font-weight:600; font-size:7pt; letter-spacing:.18em;
  text-transform:uppercase; color:var(--muted); margin:0 0 2pt}
.day .sum{font-size:9.2pt; color:var(--ink2); margin:2pt 0 4pt; max-width:165mm}
table.tt{page-break-inside:auto; margin:2pt 0 4pt; font-size:8.8pt}
table.tt thead{display:table-header-group}
table.tt tr{page-break-inside:avoid}
table.tt tr.first{break-after:avoid; page-break-after:avoid}
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
table.combo td{padding:5pt 6pt; font-size:9.2pt; vertical-align:top}
table.combo td.n{width:8mm; font-family:Unbounded,sans-serif; font-weight:800; font-size:12pt; color:var(--violet-d)}
table.combo td.nm{font-weight:700; width:44mm}
table.combo td.ch{color:var(--ink2); font-size:8.6pt}
.mods{display:grid; grid-template-columns:1fr 1fr; gap:5mm; margin:6pt 0 8pt}
.mods .m{background:var(--soft); border-radius:3pt; padding:7pt 9pt}
.mods .m.l{background:var(--lime-s)}
.mods .m .t{font-family:Unbounded,sans-serif; font-weight:700; font-size:10pt; margin-bottom:3pt}
.mods .m p{margin:0 0 2pt; font-size:9pt; line-height:1.45}
.mods .m b{font-family:Unbounded,sans-serif; font-weight:600; font-size:8.6pt}
.varbox{background:var(--pink-s); border-radius:3pt; padding:6pt 9pt; margin:6pt 0; font-size:9pt}
'''

HEAD = '''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Программы по дням · La Royal Event</title>
<link rel="stylesheet" href="brand-print-full.css"><style>%s</style></head><body>
<div class="cover">
  <img src="img/logo1.png" alt="La Royal Event">
  <p class="eyebrow">Нил · три судна · приложение к презентации</p>
  <h1>Программы по дням<br>и по часам</h1>
  <p class="sub">Два модуля — «Каир» и «Нил» — и пять готовых сочетаний. Каждый модуль расписан по дням отдельно, чтобы ничего не смешивалось.</p>
  <div class="band">
    <span style="background:var(--violet); width:62mm"></span>
    <span style="background:var(--lime); width:22mm"></span>
    <span style="background:var(--pink); width:12mm"></span>
  </div>
</div>
''' % CSS

FOOT = '''<footer>La Royal Event · программы по дням · время указано как ориентир по сетке операторов
и расписанию рейсов текущего сезона; точные часы фиксируются договором под дату</footer></body></html>'''


def render_days(days):
    out = []
    for d in days:
        out.append('<div class="day">')
        out.append('<div class="hd"><p class="lbl">%s</p><h3>%s</h3>' % (esc(d['label']), esc(d['heading'])))
        if d.get('summary'):
            out.append('<p class="sum">%s</p>' % esc(d['summary']))
        out.append('</div>')
        out.append('<table class="tt"><thead><tr><th style="width:17mm">Время</th><th style="width:46mm">Что происходит</th><th>Пояснение</th></tr></thead>')
        for j, r in enumerate(d['rows']):
            cls = ' '.join(c for c in (('opt' if r.get('optional') else ''), ('first' if j == 0 else '')) if c)
            out.append('<tr%s><td class="t">%s</td><td class="w">%s</td><td class="y">%s</td></tr>'
                       % ((' class="%s"' % cls) if cls else '', esc(r['time']), esc(r['what']), esc(r['why'])))
        out.append('</table>')
        if d.get('night'):
            out.append('<p class="night"><b>Ночь:</b> %s</p>' % esc(d['night']))
        out.append('</div>')
    return out


def render_lists(m):
    out = []
    if m.get('need_to_know'):
        out.append('<div class="note know"><div class="t">Что надо знать заранее</div><ol>')
        out.extend('<li>%s</li>' % esc(x) for x in m['need_to_know'])
        out.append('</ol></div>')
    if m.get('included') or m.get('extra'):
        out.append('<div class="two"><div><h4>В модуле</h4><ul>')
        out.extend('<li>%s</li>' % esc(x) for x in m.get('included', []))
        out.append('</ul></div><div class="x"><h4>Отдельно, по запросу</h4><ul>')
        out.extend('<li>%s</li>' % esc(x) for x in m.get('extra', []))
        out.append('</ul></div></div>')
    return out


def render(data):
    cairo, nile, combos = data['cairo'], data['nile'], data['combos']
    out = [HEAD]

    # ── страница 1: как собирается поездка ──
    out.append('<div class="pb"></div><p class="eyebrow">Как собирается поездка</p>')
    out.append('<h2 style="margin-top:2pt">Два модуля, пять готовых сочетаний</h2>')
    out.append('<div class="mods"><div class="m l"><div class="t">Модуль «Каир»</div>'
               '<p><b>1 день</b> — прилёт, отель, вечер в городе.</p>'
               '<p><b>2 дня</b> — + Гиза: квест «Код пирамид», приватный вход в пирамиду Хеопса, ужин в Lucida. По желанию — «Ночь в музее».</p>'
               '<p><b>3 дня</b> — + Большой Египетский музей, конференция в отеле, вечер на яхте по Нилу. Либо день в пустыне Эль-Файюм.</p>'
               '<p style="margin-top:3pt; color:var(--ink2)">Программа откатана на группах, тайминг проверен. Последнее утро — ранний рейс на реку.</p></div>'
               '<div class="m"><div class="t">Модуль «Нил»</div>'
               '<p><b>3 ночи</b> — пятница из Асуана в Луксор.</p>'
               '<p><b>4 ночи</b> — понедельник из Луксора в Асуан.</p>'
               '<p><b>7 ночей</b> — понедельник из Луксора, кольцо.</p>'
               '<p><b>5 ночей Lumière</b> — любой день, судно только под группу.</p>'
               '<p style="margin-top:3pt; color:var(--ink2)">Soleil и Le Fayan Suites ходят по сетке операторов; день посадки задаёт день недели всей поездки.</p></div></div>')
    out.append('<table class="combo"><tr><th style="width:8mm">№</th><th>Программа</th><th>Дни недели</th><th>Всего</th><th>Судно</th><th>Группа</th></tr>')
    for c in combos:
        out.append('<tr><td class="n">%s</td><td class="nm">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'
                   % (c['n'], esc(c['name']), esc(c['days']), esc(c['total']), esc(c['boat']), esc(c['group'])))
        out.append('<tr><td></td><td class="ch" colspan="5">%s</td></tr>' % esc(c['chain']))
    out.append('</table>')
    out.append('<div class="note" style="margin-top:5mm"><div class="t">Как читать</div>'
               '<p style="margin:0">Дальше каждый модуль расписан отдельно: сначала «Каир» по дням, потом четыре варианта «Нила». '
               'Поездка складывается так: последняя ночь в Каире → ранний рейс в Луксор или Асуан → первый день речного модуля. '
               'Левая колонка — время, средняя — что происходит, правая — зачем это так и что нужно знать. '
               'Строки на сером фоне — по желанию: решаются при бронировании.</p></div>')

    # ── модуль Каир ──
    if cairo:
        out.append('<div class="pb"></div>')
        out.append('<p class="eyebrow">Модуль «Каир» · 1, 2 или 3 дня</p>')
        out.append('<h2 class="prog">Каир: откатанная программа</h2>')
        out.append('<p class="sub">Прилёт · Гиза и квест «Код пирамид» · Большой Египетский музей, конференция, яхта · или пустыня Эль-Файюм</p>')
        out.append('<p class="intro">%s</p>' % esc(cairo['intro']))
        out.extend(render_days(cairo['days']))
        out.extend(render_lists(cairo))

    # ── модули Нил ──
    for m in nile:
        out.append('<div class="pb"></div>')
        out.append('<p class="eyebrow">Модуль «Нил»</p>')
        out.append('<h2 class="prog">%s</h2>' % esc(m['title']))
        out.append('<p class="sub">%s</p>' % esc(m['subtitle']))
        out.append('<p class="intro">%s</p>' % esc(m['intro']))
        out.extend(render_days(m['days']))
        out.extend(render_lists(m))

    out.append(FOOT)
    return '\n'.join(out)


if __name__ == '__main__':
    data = json.load(io.open(SRC, encoding='utf-8'))
    io.open(OUT, 'w', encoding='utf-8').write(render(data))
    n_days = sum(len(m['days']) for m in data['nile']) + (len(data['cairo']['days']) if data['cairo'] else 0)
    print('programmes.html собран:', n_days, 'дней')
