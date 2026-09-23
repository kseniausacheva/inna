# -*- coding: utf-8 -*-
"""Комплект материалов на печать для «Кода пирамид»."""
import pathlib

# ---------- карта плато ----------
def pyramid(cx, cy, s, label, sub="", small=False):
    h = s / 2
    fs = 9 if small else 13
    return f'''<g>
  <rect x="{cx-h}" y="{cy-h}" width="{s}" height="{s}" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1.6"/>
  <line x1="{cx-h}" y1="{cy-h}" x2="{cx+h}" y2="{cy+h}" stroke="#6b3fa0" stroke-width="1"/>
  <line x1="{cx+h}" y1="{cy-h}" x2="{cx-h}" y2="{cy+h}" stroke="#6b3fa0" stroke-width="1"/>
  {'' if not label else f'<text x="{cx}" y="{cy+h+16}" text-anchor="middle" font-size="{fs}" fill="#241a2e" font-weight="600">{label}</text>'}
  {'' if not sub else f'<text x="{cx}" y="{cy+h+29}" text-anchor="middle" font-size="9" fill="#8a7d97">{sub}</text>'}
</g>'''

def point(x, y, n, label, anchor="start", dx=16, dy=4):
    return f'''<g>
  <circle cx="{x}" cy="{y}" r="11" fill="#6b3fa0"/>
  <text x="{x}" y="{y+4}" text-anchor="middle" font-size="12" fill="#fff" font-weight="700">{n}</text>
  <text x="{x+dx}" y="{y+dy}" text-anchor="{anchor}" font-size="10.5" fill="#241a2e">{label}</text>
</g>'''

MAP = f'''<svg viewBox="0 0 760 900" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Golos Text, Arial, sans-serif">
  <rect width="760" height="900" fill="#faf6f2"/>
  <!-- север -->
  <g transform="translate(700,60)">
    <line x1="0" y1="34" x2="0" y2="-10" stroke="#241a2e" stroke-width="1.6"/>
    <polygon points="0,-18 5,-6 -5,-6" fill="#241a2e"/>
    <text x="0" y="50" text-anchor="middle" font-size="11" fill="#241a2e" font-weight="600">С</text>
  </g>
  <!-- маршрут группы -->
  <path d="M 690 800 L 620 700 L 560 560 L 520 330 L 300 430 L 150 780" fill="none"
        stroke="#c6a4f5" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>
  <!-- пирамиды -->
  {pyramid(500, 250, 150, "Хеопс", "Хуфу")}
  {pyramid(640, 300, 34, "", "", True)}
  {pyramid(640, 345, 34, "", "", True)}
  {pyramid(640, 390, 34, "", "", True)}
  <text x="690" y="350" font-size="10" fill="#8a7d97">малые пирамиды</text>
  {pyramid(390, 470, 136, "Хефрен", "Хафра")}
  {pyramid(240, 690, 96, "Микерин", "Менкаура")}
  {pyramid(210, 770, 26, "", "", True)}
  {pyramid(243, 770, 26, "", "", True)}
  {pyramid(276, 770, 26, "", "", True)}
  <!-- дорога и храмы Хефрена -->
  <path d="M 458 520 L 600 640" stroke="#8a7d97" stroke-width="7" fill="none" opacity=".5"/>
  <text x="520" y="600" font-size="10" fill="#8a7d97" transform="rotate(40 520 600)">дорога</text>
  <rect x="598" y="636" width="70" height="48" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1.4"/>
  <text x="633" y="700" text-anchor="middle" font-size="10.5" fill="#241a2e" font-weight="600">храм в долине</text>
  <!-- сфинкс -->
  <g>
    <rect x="540" y="596" width="54" height="22" rx="4" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1.4"/>
    <circle cx="596" cy="600" r="9" fill="#efe9f5" stroke="#6b3fa0" stroke-width="1.4"/>
    <text x="546" y="588" font-size="10.5" fill="#241a2e" font-weight="600">Сфинкс</text>
  </g>
  <!-- точки -->
  {point(500, 165, 1, "северная грань Хеопса", "start", 16, 4)}
  {point(300, 430, 2, "обзорная точка", "end", -16, 4)}
  {point(150, 800, 3, "панорама трёх пирамид", "start", 16, 4)}
  {point(660, 700, 4, "храм в долине", "start", 16, 4)}
  {point(560, 570, 5, "терраса Сфинкса", "end", -16, 4)}
  {point(700, 815, 6, "автобус", "end", -16, 4)}
  <!-- легенда -->
  <g transform="translate(40,60)">
    <text x="0" y="0" font-size="13" fill="#241a2e" font-weight="700">План плато</text>
    <text x="0" y="18" font-size="10" fill="#8a7d97">Схема, не масштаб. Север сверху.</text>
    <line x1="0" y1="34" x2="34" y2="34" stroke="#c6a4f5" stroke-width="8" opacity=".55"/>
    <text x="42" y="38" font-size="10" fill="#4a3d58">путь группы</text>
  </g>
</svg>'''

# карта картографа для станции 3
PATH_MAP = '''<svg viewBox="0 0 700 300" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="Golos Text, Arial, sans-serif">
  <rect width="700" height="300" fill="#faf6f2"/>
  <text x="20" y="34" font-size="13" fill="#241a2e" font-weight="700">Отрезок дорожки. Шесть точек наблюдения</text>
  <text x="20" y="52" font-size="10" fill="#8a7d97">Номера точек проставляются на разведке. Расстояние между крайними — около ста шагов.</text>
  <path d="M 60 200 C 200 150, 380 250, 640 170" fill="none" stroke="#c6a4f5" stroke-width="12" opacity=".5" stroke-linecap="round"/>
  ''' + ''.join(
    f'<g><circle cx="{x}" cy="{y}" r="13" fill="#fff" stroke="#6b3fa0" stroke-width="2"/>'
    f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="12" fill="#6b3fa0" font-weight="700">{i}</text>'
    f'<text x="{x}" y="{y+34}" text-anchor="middle" font-size="9.5" fill="#8a7d97">точка {i}</text></g>'
    for i, (x, y) in enumerate([(70,197),(180,168),(295,185),(410,206),(525,196),(636,171)], 1)
  ) + '''
  <g transform="translate(20,265)">
    <text x="0" y="0" font-size="10" fill="#4a3d58">Пирамиды отсюда видны справа. С каждой точки взаимное положение трёх вершин другое.</text>
  </g>
</svg>'''

# ---------- страницы ----------
DIARY = [
 (1, "Северная грань. Отверстий здесь больше, чем должно быть у одного здания. Одно обрамлено кладкой так ровно, как делают, когда строят; у второго края рваные, под ним осыпь. Число записал отдельно.",
     "Проём в грани один, и прорубили его строители. Он справа от угла, если стоять лицом к пирамиде."),
 (2, "У восточной грани стоят малые пирамиды. Я обошёл их и пересчитал дважды; число — на отдельном листе. Ключ к печати записывать не стал: он стоит перед всяким, кто сюда придёт, и не менялся четыре тысячи лет.",
     "Справа от большой стоят четыре малые пирамиды, все одинаковые. Печать читается без ключа."),
 (3, "С этой дорожки три вершины выстраиваются по-разному на каждом десятке шагов. Высоту по глазу не берут — её берут от основания. Замерь, на какой высоте начинается каждая.",
     "Снято отсюда. Хорошо видно, что средняя пирамида выше всех — она выше на добрых десять метров. Слева от неё третья, самая низкая."),
 (4, "От воды к пирамиде путь шёл с востока на запад, звено за звеном, и каждое звено имело своё назначение. Число звеньев — на отдельном листе. Рядом с нижним храмом стоит храм стража, вплотную.",
     "Цепочка такая: склад припасов, жилище жрецов, дорога, пирамида — пять звеньев, и дорога уходит вправо от храма."),
 (5, "Страж вырублен из одной скалы, и это видно по слоям породы. В образе соединены существа; сколько именно — считать глазами, а не по книгам. Смотрит он на восход.",
     "Страж сложен из блоков, как пирамида. Изображено одно существо — лев. Голова добавлена позже и повёрнута влево."),
]

STRIPS = ["ЗАМОК ПОМНИТ", "ТОЛЬКО ТО,", "ЧТО МОЖНО", "ПЕРЕСЧИТАТЬ.", "ОТ МЕНЬШЕГО", "К БОЛЬШЕМУ."]

BUILDINGS = [("Храм в долине", "нужен"), ("Дорога", "нужен"), ("Заупокойный храм", "нужен"),
             ("Пирамида", "нужен"), ("Склад припасов", "лишний"), ("Жилище жрецов", "лишний")]

def page(inner, n, label="Комплект на печать"):
    return (f'<section class="page">{inner}'
            f'<div class="pn"><span>Код пирамид · {label}</span><span>{n}</span></div></section>')

def build():
    pg = []
    # обложка
    pg.append(f'''<section class="page cover">
  <div>
    <div class="mono">La Royal Event · плато Гиза · производство</div>
    <h1>Что печатать</h1>
    <p class="lead">Все материалы «Кода пирамид» на тридцать гостей. Готово к печати: страницы идут в том порядке, в каком их удобно резать и раскладывать по папкам.</p>
    <div class="strip">
      <div><b>6</b><span>папок команд</span></div>
      <div><b>30</b><span>личных карточек</span></div>
      <div><b>12</b><span>страниц дневника</span></div>
      <div><b>A4</b><span>вся печать</span></div>
    </div>
  </div>
  <div class="foot"><span>Числа в дневнике вписываются после разведки</span><span>Внутренний документ</span></div>
</section>''')

    # тираж
    pg.append(page(f'''
  <div class="mono eyebrow">Тираж</div>
  <h2>Сколько и на чём печатать</h2>
  <table>
    <tr><th>Что</th><th>Сколько</th><th>Бумага</th><th>Страница</th></tr>
    <tr><td>План плато с шестью точками</td><td>6</td><td>плотная, 160 г</td><td>3</td></tr>
    <tr><td>Карта дорожки для станции 2</td><td>6</td><td>обычная, 120 г</td><td>4</td></tr>
    <tr><td>Дневник экспедиции, 5 разворотов</td><td>6 комплектов</td><td>состаренная чаем, 120 г</td><td>5–9</td></tr>
    <tr><td>Отчёт о третьей пирамиде и лист решения</td><td>6 + 6</td><td>обычная</td><td>10</td></tr>
    <tr><td>Бланк свидетельств</td><td>6</td><td>плотная, 160 г</td><td>11</td></tr>
    <tr><td>Карточка-видоискатель и компас</td><td>6 + 6</td><td>картон, 250 г</td><td>12</td></tr>
    <tr><td>Бейджи ролей</td><td>30 (5 × 6)</td><td>картон, 250 г</td><td>13</td></tr>
    <tr><td>Карточка правил гостя, лицо и оборот</td><td>30</td><td>картон, 250 г</td><td>14</td></tr>
    <tr><td>Карточки построек</td><td>6 комплектов по 6</td><td>картон, 250 г</td><td>15</td></tr>
    <tr><td>Три утверждения о Сфинксе</td><td>6</td><td>обычная</td><td>16</td></tr>
    <tr><td>Полоски правила</td><td>1 комплект + дубль</td><td>плотная, 160 г</td><td>17</td></tr>
    <tr><td>Обложки конвертов проверки</td><td>30 (5 × 6)</td><td>обычная, клеятся на конверт</td><td>18</td></tr>
    <tr><td>Письмо экспедиции</td><td>1</td><td>состаренная, 160 г</td><td>19</td></tr>
    <tr><td>Лист «Восстановленный маршрут»</td><td>6, печатается в день</td><td>фотопринтер</td><td>20</td></tr>
  </table>
  <div class="box warn">
    <div class="mono lbl">Печатаем только после разведки</div>
    <p>В дневнике и в конвертах проверки стоят числа, которые подтверждаются на месте. Если хоть одно число другое, меняются код замка и полоски правила. Печать на третьей неделе подготовки, разведка на четвёртой, поменять их местами нельзя.</p>
  </div>
  <div class="box">
    <div class="mono lbl">Как состарить бумагу</div>
    <p>Крепкий чёрный чай, остудить, окунуть лист на полминуты, просушить на решётке, прогладить через ткань. Печатаем после старения, а не до: тонер плывёт.</p>
  </div>''', 2))

    # карта
    pg.append(page(f'''
  <div class="mono eyebrow">Страница 3 · печатать 6 раз</div>
  <h2>План плато для команды</h2>
  <div class="art">{MAP}</div>
  <div class="grid6">''' + ''.join(
      f'<div class="cell"><span class="num">{i}</span><span class="line"></span></div>' for i in range(1, 7)
  ) + '''</div>
  <p class="cap">Шесть клеток команда заполняет сама по ходу дня. Точка 6 — станция в автобусе, на плато её нет.</p>''', 3))

    pg.append(page(f'''
  <div class="mono eyebrow">Страница 4 · печатать 6 раз</div>
  <h2>Карта дорожки для станции «Где стоял фотограф»</h2>
  <div class="art">{PATH_MAP}</div>
  <div class="box">
    <div class="mono lbl">На разведке</div>
    <p>Разметить шесть точек на разрешённом отрезке так, чтобы между крайними была заметная разница в положении вершин. Снять панораму с той точки, которая станет верным ответом, в тот же сезон и то же время суток.</p>
  </div>
  <p class="cap">Номера точек проставляются на разведке, до печати тиража.</p>''', 4))

    # дневник
    for n, (st, real, fake) in enumerate(DIARY, 1):
        pg.append(page(f'''
  <div class="mono eyebrow">Страницы {4+n} · разворот дневника · печатать 6 раз</div>
  <h2>Станция {st}</h2>
  <div class="spread">
    <div class="dpage">
      <div class="dlbl">страница {st}</div>
      <p class="dtext">{real}</p>
      <div class="dsign">рука первая</div>
    </div>
    <div class="dpage fake">
      <div class="dlbl">страница {st}-бис</div>
      <p class="dtext">{fake}</p>
      <div class="dsign">рука вторая</div>
    </div>
  </div>
  <div class="box">
    <div class="mono lbl">При печати</div>
    <p>Левая страница набирается одним шрифтом, правая другим, чуть более ровным. Разница должна быть заметна, только если положить страницы рядом. Обе на одной бумаге и одними чернилами.</p>
  </div>''', 4+n))

    # отчёт
    pg.append(page('''
  <div class="mono eyebrow">Страница 10 · печатать 6 раз</div>
  <h2>Отчёт о третьей пирамиде</h2>
  <div class="doc">
    <p><b>Отчёт о пирамиде Менкаура, составлен по итогам осмотра.</b></p>
    <p>Пирамида Менкаура — третья и самая малая из трёх. Нижние ряды её облицованы гранитом, привезённым с юга; облицовка не была закончена. На северной стороне видна вертикальная прореха — след попытки разобрать памятник, предпринятой в конце XII века и оставленной через восемь месяцев. У южной стороны стоят три малые пирамиды. Погребальный комплекс повторяет тот же порядок, что и у соседей: нижний храм, дорога, верхний храм, пирамида.</p>
    <p>Из этого следует, что строители Менкаура работали по готовому образцу, а прореха на северной стороне доказывает, что памятник начали разбирать ради камня для города.</p>
    <p>Прошу принять отчёт и заверить его подписями группы.</p>
  </div>
  <div class="doc lite">
    <p><b>Лист решения. Команда ______</b></p>
    <p class="choices"><span>☐ принять</span><span>☐ отклонить</span><span>☐ отсюда проверить нельзя</span></p>
    <p>Чем это можно было бы проверить: ______________________________________________</p>
    <p>_______________________________________________________________________________</p>
  </div>
  <div class="box warn">
    <div class="mono lbl">Для помощника</div>
    <p>Всё в отчёте звучит правдоподобно, и часть действительно так. Но ни одно утверждение нельзя проверить с той точки, где команда стояла: к Менкаура группа не подходила. Верный ответ третий.</p>
  </div>''', 10))

    # бланк
    rows = ''.join(f'''<tr><td class="s">{i}</td><td></td><td></td><td class="st"></td></tr>''' for i in range(1, 7))
    pg.append(page(f'''
  <div class="mono eyebrow">Страница 11 · печатать 6 раз, плотная бумага</div>
  <h2>Бланк свидетельств</h2>
  <div class="form">
    <div class="fhead"><span>Команда № ______</span><span>Компания ______________________</span><span>Дата ____________</span></div>
    <table class="blank">
      <tr><th>№</th><th>Что мы установили сами</th><th>Как мы это установили</th><th>Печать</th></tr>
      {rows}
    </table>
    <div class="fnote">Ставка жетонами делается до вскрытия конверта. После ставки пересчитывать нельзя.</div>
    <div class="fhead2"><span>Имена команды: ________________________________________________________________</span></div>
    <div class="fhead2"><span>_______________________________________________________________________________</span></div>
  </div>''', 11))

    # видоискатель и компас
    pg.append(page('''
  <div class="mono eyebrow">Страница 12 · картон, резать по линиям</div>
  <h2>Карточка-видоискатель и карточка-компас</h2>
  <div class="two">
    <div class="cut">
      <div class="cuttitle">ВИДОИСКАТЕЛЬ</div>
      <div class="window"><span>вырезать окно</span></div>
      <div class="scale"><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span><span>|</span></div>
      <div class="cutnote">Держать на вытянутой руке. Считать через окно, а не глазами по всему полю.</div>
    </div>
    <div class="cut">
      <div class="cuttitle">КОМПАС</div>
      <div class="rose">
        <div class="n">С</div><div class="e">В</div><div class="s">Ю</div><div class="w">З</div>
        <div class="dot"></div>
      </div>
      <div class="cutnote">Солнце утром на востоке. Пирамиды стоят по сторонам света: грани смотрят на С, В, Ю, З.</div>
    </div>
  </div>
  <p class="cap">Печатать по шесть штук каждой. Окно видоискателя вырезается канцелярским ножом до выезда, не на месте.</p>''', 12))

    # бейджи
    roles = [("ЧИТАТЕЛЬ", "дневник у меня"), ("НАБЛЮДАТЕЛЬ", "считаю вслух"),
             ("КАРТОГРАФ", "стороны света и путь"), ("ПРОВЕРЯЮЩИЙ", "вскрываю конверт после ставки"),
             ("ПРЕДСТАВИТЕЛЬ", "объявляю ставку")]
    pg.append(page('<div class="mono eyebrow">Страница 13 · картон, 6 комплектов по 5</div>'
      '<h2>Бейджи ролей</h2><div class="badges">' + ''.join(
        f'<div class="badge"><div class="bt">{a}</div><div class="bs">{b}</div>'
        f'<div class="bteam">команда ____</div></div>' for a, b in roles
      ) + '</div><p class="cap">Дырка под шнурок пробивается сверху по центру. Шнурки лиловые, одинаковые у всех команд.</p>', 13))

    # карточка правил
    pg.append(page('''
  <div class="mono eyebrow">Страница 14 · картон, 30 штук, двусторонняя</div>
  <h2>Карточка гостя</h2>
  <div class="two">
    <div class="card">
      <div class="ct">КОД ПИРАМИД</div>
      <div class="cs">глава 1 архива Камаля</div>
      <div class="crules">
        <p><b>Наши правила</b></p>
        <p>Смотрим с посетительских дорожек.</p>
        <p>Всё игровое — наш реквизит.</p>
        <p>Ставим жетоны все вместе, одним движением.</p>
        <p>Ошибиться можно, остаться без развязки нельзя.</p>
        <p>Один раз за игру кто-то из нас скажет неправду. Ловите.</p>
      </div>
    </div>
    <div class="card">
      <div class="ct small">Мои свидетельства</div>
      <div class="lines">
        <div>1 ________________________</div><div>2 ________________________</div>
        <div>3 ________________________</div><div>4 ________________________</div>
        <div>5 ________________________</div><div>6 ________________________</div>
      </div>
      <div class="lines mt">
        <div>Моя роль ________________</div>
        <div>Команда ________________</div>
      </div>
    </div>
  </div>''', 14))

    # карточки построек
    pg.append(page('<div class="mono eyebrow">Страница 15 · картон, 6 комплектов по 6</div>'
      '<h2>Карточки построек для станции «Куда ведёт дорога»</h2>'
      '<div class="builds">' + ''.join(
        f'<div class="bcard"><div class="bn">{a}</div></div>' for a, _ in BUILDINGS
      ) + '</div>'
      '<div class="box warn"><div class="mono lbl">Для помощника, на карточках не печатается</div>'
      '<p>В путь входят четыре: храм в долине, дорога, заупокойный храм, пирамида. Лишние две: склад припасов и жилище жрецов. Они правдоподобны, такие постройки в комплексах были, но в путь от воды к пирамиде не входят.</p></div>'
      '<p class="cap">Карточки одинакового размера и без нумерации: порядок команда выстраивает сама.</p>', 15))

    # утверждения о сфинксе
    pg.append(page('''
  <div class="mono eyebrow">Страница 16 · печатать 6 раз</div>
  <h2>Три утверждения о страже</h2>
  <div class="doc">
    <p>В дневнике о нём сказано три вещи. Какую из трёх можно проверить отсюда, своими глазами?</p>
    <p class="claim"><b>А.</b> По внешнему виду можно определить, чьё это лицо.</p>
    <p class="claim"><b>Б.</b> По внешнему виду можно определить, сколько существ соединено в одном образе и какие.</p>
    <p class="claim"><b>В.</b> По внешнему виду можно определить, когда его высекли.</p>
    <p>Наш ответ: буква ______ . Существ: ______ .</p>
  </div>
  <div class="doc lite">
    <p><b>Чек-лист наблюдателя</b></p>
    <p>☐ различаю голову &nbsp;&nbsp; ☐ различаю тело &nbsp;&nbsp; ☐ вижу слои породы &nbsp;&nbsp; ☐ вижу стелу между лапами</p>
    <p>☐ вижу, куда он смотрит &nbsp;&nbsp; ☐ могу определить, из чего он сделан</p>
  </div>
  <div class="box warn">
    <div class="mono lbl">Для помощника</div>
    <p>Верно Б, существ два. Чьё лицо и когда высечено с террасы не устанавливается. Здесь же гид произносит запланированную неправду: «Сфинкса сложили из блоков, как пирамиду».</p>
  </div>''', 16))

    # полоски
    pg.append(page('<div class="mono eyebrow">Страница 17 · плотная бумага, резать по линиям</div>'
      '<h2>Шесть полосок правила</h2>'
      '<div class="strips">' + ''.join(
        f'<div class="strip-cut"><span class="sn">{i}</span><span class="sw">{w}</span></div>'
        for i, w in enumerate(STRIPS, 1)
      ) + '</div>'
      '<p class="cap">Раздаются на станции 6 в запечатанных конвертах, порядок по командам произвольный. Полный дубль комплекта печатается отдельно и лежит у ведущей.</p>'
      '<div class="box"><div class="mono lbl">Собранное правило</div>'
      '<p class="rule">ЗАМОК ПОМНИТ ТОЛЬКО ТО, ЧТО МОЖНО ПЕРЕСЧИТАТЬ. ОТ МЕНЬШЕГО К БОЛЬШЕМУ.</p></div>', 17))

    # конверты
    envs = [("СВЕРКА · станция 1", "вскрыть после ставки"), ("СВЕРКА · станция 2", "вскрыть после ставки"),
            ("СВЕРКА · станция 3", "вскрыть после ставки"), ("СВЕРКА · станция 4", "вскрыть после ставки"),
            ("СВЕРКА · станция 5", "вскрыть после ставки"), ("ПРАВИЛО", "не вскрывать до зала финала")]
    pg.append(page('<div class="mono eyebrow">Страница 18 · наклейки на конверты, 6 комплектов</div>'
      '<h2>Обложки конвертов</h2><div class="envs">' + ''.join(
        f'<div class="env"><div class="et">{a}</div><div class="es">{b}</div>'
        f'<div class="eteam">команда ____</div></div>' for a, b in envs
      ) + '</div><p class="cap">Конверт до вскрытия лежит печатью вверх. Проверяющий вскрывает его сам, помощник к конверту не прикасается.</p>', 18))

    # письмо
    pg.append(page('''
  <div class="mono eyebrow">Страница 19 · один экземпляр, состаренная бумага</div>
  <h2>Письмо экспедиции</h2>
  <div class="letter">
    <p>Тому, кто дошёл сюда и пересчитал сам.</p>
    <p>Я знаю, кто переписывал мой дневник. Это Фарид, курьер Юсуфа Надима — человека, которого я учил девять лет и который теперь продаёт коллекционерам красивые истории о происхождении вещей. Ему нужна не находка. Ему нужен документ: маршрут, восстановленный уважаемыми людьми, с их подписями. Тогда любая вещь, привязанная к этому маршруту, стоит в десять раз дороже. Он не крал у меня ничего, кроме порядка слов.</p>
    <p>Мы молчим третий месяц, и это не беда, а расчёт. Пока он уверен, что подмена не раскрыта, он подделывает по-старому — а по-старому у него выходит одинаково: он пишет «справа» и «слева», потому что смотрит на снимки и никогда не стоит на месте. Шесть страниц одной руки — это уже не подозрение.</p>
    <p>Я разделил записи потому, что подделать можно мнение, а пересчитанное подделать нельзя. Вы пересчитали.</p>
    <p>Диск под этим письмом расколот на шесть частей. Одна часть — ваша: возьмите по кусочку, их здесь ровно тридцать. Если однажды соберутся все шесть, остальное объясню я сам.</p>
    <p>Архив я оставляю тем, кто проверяет. Сегодня это вы — <span class="fill">название компании</span>.</p>
    <p class="sign">А. Камаль. Подпись важнее золота.</p>
  </div>''', 19))

    # восстановленный маршрут
    pg.append(page('''
  <div class="mono eyebrow">Страница 20 · шаблон, печатается в день программы</div>
  <h2>Лист «Восстановленный маршрут»</h2>
  <div class="route">
    <div class="rhead">ВОССТАНОВЛЕННЫЙ МАРШРУТ<span>Плато Гиза · ____________ · команда ____ · ____________________</span></div>
    <div class="rgrid">''' + ''.join(
      f'<div class="rc"><span class="rn">{i}</span><span class="rph">фото со станции</span>'
      f'<span class="rl">свидетельство _______________________</span></div>' for i in range(1, 7)
    ) + '''</div>
    <div class="rfoot">Числа в этом листе никто не сообщал. Их пересчитали пять человек, чьи имена стоят выше.</div>
  </div>
  <div class="box">
    <div class="mono lbl">Как печатается</div>
    <p>Координатор собирает фотографии станций с телефонов помощников во время переезда и печатает шесть листов на портативном принтере. Запасной аккумулятор обязателен: на шесть листов уходит около двадцати минут.</p>
  </div>''', 20))
    return pg

CSS = '''
.art{background:#fff;border:1px solid var(--rule);border-radius:2mm;padding:3mm;margin-bottom:3mm}
.cap{color:var(--dim);font-size:8.6pt;margin-bottom:4mm}
.spread{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-bottom:4mm}
.dpage{background:#fbf7ee;border:1px solid #d9cdbb;border-radius:1.5mm;padding:6mm;min-height:62mm;display:flex;flex-direction:column}
.dpage.fake{background:#fbf8f2}
.dlbl{font-family:"JetBrains Mono",monospace;font-size:7pt;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);margin-bottom:3mm}
.dtext{font-family:"Spectral",Georgia,serif;font-size:11.5pt;line-height:1.6;color:#2a2233;flex:1}
.dpage.fake .dtext{font-family:"Golos Text",Arial,sans-serif;font-size:11pt;line-height:1.65}
.dsign{font-size:7.5pt;color:var(--dim);text-align:left}
.doc{background:#fff;border:1px solid var(--rule);border-radius:2mm;padding:6mm;margin-bottom:4mm;font-family:"Spectral",Georgia,serif;font-size:10.5pt;line-height:1.6}
.doc.lite{font-family:"Golos Text",Arial,sans-serif;font-size:10pt}
.doc .claim{margin-bottom:2mm}
.choices{display:flex;gap:10mm;font-size:10.5pt}
.form{background:#fff;border:1px solid var(--rule);border-radius:2mm;padding:6mm}
.fhead{display:flex;gap:8mm;font-size:9.5pt;color:var(--ink-2);margin-bottom:4mm}
.fhead2{font-size:9.5pt;color:var(--ink-2);margin-top:3mm}
table.blank{width:100%;border-collapse:collapse;margin-bottom:3mm}
table.blank th{font-size:8pt;color:var(--violet);text-transform:uppercase;letter-spacing:.08em;padding-bottom:1.5mm;border-bottom:1px solid var(--violet);text-align:left}
table.blank td{height:13mm;border-bottom:1px solid var(--rule)}
table.blank td.s{width:8mm;color:var(--dim);vertical-align:top;padding-top:2mm}
table.blank td.st{width:26mm;background:#faf7fc}
.fnote{font-size:8.6pt;color:var(--dim)}
.cut{border:1px dashed var(--violet);border-radius:2mm;padding:5mm;text-align:center}
.cuttitle{font-family:"JetBrains Mono",monospace;font-size:8pt;letter-spacing:.14em;color:var(--violet);margin-bottom:4mm}
.window{height:34mm;border:1.2mm solid var(--ink);border-radius:1mm;display:flex;align-items:center;justify-content:center;color:var(--dim);font-size:8.5pt;margin-bottom:3mm}
.scale{display:flex;justify-content:space-between;color:var(--ink-2);font-size:9pt;margin-bottom:3mm}
.cutnote{font-size:8.6pt;color:var(--ink-2)}
.rose{width:44mm;height:44mm;border:1.2mm solid var(--ink);border-radius:50%;margin:0 auto 3mm;position:relative}
.rose div{position:absolute;font-weight:700;font-size:11pt}
.rose .n{top:2mm;left:50%;transform:translateX(-50%)}
.rose .s{bottom:2mm;left:50%;transform:translateX(-50%)}
.rose .e{right:2.5mm;top:50%;transform:translateY(-50%)}
.rose .w{left:2.5mm;top:50%;transform:translateY(-50%)}
.rose .dot{width:3mm;height:3mm;background:var(--violet);border-radius:50%;top:50%;left:50%;transform:translate(-50%,-50%)}
.badges{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-bottom:4mm}
.badge{border:1px dashed var(--violet);border-radius:2mm;padding:6mm 4mm;text-align:center;min-height:38mm;display:flex;flex-direction:column;justify-content:center;gap:2mm}
.bt{font-family:"Spectral",Georgia,serif;font-size:13pt;color:var(--violet)}
.bs{font-size:9pt;color:var(--ink-2)}
.bteam{font-size:8.4pt;color:var(--dim);margin-top:2mm}
.card{border:1px dashed var(--violet);border-radius:2mm;padding:6mm;min-height:80mm}
.ct{font-family:"Spectral",Georgia,serif;font-size:14pt;color:var(--violet)}
.ct.small{font-size:11pt}
.cs{font-size:8.6pt;color:var(--dim);margin-bottom:4mm}
.crules p{font-size:9.4pt;margin-bottom:1.6mm;color:var(--ink-2)}
.lines div{font-size:9.6pt;color:var(--ink-2);margin-bottom:3mm}
.lines.mt{margin-top:6mm}
.builds{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-bottom:4mm}
.bcard{border:1px dashed var(--violet);border-radius:2mm;min-height:28mm;display:flex;align-items:center;justify-content:center;text-align:center;padding:4mm}
.bn{font-family:"Spectral",Georgia,serif;font-size:12pt}
.strips{margin-bottom:4mm}
.strip-cut{border:1px dashed var(--violet);border-radius:1.5mm;padding:4mm 5mm;margin-bottom:3mm;display:flex;align-items:center;gap:6mm}
.strip-cut .sn{font-family:"JetBrains Mono",monospace;font-size:8pt;color:var(--dim)}
.strip-cut .sw{font-family:"Spectral",Georgia,serif;font-size:15pt;letter-spacing:.04em}
.rule{font-family:"Spectral",Georgia,serif;font-size:12pt;color:var(--violet);margin:0}
.envs{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-bottom:4mm}
.env{border:1px dashed var(--violet);border-radius:2mm;padding:5mm;min-height:32mm;display:flex;flex-direction:column;justify-content:center;gap:1.5mm}
.et{font-family:"JetBrains Mono",monospace;font-size:8.4pt;letter-spacing:.08em;color:var(--violet)}
.es{font-size:9pt;color:var(--ink-2)}
.eteam{font-size:8.4pt;color:var(--dim);margin-top:2mm}
.letter{background:#fbf7ee;border:1px solid #d9cdbb;border-radius:2mm;padding:8mm;font-family:"Spectral",Georgia,serif;font-size:10.6pt;line-height:1.65}
.letter p{margin-bottom:3mm}
.letter .fill{border-bottom:1px solid var(--dim);padding:0 8mm}
.letter .sign{margin-top:5mm;text-align:left}
.route{background:#fff;border:1px solid var(--rule);border-radius:2mm;padding:6mm;margin-bottom:4mm}
.rhead{font-family:"Spectral",Georgia,serif;font-size:13pt;color:var(--violet);margin-bottom:4mm}
.rhead span{display:block;font-family:"Golos Text",Arial,sans-serif;font-size:9pt;color:var(--dim);margin-top:1.5mm}
.rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-bottom:4mm}
.rc{border:1px solid var(--rule);border-radius:1.5mm;padding:3mm;display:flex;flex-direction:column;gap:2mm;min-height:34mm}
.rn{font-family:"JetBrains Mono",monospace;font-size:8pt;color:var(--violet)}
.rph{flex:1;background:#f3eef7;border-radius:1mm;display:flex;align-items:center;justify-content:center;font-size:8pt;color:var(--dim);min-height:18mm}
.rl{font-size:8.4pt;color:var(--ink-2)}
.rfoot{font-size:9pt;color:var(--dim);border-top:1px solid var(--rule);padding-top:3mm}
.grid6{display:grid;grid-template-columns:repeat(6,1fr);gap:3mm;margin:4mm 0 2mm}
.cell{border:1px solid var(--rule);border-radius:1.5mm;padding:3mm;text-align:center}
.cell .num{display:block;font-family:"JetBrains Mono",monospace;font-size:8pt;color:var(--violet);margin-bottom:2mm}
.cell .line{display:block;border-bottom:1px solid var(--ink);height:6mm}
'''

pages = build()
doc = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Код пирамид — комплект на печать</title>'
       '<link rel="stylesheet" href="fonts/local.css"><link rel="stylesheet" href="doc.css">'
       '<style>' + CSS + '</style></head><body>' + ''.join(pages) + '</body></html>')
pathlib.Path('giza-komplekt-pechati.html').write_text(doc, encoding='utf-8')
print('страниц:', len(pages))
