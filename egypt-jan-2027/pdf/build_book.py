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
PRICE = '<h2 class="brk">Стоимость</h2>\n<p class="lede">Смета составлена <b>на всю группу</b>. Мы показываем состав построчно\nи отдельно — то, чего в цифре ещё нет: у части поставщиков мы ждём письменные\nподтверждения. Круглой цифры «под ключ» здесь намеренно нет, пока не придут все ответы.</p>\n\n<div class="cols">\n<div class="box" style="background:var(--lime-s)"><h3>Вариант A · 9 дней</h3>\n<p style="font-family:Unbounded,sans-serif; font-weight:800; font-size:20pt; line-height:1;\n   letter-spacing:-.02em; color:var(--violet-d); margin:3pt 0 2pt">349 029 $</p>\n<p class="small" style="margin:0">за группу из 16 гостей · 21 814 $ на человека</p></div>\n<div class="box" style="background:var(--pink-s)"><h3>Вариант B · 10 дней</h3>\n<p style="font-family:Unbounded,sans-serif; font-weight:800; font-size:20pt; line-height:1;\n   letter-spacing:-.02em; color:var(--pink-d); margin:3pt 0 2pt">413 153 $</p>\n<p class="small" style="margin:0">за группу из 16 гостей · 25 822 $ на человека</p></div>\n</div>\n\n<div class="legend" style="margin-top:6pt">\n  <span><i>✓</i> цена названа поставщиком</span>\n  <span><i>~</i> названа, уточняется состав</span>\n  <span><i>≈</i> наша оценка до предложения</span>\n</div>\n\n<h3>Состав сметы · на всю группу, при 16 гостях</h3>\n<table>\n<tr><th style="width:36%">Статья</th><th style="width:15%; text-align:right">Вариант A</th><th style="width:15%; text-align:right">Вариант B</th><th>Статус</th></tr>\n<tr><td><b>Частный фрахт судна</b>, 4 или 5 ночей</td><td style="text-align:right"><b>218 000</b></td><td style="text-align:right"><b>272 500</b></td><td><b>~</b> Названо оператором. Экипаж, полный пансион, напитки, гид, портовые сборы</td></tr>\n<tr><td><b>Приватный вечер на острове Филе</b></td><td style="text-align:right">17 234</td><td style="text-align:right">17 234</td><td><b>✓</b> Подтверждено письменно. 15 000 EUR</td></tr>\n<tr><td>Отель в Каире, 2 ночи</td><td style="text-align:right">10 400</td><td style="text-align:right">10 400</td><td><b>≈</b> Групповой тариф запрошен</td></tr>\n<tr><td>Абу-Симбел самолётом</td><td style="text-align:right">7 520</td><td style="text-align:right">7 520</td><td><b>~</b> Уточняем, что входит кроме перелёта</td></tr>\n<tr><td><b>Плато Гизы</b>, два приватных открытия для группы</td><td style="text-align:right">7 000</td><td style="text-align:right">7 000</td><td><b>✓</b> Персональное разрешение и доступ во все зоны. По 3 500 за визит</td></tr>\n<tr><td>Входные билеты на плато, два посещения</td><td style="text-align:right">5 760</td><td style="text-align:right">5 760</td><td><b>✓</b> 180 за билет на человека, оплачиваются сверх открытия</td></tr>\n<tr><td>Отель 29 января (A) или 30 января (B)</td><td style="text-align:right">4 000</td><td style="text-align:right">9 120</td><td><b>≈</b> A: Асуан. B: Four Seasons, цена названа отелем</td></tr>\n<tr><td>Сопровождение La Royal Event на месте</td><td style="text-align:right">4 420</td><td style="text-align:right">5 060</td><td>Четыре-пять человек всю поездку</td></tr>\n<tr><td>Внутренние перелёты</td><td style="text-align:right">4 000</td><td style="text-align:right">4 000</td><td><b>≈</b> По открытым тарифам. Групповой запрошен</td></tr>\n<tr><td>Прощальный ужин</td><td style="text-align:right">4 000</td><td style="text-align:right">на борту</td><td><b>~</b> A: площадка в Асуане. B: верхняя палуба судна</td></tr>\n<tr><td>Полёт на шаре, две корзины</td><td style="text-align:right">5 000</td><td style="text-align:right">5 000</td><td><b>✓</b> Названо оператором</td></tr>\n<tr><td>Питание в отелях вне названных ресторанов</td><td style="text-align:right">3 200</td><td style="text-align:right">3 200</td><td><b>≈</b> Ужин 40–60, обед 25–35 на человека</td></tr>\n<tr><td>Отель в Луксоре, 1 ночь</td><td style="text-align:right">2 720</td><td style="text-align:right">2 720</td><td><b>≈</b> Групповой тариф запрошен</td></tr>\n<tr><td>Ужин в Lucida</td><td style="text-align:right">2 400</td><td style="text-align:right">2 400</td><td><b>✓</b> Подтверждено, без алкоголя</td></tr>\n<tr><td>Ужин на острове Филе</td><td style="text-align:right">2 400</td><td style="text-align:right">2 400</td><td><b>≈</b> 150 на человека, сверх приватного вечера</td></tr>\n<tr><td>Большой Египетский музей, индивидуальная экскурсия</td><td style="text-align:right">1 920</td><td style="text-align:right">1 920</td><td><b>✓</b> 120 на человека, с трансфером</td></tr>\n<tr><td>Завтрак в Khufu’s у пирамиды</td><td style="text-align:right">1 440</td><td style="text-align:right">1 440</td><td><b>✓</b> 90 на человека</td></tr>\n<tr><td>Живая музыка на прощальном вечере</td><td style="text-align:right">650</td><td style="text-align:right">650</td><td><b>≈</b> Запрошено</td></tr>\n<tr style="background:var(--soft)"><td><b>Итого по известному</b></td><td style="text-align:right"><b>303 504</b></td><td style="text-align:right"><b>359 264</b></td><td></td></tr>\n<tr><td>Организация La Royal Event, 15 %</td><td style="text-align:right">45 525</td><td style="text-align:right">53 889</td><td>Включено в цену, сверху не добавляется</td></tr>\n<tr style="background:var(--lime-s)"><td><b>ВСЕГО ЗА ГРУППУ</b></td><td style="text-align:right"><b>349 029 $</b></td><td style="text-align:right"><b>413 153 $</b></td><td><b>Не окончательно</b></td></tr>\n</table>\n\n<h2 class="brk">Сколько стоит группа другого размера</h2>\n<p class="lede">Самый частый вопрос организатора: а если людей будет больше? Отвечаем честно, с условием, которое обычно забывают назвать.</p>\n<p>Смета делится на две части. <b>Постоянная</b> — фрахт судна, приватные открытия в Гизе, закрытый остров Филе, живая музыка: стоит одинаково хоть при шестнадцати гостях, хоть при тридцати. <b>Переменная</b> — отели, перелёты, питание, входные билеты: считается по головам. При шестнадцати гостях постоянная часть — <b>восемьдесят два процента сметы</b>, и именно поэтому цена на человека так резко падает с ростом группы.</p>\n<div class="note"><p class="t">Но есть условие, и оно решающее</p><p style="margin:0" class="small">Постоянная часть остаётся постоянной ровно до тех пор, пока хватает кают. <b>Гостям нужны одноместные каюты плюс две-три для нашей команды.</b> Как только группа перерастает борт, нужен другой борт — и фрахт, то есть главная строка сметы, перестаёт быть постоянным. Поэтому цена на человека не делится пополам при удвоении группы, как кажется из арифметики.</p></div>\n<table>\n<tr><th style="width:22%">Размер группы</th><th style="width:16%">Кают нужно</th><th style="width:22%">Какое судно</th><th style="text-align:right">Всего за группу</th><th style="text-align:right">На гостя</th></tr>\n<tr><td><b>16 гостей</b></td><td>18</td><td>Наш нынешний борт подходит</td><td style="text-align:right"><b>349 029 $</b></td><td style="text-align:right"><b>21 814 $</b></td></tr>\n<tr><td><b>20 гостей</b></td><td>23</td><td>Борт на 22–24 каюты</td><td style="text-align:right"><b>367 326 $</b></td><td style="text-align:right"><b>18 366 $</b></td></tr>\n<tr><td><b>30 гостей</b></td><td>33</td><td>Борт на 35–40 кают, другой класс</td><td style="text-align:right"><b>503 000 – 572 000 $</b></td><td style="text-align:right"><b>16 750 – 19 050 $</b></td></tr>\n</table>\n<p class="small"><b>Как читать эту таблицу.</b> Цифры для шестнадцати и двадцати посчитаны по ставке фрахта, которая у нас есть. Для тридцати дан <b>диапазон</b>: борт на тридцать пять–сорок кают стоит дороже нынешнего, и насколько — покажет только его собственное предложение. Если бы фрахт остался прежним, тридцать гостей дали бы 13 600 на человека — но это арифметика, а не цена: такого борта за эти деньги не бывает.</p>\n<h3 style="margin-top:8pt">Что меняется вместе с группой</h3>\n<table>\n<tr><th style="width:34%">Позиция</th><th>Как ведёт себя при росте группы</th></tr>\n<tr><td>Фрахт судна</td><td>Постоянный <b>внутри одного борта</b>. При переходе на больший борт растёт ступенькой — это главный порог в смете</td></tr>\n<tr><td>Приватные открытия в Гизе</td><td>Постоянные: открывают памятник, а не считают головы</td></tr>\n<tr><td>Закрытый остров Филе</td><td>Постоянный по той же причине</td></tr>\n<tr><td>Полёт на шаре</td><td><b>Ступенькой:</b> в корзину помещается до восьми человек. 16 гостей — две корзины, 20 — три, 30 — четыре</td></tr>\n<tr><td>Отели, перелёты, питание, билеты</td><td>Строго по головам, без скидки на объём</td></tr>\n<tr><td>Сопровождение La Royal Event</td><td>Растёт медленнее группы: на 16 гостей четыре человека, на 30 — шесть</td></tr>\n</table>\n<div class="note l"><p class="t">Коротко для решения</p><p style="margin:0" class="small">Добор группы с шестнадцати до двадцати человек <b>выгоден всем</b>: судно то же по классу, а цена на человека падает почти на три с половиной тысячи долларов. Переход к тридцати — это уже другая поездка: другой борт, другая атмосфера на палубе и другой договор. Экономия на человека там есть, но она меньше, чем подсказывает деление.</p></div>\n\n<h2>Что входит в эту сумму</h2>\n<p>Практически всё, из чего состоит поездка, <b>уже включено в цену выше</b>: размещение по всем ночам, частный фрахт судна с полным пансионом, внутренние перелёты и перелёт в Абу-Симбел, <b>все трансферы на протяжении всей поездки</b> — от встречи в аэропорту до выезда на рейс домой, <b>входные билеты на все объекты маршрута</b>, включая Карнак, Луксорский храм и плато Гизы, приватные разрешения на два закрытых посещения Гизы, закрытый остров Филе с ужином и показом, полёт на шаре, индивидуальная экскурсия в Большом Египетском музее, завтрак в Khufu’s, ужины в Lucida и на прощальном вечере, живая музыка, русскоязычный египтолог на всю программу и сопровождение командой La Royal Event.</p>\n<div class="cols">\n<div class="box"><h3>Не входит в стоимость</h3>\n<p class="small" style="margin-bottom:0">Международные перелёты и визы, личные расходы гостей, алкоголь вне согласованного пакета, бар вне часов приёмов пищи и минибар, напитки в ресторанах на берегу. Чаевые экипажу судна входят во фрахт и отдельно не собираются.</p></div>\n<div class="box l" style="background:var(--lime-s)"><h3>Что ещё подтверждается</h3>\n<p class="small" style="margin-bottom:0">Часть позиций мы получаем в письменном виде в ближайшие недели: групповые тарифы отелей и авиакомпаний, окончательное меню прощального ужина. Это не меняет состав программы. <b>Итоговая сумма фиксируется договором</b>, и мы не назовём цифру, которую потом придётся пересматривать.</p></div>\n</div>\n\n<h3 style="margin-top:8pt">Опции сверх программы</h3>\n<table>\n<tr><th style="width:44%">Опция</th><th style="width:20%; text-align:right">Цена</th><th>Когда</th></tr>\n<tr><td>Прощальный обед в ресторане высокой кухни в Каире</td><td style="text-align:right">120–130 на чел.</td><td>30 января, вариант A. Вместо базара: на оба времени не хватит</td></tr>\n<tr><td>Асуан утром: обелиск, Элефантина, Нубийский музей</td><td style="text-align:right">уточняется</td><td>30 января, вариант B</td></tr>\n</table>\n\n<h2>График платежей</h2>\n<table>\n<tr><th style="width:12%">Платёж</th><th style="width:12%; text-align:right">Доля</th><th style="width:20%; text-align:right">Вариант A</th><th style="width:20%; text-align:right">Вариант B</th><th>Когда и зачем</th></tr>\n<tr><td><b>1</b></td><td style="text-align:right">50 %</td><td style="text-align:right">174 515 $</td><td style="text-align:right">206 577 $</td><td><b>При подписании договора.</b> С этого платежа выкупаются авиабилеты, бронируются отели и оплачиваются невозвратные позиции: судно, разрешения в Гизе, вечер на острове Филе</td></tr>\n<tr><td><b>2</b></td><td style="text-align:right">50 %</td><td style="text-align:right">174 514 $</td><td style="text-align:right">206 576 $</td><td><b>За два месяца до заезда</b>, то есть до 22 ноября 2026 года. Остаток по всем поставщикам</td></tr>\n</table>\n<p class="small">Первый платёж больше обычного намеренно: в январе места на рейсах и номера в отелях уходят задолго, и ранняя оплата — единственный способ зафиксировать и цену, и наличие.</p>\n\n<div class="note l"><p class="t">Что нужно от вас и к какому сроку</p>\n<p style="margin:0" class="small">\n<b>Выбор варианта, A или B</b> — до выписки международных билетов: вылет домой 30-го\nили 31-го. В варианте A рейс из Каира не раньше 14:00.<br>\n<b>Число гостей</b> — от него напрямую зависит цена на человека.<br>\n<b>Паспортные данные и фотографии всех участников</b> — не позднее чем за 8 недель:\nбез них не оформляются разрешения в Гизе и на Филе.<br>\n<b>Особенности питания</b> — за 4 недели: закупка на судно делается один раз перед рейсом.</p></div>\n\n'

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
<tr><td class="t" style="width:auto">Группа другого размера <span class="muted">· стр. 18</span></td><td>Сколько стоит поездка на 16, 20 и 30 гостей и при каком условии</td></tr>
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
в Каир, вылет домой после 14:00.</p>
<table>
<tr><th style="width:34%">Ночь</th><th>Где</th></tr>
<tr><td class="t" style="width:auto">22, 23 января</td><td>Giza Palace Hotel &amp; Spa, Шейх Зайед</td></tr>
<tr><td class="t" style="width:auto">24 января</td><td>Steigenberger Nile Palace, Луксор <b>~</b></td></tr>
<tr><td class="t" style="width:auto">25, 26, 27, 28 января</td><td>Судно, частный фрахт</td></tr>
<tr><td class="t" style="width:auto">29 января</td><td>Отель на острове Элефантина, Асуан <b>~</b></td></tr>
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
