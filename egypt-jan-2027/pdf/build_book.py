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

SUM_A = '<h3 style="margin-top:6pt">Расписание на одной странице</h3>\n<table>\n<tr><th style="width:13%">Дата</th><th style="width:22%">Где</th><th>Главное за день</th><th style="width:22%">Ночь</th></tr>\n<tr><td class="t" style="width:auto">22.01 пт</td><td>Каир</td><td>Прилёт, встреча, заселение. Экскурсий нет</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">23.01 сб</td><td>Каир</td><td><b>Плато Гизы до открытия</b> 06:00 · завтрак в Khufu\'s · Большой Египетский музей · ужин в Lucida · <b>ночные пирамиды</b> 00:00–03:00</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">24.01 вс</td><td>Каир → Луксор</td><td>Перелёт в 12:00 · <b>Карнак</b> 15:40 · <b>Луксорский храм</b> 17:45</td><td>Steigenberger</td></tr>\n<tr><td class="t" style="width:auto">25.01 пн</td><td>Луксор</td><td><b>Шар на рассвете</b> 06:00 · посадка на судно 11:30 · рабочая сессия</td><td>Судно, Луксор</td></tr>\n<tr><td class="t" style="width:auto">26.01 вт</td><td>Западный берег → река</td><td><b>Хатшепсут</b> 06:15 · Дейр-эль-Медина · Колоссы · отход 09:45 · шлюз Эсны</td><td>Судно, в пути</td></tr>\n<tr><td class="t" style="width:auto">27.01 ср</td><td>Эдфу → Асуан</td><td><b>Храм Гора в Эдфу</b> 07:00 · <b>Ком-Омбо</b> 15:00 · приход в Асуан</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">28.01 чт</td><td>Асуан</td><td>Сессия · фелюкка · <b>закрытый остров Филе</b> 17:00: напитки, храм, ужин, светозвуковой показ</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">29.01 пт</td><td>Абу-Симбел → Асуан</td><td>Высадка 05:15 · <b>Абу-Симбел</b> 08:15 · остров Элефантина 13:30 · <b>прощальный ужин</b> 19:30</td><td>Отель, Элефантина</td></tr>\n<tr><td class="t" style="width:auto">30.01 сб</td><td>Асуан → Каир</td><td>Рейс 08:45 · Каир 10:10 · прощальный обед или базар · <b>вылет домой после 14:00</b></td><td>—</td></tr>\n</table>\n\n'
SUM_B = '<h3 style="margin-top:6pt">Расписание на одной странице</h3>\n<table>\n<tr><th style="width:13%">Дата</th><th style="width:22%">Где</th><th>Главное за день</th><th style="width:22%">Ночь</th></tr>\n<tr><td class="t" style="width:auto">22.01 пт</td><td>Каир</td><td>Прилёт, встреча, заселение. Экскурсий нет</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">23.01 сб</td><td>Каир</td><td><b>Плато Гизы до открытия</b> 06:00 · завтрак в Khufu\'s · Большой Египетский музей · ужин в Lucida · <b>ночные пирамиды</b> 00:00–03:00</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">24.01 вс</td><td>Каир → Луксор</td><td>Перелёт в 12:00 · <b>Карнак</b> 15:40 · <b>Луксорский храм</b> 17:45</td><td>Steigenberger</td></tr>\n<tr><td class="t" style="width:auto">25.01 пн</td><td>Луксор</td><td><b>Шар на рассвете</b> 06:00 · посадка на судно 11:30 · рабочая сессия</td><td>Судно, Луксор</td></tr>\n<tr><td class="t" style="width:auto">26.01 вт</td><td>Западный берег → река</td><td><b>Хатшепсут</b> 06:15 · Дейр-эль-Медина · Колоссы · отход 09:45 · шлюз Эсны</td><td>Судно, в пути</td></tr>\n<tr><td class="t" style="width:auto">27.01 ср</td><td>Эдфу → Асуан</td><td><b>Храм Гора в Эдфу</b> 07:00 · <b>Ком-Омбо</b> 15:00 · приход в Асуан</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">28.01 чт</td><td>Асуан</td><td>Сессия · фелюкка · <b>закрытый остров Филе</b> 17:00: напитки, храм, ужин, светозвуковой показ</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">29.01 пт</td><td>Абу-Симбел</td><td><b>Абу-Симбел</b> 08:15 с возвратом на борт · чемоданы не трогаются · <b>прощальный ужин на палубе</b> 19:30</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">30.01 сб</td><td>Асуан → Каир</td><td>Высадка 09:30 · Асуан: обелиск, Элефантина, музей · перелёт в Каир · свободный вечер</td><td>Four Seasons</td></tr>\n<tr><td class="t" style="width:auto">31.01 вс</td><td>Каир</td><td>Завтрак без спешки · <b>вылет домой в любое время</b></td><td>—</td></tr>\n</table>\n\n'
PRICE = '<h2 class="brk">Стоимость</h2>\n<p class="lede">Здесь показано всё, что уже названо поставщиками, и отдельно то, что ещё\nуточняется. Мы не называем красивую круглую цифру: вы видите состав и понимаете,\nоткуда он складывается и где он ещё может измениться.</p>\n\n<div class="legend">\n  <span><i>✓</i> цена названа поставщиком</span>\n  <span><i>~</i> названа, уточняется состав или условия</span>\n  <span><i>≈</i> наша оценка до получения предложения</span>\n</div>\n\n<h3>Что известно уже сейчас · вариант A, при 16 гостях</h3>\n<table>\n<tr><th style="width:46%">Статья</th><th style="width:16%; text-align:right">На гостя</th><th>Статус</th></tr>\n<tr><td><b>Частный фрахт судна</b>, 4 ночи</td><td style="text-align:right"><b>13 625</b></td><td><b>~</b> Названо оператором. Включает экипаж, полный пансион, напитки, гида, портовые сборы</td></tr>\n<tr><td><b>Приватный вечер на острове Филе</b></td><td style="text-align:right">1 077</td><td><b>✓</b> Подтверждено письменно, оплачено частично</td></tr>\n<tr><td>Отели: Каир 2 ночи, Луксор, Асуан</td><td style="text-align:right">1 070</td><td><b>≈</b> Запрошен групповой тариф у всех трёх</td></tr>\n<tr><td>Абу-Симбел самолётом</td><td style="text-align:right">470</td><td><b>~</b> Названо. Уточняем, что входит кроме перелёта</td></tr>\n<tr><td><b>Приватный доступ на плато Гизы</b>, два посещения</td><td style="text-align:right">438</td><td><b>✓</b> Названо подрядчиком: персональное разрешение, все зоны</td></tr>\n<tr><td>Внутренние перелёты Каир — Луксор, Асуан — Каир</td><td style="text-align:right">313</td><td><b>≈</b> По открытым тарифам. Групповой запрошен</td></tr>\n<tr><td>Полёт на воздушном шаре, две корзины</td><td style="text-align:right">312</td><td><b>✓</b> Названо оператором</td></tr>\n<tr><td>Сопровождение La Royal Event на месте</td><td style="text-align:right">254</td><td>Четыре-пять человек всю поездку</td></tr>\n<tr><td>Прощальный ужин</td><td style="text-align:right">250</td><td><b>~</b> Площадка подтверждается, цена ориентировочная</td></tr>\n<tr><td>Питание в отелях вне названных ресторанов</td><td style="text-align:right">200</td><td><b>≈</b> Ужин 40–60, обед 25–35 на человека</td></tr>\n<tr><td>Ужин в Lucida</td><td style="text-align:right">150</td><td><b>✓</b> Подтверждено, без алкоголя</td></tr>\n<tr><td>Живая музыка на прощальном вечере</td><td style="text-align:right">41</td><td><b>≈</b> Запрошено</td></tr>\n<tr style="background:var(--soft)"><td><b>Итого по известному</b></td><td style="text-align:right"><b>18 159</b></td><td></td></tr>\n<tr><td>Организация La Royal Event, 15 %</td><td style="text-align:right">2 724</td><td>Включено в цену, сверху не добавляется</td></tr>\n<tr style="background:var(--lime-s)"><td><b>ЦЕНА НА СЕГОДНЯ</b></td><td style="text-align:right"><b>20 883 $</b></td><td><b>Не окончательная</b></td></tr>\n</table>\n\n<h3 style="margin-top:8pt">Чего в этой цифре ещё нет</h3>\n<p class="small">Мы предпочитаем сказать это прямо: перечисленное ниже <b>добавится к цене</b>.\nТочную сумму назовём, когда придут письменные подтверждения — ждём их в ближайшие недели.</p>\n<table>\n<tr><th style="width:46%">Позиция</th><th>Почему пока без цены</th></tr>\n<tr><td><b>Наземная программа 22–25 января</b></td><td>Гид, транспорт, входные билеты и Большой Египетский музей в Каире и Луксоре. Самая крупная из недостающих позиций</td></tr>\n<tr><td>Ужин на острове Филе</td><td>Идёт отдельной строкой сверх приватного вечера. Цена запрошена</td></tr>\n<tr><td>Завтрак в Khufu\'s</td><td>Бронируется напрямую в ресторане</td></tr>\n<tr><td>Абу-Симбел: билеты и транспорт на месте</td><td>470 — это только перелёт</td></tr>\n<tr><td>Встреча в аэропортах, fast track</td><td>Уточняется у принимающей компании</td></tr>\n<tr><td>Резерв на решения на месте</td><td>Обычно 2–3 % сметы. Ставится по согласованию с вами</td></tr>\n</table>\n\n<h3 style="margin-top:8pt">Как цена зависит от числа гостей</h3>\n<p class="small">Судно, приватные разрешения, закрытый остров Филе и корзины шара стоят\nодинаково при любом числе участников. Эта сумма делится на группу, поэтому каждые двое\nдополнительных гостей снижают цену примерно на две тысячи долларов для каждого.</p>\n<table>\n<tr><th style="width:34%">Число гостей</th><th style="text-align:right">14</th><th style="text-align:right">16</th><th style="text-align:right">18</th></tr>\n<tr><td>Вариант A, 9 дней</td><td style="text-align:right">23 473 $</td><td style="text-align:right"><b>20 883 $</b></td><td style="text-align:right">18 868 $</td></tr>\n<tr><td>Вариант B, 10 дней</td><td style="text-align:right">28 083 $</td><td style="text-align:right"><b>24 927 $</b></td><td style="text-align:right">22 471 $</td></tr>\n</table>\n\n<h3 style="margin-top:8pt">Опции сверх программы</h3>\n<table>\n<tr><th style="width:46%">Опция</th><th style="width:18%; text-align:right">Цена</th><th>Когда</th></tr>\n<tr><td>Прощальный обед в ресторане высокой кухни в Каире</td><td style="text-align:right">120–130 на чел.</td><td>30 января, вариант A. Вместо базара: на оба времени не хватит</td></tr>\n<tr><td>Асуан утром: обелиск, Элефантина, Нубийский музей</td><td style="text-align:right">уточняется</td><td>30 января, вариант B</td></tr>\n</table>\n\n<h2>График платежей</h2>\n<table>\n<tr><th style="width:12%">Этап</th><th style="width:14%; text-align:right">Доля</th><th style="width:26%">Когда</th><th>Что этим закрывается</th></tr>\n<tr><td><b>1</b></td><td style="text-align:right">25 %</td><td>При подписании договора</td><td>Невозвратные брони: судно, разрешения в Гизе, вечер на Филе</td></tr>\n<tr><td><b>2</b></td><td style="text-align:right">45 %</td><td>За 120 дней до заезда</td><td>Отели, внутренние перелёты, наземная программа</td></tr>\n<tr><td><b>3</b></td><td style="text-align:right">30 %</td><td>За 45 дней до заезда</td><td>Остаток по всем поставщикам</td></tr>\n</table>\n<p class="small muted">График предварительный: он будет приведён в соответствие с условиями\nсудового оператора, как только придёт его депозитный график.</p>\n\n<div class="note l"><p class="t">Что нужно от вас и к какому сроку</p>\n<p style="margin:0" class="small">\n<b>Выбор варианта, A или B</b> — до выписки международных билетов: вылет домой 30-го\nили 31-го. В варианте A рейс из Каира не раньше 14:00.<br>\n<b>Число гостей</b> — от него напрямую зависит цена.<br>\n<b>Паспортные данные и фотографии всех участников</b> — не позднее чем за 8 недель:\nбез них не оформляются разрешения в Гизе и на Филе.<br>\n<b>Особенности питания</b> — за 4 недели: закупка на судно делается один раз перед рейсом.</p></div>\n\n'

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
  <span class="stamp">Расписание · стоимость · храмы</span>
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
<tr><td class="t" style="width:auto"><b>Стоимость</b></td><td>Что уже названо поставщиками, чего ещё нет в цене, график платежей</td></tr>
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

''' + SUM_A + ''.join(recolour(common + [a29, a30]))

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

''' + SUM_B + ''.join(recolour(common + [b29, b30, b31]))

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
    head + compare + nights + secA + secB + meals + onboard + PRICE + temples + tail)
print('book.html пересобран')
