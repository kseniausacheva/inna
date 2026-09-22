#!/usr/bin/env python3
"""Собирает клиентский файл «Программа и храмы» из prog-client.html и temples.html.
Дни и справочник берутся из источников, а не дублируются, — чтобы они не разъезжались."""
import io, re
import costs

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

SUM_A = '<h3 style="margin-top:6pt">Расписание на одной странице</h3>\n<table>\n<tr><th style="width:13%">Дата</th><th style="width:22%">Где</th><th>Главное за день</th><th style="width:22%">Ночь</th></tr>\n<tr><td class="t" style="width:auto">22.01 пт</td><td>Каир</td><td>Прилёт, встреча, заселение. Экскурсий нет</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">23.01 сб</td><td>Каир</td><td><b>Плато Гизы до открытия</b> 06:00 · завтрак в Khufu\'s · Большой Египетский музей · ужин в Lucida · <b>ночные пирамиды</b> 00:00–03:00</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">24.01 вс</td><td>Каир → Луксор</td><td>Перелёт в 12:00 · <b>Карнак</b> 15:40 · <b>Луксорский храм</b> 17:45</td><td>Sonesta St. George</td></tr>\n<tr><td class="t" style="width:auto">25.01 пн</td><td>Луксор</td><td><b>Шар на рассвете</b> 06:00 · посадка на судно 11:30 · рабочая сессия</td><td>Судно, Луксор</td></tr>\n<tr><td class="t" style="width:auto">26.01 вт</td><td>Западный берег → река</td><td><b>Хатшепсут</b> 06:15 · Дейр-эль-Медина · Колоссы · отход 09:45 · шлюз Эсны</td><td>Судно, в пути</td></tr>\n<tr><td class="t" style="width:auto">27.01 ср</td><td>Эдфу → Асуан</td><td><b>Храм Гора в Эдфу</b> 07:00 · <b>Ком-Омбо</b> 15:00 · приход в Асуан</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">28.01 чт</td><td>Асуан</td><td>Сессия · фелюкка · <b>закрытый остров Филе</b> 17:00: напитки, храм, ужин, светозвуковой показ</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">29.01 пт</td><td>Абу-Симбел → Асуан</td><td>Высадка 05:15 · <b>Абу-Симбел</b> 08:15 · остров Элефантина 13:30 · <b>прощальный ужин</b> 19:30</td><td>Отель, Элефантина</td></tr>\n<tr><td class="t" style="width:auto">30.01 сб</td><td>Асуан → Каир</td><td>Рейс 08:45 · Каир 10:10 · прощальный обед или базар · <b>вылет домой после 14:00</b></td><td>—</td></tr>\n</table>\n\n'
SUM_B = '<h3 style="margin-top:6pt">Расписание на одной странице</h3>\n<table>\n<tr><th style="width:13%">Дата</th><th style="width:22%">Где</th><th>Главное за день</th><th style="width:22%">Ночь</th></tr>\n<tr><td class="t" style="width:auto">22.01 пт</td><td>Каир</td><td>Прилёт, встреча, заселение. Экскурсий нет</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">23.01 сб</td><td>Каир</td><td><b>Плато Гизы до открытия</b> 06:00 · завтрак в Khufu\'s · Большой Египетский музей · ужин в Lucida · <b>ночные пирамиды</b> 00:00–03:00</td><td>Giza Palace</td></tr>\n<tr><td class="t" style="width:auto">24.01 вс</td><td>Каир → Луксор</td><td>Перелёт в 12:00 · <b>Карнак</b> 15:40 · <b>Луксорский храм</b> 17:45</td><td>Sonesta St. George</td></tr>\n<tr><td class="t" style="width:auto">25.01 пн</td><td>Луксор</td><td><b>Шар на рассвете</b> 06:00 · посадка на судно 11:30 · рабочая сессия</td><td>Судно, Луксор</td></tr>\n<tr><td class="t" style="width:auto">26.01 вт</td><td>Западный берег → река</td><td><b>Хатшепсут</b> 06:15 · Дейр-эль-Медина · Колоссы · отход 09:45 · шлюз Эсны</td><td>Судно, в пути</td></tr>\n<tr><td class="t" style="width:auto">27.01 ср</td><td>Эдфу → Асуан</td><td><b>Храм Гора в Эдфу</b> 07:00 · <b>Ком-Омбо</b> 15:00 · приход в Асуан</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">28.01 чт</td><td>Асуан</td><td>Сессия · фелюкка · <b>закрытый остров Филе</b> 17:00: напитки, храм, ужин, светозвуковой показ</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">29.01 пт</td><td>Абу-Симбел</td><td><b>Абу-Симбел</b> 08:15 с возвратом на борт · чемоданы не трогаются · <b>прощальный ужин на палубе</b> 19:30</td><td>Судно, Асуан</td></tr>\n<tr><td class="t" style="width:auto">30.01 сб</td><td>Асуан → Каир</td><td>Высадка 09:30 · Асуан: обелиск, Элефантина, музей · перелёт в Каир · свободный вечер</td><td>Four Seasons</td></tr>\n<tr><td class="t" style="width:auto">31.01 вс</td><td>Каир</td><td>Завтрак без спешки · <b>вылет домой в любое время</b></td><td>—</td></tr>\n</table>\n\n'
PRICE_TMPL = '<h2 class="brk">Стоимость</h2>\n<p class="lede">Смета составлена <b>на всю группу</b> и приведена для <b>шестнадцати гостей</b> — это нижняя граница набора. Чем больше гостей, тем дешевле каждому: шкала цен по размеру группы идёт сразу за таблицей. Состав показан построчно, и отдельно — то, чего в цифре ещё нет: у части поставщиков мы ждём письменные подтверждения.</p>\n\n<div class="cols">\n<div class="box" style="background:var(--lime-s)"><h3>Вариант A · 9 дней</h3>\n<p style="font-family:Unbounded,sans-serif; font-weight:800; font-size:20pt; line-height:1;\n   letter-spacing:-.02em; color:var(--violet-d); margin:3pt 0 2pt">{TA} $</p>\n<p class="small" style="margin:0">при 16 гостях · <b>{PA} $ на человека</b><br><span class="muted">при 27 гостях — {PA27} $</span></p></div>\n<div class="box" style="background:var(--pink-s)"><h3>Вариант B · 10 дней</h3>\n<p style="font-family:Unbounded,sans-serif; font-weight:800; font-size:20pt; line-height:1;\n   letter-spacing:-.02em; color:var(--pink-d); margin:3pt 0 2pt">{TB} $</p>\n<p class="small" style="margin:0">при 16 гостях · <b>{PB} $ на человека</b><br><span class="muted">при 27 гостях — {PB27} $</span></p></div>\n</div>\n\n<div class="legend" style="margin-top:6pt">\n  <span><i>✓</i> цена названа поставщиком</span>\n  <span><i>~</i> названа, уточняется состав</span>\n  <span><i>≈</i> наша оценка до предложения</span>\n</div>\n\n{TABLE}<h2 class="brk">Цена и размер группы</h2>\n<p class="lede">Итоговой суммы «за группу» без числа гостей не существует. Ниже — цена\nна человека для каждого размера группы, чтобы её можно было называть до того, как набор\nзакрыт. Судно фрахтуется целиком, поэтому чем больше гостей, тем дешевле каждому.</p>\n<div class="note l"><p class="t">Откуда берётся разница</p><p style="margin:0" class="small">Фрахт — это выкуп всего судна, а не плата за каюты. <b>На борту тридцать кают</b>, и при шестнадцати гостях почти половина из них идёт пустыми — уже оплаченными. Судно, разрешения в Гизе и закрытый остров Филе стоят одинаково хоть при шестнадцати гостях, хоть при двадцати семи. Поэтому каждый следующий гость добавляет к смете только <b>свои собственные расходы — 4 499 $</b>: отели, перелёты, билеты, питание.</p></div>\n<table>\n<tr><th style="width:20%">Гостей</th><th style="text-align:right" colspan="2">На человека</th><th style="text-align:right" colspan="2">За всю группу</th></tr>\n<tr><th></th><th style="text-align:right">Вариант A</th><th style="text-align:right">Вариант B</th><th style="text-align:right">Вариант A</th><th style="text-align:right">Вариант B</th></tr>\n<tr><td><b>16 гостей</b></td><td style="text-align:right"><b>22 310 $</b></td><td style="text-align:right"><b>26 285 $</b></td><td style="text-align:right">356 963 $</td><td style="text-align:right">420 558 $</td></tr>\n<tr><td><b>18 гостей</b></td><td style="text-align:right"><b>20 490 $</b></td><td style="text-align:right"><b>24 030 $</b></td><td style="text-align:right">368 825 $</td><td style="text-align:right">432 535 $</td></tr>\n<tr><td><b>20 гостей</b></td><td style="text-align:right"><b>18 891 $</b></td><td style="text-align:right"><b>22 082 $</b></td><td style="text-align:right">377 812 $</td><td style="text-align:right">441 637 $</td></tr>\n<tr><td><b>22 гостя</b></td><td style="text-align:right"><b>17 582 $</b></td><td style="text-align:right"><b>20 488 $</b></td><td style="text-align:right">386 799 $</td><td style="text-align:right">450 739 $</td></tr>\n<tr><td><b>24 гостя</b></td><td style="text-align:right"><b>16 491 $</b></td><td style="text-align:right"><b>19 160 $</b></td><td style="text-align:right">395 786 $</td><td style="text-align:right">459 841 $</td></tr>\n<tr style="background:var(--lime-s)"><td><b>27 гостей</b></td><td style="text-align:right"><b>15 264 $</b></td><td style="text-align:right"><b>17 643 $</b></td><td style="text-align:right">412 141 $</td><td style="text-align:right">476 369 $</td></tr>\n</table>\n<p class="small"><b>Как читать.</b> От шестнадцати гостей к двадцати семи общая сумма растёт\nна 55 178, а цена на человека падает на <b>7 046</b> — почти на треть. Это не скидка\nза объём, а деление уже оплаченного фрахта на большее число людей. Цены действуют\nпри одноместном размещении и включают всё, что перечислено в смете выше.</p>\n<h3 style="margin-top:8pt">Что задаёт границы</h3>\n<table>\n<tr><th style="width:34%">Что ограничивает</th><th>Где граница</th></tr>\n<tr><td><b>Размещение на судне</b></td><td>Программа рассчитана <b>до 27 гостей</b> при одноместном размещении. Дальше нужны либо двухместные каюты, либо другой борт</td></tr>\n<tr><td>Полёт на шаре</td><td>В корзину восемь человек. До 16 гостей — две корзины, до 24 — три, дальше четыре. В ценах это уже учтено</td></tr>\n<tr><td>Отели и перелёты</td><td>Блоки номеров и места на рейсах бронируются под финальное число. Чем раньше оно известно, тем надёжнее январские даты и тарифы</td></tr>\n<tr><td>Приватные открытия и Филе</td><td>Не ограничивают: открывают памятник для группы, а не считают головы</td></tr>\n</table>\n\n<h2>Что входит в эту сумму</h2>\n<p>Практически всё, из чего состоит поездка, <b>уже включено в цену выше</b>: размещение по всем ночам, частный фрахт судна с полным пансионом, внутренние перелёты и перелёт в Абу-Симбел, <b>все трансферы на протяжении всей поездки</b> — от встречи в аэропорту до выезда на рейс домой, <b>входные билеты на все объекты маршрута</b>, включая Карнак, Луксорский храм и плато Гизы, приватные разрешения на два закрытых посещения Гизы, закрытый остров Филе с ужином и показом, полёт на шаре, индивидуальная экскурсия в Большом Египетском музее, завтрак в Khufu’s, ужины в Lucida и на прощальном вечере, живая музыка, русскоязычный египтолог на всю программу и сопровождение командой La Royal Event. <b>Оформление прощального вечера — наша работа и отдельно не считается:</b> декор палубы, сервировка стола, рассадка и микрофоны, если они нужны для слова или поздравления.</p>\n<div class="cols">\n<div class="box"><h3>Не входит в стоимость</h3>\n<p class="small" style="margin-bottom:0">Международные перелёты и визы, личные расходы гостей, алкоголь вне согласованного пакета, бар вне часов приёмов пищи и минибар, напитки в ресторанах на берегу. Чаевые экипажу судна входят во фрахт и отдельно не собираются. Техническое оснащение сверх микрофонов — свет, звук, экраны, сцена — запрашивается отдельно.</p></div>\n<div class="box l" style="background:var(--lime-s)"><h3>Что ещё подтверждается</h3>\n<p class="small" style="margin-bottom:0">Часть позиций мы получаем в письменном виде в ближайшие недели: групповые тарифы отелей и авиакомпаний, окончательное меню прощального ужина. Это не меняет состав программы. <b>Итоговая сумма фиксируется договором</b>, и мы не назовём цифру, которую потом придётся пересматривать.</p></div>\n</div>\n\n<h3 style="margin-top:8pt">Опции сверх программы</h3>\n<table>\n<tr><th style="width:44%">Опция</th><th style="width:20%; text-align:right">Цена</th><th>Когда</th></tr>\n<tr><td>Прощальный обед в ресторане высокой кухни в Каире</td><td style="text-align:right">120–130 на чел.</td><td>30 января, вариант A. Вместо базара: на оба времени не хватит</td></tr>\n<tr><td>Асуан утром: обелиск, Элефантина, Нубийский музей</td><td style="text-align:right">уточняется</td><td>30 января, вариант B</td></tr>\n</table>\n\n<h2>График платежей</h2>\n<table>\n<tr><th style="width:12%">Платёж</th><th style="width:12%; text-align:right">Доля</th><th style="width:20%; text-align:right">Вариант A</th><th style="width:20%; text-align:right">Вариант B</th><th>Когда и зачем</th></tr>\n<tr><td><b>1</b></td><td style="text-align:right">50 %</td><td style="text-align:right">{P1A} $</td><td style="text-align:right">{P1B} $</td><td><b>При подписании договора.</b> С этого платежа выкупаются авиабилеты, бронируются отели и оплачиваются невозвратные позиции: судно, разрешения в Гизе, вечер на острове Филе</td></tr>\n<tr><td><b>2</b></td><td style="text-align:right">50 %</td><td style="text-align:right">{P2A} $</td><td style="text-align:right">{P2B} $</td><td><b>За два месяца до заезда</b>, то есть до 22 ноября 2026 года. Остаток по всем поставщикам</td></tr>\n</table>\n<p class="small">Первый платёж больше обычного намеренно: в январе места на рейсах и номера в отелях уходят задолго, и ранняя оплата — единственный способ зафиксировать и цену, и наличие.</p>\n\n<div class="note l"><p class="t">Что нужно от вас и к какому сроку</p>\n<p style="margin:0" class="small">\n<b>Выбор варианта, A или B</b> — до выписки международных билетов: вылет домой 30-го\nили 31-го. В варианте A рейс из Каира не раньше 14:00.<br>\n<b>Число гостей</b> — от него напрямую зависит цена на человека.<br>\n<b>Паспортные данные и фотографии всех участников</b> — не позднее чем за 8 недель:\nбез них не оформляются разрешения в Гизе и на Филе.<br>\n<b>Особенности питания</b> — за 4 недели: закупка на судно делается один раз перед рейсом.</p></div>\n\n'

def _price():
    rows = costs.client_rows()
    sa = sum(r[1] or 0 for r in rows)
    sb = sum(r[2] or 0 for r in rows)
    ca, cb = costs.total('A'), costs.total('B')
    assert sa == ca and sb == cb, 'клиентская таблица не сходится с итогом: %d/%d против %d/%d' % (sa, sb, ca, cb)
    ta, tb = costs.client_total('A'), costs.client_total('B')
    r = lambda x: '<td style="text-align:right">%s</td>' % costs.ru(x)
    out = ['<h3>\u0421\u043e\u0441\u0442\u0430\u0432 \u0441\u043c\u0435\u0442\u044b \u00b7 \u043d\u0430 \u0432\u0441\u044e \u0433\u0440\u0443\u043f\u043f\u0443, \u043f\u0440\u0438 16 \u0433\u043e\u0441\u0442\u044f\u0445</h3>',
           '<table>',
           '<tr><th style="width:36%">\u0421\u0442\u0430\u0442\u044c\u044f</th>'
           '<th style="width:15%; text-align:right">\u0412\u0430\u0440\u0438\u0430\u043d\u0442 A</th>'
           '<th style="width:15%; text-align:right">\u0412\u0430\u0440\u0438\u0430\u043d\u0442 B</th>'
           '<th>\u0421\u0442\u0430\u0442\u0443\u0441</th></tr>']
    for title, a, b, mark, note in rows:
        cb_ = r(b) if b is not None else '<td style="text-align:right">\u043d\u0430 \u0431\u043e\u0440\u0442\u0443</td>'
        st = ('<b>%s</b> %s' % (mark, note)) if mark else note
        out.append('<tr><td>%s</td>%s%s<td>%s</td></tr>' % (title, r(a), cb_, st))
    out.append('<tr style="background:var(--soft)"><td><b>\u0418\u0442\u043e\u0433\u043e \u043f\u043e \u0438\u0437\u0432\u0435\u0441\u0442\u043d\u043e\u043c\u0443</b></td>'
               '<td style="text-align:right"><b>%s</b></td><td style="text-align:right"><b>%s</b></td><td></td></tr>'
               % (costs.ru(ca), costs.ru(cb)))
    out.append('<tr><td>\u041e\u0440\u0433\u0430\u043d\u0438\u0437\u0430\u0446\u0438\u044f La Royal Event, 15 %%</td>'
               '<td style="text-align:right">%s</td><td style="text-align:right">%s</td>'
               '<td>\u0412\u043a\u043b\u044e\u0447\u0435\u043d\u043e \u0432 \u0446\u0435\u043d\u0443, \u0441\u0432\u0435\u0440\u0445\u0443 \u043d\u0435 \u0434\u043e\u0431\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f</td></tr>'
               % (costs.ru(ta - ca), costs.ru(tb - cb)))
    out.append('<tr style="background:var(--lime-s)"><td><b>\u0412\u0421\u0415\u0413\u041e \u0417\u0410 \u0413\u0420\u0423\u041f\u041f\u0423</b></td>'
               '<td style="text-align:right"><b>%s $</b></td><td style="text-align:right"><b>%s $</b></td>'
               '<td><b>\u041d\u0435 \u043e\u043a\u043e\u043d\u0447\u0430\u0442\u0435\u043b\u044c\u043d\u043e</b></td></tr>'
               % (costs.ru(ta), costs.ru(tb)))
    out.append('</table>\n\n')
    return PRICE_TMPL.format(
        TABLE='\n'.join(out), TA=costs.ru(ta), TB=costs.ru(tb),
        PA=costs.ru(ta / 16.0), PB=costs.ru(tb / 16.0),
        PA27=costs.ru(costs.client_total('A', 27) / 27.0),
        PB27=costs.ru(costs.client_total('B', 27) / 27.0),
        P1A=costs.ru(ta - ta // 2), P1B=costs.ru(tb - tb // 2),
        P2A=costs.ru(ta // 2), P2B=costs.ru(tb // 2))

PRICE = _price()


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
    <span>последний вечер — Асуан или Каир</span>
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
<tr><td class="t" style="width:auto">Два варианта <span class="muted">· стр. 1</span></td><td>Чем они отличаются, что каждый даёт и что стоит, наша рекомендация</td></tr>
<tr><td class="t" style="width:auto">Вариант A, 9 дней <span class="muted">· стр. 3</span></td><td>Полная программа по дням, с 22 по 30 января</td></tr>
<tr><td class="t" style="width:auto">Вариант B, 10 дней <span class="muted">· стр. 8</span></td><td>Полная программа по дням, с 22 по 31 января</td></tr>
<tr><td class="t" style="width:auto">Питание и напитки <span class="muted">· стр. 13</span></td><td>Что входит в судовой пакет, что считается отдельно, все приёмы пищи по дням</td></tr>
<tr><td class="t" style="width:auto"><b>Стоимость</b> <span class="muted">· стр. 16</span></td><td>Полная смета на группу, что входит, график платежей 50/50</td></tr>
<tr><td class="t" style="width:auto">Цена и размер группы <span class="muted">· стр. 18</span></td><td>Цена на человека при разном числе гостей, от 16 до 27</td></tr>
<tr><td class="t" style="width:auto">Храмы маршрута <span class="muted">· стр. 20</span></td><td>История, тексты и эзотерическая традиция каждого объекта</td></tr>
<tr><td class="t" style="width:auto">Что можно добавить <span class="muted">· стр. 26</span></td><td>Десять мест вне программы, с ценой по времени</td></tr>
</table>

<div class="legend">
  <span><i>✓</i> подтверждено</span>
  <span><i>~</i> подтверждается поставщиком</span>
  <span><i>?</i> требует вашего решения</span>
</div>

'''

secA = '''<h2 class="brk">Вариант A · 9 дней · 22–30 января</h2>
<p class="small muted">Четыре ночи на борту. Прощальный ужин и последняя ночь —
на острове Элефантина в Асуане, вечером 29 января. Утром 30-го перелёт
в Каир, вылет домой после 14:00 — либо ночь в Four Seasons и вылет 31-го.</p>
<table>
<tr><th style="width:34%">Ночь</th><th>Где</th></tr>
<tr><td class="t" style="width:auto">22, 23 января</td><td>Giza Palace Hotel &amp; Spa, Шейх Зайед</td></tr>
<tr><td class="t" style="width:auto">24 января</td><td>Sonesta St. George, Луксор <b>✓</b></td></tr>
<tr><td class="t" style="width:auto">25, 26, 27, 28 января</td><td>Судно, частный фрахт</td></tr>
<tr><td class="t" style="width:auto">29 января</td><td>Отель на острове Элефантина, Асуан <b>~</b></td></tr>
<tr><td class="t" style="width:auto">30 января <span class="muted">опция</span></td><td>Four Seasons Cairo at Nile Plaza — если берёте лишнюю ночь <b>?</b></td></tr>
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
<tr><td class="t" style="width:auto">24 января</td><td>Sonesta St. George, Луксор <b>✓</b></td></tr>
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
