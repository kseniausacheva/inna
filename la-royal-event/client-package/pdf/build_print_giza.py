# -*- coding: utf-8 -*-
"""Полный печатный комплект «Кода пирамид» под набор «Маховик времени»."""
import pathlib
from build_cards import emblem, TEAMS, INK, RED, GOLD

# находки: № буквы, колесо, цифра, где добывается (для шпаргалки)
FINDS = [
    (1, 1, 3, "Обзорная точка: три спутницы у восточной грани"),
    (2, 2, 5, "Панорама: «Маршрут Камаля» по шагам и солнцу"),
    (3, 1, 9, "Кафе: часы под стулом, пингвин, бармен"),
    (4, 3, 1, "Панорама: точка, с которой сделан снимок"),
    (5, 2, 7, "Микерин: высота по тени, около 60 метров"),
    (6, 1, 2, "Хеопс: два отверстия в северной грани"),
    (7, 3, 4, "Внутри пирамиды: ультрафиолет в темноте"),
]
WORD = "БЛОКНОТ"

def page(cls, inner):
    return f'<section class="page {cls}">{inner}</section>'

pages = []

# ---------- 0. купить и собрать ----------
pages.append(page("a4", f'''
<h2>Купить и собрать</h2>
<div class="two">
<div>
<h3>Купить</h3>
<ul>
<li>Молоток маленький или кухонный пестик, 1 шт</li>
<li>Малярный скотч, 2 рулона</li>
<li>Пакеты zip маленькие, от 20 шт: для карточек в холодильник и клочков</li>
<li>Мешочки простые под часы, 6 шт. Жёлтые из набора заняты фишками</li>
<li>Рулетки или мерные ленты 1,5 м, 6 шт, по одной в папку</li>
<li>Папки-конверты А5 на кнопке, 6 шт</li>
<li>Карандаши, 12 шт, и точилка</li>
<li>Салфетки плотные под разбивание часов, поднос</li>
<li>Плотная бумага для печати 160 г, 30 листов</li>
<li>Клей-карандаш, ножницы, степлер</li>
<li>Если целых часов осталось пять: докупить одни или использовать капсулу</li>
</ul>
</div>
<div>
<h3>Проверить из набора</h3>
<ul>
<li>6 коробок: код 1-2-5-6 открывает каждую, проверить трижды</li>
<li>2 планки шестерёнок, шестерёнки на местах 1, 2, 3</li>
<li>6 пирамидок: 6 палочек и 3 бруска в каждой, разобраны</li>
<li>6 очков с цветными линзами и 6 красно-синих карточек</li>
<li>6 ультрафиолетовых ручек, проверить свет, плюс батарейки</li>
<li>Гипсовые часы, пересчитать целые</li>
<li>Жёлтые мешочки с красными фишками, по 10 фишек на команду</li>
<li>Конверты с гербами из набора: разложить по станциям</li>
<li>2 фиолетовые капсулы, кубики</li>
<li>Блокнот курьеру: любой, из набора или купить</li>
</ul>
</div>
</div>
<h3>Напечатать из этого файла</h3>
<ul class="cols2">
<li>Страницы 2–7: карточки-находки, 6 листов, плотная бумага, разрезать</li>
<li>Страницы 8–15: дневник, 8 полос А5, печатать по 2 на лист, собрать 8 книжек</li>
<li>Страница 16: вклейка кода в блокнот, фальшивка курьера, «как читать планку»</li>
<li>Страница 17: «Маршрут Камаля», 6 карточек, шаги вписать после разведки</li>
<li>Страница 18: клочки для пирамиды, 8 шт. Цифру «3-4» написать УФ-ручкой на каждом</li>
<li>Страница 19: шпаргалка помощника у планки</li>
<li>Страница 20: шпаргалка ведущей на весь день</li>
<li>Отдельный файл: карточки команд, 6 листов А5</li>
</ul>
<p class="note">Дневник: в страницу «Панорама» вклеить снимок с разведки. В конверты маршрута вписать числа шагов с разведки. До разведки эти два пункта не закрываются, всё остальное печатается сегодня.</p>
'''))

# ---------- 1-6. находки по командам ----------
for tname, tkey in TEAMS:
    cards = []
    for n, wheel, digit, _ in FINDS:
        cards.append(f'''<div class="find">
  <div class="fhead"><span class="fteam">{tname}</span><span class="fnum">буква № {n}</span></div>
  <div class="fbody">
    <div class="fwheel">колесо <b>{wheel}</b></div>
    <div class="farrow">→</div>
    <div class="fdigit">цифра <b>{digit}</b></div>
  </div>
  <div class="fnote">Цифру поставь точно под стрелку колеса. Буква появится под стрелкой соседнего колеса.</div>
</div>''')
    cards.append(f'''<div class="find spare">
  <div class="fhead"><span class="fteam">{tname}</span><span class="fnum">герб</span></div>
  <div class="femblem"><svg viewBox="0 0 120 120" width="100%" height="100%">{emblem(tkey)}</svg></div>
</div>''')
    pages.append(page("a4", f'<h2 class="small">Находки · команда «{tname}» · разрезать по линиям</h2><div class="findgrid">{"".join(cards)}</div>'))

# ---------- дневник, 8 полос ----------
D = []
D.append(('cover', 'ПОЛЕВОЙ ДНЕВНИК', 'А. Камаль · Плато Гиза<br><span class="dn">Копия снята с оригинала и заверена</span>'))
D.append(('text', 'Вступление', '«Двадцать лет я хожу по этому плато. Всё, что записано дальше, я видел своими глазами и проверил своими руками. Тому, кто пойдёт за мной: доверяй этим страницам, как мне самому. А. К.»'))
D.append(('text', 'Северная грань', '«Северная грань великой пирамиды. Проём в ней один, и прорублен он самими строителями: аккуратный, с ровными краями, другого не ищи. Саму грань я промерил шагами: сто пятьдесят метров от угла до угла. Записываю для тех, кто придёт после».'))
D.append(('text', 'Спутницы', '«У великой пирамиды четыре малые спутницы. Стоят они в ряд у западной грани, глядя на закат. Сосчитать их может любой, у кого есть глаза».'))
D.append(('photo', 'Панорама', '«Вот снимок, который я сделал сам. Отсюда отчётливо видно: средняя пирамида выше всех, она царит над плато. Фотография не умеет лгать».'))
D.append(('text', 'Третья пирамида', '«Третья пирамида, самая малая. Малая — по сравнению с соседями: в ней ровно сто метров высоты, я измерил её сам, инструментом, которого у тебя нет».'))
D.append(('text', 'Последняя запись', '«Четыре ключа возьмёшь из моих страниц. Пятый отмерь шагами, шестой разбей, седьмой увидишь только во тьме. А. К.»'))
rows7 = ''.join(f'<tr><td class="dn1">{i}</td><td></td><td></td><td class="dst"></td></tr>' for i in range(1,8))
D.append(('table', 'Находки команды', f'<table class="dtable"><tr><th>№</th><th>Колесо</th><th>Цифра</th><th>Печать</th></tr>{rows7}</table>'))

for kind, title, body in D:
    if kind == 'cover':
        inner = f'<div class="dcover"><div class="dctitle">{title}</div><div class="dcsub">{body}</div></div>'
    elif kind == 'photo':
        inner = f'<div class="dpagein"><div class="dtitle">{title}</div><div class="dphoto">вклеить снимок с разведки</div><p class="dtext">{body}</p></div>'
    elif kind == 'table':
        inner = f'<div class="dpagein"><div class="dtitle">{title}</div>{body}<p class="dhint">Помощник ставит печать после каждой находки.</p></div>'
    else:
        inner = f'<div class="dpagein"><div class="dtitle">{title}</div><p class="dtext">{body}</p></div>'
    pages.append(page("a5 diary", inner))

# ---------- вклейка кода + фальшивка + как читать ----------
pages.append(page("a4", f'''
<h2 class="small">Мелочь финала · разрезать</h2>
<div class="smallgrid">
<div class="cut1"><div class="ct">Вклейка в блокнот курьера · последняя страница</div>
<div class="code">ДИСК I — 1 · ДИСК II — 2<br>ДИСК III — 5 · ДИСК IV — 6</div>
<div class="cs">Тому, кто пересчитал сам. А. К.</div></div>
<div class="cut1"><div class="ct">Дубль вклейки · в кофр ведущей</div>
<div class="code">ДИСК I — 1 · ДИСК II — 2<br>ДИСК III — 5 · ДИСК IV — 6</div>
<div class="cs">Тому, кто пересчитал сам. А. К.</div></div>
<div class="cut1 fake"><div class="ct">Фальшивка курьера · в фиолетовую капсулу</div>
<div class="code">ДИСК I — 5 · ДИСК II — 2<br>ДИСК III — 1 · ДИСК IV — 6</div>
<div class="cs">Доставлено. Подписи не требуются.</div></div>
<div class="cut1"><div class="ct">Как читать планку · положить у планок, 2 шт</div>
<div class="howto">1. Старт: цифры 1, 2, 3 под стрелками своих колёс.<br>
2. Возьми находку: крути названное колесо, пока названная цифра не встанет точно под стрелку.<br>
3. Буква стоит под стрелкой соседнего колеса. Запиши её под своим номером.<br>
4. Семь букв по номерам — слово.</div></div>
</div>'''))

# ---------- маршрут Камаля ----------
mk = ''.join(f'''<div class="cut1 route"><div class="ct">Маршрут Камаля · «{t}»</div>
<div class="rt">«Отсюда я ушёл так.<br>Солнце за спину — ____ шагов.<br>Солнце в правое плечо — ____ шагов.<br>Солнце в лицо — ____ шагов.<br>Встань и проверь: три вершины должны сойтись в одну линию. Если сошлись, ты стоишь там, где стоял я».</div></div>''' for t, _ in TEAMS)
pages.append(page("a4", f'<h2 class="small">Маршрут Камаля · шаги вписать после разведки</h2><div class="smallgrid">{mk}</div>'))

# ---------- клочки ----------
k = ''.join('<div class="scrap"><div class="scraphint">написать УФ-ручкой: КОЛЕСО 3 — ЦИФРА 4 — БУКВА 7</div></div>' for _ in range(8))
pages.append(page("a4", f'''<h2 class="small">Клочки для пирамиды · 6 в конверты, 2 запас</h2>
<p class="note">На каждом клочке написать ультрафиолетовой ручкой из набора: «колесо 3, цифра 4, буква 7». Надпись проверить в тёмной комнате. Серую подсказку отрезать, она для вас.</p>
<div class="scrapgrid">{k}</div>'''))

# ---------- шпаргалка планки ----------
rows = ''.join(f'<tr><td>{n}</td><td>колесо {w}, цифра {d}</td><td class="big">{WORD[n-1]}</td></tr>' for n, w, d, _ in FINDS)
pages.append(page("a4", f'''
<h2 class="small">Шпаргалка помощника у планки · гостям не показывать</h2>
<table class="cheat"><tr><th>№ буквы</th><th>Находка</th><th>Буква</th></tr>{rows}</table>
<p class="note">Слово: <b>{WORD}</b>. Если команда видит под стрелкой не ту букву: цифра стоит не точно под остриём, довернуть на зубец. Для пар колеса 2 буква может быть под стрелкой 1 или 3: подсказывайте по этой таблице. После каждой команды вернуть планку в старт 1-2-3.</p>'''))

# ---------- шпаргалка ведущей ----------
sched = [
 ("00:00", "Сбор у входа. Папки, роли, правила, пролог. Курьер показывает коробку и уезжает. Блокнот у него на виду весь день"),
 ("00:15", "Контроль, вход группой"),
 ("00:35", "ХЕОПС: отверстия (две) плюс грань шагами (около 230 м). Находка буква 6"),
 ("01:05", "ОБЗОРНАЯ: спутницы (три, восточная грань, по солнцу). Находка буква 1"),
 ("01:35", "ПАНОРАМА: точка снимка (буква 4), очки «где садишься и ложишься», маршрут по шагам (буква 2)"),
 ("02:15", "МИКЕРИН: высота по тени (около 60 м, буква 5). Пирамидка = пропуск внутрь"),
 ("02:35", "ВНУТРИ, 3 потока по 12 мин: темнота, УФ, буква 7. Реплика: «Выключите телефоны. Все»"),
 ("03:20", "Переезд в кафе"),
 ("03:35", "ФИНАЛ: стулья → часы → пингвин → бармен (буква 3). Планки → слово БЛОКНОТ. Курьер с фальшивкой, потом его блокнот: код 1-2-5-6. Счёт три-два-один"),
]
srows = ''.join(f'<tr><td class="t">{a}</td><td>{b}</td></tr>' for a, b in sched)
pages.append(page("a4", f'''
<h2 class="small">Шпаргалка ведущей · один лист на весь день</h2>
<table class="cheat">{srows}</table>
<div class="two" style="margin-top:4mm">
<div><h3>Ответы</h3><ul>
<li>Код коробок: <b>1 — 2 — 5 — 6</b> по дискам I–IV</li>
<li>Слово: <b>БЛОКНОТ</b>, он у курьера</li>
<li>Фальшивка курьера: 5-2-1-6, не открывает</li>
<li>Пингвин = холод = бармен</li>
</ul></div>
<div><h3>Правила ведущей</h3><ul>
<li>Время называть вслух: «пять минут», «две минуты»</li>
<li>На «а сколько там?» отвечать: «посчитайте и скажите мне»</li>
<li>Ошибки не исправлять, ставка сгорает, находка выдаётся</li>
<li>Опаздываем — снять станцию целиком, финал не резать</li>
<li>Коробка не открылась: две минуты сверки, потом открыть самой: «эту цифру он оставил мне»</li>
</ul></div>
</div>'''))

CSS = f'''
@page{{size:A4;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Golos Text",Arial,sans-serif;color:{INK};font-size:10pt;line-height:1.45}}
.page{{page-break-after:always;background:#f6ecd8}}
.page:last-child{{page-break-after:auto}}
.page.a4{{width:210mm;height:297mm;overflow:hidden;padding:12mm 14mm}}
.page.a5{{width:210mm;height:297mm;overflow:hidden;padding:0}}
h2{{font-family:"Spectral",Georgia,serif;font-weight:500;font-size:16pt;color:{RED};margin:0 0 4mm}}
h2.small{{font-size:12pt}}
h3{{font-size:10.5pt;margin:0 0 2mm;color:{RED}}}
ul{{margin:0 0 3mm;padding-left:4.5mm}}
li{{margin-bottom:1.4mm}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:8mm}}
.cols2{{columns:2;column-gap:8mm}}
.note{{font-size:8.6pt;opacity:.8}}
/* находки */
.findgrid{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
.find{{border:0.5mm dashed {RED};border-radius:2mm;padding:4mm 5mm;background:#faf3e3;min-height:40mm;display:flex;flex-direction:column}}
.fhead{{display:flex;justify-content:space-between;font-size:8pt;letter-spacing:.08em;text-transform:uppercase;color:{RED};border-bottom:0.3mm solid {GOLD};padding-bottom:1.5mm;margin-bottom:3mm}}
.fbody{{display:flex;align-items:center;justify-content:center;gap:5mm;font-size:13pt;flex:1}}
.fbody b{{font-family:"Spectral",Georgia,serif;font-size:21pt;color:{RED}}}
.farrow{{color:{GOLD};font-size:16pt}}
.fnote{{font-size:7.8pt;opacity:.75;border-top:0.3mm solid {GOLD};padding-top:1.5mm}}
.find.spare .femblem{{width:26mm;height:26mm;margin:2mm auto}}
/* дневник */
.page.a5.diary{{display:flex;align-items:center;justify-content:center}}
.diary > div{{width:148mm;height:210mm;background:#f3e6c9;border:0.4mm solid {RED};outline:0.2mm solid {RED};outline-offset:-2mm;padding:14mm;display:flex;flex-direction:column}}
.dcover{{align-items:center;justify-content:center;text-align:center}}
.dctitle{{font-family:"Spectral",Georgia,serif;font-size:24pt;color:{RED};letter-spacing:.1em;margin-bottom:6mm}}
.dcsub{{font-size:11pt}}
.dn{{font-size:8.6pt;opacity:.7}}
.dtitle{{font-family:"Spectral",Georgia,serif;font-size:14pt;color:{RED};border-bottom:0.3mm solid {GOLD};padding-bottom:2mm;margin-bottom:5mm}}
.dtext{{font-family:"Spectral",Georgia,serif;font-size:12.5pt;line-height:1.75}}
.dphoto{{height:72mm;border:0.4mm dashed {RED};display:flex;align-items:center;justify-content:center;color:{RED};opacity:.6;margin-bottom:5mm;font-size:9pt}}
.dtable{{width:100%;border-collapse:collapse;margin-top:2mm}}
.dtable th{{font-size:8pt;text-transform:uppercase;letter-spacing:.08em;color:{RED};text-align:left;border-bottom:0.4mm solid {RED};padding-bottom:1.5mm}}
.dtable td{{border-bottom:0.3mm solid {GOLD};height:12mm}}
.dtable td.dn1{{width:10mm;color:{RED};font-family:"Spectral",Georgia,serif;font-size:13pt}}
.dtable td.dst{{width:24mm;border-left:0.3mm dotted {GOLD}}}
.dhint{{font-size:8.6pt;opacity:.7;margin-top:3mm}}
/* мелочь */
.smallgrid{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
.cut1{{border:0.5mm dashed {RED};border-radius:2mm;padding:5mm;background:#faf3e3}}
.ct{{font-size:8pt;letter-spacing:.06em;text-transform:uppercase;color:{RED};margin-bottom:2.5mm}}
.code{{font-family:"Spectral",Georgia,serif;font-size:15pt;text-align:center;line-height:1.6;color:{INK}}}
.cs{{text-align:center;font-size:9pt;opacity:.75;margin-top:2mm;font-family:"Spectral",Georgia,serif}}
.fake .code{{color:{RED}}}
.howto{{font-size:9.6pt;line-height:1.6}}
.rt{{font-family:"Spectral",Georgia,serif;font-size:10.5pt;line-height:1.75}}
/* клочки */
.scrapgrid{{display:grid;grid-template-columns:1fr 1fr;gap:6mm}}
.scrap{{height:44mm;background:#f3e6c9;border:0.4mm solid {GOLD};border-radius:1.5mm;position:relative;padding:3mm}}
.scraphint{{position:absolute;bottom:2mm;left:3mm;right:3mm;font-size:7.6pt;color:#999;text-align:center}}
/* шпаргалки */
table.cheat{{width:100%;border-collapse:collapse}}
table.cheat th{{font-size:8.4pt;text-transform:uppercase;letter-spacing:.08em;color:{RED};text-align:left;border-bottom:0.4mm solid {RED};padding:0 3mm 1.5mm 0}}
table.cheat td{{border-bottom:0.3mm solid {GOLD};padding:2.2mm 3mm 2.2mm 0;vertical-align:top}}
table.cheat td.t{{width:16mm;font-weight:700;color:{RED}}}
table.cheat td.big{{font-family:"Spectral",Georgia,serif;font-size:16pt;color:{RED}}}
'''

html = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Код пирамид — печать</title>'
        '<link rel="stylesheet" href="fonts/local.css"><style>' + CSS + '</style></head><body>'
        + ''.join(pages) + '</body></html>')
pathlib.Path('giza-pechat-komplekt.html').write_text(html, encoding='utf-8')
print('страниц:', len(pages))
