# -*- coding: utf-8 -*-
"""Калькулятор сметы. Жёлтые ячейки — ввод, сиреневые — формулы.
Гостевые строки считаются только по гостям. Расходы команды La Royal собраны
на отдельном листе и попадают в себестоимость через переключатель."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
H   = Font(bold=True, size=11, color="FFFFFF")
HF  = PatternFill("solid", fgColor="5B46B8")
SUB = Font(bold=True, size=11, color="5B46B8")
INP = PatternFill("solid", fgColor="FFF2CC")
CALC= PatternFill("solid", fgColor="EFECFB")
TOT = PatternFill("solid", fgColor="D9E2F3")
FIN = PatternFill("solid", fgColor="C3E850")
WARN= PatternFill("solid", fgColor="FBF0FB")
B   = Font(bold=True)
I   = Font(italic=True, size=9, color="7A729C")
thin= Side(style="thin", color="E4DFF8")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP= Alignment(wrap_text=True, vertical="top")
MON = '#,##0'

def hdr(ws, row, cells):
    for i, v in enumerate(cells, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = H; c.fill = HF
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# ═══════════════ Лист 1: Калькулятор ═══════════════
ws = wb.active; ws.title = "Калькулятор"
for col, w in zip("ABCDEF", (46, 13, 16, 13, 13, 50)): ws.column_dimensions[col].width = w

ws["A1"] = "СМЕТА НА ОДНОГО ГОСТЯ · Египет, январь 2027 · La Royal Event"
ws["A1"].font = Font(bold=True, size=14, color="5B46B8")
ws["A2"] = ("Жёлтое меняем руками, сиреневое считается само. Цены поставщиков названы устно; "
            "цены отелей взяты из открытых источников и предложением не являются.")
ws["A2"].font = I

ws["A4"] = "ИСХОДНЫЕ ДАННЫЕ"; ws["A4"].font = SUB
params = [
    ("Гостей",                    16, "чел",  "На это число делится всё"),
    ("Дней фрахта, вариант A",     4, "дней", "25–29 января"),
    ("Дней фрахта, вариант B",     5, "дней", "25–30 января"),
    ("Фрахт за день, USD",     54500, "USD",  "ПРОВЕРИТЬ: за ночь фрахта или за календарный день"),
    ("Курс EUR/USD",          1.1489, "",     "На 20.09.2026. На дату платежа будет другим"),
    ("Вознаграждение La Royal", 0.15, "доля", "Наценка на себестоимость"),
]
r = 5
hdr(ws, r, ["Параметр", "Значение", "Ед.", "", "", "Комментарий"]); r += 1
p0 = r
for name, val, unit, note in params:
    ws.cell(r, 1, name).font = B
    c = ws.cell(r, 2, val); c.fill = INP; c.border = BOX
    c.number_format = '0.0000' if "Курс" in name else ('0%' if "Вознаграждение" in name else MON)
    ws.cell(r, 3, unit).font = I
    n = ws.cell(r, 6, note); n.alignment = WRAP; n.font = I
    if "ПРОВЕРИТЬ" in note: n.fill = WARN
    r += 1
G, DA, DB, DAY, RATE, MARG = [f"$B${p0+i}" for i in range(6)]

r += 1
ws.cell(r, 1, "РАСЧЁТ").font = SUB
ws.cell(r, 6, "Все строки, кроме последней, считаются только по гостям").font = I
r += 1
hdr(ws, r, ["Статья", "Цена", "Единица", "A, на гостя", "B, на гостя", "Что уточнить"]); r += 1
start = r

# (название, цена или None→формула, единица, формула A, формула B, комментарий)
rows = [
 ("Фрахт судна", f"={DAY}", "за день",
  f"={DAY}*{DA}/{G}", f"={DAY}*{DB}/{G}",
  "ПРОВЕРИТЬ: «в день» — за ночь фрахта или за календарный день"),
 ("Филе: визит и показ", 15000, "EUR за группу",
  "=B{row}*"+RATE+"/"+G, "=B{row}*"+RATE+"/"+G,
  "Договор в евро. Входит ли лодка от Шеллала"),
 ("Ужин на острове Филе", 0, "за группу",
  "=B{row}/"+G, "=B{row}/"+G,
  "ЦЕНЫ НЕТ. Плюсом к 15 000 EUR"),
 ("Гиза: приватный доступ, одно посещение", 3500, "за посещение",
  "=B{row}*2/"+G, "=B{row}*2/"+G,
  "ПОДТВЕРЖДЕНО: персональное разрешение, доступ во все зоны. Нужно два"),
 ("Абу-Симбел самолётом", 470, "на гостя",
  "=B{row}", "=B{row}",
  "Обязательная часть для всех. Альтернатива по земле — см. лист «Абу-Симбел»"),
 ("Giza Palace, ночь", 325, "за номер за ночь",
  "=B{row}*2", "=B{row}*2",
  "Две ночи. Открытые источники 222–349. Запросить групповой тариф"),
 ("Steigenberger Nile Palace, ночь", 170, "за номер за ночь",
  "=B{row}", "=B{row}",
  "Открытые источники 120–176. Запросить групповой тариф"),
 ("Four Seasons Cairo, ночь", 570, "на гостя",
  "=B{row}", "=B{row}",
  "Названо отелем, все налоги включены"),
 ("Прощальный ужин в Four Seasons", 250, "на гостя",
  "=B{row}", "=0",
  "Net или ++? С надбавками 319. Только вариант A"),
 ("Ужин в Lucida", 150, "на гостя",
  "=B{row}", "=B{row}",
  "ПОДТВЕРЖДЕНО: 150 без алкоголя"),
 ("Питание в отелях вне названных ресторанов", 200, "на гостя",
  "=B{row}", "=B{row}",
  "Наша оценка на всю поездку: ужин 40–60, обед 25–35"),
 ("Полёт на шаре, две корзины", 5000, "за все корзины",
  "=B{row}/"+G, "=B{row}/"+G,
  "ПОДТВЕРЖДЕНО: две корзины, по 8 человек"),
 ("Нубийский ансамбль", 650, "за вечер",
  "=B{row}/"+G, "=B{row}/"+G,
  "Наша оценка 400–900. Публичных прайсов нет"),
 ("Гала-ужин на борту, вариант B", 0, "за группу",
  "=0", "=B{row}/"+G,
  "ЦЕНЫ НЕТ. Меню, декор, музыка сверх пансиона"),
 ("Наземная программа 22–25 января", 0, "за группу",
  "=B{row}/"+G, "=B{row}/"+G,
  "ЦЕНЫ НЕТ. Гид, транспорт, билеты, GEM. Крупнейшая дыра в смете"),
 ("Перелёты Каир–Луксор и Асуан–Каир", 0, "на гостя",
  "=B{row}", "=B{row}",
  "ЦЕНЫ НЕТ. Групповой тариф. Места команды — на листе «Команда»"),
 ("Прочее: Khufu's, meet & greet, fast track", 0, "на гостя",
  "=B{row}", "=B{row}",
  "ЦЕНЫ НЕТ"),
 ("Резерв на решения на месте", 0, "на гостя",
  "=B{row}", "=B{row}",
  "НЕ ЗАЛОЖЕН. Обычно 2–3 % от сметы. Ваше решение"),
 ("ПРОПУЩЕННЫЕ СТАТЬИ — итог с листа «Пропущено»", "=Пропущено!$B$19", "за группу",
  "=B{row}/"+G, "=B{row}/"+G,
  "Двенадцать позиций, найденных при сверке. Пока нули"),
 ("КОМАНДА LA ROYAL", "=Команда!$B$22", "за группу",
  "=B{row}*Команда!$B$24/"+G, "=B{row}*Команда!$B$24/"+G,
  "Переключатель «в себестоимость / из вознаграждения» — на листе «Команда»"),
]
for name, price, unit, fa, fb, note in rows:
    ws.cell(r, 1, name).alignment = WRAP
    is_formula = isinstance(price, str)
    c = ws.cell(r, 2, price)
    c.fill = CALC if is_formula else INP
    c.border = BOX; c.number_format = MON
    ws.cell(r, 3, unit).font = I
    for col, f in ((4, fa), (5, fb)):
        cc = ws.cell(r, col, f.format(row=r)); cc.number_format = MON; cc.fill = CALC; cc.border = BOX
    nc = ws.cell(r, 6, note); nc.alignment = WRAP; nc.font = I
    if "ЦЕНЫ НЕТ" in note or "ПРОВЕРИТЬ" in note: nc.fill = WARN
    r += 1
end = r - 1

ws.cell(r, 1, "СЕБЕСТОИМОСТЬ НА ГОСТЯ").font = B
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"=SUM({L}{start}:{L}{end})")
    c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
cost = r; r += 1

ws.cell(r, 1, "Вознаграждение La Royal").font = B
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"={L}{cost}*{MARG}"); c.number_format = MON; c.fill = CALC; c.border = BOX
marg = r; r += 1

ws.cell(r, 1, "ЦЕНА ДЛЯ ГОСТЯ").font = Font(bold=True, size=12, color="5B46B8")
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"={L}{cost}+{L}{marg}")
    c.number_format = MON; c.fill = FIN; c.font = Font(bold=True, size=12); c.border = BOX
price_row = r; r += 1

ws.cell(r, 1, "Вознаграждение со всей группы").font = I
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"={L}{marg}*{G}-Команда!$B$22*(1-Команда!$B$24)")
    c.number_format = MON; c.fill = TOT; c.border = BOX
ws.cell(r, 6, "Если команда идёт из вознаграждения, её расходы вычитаются здесь").font = I
r += 1

ws.cell(r, 1, "Если 15 % считать долей в цене, а не наценкой").font = I
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"={L}{cost}/(1-{MARG})"); c.number_format = MON; c.fill = WARN; c.border = BOX
alt = r; r += 1
ws.cell(r, 1, "Разница между двумя трактовками, на гостя").font = I
for col in (4, 5):
    L = chr(64 + col)
    c = ws.cell(r, col, f"={L}{alt}-{L}{price_row}"); c.number_format = MON; c.fill = WARN; c.border = BOX
r += 2
ws.cell(r, 1, "Пока в столбце «Что уточнить» есть розовые строки, итог занижен и клиенту не называется.").font = Font(bold=True, color="A85CB0")

# ═══════════════ Лист 2: Команда ═══════════════
ws2 = wb.create_sheet("Команда")
for col, w in zip("ABCD", (44, 14, 6, 56)): ws2.column_dimensions[col].width = w
ws2["A1"] = "КОМАНДА LA ROYAL: СВОИ РАСХОДЫ"
ws2["A1"].font = Font(bold=True, size=13, color="5B46B8")
ws2["A2"] = ("Четыре-пять человек сопровождают группу всю поездку. На судне живут без доплаты: "
             "борт зафрахтован целиком. В Каире размещаются сами. На выезды идут не в полном составе.")
ws2["A2"].font = I

hdr(ws2, 4, ["Параметр", "Значение", "", "Комментарий"])
tp = [("Человек в команде",            4, "Всего в поездке"),
      ("Человек в номере",             2, "2 = по двое. 1 = одноместно, дороже"),
      ("Едет на выезды",               2, "Абу-Симбел и рестораны — не весь состав"),
      ("Отель в Каире, за номер",     90, "Свой отель, не Giza Palace"),
      ("Отель в Луксоре, за номер",  170, "С группой"),
      ("Four Seasons, за номер",     570, "С группой"),
      ("Питание на берегу, на чел",  120, "За всю поездку. На борту бесплатно")]
rr = 5
t0 = rr
for name, val, note in tp:
    ws2.cell(rr, 1, name).font = B
    c = ws2.cell(rr, 2, val); c.fill = INP; c.border = BOX; c.number_format = MON
    n = ws2.cell(rr, 4, note); n.alignment = WRAP; n.font = I
    rr += 1
S, PER, OUT, CAI, LUX, FSN, TF = [f"$B${t0+i}" for i in range(7)]
SR = f"ROUNDUP({S}/{PER},0)"

rr += 1
hdr(ws2, rr, ["Статья", "USD", "", "Как считается"]); rr += 1
c0 = rr
lines = [
 ("Судно", "=0", "Борт зафрахтован целиком — команда на борту без доплаты"),
 ("Каир, свой отель, 2 ночи", f"={SR}*2*{CAI}", "Номеров × 2 ночи × цена"),
 ("Луксор, 1 ночь", f"={SR}*{LUX}", "Номеров × цена"),
 ("Four Seasons, 1 ночь", f"={SR}*{FSN}", "Номеров × цена"),
 ("Абу-Симбел самолётом", f"={OUT}*470", "Летят не все"),
 ("Ужины в Lucida и Four Seasons", f"={OUT}*400", "150 + 250 на человека"),
 ("Питание на берегу", f"={S}*{TF}", "Весь состав"),
 ("Внутренние перелёты команды", "=0", "ЦЕНЫ НЕТ. Заполнить, когда придёт тариф"),
]
for name, f, note in lines:
    ws2.cell(rr, 1, name).alignment = WRAP
    c = ws2.cell(rr, 2, f); c.number_format = MON; c.fill = CALC; c.border = BOX
    n = ws2.cell(rr, 4, note); n.alignment = WRAP; n.font = I
    if "ЦЕНЫ НЕТ" in note: n.fill = WARN
    rr += 1
c1 = rr - 1
ws2.cell(rr, 1, "ИТОГО РАСХОДЫ КОМАНДЫ").font = B
c = ws2.cell(rr, 2, f"=SUM(B{c0}:B{c1})"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
total_row = rr; rr += 1
ws2.cell(rr, 1, "На одного гостя").font = B
c = ws2.cell(rr, 2, f"=B{total_row}/Калькулятор!$B$6"); c.number_format = MON; c.fill = TOT; c.border = BOX
rr += 1

ws2.cell(rr, 1, "ПЕРЕКЛЮЧАТЕЛЬ: 1 = в себестоимость, 0 = из вознаграждения").font = Font(bold=True, color="5B46B8")
c = ws2.cell(rr, 2, 1); c.fill = INP; c.border = BOX
n = ws2.cell(rr, 4, "1 — клиент платит за сопровождение, не видя отдельной строки. "
                    "0 — содержим команду из своей комиссии."); n.alignment = WRAP; n.font = I
switch_row = rr
assert total_row == 22 and switch_row == 24, (total_row, switch_row)
rr += 2
ws2.cell(rr, 1, "Рекомендация: 1. Сопровождение собственной командой — услуга, которая отличает вас "
                "от агентства с пакетом. Услуги входят в цену.").font = Font(bold=True, color="6E8F13")

# ═══════════════ Лист 3: Вопросы ═══════════════
ws3 = wb.create_sheet("Вопросы поставщикам")
for col, w in zip("ABCD", (5, 58, 26, 46)): ws3.column_dimensions[col].width = w
ws3["A1"] = "ШЕСТЬ ВОПРОСОВ, БЕЗ КОТОРЫХ СЧИТАТЬ НЕЛЬЗЯ"
ws3["A1"].font = Font(bold=True, size=13, color="5B46B8")
hdr(ws3, 3, ["№", "Вопрос", "Кому", "Сколько за этим стоит"])
qs = [
 ("«54 500 в день» — за ночь фрахта или за календарный день? Считается ли утро высадки оплачиваемым днём?",
  "Судовой оператор", "54 500, то есть 3 406 на гостя"),
 ("Наземная программа 22–25 января: гид, транспорт, билеты, GEM",
  "Принимающая компания", "Позиции в смете нет вообще"),
 ("Групповой тариф: Каир — Луксор и Асуан — Каир",
  "Билетный агент / EgyptAir", "Два рейса на всю группу"),
 ("Прощальный ужин в Four Seasons: 250 — net или ++? Минимальный счёт за приватную зону?",
  "Four Seasons", "Около 1 100 на группу"),
 ("Филе: фиксируем курс? Входит ли лодка от Шеллала? Цена ужина на острове?",
  "Мара, Egypt & Africa Travel", "Разброс 1 100 плюс неизвестная"),
 ("Групповой блок номеров на январь: Giza Palace и Steigenberger",
  "Отделы продаж отелей", "Наши 325 и 170 — из интернета, ±30 %. Письма готовы"),
]
rr = 4
for i, (q, who, money) in enumerate(qs, 1):
    ws3.cell(rr, 1, i).font = B
    ws3.cell(rr, 2, q).alignment = WRAP
    ws3.cell(rr, 3, who).alignment = WRAP
    c = ws3.cell(rr, 4, money); c.alignment = WRAP; c.fill = WARN
    ws3.row_dimensions[rr].height = 42
    rr += 1


# ═══════════════ Лист: Абу-Симбел ═══════════════
ws4 = wb.create_sheet("Абу-Симбел")
for col, w in zip("ABCD", (42, 15, 15, 52)): ws4.column_dimensions[col].width = w
ws4["A1"] = "АБУ-СИМБЕЛ: САМОЛЁТОМ ИЛИ ПО ЗЕМЛЕ"
ws4["A1"].font = Font(bold=True, size=13, color="5B46B8")
ws4["A2"] = ("Берём обязательной частью для всех. Здесь считается, во что обходится каждый способ "
             "и сколько экономит дорога.")
ws4["A2"].font = I
hdr(ws4, 4, ["Строка", "Самолётом", "По земле", "Комментарий"])
rows4 = [
 ("Стоимость перелёта, на человека", 470, 0, "470 названо поставщиком"),
 ("Автобус с гидом на день, за машину", 0, 600, "ОЦЕНКА 400–800. Нужен запрос в принимающую компанию"),
 ("Время в дороге в одну сторону", 0.7, 3.75, "Часы. 280–290 км по пустынной трассе"),
 ("Весь день занят", 0, 1, "1 = да. По земле день уходит целиком"),
]
rr = 5
r0 = rr
for name, air, road, note in rows4:
    ws4.cell(rr, 1, name).alignment = WRAP
    for col, v in ((2, air), (3, road)):
        c = ws4.cell(rr, col, v); c.fill = INP; c.border = BOX
        c.number_format = '0.00' if "Время" in name else MON
    n = ws4.cell(rr, 4, note); n.alignment = WRAP; n.font = I
    if "ОЦЕНКА" in note: n.fill = WARN
    rr += 1
rr += 1
ws4.cell(rr, 1, "На одного гостя").font = B
c = ws4.cell(rr, 2, f"=B{r0}"); c.number_format = MON; c.fill = CALC; c.border = BOX
c = ws4.cell(rr, 3, f"=C{r0+1}/Калькулятор!$B$6"); c.number_format = MON; c.fill = CALC; c.border = BOX
per = rr; rr += 1
ws4.cell(rr, 1, "ЭКОНОМИЯ ДОРОГИ, на гостя").font = B
c = ws4.cell(rr, 2, f"=B{per}-C{per}"); c.number_format = MON; c.fill = FIN; c.font = B; c.border = BOX
rr += 1
ws4.cell(rr, 1, "ЭКОНОМИЯ ДОРОГИ, на группу").font = B
c = ws4.cell(rr, 2, f"=(B{per}-C{per})*Калькулятор!$B$6"); c.number_format = MON; c.fill = FIN; c.font = B; c.border = BOX
rr += 2
ws4.cell(rr, 1, "Входные билеты в храмы одинаковы в обоих случаях и сидят в наземной программе.").font = I
rr += 1
ws4.cell(rr, 1, "ВНИМАНИЕ: по земле цена ФИКСИРОВАННАЯ за машину. Если делать это опцией, "
                "работает та же ловушка, что с шаром: чем меньше едет, тем дороже каждому.").font = Font(bold=True, color="A85CB0")


# ═══════════════ Лист: Пропущено ═══════════════
ws5 = wb.create_sheet("Пропущено")
for col, w in zip("ABCD", (48, 14, 6, 56)): ws5.column_dimensions[col].width = w
ws5["A1"] = "СТАТЬИ, НАЙДЕННЫЕ ПРИ СВЕРКЕ МАРШРУТА"
ws5["A1"].font = Font(bold=True, size=13, color="5B46B8")
ws5["A2"] = ("Прошли весь маршрут по дням и сверили с расчётом. Вот чего в нём не было. "
             "Заполняйте по мере получения цен — итог сам попадёт в себестоимость.")
ws5["A2"].font = I
hdr(ws5, 4, ["Статья", "USD за группу", "", "Почему это возникает"])
items = [
 ("Дневные номера в Асуане 29-го (вариант A)", 0,
  "Судно освобождается в 05:15, рейс в Каир днём. Между ними 18 человек с чемоданами и негде ждать"),
 ("Трансферы 29 и 30 января", 0,
  "Наземная программа посчитана только на 22–25. Асуан и Каир в конце поездки не покрыты"),
 ("Багажная машина в дни переездов", 0,
  "18 гостей — это 20+ чемоданов. В легковые машины они не входят"),
 ("Перевес багажа на внутренних рейсах", 0,
  "Норма EgyptAir 23 кг. На девятидневной поездке перевес почти гарантирован"),
 ("Русскоязычный египтолог на речную часть", 0,
  "Оператор обещает «гида» — почти наверняка англоязычного. Наш гид 25–29: каюта, питание, гонорар"),
 ("Фелюкка и остров Китченера 28-го", 0,
  "Стоит в программе, в судовой пакет не входит"),
 ("Асуан утром 30-го: обелиск, Элефантина, музей", 0,
  "Только вариант B. Билеты, гид, транспорт"),
 ("Абу-Симбел: входные билеты и автобус на месте", 0,
  "470 — это только перелёт"),
 ("Банковские комиссии и конвертация", 0,
  "Платежи в EUR и USD. Обычно 1–3 % от оборота"),
 ("Подарки и welcome-набор в номера", 0,
  "Для поездки такого уровня ожидаемо гостями"),
 ("Чаевые береговой части", 0,
  "Во фрахт входят чаевые ЭКИПАЖУ. Водители, гиды, носильщики и лодочники на берегу — отдельно"),
 ("Фото- и видеосъёмка поездки", 0,
  "Если нужна. Не обсуждалось"),
]
rr = 5
m0 = rr
for name, val, note in items:
    ws5.cell(rr, 1, name).alignment = WRAP
    c = ws5.cell(rr, 2, val); c.fill = INP; c.border = BOX; c.number_format = MON
    n = ws5.cell(rr, 4, note); n.alignment = WRAP; n.font = I
    rr += 1
m1 = rr - 1
rr += 2
ws5.cell(rr, 1, "ИТОГО ПРОПУЩЕНО").font = B
c = ws5.cell(rr, 2, f"=SUM(B{m0}:B{m1})"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
miss_total = rr
assert miss_total == 19, miss_total
rr += 1
ws5.cell(rr, 1, "На одного гостя").font = B
c = ws5.cell(rr, 2, f"=B{miss_total}/Калькулятор!$B$6"); c.number_format = MON; c.fill = TOT; c.border = BOX
rr += 2
ws5.cell(rr, 1, "Отдельно от этого списка остаются семь крупных позиций на листе «Калькулятор»: "
                "наземная программа 22–25, перелёты, ужин на Филе, гала на борту, Khufu's, "
                "meet & greet и резерв.").alignment = WRAP
ws5.cell(rr, 1).font = Font(bold=True, color="A85CB0")

wb.save("Смета_Египет_2027.xlsx")
print("saved")
