# -*- coding: utf-8 -*-
"""Схема финала одной страницей."""
import pathlib

def sheet(x, y, team, rows, w=52, h=64):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#fff" stroke="#c9bdd8" stroke-width="1.2"/>',
           f'<text x="{x+5}" y="{y+11}" font-size="7" fill="#8a7d97">команда {team}</text>']
    for i, (label, num) in enumerate(rows):
        yy = y + 19 + i * 7.6
        col = "#6b3fa0" if num else "#b8b0c2"
        out.append(f'<line x1="{x+5}" y1="{yy+1.4}" x2="{x+w-14}" y2="{yy+1.4}" stroke="#e2d9cf" stroke-width="0.8"/>')
        out.append(f'<text x="{x+5}" y="{yy}" font-size="5.6" fill="#4a3d58">{label}</text>')
        out.append(f'<text x="{x+w-7}" y="{yy}" font-size="7" font-weight="700" fill="{col}" text-anchor="middle">{num or "—"}</text>')
    return ''.join(out)

ROWS = [("грань Хеопса", "2"), ("панорама", ""), ("Хефрен", "3"),
        ("храм в долине", "4"), ("Сфинкс", "2"), ("отчёт", "")]

STRIPS = ["ЗАМОК ПОМНИТ", "ТОЛЬКО ТО,", "ЧТО МОЖНО", "ПЕРЕСЧИТАТЬ.", "ОТ МЕНЬШЕГО", "К БОЛЬШЕМУ."]

def strip(x, y, i, w=86):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="17" rx="2.5" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1" stroke-dasharray="3 2"/>'
            f'<text x="{x+6}" y="{y+11.5}" font-size="6" fill="#8a7d97">{i}</text>'
            f'<text x="{x+w/2+4}" y="{y+11.5}" font-size="8.4" fill="#241a2e" text-anchor="middle" font-weight="600">{STRIPS[i-1]}</text></g>')

def dial(cx, cy, n, r=17):
    return (f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#6b3fa0" stroke-width="2"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-5}" fill="none" stroke="#e2d9cf" stroke-width="1"/>'
            f'<text x="{cx}" y="{cy+7}" font-size="19" font-weight="700" fill="#6b3fa0" text-anchor="middle">{n}</text></g>')

SVG = f'''<svg viewBox="0 0 560 728" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Golos Text, Arial, sans-serif">
<rect width="560" height="728" fill="#faf6f2"/>

<!-- шаг 1 -->
<text x="24" y="30" font-size="11" font-weight="700" fill="#6b3fa0">1</text>
<text x="40" y="30" font-size="11" font-weight="700" fill="#241a2e">За день каждая команда заполняет свой бланк</text>
<text x="40" y="45" font-size="8.6" fill="#8a7d97">Шесть строк: по одной за каждую станцию. Четыре строки с числами, две со словами.</text>
{sheet(40, 56, 1, ROWS)}
{sheet(104, 56, 2, ROWS)}
{sheet(168, 56, 3, ROWS)}
{sheet(232, 56, 4, ROWS)}
{sheet(296, 56, 5, ROWS)}
{sheet(360, 56, 6, ROWS)}
<text x="432" y="92" font-size="8" fill="#4a3d58">У всех шести</text>
<text x="432" y="104" font-size="8" fill="#4a3d58">команд бланки</text>
<text x="432" y="116" font-size="8" fill="#4a3d58">заполнены,</text>
<text x="432" y="128" font-size="8" fill="#4a3d58">но что дальше</text>
<text x="432" y="140" font-size="8" fill="#4a3d58">делать, никто</text>
<text x="432" y="152" font-size="8" fill="#4a3d58">не знает.</text>

<line x1="24" y1="140" x2="536" y2="140" stroke="#e2d9cf" stroke-width="1"/>

<!-- шаг 2 -->
<text x="24" y="168" font-size="11" font-weight="700" fill="#6b3fa0">2</text>
<text x="40" y="168" font-size="11" font-weight="700" fill="#241a2e">У каждой команды есть запечатанный конверт с куском записки</text>
<text x="40" y="183" font-size="8.6" fill="#8a7d97">Одна команда со своим куском не прочитает ничего. Конверты выдаются ещё в автобусе, вскрывают их только в зале.</text>
{strip(40, 194, 1)}{strip(136, 194, 2)}{strip(232, 194, 3)}
{strip(40, 216, 4)}{strip(136, 216, 5)}{strip(232, 216, 6)}
<g>
  <path d="M 340 218 L 372 218" stroke="#6b3fa0" stroke-width="1.6" marker-end="url(#a)"/>
  <text x="380" y="206" font-size="8" fill="#4a3d58">шесть команд</text>
  <text x="380" y="218" font-size="8" fill="#4a3d58">кладут куски</text>
  <text x="380" y="230" font-size="8" fill="#4a3d58">на один стол</text>
</g>
<rect x="40" y="244" width="476" height="30" rx="3" fill="#6b3fa0"/>
<text x="278" y="259" font-size="10" fill="#fff" text-anchor="middle" font-weight="600">ЗАМОК ПОМНИТ ТОЛЬКО ТО, ЧТО МОЖНО ПЕРЕСЧИТАТЬ.</text>
<text x="278" y="270" font-size="10" fill="#fff" text-anchor="middle" font-weight="600">ОТ МЕНЬШЕГО К БОЛЬШЕМУ.</text>

<line x1="24" y1="294" x2="536" y2="294" stroke="#e2d9cf" stroke-width="1"/>

<!-- шаг 3 -->
<text x="24" y="322" font-size="11" font-weight="700" fill="#6b3fa0">3</text>
<text x="40" y="322" font-size="11" font-weight="700" fill="#241a2e">Теперь понятно, что делать с бланками</text>
<text x="40" y="337" font-size="8.6" fill="#8a7d97">Берём только те строки, где есть число. Две строки со словами отпадают.</text>

<g transform="translate(40,350)">
  <rect x="0" y="0" width="230" height="120" rx="3" fill="#fff" stroke="#c9bdd8" stroke-width="1.2"/>
  <text x="10" y="16" font-size="7.6" fill="#8a7d97">что у команды в бланке</text>
  <g font-size="9">
    <text x="10" y="35" fill="#241a2e">грань Хеопса</text><text x="205" y="35" fill="#6b3fa0" font-weight="700" text-anchor="middle">2</text>
    <text x="10" y="53" fill="#b8b0c2">панорама — впечатление</text><text x="205" y="53" fill="#b8b0c2" text-anchor="middle">нет</text>
    <text x="10" y="71" fill="#241a2e">Хефрен</text><text x="205" y="71" fill="#6b3fa0" font-weight="700" text-anchor="middle">3</text>
    <text x="10" y="89" fill="#241a2e">храм в долине</text><text x="205" y="89" fill="#6b3fa0" font-weight="700" text-anchor="middle">4</text>
    <text x="10" y="107" fill="#241a2e">Сфинкс</text><text x="205" y="107" fill="#6b3fa0" font-weight="700" text-anchor="middle">2</text>
  </g>
</g>
<text x="286" y="404" font-size="8.6" fill="#4a3d58">Числа есть у четырёх строк:</text>
<text x="286" y="418" font-size="8.6" fill="#4a3d58">2, 3, 4 и 2.</text>
<text x="286" y="438" font-size="8.6" fill="#4a3d58">Записка говорит: от меньшего</text>
<text x="286" y="452" font-size="8.6" fill="#4a3d58">к большему. Значит, порядок:</text>
<text x="286" y="478" font-size="15" font-weight="700" fill="#6b3fa0">2 — 2 — 3 — 4</text>

<line x1="24" y1="500" x2="536" y2="500" stroke="#e2d9cf" stroke-width="1"/>

<!-- шаг 4 -->
<text x="24" y="528" font-size="11" font-weight="700" fill="#6b3fa0">4</text>
<text x="40" y="528" font-size="11" font-weight="700" fill="#241a2e">Четыре числа — четыре диска на замке</text>
<text x="40" y="543" font-size="8.6" fill="#8a7d97">Крутят четыре команды, по одному диску каждая. Две оставшиеся держат ларец</text>
<text x="40" y="554" font-size="8.6" fill="#8a7d97">и говорят вслух, что в код не вошло и почему.</text>

<g transform="translate(150,578)">
  <rect x="-40" y="0" width="300" height="96" rx="6" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1.6"/>
  <rect x="90" y="-16" width="40" height="24" rx="12" fill="none" stroke="#6b3fa0" stroke-width="3"/>
  {dial(20, 50, 2)}{dial(80, 50, 2)}{dial(140, 50, 3)}{dial(200, 50, 4)}
</g>
<text x="40" y="690" font-size="8.6" fill="#4a3d58">Если хоть одно число чужое, замок не открывается. Тогда две минуты вся группа</text>
<text x="40" y="702" font-size="8.6" fill="#4a3d58">сверяет бланки между столами и ищет, у кого ошибка. Через две минуты ведущая</text>
<text x="40" y="714" font-size="8.6" fill="#4a3d58">открывает в любом случае: без развязки никто не уходит.</text>

<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
  <path d="M0,0 L8,4 L0,8 z" fill="#6b3fa0"/></marker></defs>
</svg>'''

CSS = '''
.art{background:#fff;border:1px solid var(--rule);border-radius:2mm;padding:4mm}
h2{margin-bottom:2mm}
.sub{color:var(--ink-2);margin-bottom:4mm;max-width:150mm}
'''
doc = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Как работает финал</title>'
 '<link rel="stylesheet" href="fonts/local.css"><link rel="stylesheet" href="doc.css"><style>' + CSS + '</style></head><body>'
 '<section class="page">'
 '<div class="mono eyebrow">Код пирамид · финал</div>'
 '<h2>Почему ларец нельзя открыть в одиночку</h2>'
 '<p class="sub">Четыре шага. Первые два идут весь день, последние два в зале финала.</p>'
 f'<div class="art">{SVG}</div>'
 '<div class="pn"><span>La Royal Event · схема финала</span><span></span></div>'
 '</section></body></html>')
pathlib.Path('giza-shema-finala.html').write_text(doc, encoding='utf-8')
print('ok')
