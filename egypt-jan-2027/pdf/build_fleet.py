#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает презентацию «Нил. Три судна. Программы для групп» — fleet.html.

Шапка со шрифтами и базовой типографикой берётся из _shared_head.html (та же, что у Le Fayan).
Факты о судах — из официальных брошюр операторов (sources/brochures) и презентации Le Fayan.
Фото — pdf/img (Le Fayan), pdf/img/fleet (кропы из брошюр, переработанные фото вечеров).
"""
import io

head = io.open('_shared_head.html', encoding='utf-8').read()

extra_css = '''
<style>
/* дополнения для флотской презентации */
.full{padding:0 !important; position:relative}
.full .img{position:absolute; inset:0; background-size:cover; background-position:center}
.full .veil{position:absolute; inset:0; background:linear-gradient(180deg,rgba(25,20,54,0) 35%,rgba(25,20,54,.78) 100%)}
.full .cap{position:absolute; left:18mm; right:18mm; bottom:14mm; color:#fff}
.full .cap h1,.full .cap h2{color:#fff}
.full .cap .eyebrow{color:var(--lime)}
.full .cap p{color:rgba(255,255,255,.88)}
.split{padding:0 !important; display:grid}
.split.l{grid-template-columns:1fr 128mm}
.split.r{grid-template-columns:128mm 1fr}
.split .img{background-size:cover; background-position:center}
.split .txt{padding:16mm 18mm; display:flex; flex-direction:column; justify-content:center}
.kpi{display:grid; grid-template-columns:repeat(3,1fr); gap:6mm; margin-top:6mm}
.kpi div{border-top:1.2mm solid var(--violet); padding-top:3mm}
.kpi .n{font-family:Unbounded,sans-serif; font-weight:800; font-size:22pt; line-height:1; color:var(--ink)}
.kpi .l{font-size:8.6pt; color:var(--muted); margin-top:1.5mm; line-height:1.35}
.stat{display:flex; flex-direction:column; justify-content:center; align-items:flex-start}
.stat h1{font-size:34pt; max-width:230mm}
.stat .lead{margin-top:6mm}
.boat3{display:grid; grid-template-columns:repeat(3,1fr); gap:7mm; height:100%}
.boat3 .c{display:flex; flex-direction:column}
.boat3 .ph{height:56mm; border-radius:3mm; background-size:cover; background-position:center}
.boat3 h3{margin:5mm 0 1.5mm; font-size:14pt; font-weight:800}
.boat3 .who{font-family:Unbounded,sans-serif; font-weight:600; font-size:7.2pt; letter-spacing:.16em; text-transform:uppercase; color:var(--violet-d); margin-bottom:2.5mm}
.boat3 p{font-size:9.4pt; line-height:1.45; color:var(--ink2); margin:0}
.boat3 .spec{margin-top:auto; padding-top:3mm; border-top:.4mm solid var(--line); font-size:8.6pt; color:var(--muted); line-height:1.45}
.grid4{display:grid; grid-template-columns:repeat(4,1fr); gap:4mm}
.grid4 .ph{height:44mm; border-radius:2.5mm; background-size:cover; background-position:center}
.tbl{width:100%; border-collapse:collapse; font-size:9.6pt}
.tbl th{font-family:Unbounded,sans-serif; font-weight:600; font-size:7.2pt; letter-spacing:.14em; text-transform:uppercase;
  color:var(--violet-d); text-align:left; padding:0 3mm 2.2mm 0; border-bottom:.5mm solid var(--violet)}
.tbl td{padding:3mm 3mm 3mm 0; border-bottom:.35mm solid var(--line); vertical-align:top; line-height:1.4}
.tbl tr:last-child td{border-bottom:none}
.tbl .b{font-weight:700; color:var(--ink)}
.tbl .m{color:var(--muted); font-size:8.6pt}
.days{display:grid; grid-template-columns:repeat(var(--n),1fr); gap:3.5mm}
.days .d{background:var(--soft); border-radius:3mm; padding:4.5mm 4.5mm 4mm; min-height:0}
.days .d.c{background:#F1FADB} .days .d.p{background:#FBF0FB}
.days .d .k{font-family:Unbounded,sans-serif; font-weight:600; font-size:7pt; letter-spacing:.14em; text-transform:uppercase; color:var(--violet-d)}
.days .d h3{font-size:10pt; margin:1.5mm 0 2mm; line-height:1.2}
.days .d p{font-size:8.4pt; line-height:1.4; color:var(--ink2); margin:0}
.chip{display:inline-block; font-family:Unbounded,sans-serif; font-weight:600; font-size:7pt; letter-spacing:.1em; text-transform:uppercase;
  padding:1.4mm 3mm; border-radius:3mm; background:var(--soft); color:var(--violet-d); margin:0 1.5mm 1.5mm 0}
.chip.l{background:#F1FADB; color:#5a7a10} .chip.p{background:#FBF0FB; color:#a04fa8}
.mod{display:grid; grid-template-columns:1fr 1fr; gap:10mm; align-items:start}
.mod .box{background:var(--soft); border-radius:4mm; padding:7mm}
.mod .box.l{background:#F1FADB}
.mod .row{display:flex; gap:3mm; flex-wrap:wrap; margin-top:3mm}
.mod .opt{border:.45mm solid var(--violet); border-radius:3mm; padding:3mm 4mm; font-size:9.2pt; min-width:36mm}
.mod .opt b{display:block; font-family:Unbounded,sans-serif; font-weight:700; font-size:11pt; margin-bottom:.8mm}
.note{font-size:8.6pt; color:var(--muted); line-height:1.45}
.src{position:absolute; left:18mm; bottom:10mm; font-size:7.4pt; color:var(--muted)}
</style>
'''

LOGO = 'img/logo1.png'

body = '''<body>

<!-- 01 ОБЛОЖКА -->
<section class="pg full">
  <div class="img" style="background-image:url('img/hero.jpg')"></div>
  <div class="veil"></div>
  <img src="{{LOGO}}" alt="La Royal Event" style="position:absolute; left:18mm; top:14mm; width:44mm; filter:brightness(0) invert(1)">
  <div class="cap">
    <p class="eyebrow">La Royal Event · Египет</p>
    <h1 style="font-size:40pt; max-width:220mm">Нил. Три судна.<br>Программы для групп от 16 до 70</h1>
    <p class="lead" style="margin-top:5mm; max-width:200mm">Lumière · Le Fayan Suites · Soleil. Частный фрахт и блоки на регулярных
    отправлениях, Каир по желанию, приватные вечера в храмах.</p>
  </div>
</section>

<!-- 02 КТО МЫ -->
<section class="pg stat">
  <p class="eyebrow">Как мы работаем</p>
  <h1>Мы не продаём каюты.<br>Мы собираем поездку вокруг группы.</h1>
  <p class="lead">Три судна разного масштаба позволяют закрыть любой размер группы — от восьми кают
  частной дахабии до пятидесяти трёх кают полного фрахта. Маршрут, день отправления, Каир до или после,
  приватный вечер в храме — всё это конструктор, а не каталог.</p>
  <div class="kpi" style="max-width:220mm">
    <div><div class="n">3</div><div class="l">судна: 8, 37 и 53 каюты</div></div>
    <div><div class="n">3–7</div><div class="l">ночей на реке, стандартные отправления по понедельникам и пятницам</div></div>
    <div><div class="n">16–70</div><div class="l">гостей: от частной дахабии до полного фрахта</div></div>
  </div>
  <span class="pn">02</span>
</section>

<!-- 03 ТРИ СУДНА -->
<section class="pg">
  <p class="eyebrow">Флот</p>
  <h2>Три судна — три масштаба</h2>
  <div class="boat3" style="height:120mm">
    <div class="c">
      <div class="ph" style="background-image:url('img/fleet/lum-exterior.jpg')"></div>
      <div class="who">Группа 16–20 · только частный фрахт</div>
      <h3>Lumière</h3>
      <p>Дахабия нового поколения: восемь кают, собственный бассейн, лаунж с панорамными окнами.
      Ходит там, куда большие суда не заходят, — с ночёвками у островов.</p>
      <div class="spec">8 кают · 5 Luxury 24 м² · 2 Junior Suite 39 м² · Lumière Suite 68 м²<br>Луксор — Асуан, 5 ночей</div>
    </div>
    <div class="c">
      <div class="ph" style="background-image:url('img/aerial.jpg')"></div>
      <div class="who">Группа 25–40 · фрахт или блок</div>
      <h3>Le Fayan Suites</h3>
      <p>Судно, построенное вокруг одного типа размещения: все каюты — сюиты по 39 м². Четыре палубы,
      бассейн на солнечной палубе, спокойная палитра.</p>
      <div class="spec">37 кают · 36 сюитов 39 м² · Royal Suite 58 м² · 75 м<br>3, 4 и 7 ночей по расписанию</div>
    </div>
    <div class="c">
      <div class="ph" style="background-image:url('img/fleet/sol-exterior.jpg')"></div>
      <div class="who">Группа 50–100 · фрахт или блок</div>
      <h3>Soleil</h3>
      <p>Флагман: ресторан на 110 мест, спа с крытым бассейном, сауной и хаммамом, отдельная приватная
      столовая, лифт. Единственное из трёх судов, которое принимает группу в семьдесят человек целиком.</p>
      <div class="spec">53 каюты · 41 Luxury 21 м² · 8 Junior 39 м² · 2 Royal 44 м² · 2 Soleil Suite 58 м²<br>3, 4 и 7 ночей по расписанию</div>
    </div>
  </div>
  <span class="pn">03</span>
</section>

<!-- 04 LUMIÈRE -->
<section class="pg split r">
  <div class="img" style="background-image:url('img/fleet/lum-pool.jpg')"></div>
  <div class="txt">
    <p class="eyebrow">Lumière · 8 кают</p>
    <h2>Для группы, которая хочет<br>весь борт себе</h2>
    <p>Lumière не продаётся по каютам — только целиком. Пять кают Luxury на одного, двоих или троих,
    два Junior Suite с ванной у окна и Lumière Suite на 68 м² с джакузи и окнами на три стороны.</p>
    <p>Маршрут собирается под группу: стандартные пять ночей Луксор — Асуан идут с ночёвками
    у островов Фавза, Бесау и Хербиаб, остановкой в каменоломнях Гебель эль-Сильсила
    и приватным ужином на острове.</p>
    <div style="margin-top:4mm">
      <span class="chip">бассейн</span><span class="chip">лаунж-бар</span><span class="chip">ресторан à la carte</span>
      <span class="chip">массаж</span><span class="chip">зал</span>
    </div>
    <p class="note" style="margin-top:5mm">16 гостей при двухместном размещении, до 19 — с третьими местами в каютах Luxury.
    Источник: брошюра оператора, сентябрь 2026.</p>
  </div>
  <span class="pn" style="color:#fff">04</span>
</section>

<section class="pg" style="padding:12mm 18mm">
  <div class="grid4" style="height:100%; grid-template-rows:1fr 1fr">
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-suite.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-suite-bath.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-junior.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-cabin.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-lounge-bar.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-restaurant.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-sundeck.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/lum-island-dinner.jpg')"></div>
  </div>
  <span class="pn">05</span>
</section>

<!-- 06 LE FAYAN -->
<section class="pg split l">
  <div class="txt">
    <p class="eyebrow">Le Fayan Suites · 37 кают</p>
    <h2>Все каюты — сюиты.<br>Группа до сорока — весь борт</h2>
    <p>Тридцать шесть одинаковых сюитов по 39 м² и один Royal Suite. Это снимает главную головную боль
    группового размещения: никто не получает каюту хуже соседа. При одноместном размещении борт закрывает
    группу до 37 человек, при двухместном — до 70.</p>
    <p>Четыре палубы и солнечная палуба с бассейном, ресторан с панорамными окнами, спа.
    Стандартные отправления — четыре ночи из Луксора по понедельникам, три из Асуана по пятницам,
    семь ночей в обе стороны. При фрахте день посадки назначается под группу.</p>
    <div class="kpi" style="margin-top:5mm">
      <div><div class="n">39 м²</div><div class="l">каждый сюит</div></div>
      <div><div class="n">75 м</div><div class="l">длина, 4 палубы + солнечная</div></div>
      <div><div class="n">37</div><div class="l">кают: 36 сюитов + Royal Suite</div></div>
    </div>
  </div>
  <div class="img" style="background-image:url('img/royal2.jpg')"></div>
  <span class="pn">06</span>
</section>

<section class="pg" style="padding:12mm 18mm">
  <div class="grid4" style="height:100%; grid-template-rows:1fr 1fr">
    <div class="ph" style="height:auto; background-image:url('img/royal1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/suite2.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/rest1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/lounge1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/deck1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/deck2.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/well1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/sunset.jpg')"></div>
  </div>
  <span class="pn">07</span>
</section>

<!-- 08 SOLEIL -->
<section class="pg split r">
  <div class="img" style="background-image:url('img/fleet/sol-pool-sunset.jpg')"></div>
  <div class="txt">
    <p class="eyebrow">Soleil · 53 каюты</p>
    <h2>Флагман для больших групп</h2>
    <p>Пятьдесят три каюты четырёх категорий: сорок одна Luxury с панорамным балконом, восемь Junior Suite
    с ванной у окна, два Royal Suite и два Soleil Suite по 58 м² с джакузи. Ресторан на 110 мест принимает
    всю группу за один раз, отдельная приватная столовая — для совета директоров или семьи.</p>
    <p>Спа такого размера на Ниле больше нет: крытый мраморный бассейн с окнами в два этажа, сауна, хаммам,
    два массажных кабинета. На солнечной палубе — бассейн, открытое джакузи и бар.</p>
    <div class="kpi" style="margin-top:5mm">
      <div><div class="n">110</div><div class="l">мест в ресторане</div></div>
      <div><div class="n">260 м²</div><div class="l">лаунж-бар</div></div>
      <div><div class="n">53</div><div class="l">каюты, до 106 гостей</div></div>
    </div>
  </div>
  <span class="pn" style="color:#fff">08</span>
</section>

<section class="pg" style="padding:12mm 18mm">
  <div class="grid4" style="height:100%; grid-template-rows:1fr 1fr">
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-luxury-1.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-junior-bath.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-suite-east.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-suite-jacuzzi.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-reception.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-restaurant.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-spa-pool.jpg')"></div>
    <div class="ph" style="height:auto; background-image:url('img/fleet/sol-sundeck-night.jpg')"></div>
  </div>
  <span class="pn">09</span>
</section>

<!-- 10 КАК УСТРОЕН НИЛ -->
<section class="pg">
  <p class="eyebrow">Как устроен круиз</p>
  <h2>Луксор — Асуан: один маршрут, три длины</h2>
  <div class="cols2" style="gap:12mm">
    <div>
      <p>Все нильские круизы ходят по одному участку между Луксором и Асуаном — это около 210 километров
      реки и один шлюз в Эсне. Разница только в том, откуда начинать, сколько ночей провести
      на воде и сколько раз остановиться.</p>
      <table class="tbl" style="margin-top:4mm">
        <tr><th>Формат</th><th>Посадка</th><th>Что внутри</th></tr>
        <tr><td class="b">3 ночи</td><td>Асуан, <b>пятница</b> с 12:00</td><td>Филе, Ком-Омбо, Эдфу, западный берег, Карнак, Луксорский храм. Выезд в понедельник</td></tr>
        <tr><td class="b">4 ночи</td><td>Луксор, <b>понедельник</b> с 12:00</td><td>Карнак и Луксорский храм, западный берег, Эсна, Эдфу, Ком-Омбо, Филе, Нубия. Выезд в пятницу</td></tr>
        <tr><td class="b">7 ночей</td><td>Луксор (пн) или Асуан (пт)</td><td>Полное кольцо: оба направления, ночь в Эдфу, два дня в Асуане. Самый спокойный ритм</td></tr>
        <tr><td class="b">5 ночей</td><td>Луксор, день под группу</td><td>Только Lumière: острова, Гебель эль-Сильсила, приватный ужин на острове</td></tr>
      </table>
    </div>
    <div>
      <div class="card">
        <h3>Что входит в стандартную ставку</h3>
        <ul class="ticks" style="margin-top:3mm">
          <li>Размещение, полный пансион, безалкогольные напитки на борту</li>
          <li>Экскурсии по программе с египтологом, входные билеты</li>
          <li>Наземный транспорт на время круиза, встреча в аэропорту</li>
          <li>Вечерняя программа на борту</li>
        </ul>
        <h3 style="margin-top:5mm">Считается отдельно</h3>
        <ul class="ticks p" style="margin-top:3mm">
          <li>Абу-Симбел самолётом, полёт на шаре над Луксором</li>
          <li>Алкоголь — à la carte или пакетом</li>
          <li>Перелёты Каир — Луксор / Асуан — Каир</li>
          <li>Приватные вечера в храмах</li>
        </ul>
      </div>
      <p class="note" style="margin-top:4mm">Дни посадки и состав — по опубликованным программам Soleil и Le Fayan Suites.
      При частном фрахте день посадки и маршрут назначаются под группу.</p>
    </div>
  </div>
  <span class="pn">10</span>
</section>

<!-- 11 КОНСТРУКТОР -->
<section class="pg">
  <p class="eyebrow">Конструктор программы</p>
  <h2>Каир × Нил: собирается из двух модулей</h2>
  <div class="mod">
    <div class="box">
      <h3>Модуль «Каир»</h3>
      <p class="sm" style="margin-top:2mm">До или после реки. Перелёт в Луксор или Асуан — час с небольшим.</p>
      <div class="row">
        <div class="opt"><b>0 дней</b>Прямой прилёт в Луксор. Для тех, кто уже видел пирамиды</div>
        <div class="opt"><b>1 день</b>Плато Гизы до открытия, завтрак у пирамиды, Большой Египетский музей</div>
        <div class="opt"><b>2 дня</b>Плюс Саккара и Мемфис либо Старый Каир и Хан-эль-Халили, ужин с видом на пирамиды</div>
      </div>
    </div>
    <div class="box l">
      <h3>Модуль «Нил»</h3>
      <p class="sm" style="margin-top:2mm">Длина определяет день недели посадки и порт.</p>
      <div class="row">
        <div class="opt"><b>3 ночи</b>Из Асуана, пятница. Плотно, без пауз</div>
        <div class="opt"><b>4 ночи</b>Из Луксора, понедельник. Классика</div>
        <div class="opt"><b>5 ночей</b>Lumière, с островами. Только фрахт</div>
        <div class="opt"><b>7 ночей</b>Кольцо. Для тех, кто едет ради реки</div>
      </div>
    </div>
  </div>
  <p class="lead" style="margin-top:6mm; max-width:250mm">Из двенадцати сочетаний мы отобрали четыре, которые продаются
  лучше всего и не ломают логистику, — они на следующих страницах.</p>
  <span class="pn">11</span>
</section>

<!-- 12 ПРОГРАММА 1 -->
<section class="pg">
  <p class="eyebrow">Программа 1 · Классика · 7 дней</p>
  <h2>Два дня Каира и четыре ночи на реке</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Суббота — пятница. Soleil или Le Fayan Suites. Для групп 30–70, где большинство в Египте впервые.</p>
  <div class="days" style="--n:7">
    <div class="d c"><div class="k">Сб · Каир</div><h3>Прилёт</h3><p>Встреча, отель у пирамид, приветственный ужин</p></div>
    <div class="d c"><div class="k">Вс · Каир</div><h3>Гиза и музей</h3><p>Плато до открытия, завтрак у пирамиды, Большой Египетский музей, вечером Хан-эль-Халили</p></div>
    <div class="d"><div class="k">Пн · Луксор</div><h3>Посадка</h3><p>Утренний перелёт, посадка с 12:00, обед. Карнак и Луксорский храм в подсветке</p></div>
    <div class="d"><div class="k">Вт · западный берег</div><h3>Долина царей</h3><p>Шар на рассвете по желанию. Долина царей, Хатшепсут, Колоссы. Переход к Эдфу через Эсну</p></div>
    <div class="d"><div class="k">Ср · Эдфу, Ком-Омбо</div><h3>Два храма</h3><p>Эдфу утром, Ком-Омбо на закате, приход в Асуан</p></div>
    <div class="d"><div class="k">Чт · Асуан</div><h3>Филе</h3><p>Остров Филе, нубийская деревня на лодках. Вечером — приватный вечер на Филе или ужин на палубе</p></div>
    <div class="d p"><div class="k">Пт · Асуан</div><h3>Выезд</h3><p>Абу-Симбел самолётом по желанию. Выезд до 08:00, перелёт в Каир и домой</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пн</span><span class="chip">Le Fayan · пн</span><span class="chip l">30–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: стандартное понедельничное отправление есть у обоих судов, Каир закрывается двумя днями
    без спешки, а группа возвращается домой через Каир одним перелётом.</p>
  </div>
  <span class="pn">12</span>
</section>

<!-- 13 ПРОГРАММА 2 -->
<section class="pg">
  <p class="eyebrow">Программа 2 · Короткая · 6 дней</p>
  <h2>День Каира и три ночи от Асуана</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Среда — понедельник. Soleil или Le Fayan Suites. Для корпоративных групп с жёстким графиком.</p>
  <div class="days" style="--n:6">
    <div class="d c"><div class="k">Ср · Каир</div><h3>Прилёт</h3><p>Встреча, отель, свободный вечер</p></div>
    <div class="d c"><div class="k">Чт · Каир</div><h3>Гиза и музей</h3><p>Плато до открытия, Большой Египетский музей. Вечером ужин с видом на пирамиды</p></div>
    <div class="d"><div class="k">Пт · Асуан</div><h3>Посадка</h3><p>Утренний перелёт в Асуан. Абу-Симбел по желанию. Посадка с 12:00, Филе, нубийская деревня</p></div>
    <div class="d"><div class="k">Сб · Ком-Омбо, Эдфу</div><h3>Два храма</h3><p>Ком-Омбо утром, Эдфу днём, переход в Луксор через Эсну</p></div>
    <div class="d"><div class="k">Вс · Луксор</div><h3>Главный день</h3><p>Шар на рассвете по желанию. Долина царей, Хатшепсут, Колоссы, днём Карнак и Луксорский храм</p></div>
    <div class="d p"><div class="k">Пн · Луксор</div><h3>Выезд</h3><p>Выезд до 08:00, перелёт в Каир и домой</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пт</span><span class="chip">Le Fayan · пт</span><span class="chip l">20–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: три ночи — самый продаваемый формат на Ниле, пятничная посадка в Асуане даёт
    Абу-Симбел в день приезда, а Луксор достаётся целым днём в конце, когда группа уже в ритме.</p>
  </div>
  <span class="pn">13</span>
</section>

<!-- 14 ПРОГРАММА 3 -->
<section class="pg">
  <p class="eyebrow">Программа 3 · Только Нил · 8 дней</p>
  <h2>Семь ночей по кольцу, без Каира</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Понедельник — понедельник. Soleil или Le Fayan Suites. Для тех, кто уже был в Каире и едет ради реки.</p>
  <div class="days" style="--n:8">
    <div class="d"><div class="k">Пн</div><h3>Луксор</h3><p>Прилёт в Луксор, посадка с 12:00, Луксорский храм</p></div>
    <div class="d"><div class="k">Вт</div><h3>Западный берег</h3><p>Шар по желанию, Долина царей, Хатшепсут, Эсна, ночь в Эдфу</p></div>
    <div class="d"><div class="k">Ср</div><h3>Эдфу, Ком-Омбо</h3><p>Два храма, приход в Асуан</p></div>
    <div class="d"><div class="k">Чт</div><h3>Асуан</h3><p>Филе, свободный день на воде, вечер на палубе</p></div>
    <div class="d"><div class="k">Пт</div><h3>Абу-Симбел</h3><p>Абу-Симбел по желанию, нубийская деревня на лодках</p></div>
    <div class="d"><div class="k">Сб</div><h3>Обратно</h3><p>Ком-Омбо, переход в Луксор через Эсну</p></div>
    <div class="d"><div class="k">Вс</div><h3>Карнак</h3><p>Карнакский храм, свободный день в Луксоре, прощальный вечер</p></div>
    <div class="d p"><div class="k">Пн</div><h3>Выезд</h3><p>Выезд до 08:00, вылет из Луксора</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пн</span><span class="chip">Le Fayan · пн</span><span class="chip l">30–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: неделя на одном судне без переездов и чемоданов, два дня в Асуане, свободные дни
    под рабочие сессии или отдых. Дорого в пересчёте на день, но это самый «люксовый» ритм из возможных.</p>
  </div>
  <span class="pn">14</span>
</section>

<!-- 15 ПРОГРАММА 4 -->
<section class="pg split l">
  <div class="txt">
    <p class="eyebrow">Программа 4 · Приватная дахабия · 6–8 дней</p>
    <h2>Lumière: пять ночей<br>с островами</h2>
    <p>Для группы до шестнадцати человек, которой важнее уединение, чем масштаб. Весь борт свой, день посадки
    любой, маршрут с ночёвками у островов, куда большие суда не подходят.</p>
    <table class="tbl" style="margin-top:3mm; font-size:9pt">
      <tr><td class="b" style="width:22mm">День 1</td><td>Луксор: посадка, Карнак, Луксорский храм, коктейль на палубе</td></tr>
      <tr><td class="b">День 2</td><td>Шар по желанию, западный берег, переход к Эдфу, ночь у острова Фавза</td></tr>
      <tr><td class="b">День 3</td><td>Эдфу в конных экипажах, остров Бесау, каменоломни Гебель эль-Сильсила</td></tr>
      <tr><td class="b">День 4</td><td>Ком-Омбо, остров Хербиаб: приватный ужин и вечер на берегу</td></tr>
      <tr><td class="b">День 5</td><td>Асуан: Филе, нубийская деревня, заповедник на лодках</td></tr>
      <tr><td class="b">День 6</td><td>Абу-Симбел по желанию, выезд</td></tr>
    </table>
    <p class="note" style="margin-top:4mm">Каир добавляется одним или двумя днями до посадки. Программа — по образцу оператора, сентябрь 2026.</p>
  </div>
  <div class="img" style="background-image:url('img/fleet/lum-island-dinner.jpg')"></div>
  <span class="pn">15</span>
</section>

<!-- 16 ЧТО ПРОДАВАТЬ -->
<section class="pg">
  <p class="eyebrow">Что продавать</p>
  <h2>Размер группы определяет судно, судно — программу</h2>
  <table class="tbl" style="margin-top:2mm">
    <tr><th style="width:22mm">Группа</th><th style="width:60mm">Судно и формат</th><th style="width:46mm">Размещение</th><th>Программа</th><th style="width:60mm">Почему так</th></tr>
    <tr>
      <td class="b">16–20</td>
      <td><b>Lumière</b> — весь борт<br><span class="m">либо блок 16–20 кают на Le Fayan</span></td>
      <td>8 кают: по двое, в Luxury — до троих</td>
      <td>Программа 4, Каир по желанию</td>
      <td class="m">Единственный формат, где группа такого размера получает судно целиком. Приватность — главный аргумент</td>
    </tr>
    <tr>
      <td class="b">30</td>
      <td><b>Le Fayan Suites</b> — весь борт<br><span class="m">либо блок 15–30 кают на Soleil</span></td>
      <td>37 сюитов, все одноместно</td>
      <td>Программы 1 или 3</td>
      <td class="m">Каждому — сюит 39 м² без доплаты за одноместное. Фрахт превращает пустые каюты в аргумент за добор</td>
    </tr>
    <tr>
      <td class="b">50</td>
      <td><b>Soleil</b> — весь борт<br><span class="m">либо Le Fayan по двое в сюите</span></td>
      <td>53 каюты: одноместно для всех, или 25 кают по двое</td>
      <td>Программы 1, 2 или 3</td>
      <td class="m">Ресторан на 110 и спа держат такую группу без очередей. Приватная столовая — для VIP-части группы</td>
    </tr>
    <tr>
      <td class="b">70</td>
      <td><b>Soleil</b> — весь борт</td>
      <td>35 кают по двое, 18 остаются под одноместных и команду</td>
      <td>Программы 1 или 2</td>
      <td class="m">Единственное судно из трёх, которое принимает семьдесят целиком. Короткие форматы на такой группе продаются лучше</td>
    </tr>
  </table>
  <p class="note" style="margin-top:5mm">Между размерами — блоки на регулярных отправлениях: группа едет на сборном рейсе, но со своим гидом,
  своими столами и своей программой на берегу. Блок бронируется под день отправления из расписания.</p>
  <span class="pn">16</span>
</section>

<!-- 17 ПРИВАТНЫЕ ВЕЧЕРА -->
<section class="pg full">
  <div class="img" style="background-image:url('img/fleet/gen-2.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Сигнатура La Royal Event</p>
    <h2 style="max-width:220mm">Приватные вечера в храмах</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Храм закрывается для всех, кроме вашей группы. Ужин у подножия
    храма Хатшепсут, вечер у пилонов Карнака, закрытый остров Филе со светозвуковым показом только для вас.
    Оформление, свет, музыка и кухня — наша работа.</p>
  </div>
</section>

<section class="pg" style="padding:12mm 18mm">
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; height:100%">
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/gen-3.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Карнак</div><p class="sm">Ужин у первого пилона, подсветка и лучи над дворами храма. Для групп до 100 человек</p></div>
    </div>
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/gen-6.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Хатшепсут</div><p class="sm">Длинный стол, канделябры и цветы перед террасами храма в скале. Самая кинематографичная площадка Луксора</p></div>
    </div>
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/lum-philae-aerial.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Филе</div><p class="sm">Закрытый остров на вечер: приветственные напитки, приватный визит, ужин, светозвуковой показ только для группы</p></div>
    </div>
  </div>
  <span class="pn">18</span>
</section>

<!-- 19 КАК БРОНИРУЕТСЯ -->
<section class="pg">
  <p class="eyebrow">Как это бронируется</p>
  <h2>Три решения, которые нужны от группы</h2>
  <div class="cols3" style="margin-top:4mm">
    <div class="tile"><div class="k">01 · Размер</div><p>От него зависит судно и формат — фрахт или блок. Шкала цены на человека считается под каждую точку:
    при фрахте каждый следующий гость делит уже оплаченное судно.</p></div>
    <div class="tile l"><div class="k">02 · Даты</div><p>Регулярные отправления — понедельник из Луксора, пятница из Асуана. При фрахте день посадки назначается
    под группу. Январь — высокий сезон, блоки закрываются за несколько месяцев.</p></div>
    <div class="tile p"><div class="k">03 · Каир</div><p>Ноль, один или два дня — до или после реки. Решается вместе с международными билетами:
    от этого зависит, в какой аэропорт прилетает группа.</p></div>
  </div>
  <div class="card" style="margin-top:8mm; display:grid; grid-template-columns:1fr 1fr; gap:8mm">
    <div><h3>Что мы берём на себя</h3>
      <ul class="ticks" style="margin-top:3mm"><li>Блок кают или фрахт, перелёты, отели в Каире, трансферы</li>
      <li>Русскоязычный египтолог на всю программу</li><li>Приватные вечера: разрешения, оформление, свет, кухня</li>
      <li>Команда La Royal Event рядом с группой всю поездку</li></ul></div>
    <div><h3>Условия</h3>
      <ul class="ticks v" style="margin-top:3mm"><li>50 % при подписании, 50 % за два месяца до заезда</li>
      <li>Цена фиксируется договором на группу и даты</li><li>Паспортные данные — за восемь недель: без них не оформляются разрешения</li>
      <li>Цены на человека — по запросу под размер группы</li></ul></div>
  </div>
  <span class="pn">19</span>
</section>

<!-- 20 КОНТАКТЫ -->
<section class="pg split r">
  <div class="img" style="background-image:url('img/nile.jpg')"></div>
  <div class="txt">
    <img src="{{LOGO}}" alt="La Royal Event" style="width:42mm; margin-bottom:6mm">
    <p class="eyebrow">Запросите даты</p>
    <h2>Назовите размер группы<br>и месяц</h2>
    <p>Мы подтвердим доступность судна, предложим программу и посчитаем цену на человека под ваш размер группы.</p>
    <div class="contact" style="margin-top:6mm">
      <div class="k">Телефон</div><div><span class="fill"></span></div>
      <div class="k">WhatsApp</div><div><span class="fill"></span></div>
      <div class="k">Почта</div><div><span class="fill"></span></div>
      <div class="k">Сайт</div><div><span class="fill"></span></div>
    </div>
    <p class="note" style="margin-top:5mm">Факты о судах — из брошюр операторов Soleil, Lumière и Le Fayan Suites, 2026.
    Фотографии вечеров в храмах — с мероприятий La Royal Event, переработаны.</p>
  </div>
  <span class="pn" style="color:#fff">20</span>
</section>

</body></html>
'''.replace('{{LOGO}}', LOGO)

html = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Нил · три судна · La Royal Event</title>' + head + extra_css + '</head>')
io.open('fleet.html', 'w', encoding='utf-8').write(html + body)
print('fleet.html собран')
