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
.tt{display:grid; grid-template-columns:repeat(4,1fr); gap:3.5mm 4.5mm; align-items:start}
.tt .day{background:var(--soft); border-radius:3mm; padding:3.5mm 4mm 3mm}
.tt .day.c{background:#F1FADB} .tt .day.p{background:#FBF0FB}
.tt .day .k{font-family:Unbounded,sans-serif; font-weight:600; font-size:6.8pt; letter-spacing:.14em; text-transform:uppercase; color:var(--violet-d); margin-bottom:2mm}
.tt .day .k em{font-style:normal; color:var(--muted); letter-spacing:.04em; text-transform:none; font-weight:400; margin-left:1.5mm}
.tt .row{display:grid; grid-template-columns:12mm 1fr; gap:1.5mm; font-size:7.8pt; line-height:1.25; padding:.8mm 0; border-top:.3mm solid rgba(25,20,54,.07)}
.tt .row:first-of-type{border-top:none}
.tt .row b{font-family:Unbounded,sans-serif; font-weight:600; font-size:7.2pt; color:var(--ink)}
.tt .row span{color:var(--ink2)}
.tt .row .opt{color:var(--muted)}
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
    <h1 style="font-size:40pt; max-width:220mm">Нил. Три судна.<br>Программы для групп от 16 человек</h1>
    <p class="lead" style="margin-top:5mm; max-width:210mm">Lumière · Le Fayan Suites · Soleil. Частный фрахт, блоки на регулярных
    отправлениях, регата из нескольких судов для больших групп, Каир по желанию, приватные вечера в храмах.</p>
  </div>
</section>

<!-- 02 КТО МЫ -->
<section class="pg stat">
  <p class="eyebrow">Как мы работаем</p>
  <h1>Сначала размер группы и даты.<br>Потом судно и маршрут.</h1>
  <p class="lead">Три судна разного масштаба вмещают группу любого размера: от восьми кают частной дахабии
  до пятидесяти трёх кают полного фрахта, а когда одного судна мало — идут вместе, регатой. Маршрут, день отправления, Каир до или после,
  приватный вечер в храме — каждый пункт выбираем вместе с вами.</p>
  <div class="kpi" style="max-width:220mm">
    <div><div class="n">3</div><div class="l">судна: 8, 37 и 53 каюты</div></div>
    <div><div class="n">3–7</div><div class="l">ночей на реке, стандартные отправления по понедельникам и пятницам</div></div>
    <div><div class="n">16–200</div><div class="l">гостей: от частной дахабии до регаты из трёх судов</div></div>
  </div>
  <span class="pn">2</span>
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
      <p>Дахабия на восемь кают, с бассейном и лаунжем с окнами во всю стену. Осадка меньше,
      чем у больших судов, поэтому ночует у островов, куда те не подходят.</p>
      <div class="spec">8 кают · 5 Luxury 24 м² · 2 Junior Suite 39 м² · Lumière Suite 68 м²<br>Луксор — Асуан, 5 ночей</div>
    </div>
    <div class="c">
      <div class="ph" style="background-image:url('img/aerial.jpg')"></div>
      <div class="who">Группа 25–40 · фрахт или блок</div>
      <h3>Le Fayan Suites</h3>
      <p>Все каюты одного типа — сюиты по 39 м², разницы между ними нет. Четыре палубы,
      бассейн на солнечной палубе, светлые спокойные интерьеры.</p>
      <div class="spec">37 кают · 36 сюитов 39 м² · Royal Suite 58 м² · 75 м<br>3, 4 и 7 ночей по расписанию</div>
    </div>
    <div class="c">
      <div class="ph" style="background-image:url('img/fleet/sol-exterior.jpg')"></div>
      <div class="who">Группа 50–100 · фрахт или блок</div>
      <h3>Soleil</h3>
      <p>Самое большое из трёх: ресторан на 110 мест, спа с крытым бассейном, сауной и хаммамом, отдельная
      столовая для узкого круга, лифт. Единственное судно, куда группа в семьдесят человек садится целиком.</p>
      <div class="spec">53 каюты · 41 Luxury 21 м² · 8 Junior 39 м² · 2 Royal 44 м² · 2 Soleil Suite 58 м²<br>3, 4 и 7 ночей по расписанию</div>
    </div>
  </div>
  <span class="pn">3</span>
</section>

<!-- 04 LUMIÈRE -->
<section class="pg split r">
  <div class="img" style="background-image:url('img/fleet/lum-pool.jpg')"></div>
  <div class="txt">
    <p class="eyebrow">Lumière · 8 кают</p>
    <h2>Для группы, которая хочет<br>весь борт себе</h2>
    <p>Lumière не продаётся по каютам — только целиком. Пять кают Luxury на одного, двоих или троих,
    два Junior Suite с ванной у окна и Lumière Suite на 68 м² с джакузи и окнами на три стороны.</p>
    <p>Маршрут меняется под группу. Базовый — пять ночей Луксор — Асуан: ночёвки
    у островов Фавза, Бесау и Хербиаб, стоянка в каменоломнях Гебель эль-Сильсила
    и ужин на берегу острова.</p>
    <div style="margin-top:4mm">
      <span class="chip">бассейн</span><span class="chip">лаунж-бар</span><span class="chip">ресторан à la carte</span>
      <span class="chip">массаж</span><span class="chip">зал</span>
    </div>
    <p class="note" style="margin-top:5mm">16 гостей при двухместном размещении, до 19 — с третьими местами в каютах Luxury.
    Источник: брошюра оператора, сентябрь 2026.</p>
  </div>
  <span class="pn" style="color:#fff">4</span>
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
  <span class="pn">5</span>
</section>

<!-- 06 LE FAYAN -->
<section class="pg split l">
  <div class="txt">
    <p class="eyebrow">Le Fayan Suites · 37 кают</p>
    <h2>Все каюты — сюиты.<br>Группа до сорока — весь борт</h2>
    <p>Тридцать шесть одинаковых сюитов по 39 м² и один Royal Suite. Это снимает главную головную боль
    группового размещения: никто не получает каюту хуже соседа. При одноместном размещении борт вмещает
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
  <span class="pn">6</span>
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
  <span class="pn">7</span>
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
    <p>Внутри спа — крытый мраморный бассейн с окнами в два этажа, сауна, хаммам
    и два массажных кабинета. На солнечной палубе — открытый бассейн, джакузи и бар.</p>
    <div class="kpi" style="margin-top:5mm">
      <div><div class="n">110</div><div class="l">мест в ресторане</div></div>
      <div><div class="n">260 м²</div><div class="l">лаунж-бар</div></div>
      <div><div class="n">53</div><div class="l">каюты, до 106 гостей</div></div>
    </div>
  </div>
  <span class="pn" style="color:#fff">8</span>
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
  <span class="pn">9</span>
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
          <li>Вечерние шоу и музыка на борту</li>
        </ul>
        <h3 style="margin-top:5mm">Считается отдельно</h3>
        <ul class="ticks p" style="margin-top:3mm">
          <li>Абу-Симбел самолётом, полёт на шаре над Луксором</li>
          <li>Алкоголь — à la carte или пакетом</li>
          <li>Перелёты Каир — Луксор / Асуан — Каир</li>
          <li>Приватные вечера в храмах</li>
        </ul>
      </div>
      <p class="note" style="margin-top:4mm">Дни посадки и состав — по опубликованным программам операторов: soleil-cruise.com и lefayansuites.com,
      страницы 3, 4 и 7 ночей. При частном фрахте день посадки и маршрут назначаются под группу.</p>
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
      <p class="sm" style="margin-top:2mm">Откатанная программа, тайминг проверен на группах. Последнее утро — ранний рейс на реку, час или полтора.</p>
      <div class="row">
        <div class="opt"><b>1 день</b>Прилёт, отель, welcome-ужин в городе. Утром — рейс на реку</div>
        <div class="opt"><b>2 дня</b>+ Гиза: квест «Код пирамид», приватный вход в пирамиду Хеопса, ужин в Lucida. По желанию — два часа в музее после квеста</div>
        <div class="opt"><b>3 дня</b>+ Большой Египетский музей, конференция в отеле, вечер на яхте. Либо день в пустыне Эль-Файюм</div>
      </div>
    </div>
    <div class="box l">
      <h3>Модуль «Нил»</h3>
      <p class="sm" style="margin-top:2mm">От числа ночей зависят порт и день посадки.</p>
      <div class="row">
        <div class="opt"><b>3 ночи</b>Из Асуана, пятница. Плотно, без пауз</div>
        <div class="opt"><b>4 ночи</b>Из Луксора, понедельник. Классика</div>
        <div class="opt"><b>5 ночей</b>Lumière, с островами. Только фрахт</div>
        <div class="opt"><b>7 ночей</b>Кольцо. Неделя на одном судне</div>
      </div>
    </div>
  </div>
  <p class="lead" style="margin-top:3mm; max-width:250mm; font-size:11pt">Четыре сочетания, которые продаются лучше всего, — на следующих страницах.</p>
  <span class="pn">11</span>
</section>

<section class="pg full">
  <div class="img" style="background-image:url('img/gen2/giza-a.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Программа 1 · суббота — пятница</p>
    <h2 style="max-width:230mm">Каир 2 дня + Нил 4 ночи</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Пирамиды и квест в Гизе, потом четыре ночи от Луксора до Асуана по понедельничной сетке операторов.</p>
  </div>
</section>

<!-- 12 ПРОГРАММА 1 -->
<section class="pg">
  <p class="eyebrow">Программа 1 · Каир 2 дня + Нил 4 ночи · 7 дней</p>
  <h2>Два дня Каира и четыре ночи на реке</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Суббота — пятница. Soleil или Le Fayan Suites. Для групп 30–70, где большинство в Египте впервые. Нужен третий день в Каире (музей, конференция, яхта) — начинаем в пятницу: Каир 3 дня + Нил 4 ночи.</p>
  <div class="days" style="--n:7">
    <div class="d c"><div class="k">Сб · Каир</div><h3>Прилёт</h3><p>Встреча у самолёта, отдельный коридор на паспортном контроле, отель. Вечером ужин в отеле или welcome-ужин в городе</p></div>
    <div class="d c"><div class="k">Вс · Каир</div><h3>Гиза: квест</h3><p>Сфинкс и Храм Долины, квест «Код пирамид», приватный вход в пирамиду Хеопса, обед в 9 Pyramids Lounge, ужин в Lucida</p></div>
    <div class="d"><div class="k">Пн · Луксор</div><h3>Посадка</h3><p>Утренний перелёт, Карнак прямо из аэропорта, посадка с 12:00. Луксорский храм в подсветке</p></div>
    <div class="d"><div class="k">Вт · западный берег</div><h3>Долина царей</h3><p>Шар на рассвете по желанию. Долина царей, Хатшепсут, Колоссы. Переход к Эдфу через Эсну</p></div>
    <div class="d"><div class="k">Ср · Эдфу, Ком-Омбо</div><h3>Два храма</h3><p>Эдфу утром, Ком-Омбо на закате, приход в Асуан</p></div>
    <div class="d"><div class="k">Чт · Асуан</div><h3>Филе</h3><p>Абу-Симбел по желанию утром. Остров Филе, нубийская деревня на лодках. После заката — Филе только для группы или ужин на палубе</p></div>
    <div class="d p"><div class="k">Пт · Асуан</div><h3>Выезд</h3><p>Выход с судна в 06:30, рейс 08:45, домой из Каира после 14:00</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пн</span><span class="chip">Le Fayan · пн</span><span class="chip l">30–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: по понедельникам из Луксора выходят оба судна, на Каир хватает двух дней
    без спешки, а домой группа летит через Каир с одной пересадкой.</p>
  </div>
  <span class="pn">13</span>
</section>


<section class="pg" style="padding:14mm 18mm 12mm">
  <p class="eyebrow" style="margin-bottom:3mm">Программа 1 · по часам</p>
  <h2 style="font-size:19pt; margin-bottom:1.5mm">Каир 2 дня + Нил 4 ночи: суббота — пятница</h2>
  <p class="sm" style="margin-bottom:4mm; font-size:8pt">Каир — по откатанной программе, прилёт показан по рейсу SU 400 из Москвы. Река — по сетке оператора и рейсам текущего сезона. Музей в день квеста — короткой опцией на два часа, полная экскурсия — в третьем каирском дне.</p>
  <div class="tt"><div class="day c"><div class="k">Сб<em>Каир</em></div><div class="row"><b>15:15</b><span>Прилёт, встреча у самолёта</span></div><div class="row"><b>16:00</b><span>Трансфер в отель, около часа</span></div><div class="row"><b>17:00</b><span>Заселение, отдых</span></div><div class="row"><b>19:30</b><span>Ужин в отеле или welcome-ужин в городе</span></div></div><div class="day c"><div class="k">Вс<em>Каир</em></div><div class="row"><b>08:10</b><span>Выезд на плато Гиза</span></div><div class="row"><b>10:00</b><span>Сфинкс и Храм Долины</span></div><div class="row"><b>10:40</b><span>Квест «Код пирамид»</span></div><div class="row"><b>12:00</b><span>Приватный вход в пирамиду Хеопса</span></div><div class="row"><b>14:15</b><span>Обед в 9 Pyramids Lounge, итоги квеста</span></div><div class="row"><b>15:45</b><span class="opt">Большой Египетский музей, два часа</span></div><div class="row"><b>19:30</b><span>Ужин в Lucida</span></div></div><div class="day "><div class="k">Пн<em>Каир → Луксор</em></div><div class="row"><b>03:30</b><span>Подъём, чемоданы у дверей</span></div><div class="row"><b>04:15</b><span>Выезд в аэропорт</span></div><div class="row"><b>≈07:00</b><span>Рейс в Луксор, прилёт 08:20</span></div><div class="row"><b>09:15</b><span>Карнак прямо из аэропорта</span></div><div class="row"><b>12:00</b><span>Посадка, обед на борту</span></div><div class="row"><b>16:45</b><span>Луксорский храм: засветло и в подсветке</span></div><div class="row"><b>19:30</b><span>Ужин. Ночь в Луксоре</span></div></div><div class="day "><div class="k">Вт<em>Западный берег</em></div><div class="row"><b>05:00</b><span class="opt">Шар на рассвете, по погоде</span></div><div class="row"><b>07:00</b><span>Завтрак</span></div><div class="row"><b>08:45</b><span>Долина царей, Хатшепсут, Колоссы</span></div><div class="row"><b>13:30</b><span>Обед на борту, отход</span></div><div class="row"><b>≈17:00</b><span>Подход к Эсне, шлюз по очереди</span></div><div class="row"><b>20:00</b><span>Ужин. Эдфу вечером или ночью</span></div></div><div class="day "><div class="k">Ср<em>Эдфу → Асуан</em></div><div class="row"><b>08:00</b><span>Храм Гора в Эдфу, конные экипажи</span></div><div class="row"><b>10:15</b><span>Отход, 2–3 часа хода</span></div><div class="row"><b>13:00</b><span>Ком-Омбо, обед у причала</span></div><div class="row"><b>16:00</b><span>Ком-Омбо в предзакатный час</span></div><div class="row"><b>17:30</b><span>Отход в Асуан</span></div><div class="row"><b>20:00</b><span>Ужин в пути. Ночь в Асуане</span></div></div><div class="day "><div class="k">Чт<em>Асуан</em></div><div class="row"><b>04:30</b><span class="opt">Абу-Симбел самолётом, до 12:15</span></div><div class="row"><b>08:00</b><span>Причал Шеллал, Филе катером</span></div><div class="row"><b>10:45</b><span>Плотина, Незаконченный обелиск</span></div><div class="row"><b>13:00</b><span>Обед</span></div><div class="row"><b>15:00</b><span>Нубийская деревня на лодках</span></div><div class="row"><b>18:00</b><span class="opt">Вечер на Филе — по согласованию</span></div><div class="row"><b>19:30</b><span>Ужин на борту</span></div></div><div class="day p"><div class="k">Пт<em>Асуан → домой</em></div><div class="row"><b>05:30</b><span>Чемоданы у кают, завтрак</span></div><div class="row"><b>06:30</b><span>Выход с судна, трансфер</span></div><div class="row"><b>08:45</b><span>Рейс в Каир, прилёт 10:10 (запасной 09:10)</span></div><div class="row"><b>14:00</b><span>Международный вылет — не раньше</span></div></div></div>
  <span class="pn">14</span>
</section>

<section class="pg full">
  <div class="img" style="background-image:url('img/gen2/nubian-b.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Программа 2 · среда — понедельник</p>
    <h2 style="max-width:230mm">Каир 2 дня + Нил 3 ночи</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Самый короткий формат: Гиза, перелёт в Асуан, три ночи вниз по течению до Луксора.</p>
  </div>
</section>

<!-- 13 ПРОГРАММА 2 -->
<section class="pg">
  <p class="eyebrow">Программа 2 · Каир 2 дня + Нил 3 ночи · 6 дней</p>
  <h2>Два дня Каира и три ночи от Асуана</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Среда — понедельник. Soleil или Le Fayan Suites. Для корпоративных групп с жёстким графиком.</p>
  <div class="days" style="--n:6">
    <div class="d c"><div class="k">Ср · Каир</div><h3>Прилёт</h3><p>Встреча у самолёта, отдельный коридор на паспортном контроле, отель. Вечером ужин в отеле или welcome-ужин в городе</p></div>
    <div class="d c"><div class="k">Чт · Каир</div><h3>Гиза: квест</h3><p>Сфинкс и Храм Долины, квест «Код пирамид», приватный вход в пирамиду Хеопса, обед в 9 Pyramids Lounge, ужин в Lucida</p></div>
    <div class="d"><div class="k">Пт · Асуан</div><h3>Посадка</h3><p>Утренний перелёт в Асуан, по дороге к причалу — остров Филе. Посадка с 12:00, нубийская деревня</p></div>
    <div class="d"><div class="k">Сб · Ком-Омбо, Эдфу</div><h3>Два храма</h3><p>Ком-Омбо утром, Эдфу днём, переход в Луксор через Эсну</p></div>
    <div class="d"><div class="k">Вс · Луксор</div><h3>Оба берега</h3><p>Шар на рассвете по желанию. Долина царей, Хатшепсут, Колоссы, днём Карнак и Луксорский храм</p></div>
    <div class="d p"><div class="k">Пн · Луксор</div><h3>Выезд</h3><p>Выход с судна в 07:00, утренний рейс в Каир, домой после 14:00</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пт</span><span class="chip">Le Fayan · пт</span><span class="chip l">20–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: три ночи — самый ходовой формат на Ниле, по пятницам из Асуана выходят оба судна,
    а Луксор достаётся целым днём в конце, когда группа уже втянулась в ритм поездки.</p>
  </div>
  <span class="pn">16</span>
</section>


<section class="pg" style="padding:14mm 18mm 12mm">
  <p class="eyebrow" style="margin-bottom:3mm">Программа 2 · по часам</p>
  <h2 style="font-size:19pt; margin-bottom:1.5mm">Каир 2 дня + Нил 3 ночи: среда — понедельник</h2>
  <p class="sm" style="margin-bottom:4mm; font-size:8pt">Время — ориентир по стандартным программам операторов и расписанию рейсов текущего сезона. Точные часы фиксируются в договоре под дату и сезон. Абу-Симбел сюда не помещается: нужна ночь в Асуане накануне. Вариант: в четверг вечерний перелёт в Асуан, ночь в отеле, рейс 06:55–12:15, посадка после возвращения.</p>
  <div class="tt"><div class="day c"><div class="k">Ср<em>Каир</em></div><div class="row"><b>15:15</b><span>Прилёт, встреча у самолёта</span></div><div class="row"><b>16:00</b><span>Трансфер в отель, около часа</span></div><div class="row"><b>17:00</b><span>Заселение, отдых</span></div><div class="row"><b>19:30</b><span>Ужин в отеле или welcome-ужин в городе</span></div></div><div class="day c"><div class="k">Чт<em>Каир</em></div><div class="row"><b>08:10</b><span>Выезд на плато Гиза</span></div><div class="row"><b>10:00</b><span>Сфинкс и Храм Долины</span></div><div class="row"><b>10:40</b><span>Квест «Код пирамид»</span></div><div class="row"><b>12:00</b><span>Приватный вход в пирамиду Хеопса</span></div><div class="row"><b>14:15</b><span>Обед в 9 Pyramids Lounge, итоги квеста</span></div><div class="row"><b>15:45</b><span class="opt">Большой Египетский музей, два часа</span></div><div class="row"><b>19:30</b><span>Ужин в Lucida</span></div></div><div class="day "><div class="k">Пт<em>Каир → Асуан</em></div><div class="row"><b>04:00</b><span>Выезд в аэропорт</span></div><div class="row"><b>≈06:30</b><span>Рейс в Асуан, прилёт ≈08:00</span></div><div class="row"><b>09:15</b><span>Филе катером с причала Шеллал</span></div><div class="row"><b>11:00</b><span>Высокая плотина, Незаконченный обелиск</span></div><div class="row"><b>12:15</b><span>Посадка, обед на борту</span></div><div class="row"><b>15:00</b><span>Нубийская деревня на лодках</span></div><div class="row"><b>19:30</b><span>Ужин. Ночь в Асуане</span></div></div><div class="day "><div class="k">Сб<em>Ком-Омбо, Эдфу</em></div><div class="row"><b>05:30</b><span>Отход, завтрак в пути</span></div><div class="row"><b>09:00</b><span>Ком-Омбо</span></div><div class="row"><b>10:30</b><span>Отход на Эдфу, обед в пути</span></div><div class="row"><b>14:00</b><span>Храм Гора в Эдфу, конные экипажи</span></div><div class="row"><b>16:30</b><span>Отход, шлюз Эсны по очереди</span></div><div class="row"><b>20:00</b><span>Ужин в пути. Луксор ночью</span></div></div><div class="day "><div class="k">Вс<em>Луксор</em></div><div class="row"><b>05:00</b><span class="opt">Шар на рассвете, по погоде</span></div><div class="row"><b>07:30</b><span>Завтрак</span></div><div class="row"><b>08:30</b><span>Выезд: Долина царей, Хатшепсут, Колоссы</span></div><div class="row"><b>13:30</b><span>Обед на борту</span></div><div class="row"><b>15:30</b><span>Карнакский храм</span></div><div class="row"><b>17:30</b><span>Луксорский храм в подсветке</span></div><div class="row"><b>20:00</b><span>Прощальный ужин на борту</span></div></div><div class="day p"><div class="k">Пн<em>Луксор → домой</em></div><div class="row"><b>05:30</b><span>Чемоданы у кают</span></div><div class="row"><b>06:00</b><span>Завтрак</span></div><div class="row"><b>07:00</b><span>Выход с судна, трансфер</span></div><div class="row"><b>≈09:00</b><span>Рейс в Каир, час под дату</span></div><div class="row"><b>14:00</b><span>Международный вылет — не раньше</span></div></div></div>
  <span class="pn">17</span>
</section>

<section class="pg full">
  <div class="img" style="background-image:url('img/gen2/balloons-b.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Программа 3 · понедельник — понедельник</p>
    <h2 style="max-width:230mm">Только Нил, 7 ночей</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Неделя на одном судне: чемоданы распаковываются один раз, два полных дня в Асуане.</p>
  </div>
</section>

<!-- 14 ПРОГРАММА 3 -->
<section class="pg">
  <p class="eyebrow">Программа 3 · Только Нил 7 ночей · 8 дней</p>
  <h2>Семь ночей по кольцу, без Каира</h2>
  <p class="sm" style="margin-top:-3mm; margin-bottom:5mm">Понедельник — понедельник. Soleil или Le Fayan Suites. Для тех, кто уже был в Каире; подробный тайминг — в приложении «Программы по дням».</p>
  <div class="days" style="--n:8">
    <div class="d"><div class="k">Пн</div><h3>Луксор</h3><p>Прилёт утренним рейсом, посадка с 12:00, Луксорский храм в подсветке</p></div>
    <div class="d"><div class="k">Вт</div><h3>Западный берег</h3><p>Шар по желанию, Долина царей, Хатшепсут, Эсна, ночь в Эдфу</p></div>
    <div class="d"><div class="k">Ср</div><h3>Эдфу, Ком-Омбо</h3><p>Два храма, приход в Асуан</p></div>
    <div class="d"><div class="k">Чт</div><h3>Асуан</h3><p>Филе, плотина и обелиск, свободная вторая половина дня, вечер на палубе</p></div>
    <div class="d"><div class="k">Пт</div><h3>Асуан</h3><p>Абу-Симбел по желанию, нубийская деревня на лодках</p></div>
    <div class="d"><div class="k">Сб</div><h3>Обратно</h3><p>Стоянки судна в Ком-Омбо и Эдфу, переход в Луксор через Эсну</p></div>
    <div class="d"><div class="k">Вс</div><h3>Карнак</h3><p>Карнакский храм, свободный день в Луксоре, прощальный вечер</p></div>
    <div class="d p"><div class="k">Пн</div><h3>Выезд</h3><p>Выезд до 08:00, вылет из Луксора</p></div>
  </div>
  <div style="margin-top:6mm; display:flex; gap:10mm; align-items:flex-start">
    <div style="flex:1"><span class="chip">Soleil · пн</span><span class="chip">Le Fayan · пн</span><span class="chip l">30–70 гостей</span></div>
    <p class="note" style="flex:2; margin:0">Почему эта: неделя на одном судне, чемоданы распаковываются один раз, два полных дня в Асуане, свободные
    дни под рабочие сессии или отдых. Дороже всего в сумме, зато ритм самый спокойный: ни одного переезда.</p>
  </div>
  <span class="pn">19</span>
</section>


<section class="pg" style="padding:14mm 18mm 12mm">
  <p class="eyebrow" style="margin-bottom:3mm">Программа 3 · по часам</p>
  <h2 style="font-size:19pt; margin-bottom:1.5mm">Нил 7 ночей: понедельник — понедельник</h2>
  <p class="sm" style="margin-bottom:4mm; font-size:8pt">Время — ориентир по стандартным программам операторов и расписанию рейсов текущего сезона. Точные часы фиксируются в договоре под дату. На регулярном рейсе часы отхода и стоянок в среду и субботу назначает судно.</p>
  <div class="tt"><div class="day "><div class="k">Пн<em>Луксор</em></div><div class="row"><b>08:20</b><span>Прилёт утренним рейсом, встреча</span></div><div class="row"><b>09:00</b><span>Багаж на борт, кофе на палубе</span></div><div class="row"><b>12:00</b><span>Посадка, обед</span></div><div class="row"><b>14:40</b><span>Прилёт дневного рейса, если летим двумя</span></div><div class="row"><b>17:00</b><span>Луксорский храм в подсветке</span></div><div class="row"><b>19:30</b><span>Ужин. Ночь в Луксоре</span></div></div><div class="day "><div class="k">Вт<em>Западный берег</em></div><div class="row"><b>04:30</b><span class="opt">Шар на рассвете, по погоде</span></div><div class="row"><b>07:00</b><span>Завтрак</span></div><div class="row"><b>08:00</b><span>Выезд: Долина царей, Хатшепсут, Колоссы</span></div><div class="row"><b>13:00</b><span>Обед, отход на юг</span></div><div class="row"><b>≈16:00</b><span>Эсна, шлюз по очереди</span></div><div class="row"><b>20:00</b><span>Ужин по готовности. Ночь в Эдфу</span></div></div><div class="day "><div class="k">Ср<em>Эдфу → Асуан</em></div><div class="row"><b>07:15</b><span>Храм Гора в Эдфу, конные экипажи</span></div><div class="row"><b>09:15</b><span>Отход, 2–3 часа хода</span></div><div class="row"><b>≈13:00</b><span>Ком-Омбо, обед у причала</span></div><div class="row"><b>≈14:00</b><span>Ком-Омбо</span></div><div class="row"><b>≈15:30</b><span>Отход в Асуан</span></div><div class="row"><b>≈18:30</b><span>Приход в Асуан, ужин в 20:00</span></div></div><div class="day "><div class="k">Чт<em>Асуан</em></div><div class="row"><b>08:00</b><span>Высокая плотина, Филе, Незаконченный обелиск</span></div><div class="row"><b>13:00</b><span>Обед</span></div><div class="row"><b>14:30</b><span>Свободное время: спа, палуба</span></div><div class="row"><b>18:00</b><span class="opt">Вечер на Филе — по согласованию</span></div><div class="row"><b>20:00</b><span>Ужин на борту</span></div></div><div class="day "><div class="k">Пт<em>Асуан</em></div><div class="row"><b>06:55</b><span class="opt">Абу-Симбел самолётом, до 12:15</span></div><div class="row"><b>08:30</b><span>Завтрак, свободное утро</span></div><div class="row"><b>13:00</b><span>Обед</span></div><div class="row"><b>15:00</b><span>Нубийская деревня на лодках</span></div><div class="row"><b>20:00</b><span>Ужин. Ночь в Асуане</span></div></div><div class="day "><div class="k">Сб<em>Асуан → Луксор</em></div><div class="row"><b>≈05:00</b><span>Отход по расписанию судна</span></div><div class="row"><b>≈08:30</b><span>Стоянка в Ком-Омбо, мы на борту</span></div><div class="row"><b>≈12:30</b><span>Стоянка в Эдфу, обед</span></div><div class="row"><b>≈17:30</b><span>Эсна, шлюз по очереди</span></div><div class="row"><b>20:00</b><span>Ужин в пути. Луксор поздно вечером</span></div></div><div class="day "><div class="k">Вс<em>Луксор</em></div><div class="row"><b>09:15</b><span>Карнакский храм</span></div><div class="row"><b>13:00</b><span>Обед</span></div><div class="row"><b>14:00</b><span>Свободный день или рабочая сессия</span></div><div class="row"><b>19:30</b><span>Прощальный вечер на палубе</span></div><div class="row"><b>19:30</b><span class="opt">В храме — по согласованию</span></div></div><div class="day p"><div class="k">Пн<em>Домой</em></div><div class="row"><b>06:00</b><span>Завтрак</span></div><div class="row"><b>07:00</b><span>Выход с судна, трансфер</span></div><div class="row"><b>≈09:00</b><span>Рейс в Каир, час под дату</span></div><div class="row"><b>14:00</b><span>Международный вылет — не раньше</span></div></div></div>
  <span class="pn">20</span>
</section>

<section class="pg full">
  <div class="img" style="background-image:url('img/fleet/lum-island-dinner.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Программа 4 · любой день</p>
    <h2 style="max-width:230mm">Lumière, 5 ночей с островами</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Дахабия только под вашу группу до шестнадцати человек, ночёвки у островов, ужин на берегу.</p>
  </div>
</section>

<!-- 15 ПРОГРАММА 4 -->
<section class="pg split l">
  <div class="txt">
    <p class="eyebrow">Программа 4 · Lumière 5 ночей · Каир 0–2 дня по желанию</p>
    <h2>Lumière: пять ночей<br>с островами</h2>
    <p>Для группы до шестнадцати человек, которой на борту не нужен никто чужой. Весь борт свой, день посадки
    любой, маршрут с ночёвками у островов, куда большие суда не подходят.</p>
    <table class="tbl" style="margin-top:3mm; font-size:9pt">
      <tr><td class="b" style="width:22mm">День 1</td><td>Луксор: посадка, Карнак, Луксорский храм, коктейль на палубе</td></tr>
      <tr><td class="b">День 2</td><td>Шар по желанию, западный берег, переход к Эдфу, ночь у острова Фавза</td></tr>
      <tr><td class="b">День 3</td><td>Эдфу в конных экипажах, остров Бесау, каменоломни Гебель эль-Сильсила</td></tr>
      <tr><td class="b">День 4</td><td>Ком-Омбо, остров Хербиаб: приватный ужин и вечер на берегу</td></tr>
      <tr><td class="b">День 5</td><td>Асуан: Филе, нубийская деревня, заповедник на лодках</td></tr>
      <tr><td class="b">День 6</td><td>Абу-Симбел по желанию, выезд</td></tr>
    </table>
    <p class="note" style="margin-top:4mm">Каир добавляется одним или двумя днями до посадки. Стоянки у островов — по уровню воды. Программа — по образцу оператора, сентябрь 2026.</p>
  </div>
  <div class="img" style="background-image:url('img/fleet/lum-island-dinner.jpg')"></div>
  <span class="pn">22</span>
</section>


<section class="pg" style="padding:14mm 18mm 12mm">
  <p class="eyebrow" style="margin-bottom:3mm">Программа 4 · по часам</p>
  <h2 style="font-size:19pt; margin-bottom:1.5mm">Lumière 5 ночей: шесть дней с островами</h2>
  <p class="sm" style="margin-bottom:4mm; font-size:8pt">Время — ориентир по стандартным программам операторов и расписанию рейсов текущего сезона. Точные часы фиксируются в договоре под дату. День посадки — любой: судно идёт только под вашу группу. Часы переходов между островами — оценка, расстановку по воде даёт капитан.</p>
  <div class="tt"><div class="day "><div class="k">День 1<em>Луксор</em></div><div class="row"><b>08:20</b><span>Прилёт утренним рейсом из Каира</span></div><div class="row"><b>09:15</b><span>На причал, кофе на палубе, каюты по готовности</span></div><div class="row"><b>12:30</b><span>Обед на борту</span></div><div class="row"><b>15:00</b><span>Карнакский храм</span></div><div class="row"><b>17:15</b><span>Луксорский храм: закат и подсветка</span></div><div class="row"><b>19:00</b><span>Коктейль, ужин. Ночь в Луксоре</span></div></div><div class="day "><div class="k">День 2<em>Западный берег</em></div><div class="row"><b>05:00</b><span class="opt">Шар на рассвете, по погоде</span></div><div class="row"><b>08:00</b><span>Завтрак</span></div><div class="row"><b>08:45</b><span>Долина царей, Хатшепсут, Колоссы</span></div><div class="row"><b>13:30</b><span>Обед, отход</span></div><div class="row"><b>16:30</b><span>Шлюз в Эсне, по очереди</span></div><div class="row"><b>19:30</b><span>Ужин. Ночь у острова Фавза, по уровню воды</span></div></div><div class="day "><div class="k">День 3<em>Эдфу, острова</em></div><div class="row"><b>06:30</b><span>Отход, завтрак в пути</span></div><div class="row"><b>08:15</b><span>Храм Гора в Эдфу, конные экипажи</span></div><div class="row"><b>11:30</b><span>Остров Бесау</span></div><div class="row"><b>13:00</b><span>Обед в пути</span></div><div class="row"><b>14:15</b><span>Каменоломни Гебель эль-Сильсила</span></div><div class="row"><b>19:30</b><span>Ужин. Ночь у острова близ Ком-Омбо</span></div></div><div class="day "><div class="k">День 4<em>Ком-Омбо</em></div><div class="row"><b>08:30</b><span>Ком-Омбо</span></div><div class="row"><b>10:30</b><span>Отход к острову Хербиаб</span></div><div class="row"><b>13:00</b><span>Обед</span></div><div class="row"><b>14:30</b><span>Остров Хербиаб: прогулка, закат</span></div><div class="row"><b>18:30</b><span>Ужин на берегу острова; при ветре — на борту</span></div><div class="row"><b>21:30</b><span>Возврат на борт</span></div></div><div class="day "><div class="k">День 5<em>Асуан</em></div><div class="row"><b>06:00</b><span>Отход в Асуан, завтрак в пути</span></div><div class="row"><b>09:30</b><span>Швартовка в Асуане</span></div><div class="row"><b>10:00</b><span>Остров Филе катером</span></div><div class="row"><b>12:45</b><span>Обед</span></div><div class="row"><b>14:00</b><span>Лодками через пороги: заповедник, нубийская деревня</span></div><div class="row"><b>18:00</b><span class="opt">Вечер на Филе — по согласованию</span></div><div class="row"><b>20:00</b><span>Ужин. Ночь в Асуане</span></div></div><div class="day p"><div class="k">День 6<em>Домой</em></div><div class="row"><b>05:00</b><span class="opt">Абу-Симбел самолётом, 06:55–12:15</span></div><div class="row"><b>06:40</b><span>Выход с борта: рейс в Каир 08:45</span></div><div class="row"><b>12:30</b><span>Обед для летавших в Абу-Симбел</span></div><div class="row"><b>20:15</b><span>Рейс в Каир для летавших (вт/чт — 17:30)</span></div></div></div>
  <span class="pn">23</span>
</section>

<!-- 16 ЧТО ПРОДАВАТЬ -->
<section class="pg">
  <p class="eyebrow">Что продавать</p>
  <h2>Размер группы определяет судно, судно — программу</h2>
  <table class="tbl" style="margin-top:2mm; font-size:9pt">
    <tr><th style="width:22mm">Группа</th><th style="width:60mm">Судно и формат</th><th style="width:46mm">Размещение</th><th>Программа</th><th style="width:60mm">Почему так</th></tr>
    <tr>
      <td class="b">16–20</td>
      <td><b>Lumière</b> — весь борт<br><span class="m">либо блок 16–20 кают на Le Fayan</span></td>
      <td>8 кают: по двое, в Luxury — до троих</td>
      <td>Программа 4, Каир по желанию</td>
      <td class="m">Единственный вариант, при котором группа такого размера получает судно целиком: чужих на борту нет</td>
    </tr>
    <tr>
      <td class="b">30</td>
      <td><b>Le Fayan Suites</b> — весь борт<br><span class="m">либо блок 15–30 кают на Soleil</span></td>
      <td>37 сюитов, все одноместно</td>
      <td>Программы 1 или 3</td>
      <td class="m">Каждому — сюит 39 м² без доплаты за одноместное. Семь свободных кают — запас, если группа вырастет</td>
    </tr>
    <tr>
      <td class="b">50</td>
      <td><b>Soleil</b> — весь борт<br><span class="m">либо Le Fayan по двое в сюите</span></td>
      <td>53 каюты: одноместно для всех, или 25 кают по двое</td>
      <td>Программы 1, 2 или 3</td>
      <td class="m">Ресторан на 110 мест и спа принимают такую группу без очередей. Отдельная столовая — для руководства</td>
    </tr>
    <tr>
      <td class="b">70–100</td>
      <td><b>Soleil</b> — весь борт</td>
      <td>35–50 кают по двое, остальные под одноместных и команду</td>
      <td>Программы 1 или 2</td>
      <td class="m">Единственное судно из трёх, куда сто человек садятся целиком. Такой группе удобнее три-четыре ночи, чем неделя</td>
    </tr>
    <tr>
      <td class="b">150–200</td>
      <td><b>Регата</b>: Soleil + Le Fayan Suites<br><span class="m">плюс Lumière для ядра группы</span></td>
      <td>Два-три судна идут вместе по одному расписанию</td>
      <td>Программы 1 или 2, общие вечера на берегу</td>
      <td class="m">У Soleil и Le Fayan одна сетка отправлений — понедельник и пятница, — поэтому они встают рядом в каждом порту</td>
    </tr>
  </table>
  <p class="note" style="margin-top:4mm">Между размерами — блоки на регулярных отправлениях: группа едет на сборном рейсе, но со своим гидом,
  своими столами и своей программой на берегу. Блок бронируется под день отправления из расписания.</p>
  <span class="pn">24</span>
</section>


<!-- РЕГАТА -->
<section class="pg split l">
  <div class="txt">
    <p class="eyebrow">Больше ста человек</p>
    <h2>Регата: несколько судов<br>идут вместе</h2>
    <p>Когда группа не помещается на одно судно, мы не ищем борт побольше — их на Ниле нет.
    Мы ставим два или три судна в одно расписание: они выходят в один день, стоят рядом в каждом порту
    и приходят на берег одной группой.</p>
    <p>У каждого судна остаются свой ресторан, бассейн и палуба — очередей нет. Общими становятся вечера
    на берегу: ужин в храме, светозвуковой показ на Филе, прощальный вечер. Lumière в такой регате —
    судно для ядра группы: совета директоров, владельцев, почётных гостей.</p>
    <div class="kpi" style="margin-top:5mm">
      <div><div class="n">≈ 200</div><div class="l">гостей на трёх судах по двое в каюте</div></div>
      <div><div class="n">1</div><div class="l">расписание: понедельник из Луксора или пятница из Асуана</div></div>
      <div><div class="n">3</div><div class="l">ресторана и три палубы — без очередей</div></div>
    </div>
    <p class="note" style="margin-top:5mm">Расчёт: Soleil 106 + Le Fayan 74 + Lumière 16–19 при двухместном размещении.
    Наличие судов на одну дату подтверждается операторами под запрос.</p>
  </div>
  <div class="img" style="background-image:url('img/fleet/sol-exterior.jpg')"></div>
  <span class="pn">25</span>
</section>

<!-- 17 ПРИВАТНЫЕ ВЕЧЕРА -->
<section class="pg full">
  <div class="img" style="background-image:url('img/fleet/gen-2.jpg')"></div>
  <div class="veil"></div>
  <div class="cap">
    <p class="eyebrow">Наш фирменный формат</p>
    <h2 style="max-width:220mm">Приватные вечера в храмах</h2>
    <p class="lead" style="max-width:210mm; margin-top:3mm">Храм закрывают для всех, кроме вашей группы; разрешение оформляем мы. Ужин у подножия
    храма Хатшепсут, вечер у пилонов Карнака, остров Филе со светозвуковым показом только для вас.
    Оформление, свет, музыка и кухня — наша работа.</p>
  </div>
</section>

<section class="pg" style="padding:12mm 18mm">
  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; height:100%">
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/gen-3.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Карнак</div><p class="sm">Ужин у первого пилона, подсветка и лучи над дворами храма. Вмещает всю группу, вплоть до регаты</p></div>
    </div>
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/gen-6.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Хатшепсут</div><p class="sm">Длинный стол, канделябры и цветы перед террасами храма в скале. После закрытия здесь никого, кроме группы</p></div>
    </div>
    <div style="display:flex; flex-direction:column; gap:4mm">
      <div class="ph" style="flex:1; border-radius:3mm; background:url('img/fleet/lum-philae-aerial.jpg') center/cover"></div>
      <div><div class="eyebrow" style="margin-bottom:1.5mm">Филе</div><p class="sm">Остров закрывают на вечер: напитки у причала, осмотр храма без посторонних, ужин, светозвуковой показ для группы</p></div>
    </div>
  </div>
  <span class="pn">27</span>
</section>

<!-- 19 КАК БРОНИРУЕТСЯ -->
<section class="pg">
  <p class="eyebrow">Как это бронируется</p>
  <h2>Три решения, которые нужны от группы</h2>
  <div class="cols3" style="margin-top:4mm">
    <div class="tile"><div class="k">01 · Размер</div><p>От него зависят судно и формат — фрахт или блок. Цену на человека считаем для нескольких размеров группы:
    при фрахте судно оплачено целиком, и каждый новый гость снижает её.</p></div>
    <div class="tile l"><div class="k">02 · Даты</div><p>Регулярные отправления — понедельник из Луксора, пятница из Асуана. При фрахте день посадки назначается
    под группу. Январь — высокий сезон, блоки разбирают за несколько месяцев.</p></div>
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
      <li>Цена фиксируется договором на группу и даты</li><li>Паспортные данные — за восемь недель: иначе не получить разрешения в храмы</li>
      <li>Цены на человека — по запросу под размер группы</li></ul></div>
  </div>
  <span class="pn">28</span>
</section>

<!-- 20 КОНТАКТЫ -->
<section class="pg split r">
  <div class="img" style="background-image:url('img/nile.jpg')"></div>
  <div class="txt">
    <img src="{{LOGO}}" alt="La Royal Event" style="width:42mm; margin-bottom:4mm">
    <p class="eyebrow">Запросите даты</p>
    <h2>Назовите размер группы<br>и месяц</h2>
    <p>Мы проверим у операторов, свободно ли судно на ваши даты, предложим программу и посчитаем цену на человека.</p>
    <div class="contact" style="margin-top:4mm">
      <div class="k">Телефон</div><div><span class="fill"></span></div>
      <div class="k">WhatsApp</div><div><span class="fill"></span></div>
      <div class="k">Почта</div><div><span class="fill"></span></div>
      <div class="k">Сайт</div><div><span class="fill"></span></div>
    </div>
    <p class="note" style="margin-top:3mm">Источники: сайты и брошюры операторов 2026 — soleil-cruise.com, lefayansuites.com,
    lumiere-cruise.com. Фото вечеров — с мероприятий La Royal Event, переработаны.</p>
  </div>
  <span class="pn" style="color:#fff">29</span>
</section>

</body></html>
'''.replace('{{LOGO}}', LOGO)

html = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Нил · три судна · La Royal Event</title>' + head + extra_css + '</head>')
io.open('fleet.html', 'w', encoding='utf-8').write(html + body)
print('fleet.html собран')
