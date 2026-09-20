#!/usr/bin/env python3
"""Собирает клиентский файл «Программа и храмы» из prog-client.html и temples.html.
Дни и справочник берутся из источников, а не дублируются, — чтобы они не разъезжались."""
import io, re

prog = io.open('prog-client.html', encoding='utf-8').read()
tem  = io.open('temples.html',     encoding='utf-8').read()

days = re.findall(r'<div class="day[^"]*">.*?\n</div>\n', prog, re.S)
assert len(days) == 12, len(days)
common, a29, a30, b29, b30, b31 = days[0:7], *days[7:]

def recolour(blocks):
    cls = ['', 'l', 'p']
    return [re.sub(r'<div class="day[^"]*">',
                   '<div class="day %s">' % cls[i % 3] if cls[i % 3] else '<div class="day">',
                   b, count=1) for i, b in enumerate(blocks)]

def cut(text, start, end):
    return text[text.index(start):text.index(end)]

meals   = cut(prog, '<h2 class="brk">Питание и напитки</h2>', '<h2>Работа на борту</h2>')
onboard = cut(prog, '<h2>Работа на борту</h2>', '<p class="small muted" style="margin-top:7pt">Отдельным файлом')
compare = cut(prog, '<h2>Два варианта, между которыми нужно выбрать</h2>', '<h2>Размещение по ночам</h2>')
nights  = cut(prog, '<h2>Размещение по ночам</h2>', '<h2 class="brk">Общая часть: 22–28 января</h2>')
nights  = nights.replace('<h2>Размещение по ночам</h2>', '<h2>Размещение по ночам в обоих вариантах</h2>')

tstyle = tem[tem.index('<style>'):tem.index('</style>') + 8]
tbody  = cut(tem, '<div class="legend">\n  <span><b class="mark mi">', '<footer>')

head = '''<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Египет 2027 — программа и храмы</title>
<link rel="stylesheet" href="brand-print-full.css">
''' + tstyle + '''</head><body>

<div class="cover">
  <img src="img/logo1.png" alt="La Royal Event">
  <p class="eyebrow">Индивидуальное путешествие · Египет</p>
  <h1>22–30 или<br>22–31 января 2027</h1>
  <div class="band">
    <span style="background:var(--violet); width:62mm"></span>
    <span style="background:var(--lime); width:22mm"></span>
    <span style="background:var(--pink); width:12mm"></span>
  </div>
  <div class="facts">
    <span><b>9</b> или <b>10</b> дней</span>
    <span><b>16–18</b> гостей</span>
    <span>одноместное размещение</span>
    <span>частный фрахт судна, <b>4</b> или <b>5</b> ночей</span>
    <span>последняя ночь в Каире в обоих вариантах</span>
    <span>Каир · Луксор · Асуан · Абу-Симбел</span>
  </div>
  <span class="stamp">Две программы и справочник по храмам</span>
</div>

<p class="lede">Пирамиды дважды, на рассвете и ночью. Два храма восточного берега Луксора,
Фиванский некрополь, частное судно на Ниле только для вашей группы, приватный вечер на Филе
и перелёт в Абу-Симбел.</p>

<h2>Что внутри этого файла</h2>
<table>
<tr><th style="width:34%">Раздел</th><th>О чём</th></tr>
<tr><td class="t" style="width:auto">Два варианта</td><td>Чем они отличаются, что каждый даёт и что стоит, наша рекомендация</td></tr>
<tr><td class="t" style="width:auto">Вариант A, 9 дней</td><td>Полная программа по дням, с 22 по 30 января</td></tr>
<tr><td class="t" style="width:auto">Вариант B, 10 дней</td><td>Полная программа по дням, с 22 по 31 января</td></tr>
<tr><td class="t" style="width:auto">Питание и напитки</td><td>Что входит в судовой пакет, что считается отдельно, все приёмы пищи по дням</td></tr>
<tr><td class="t" style="width:auto">Храмы маршрута</td><td>История, тексты и эзотерическая традиция каждого объекта</td></tr>
<tr><td class="t" style="width:auto">Что можно добавить</td><td>Десять мест вне программы, с ценой по времени</td></tr>
</table>

<div class="legend">
  <span><i>✓</i> подтверждено</span>
  <span><i>~</i> подтверждается поставщиком</span>
  <span><i>?</i> требует вашего решения</span>
</div>

'''

secA = '''<h2 class="brk">Вариант A · 9 дней · 22–30 января</h2>
<p class="small muted">Четыре ночи на борту. Прощальный ужин в Four Seasons Cairo вечером
29 января, там же последняя ночь. Вылет домой 30 января.</p>
<table>
<tr><th style="width:34%">Ночь</th><th>Где</th></tr>
<tr><td class="t" style="width:auto">22, 23 января</td><td>Giza Palace Hotel &amp; Spa, Шейх Зайед</td></tr>
<tr><td class="t" style="width:auto">24 января</td><td>Steigenberger Nile Palace, Луксор <b>~</b></td></tr>
<tr><td class="t" style="width:auto">25, 26, 27, 28 января</td><td>Судно, частный фрахт</td></tr>
<tr><td class="t" style="width:auto">29 января</td><td>Four Seasons Cairo at Nile Plaza <b>~</b></td></tr>
</table>

''' + ''.join(recolour(common + [a29, a30]))

secB = '''<h2 class="brk">Вариант B · 10 дней · 22–31 января</h2>
<p class="small muted">Пять ночей на борту. Прощальный ужин на верхней палубе в Асуане вечером
29 января, 30-го утро в Асуане и перелёт в Каир, ночь в Four Seasons. Вылет домой 31 января.
Дни с 22 по 28 января полностью совпадают с вариантом A и приведены здесь целиком,
чтобы программу можно было читать подряд.</p>
<table>
<tr><th style="width:34%">Ночь</th><th>Где</th></tr>
<tr><td class="t" style="width:auto">22, 23 января</td><td>Giza Palace Hotel &amp; Spa, Шейх Зайед</td></tr>
<tr><td class="t" style="width:auto">24 января</td><td>Steigenberger Nile Palace, Луксор <b>~</b></td></tr>
<tr><td class="t" style="width:auto">25, 26, 27, 28, 29 января</td><td>Судно, частный фрахт</td></tr>
<tr><td class="t" style="width:auto">30 января</td><td>Four Seasons Cairo at Nile Plaza <b>~</b></td></tr>
</table>

''' + ''.join(recolour(common + [b29, b30, b31]))

temples = '''<h2 class="brk">Храмы маршрута</h2>
<p class="lede">Египетский храм не памятник и не музей. Это работающий механизм, который строили
как модель мира и обслуживали тысячелетиями. Чтобы он читался, нужно знать три разных вещи:
что с ним происходило в истории, что о себе писали сами египтяне и что в нём увидели позже.
Мы держим эти три слоя раздельно и помечаем каждый.</p>

''' + tbody

tail = '''<footer>La Royal Event · Египет · программа и справочник от 20 сентября 2026 ·
Позиции, отмеченные знаком ~, подтверждаются поставщиками; окончательные часы внутренних
рейсов уточняются</footer>
</body></html>'''

io.open('book.html', 'w', encoding='utf-8').write(
    head + compare + nights + secA + secB + meals + onboard + temples + tail)
print('book.html пересобран')
