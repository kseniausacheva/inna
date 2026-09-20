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
  "Нужно два. Ночное может быть дороже утреннего"),
 ("Абу-Симбел самолётом", 470, "на гостя",
  "=B{row}", "=B{row}",
  "Только перелёт. Билеты и транспорт на месте — отдельно"),
 ("Giza Palace, ночь", 325, "за номер за ночь",
  "=B{row}*2", "=B{row}*2",
  "Две ночи. Открытые источники 222–349. Запросить групповой тариф"),
 ("Steigenberger Nile Palace, ночь", 170, "за номер за ночь",
  "=B{row}", "=B{row}",
  "Открытые источники 120–176. Запросить групповой тариф"),
 ("Four Seasons Cairo, ночь", 570, "на гостя",
  "=B{row}", "=B{row}",
  "Названо отелем, все налоги включены"),
 ("Ужин в Four Seasons", 250, "на гостя",
  "=B{row}", "=0",
  "Net или ++? С надбавками 319. Только вариант A"),
 ("Ужин в Lucida или руфтоп", 150, "на гостя",
  "=B{row}", "=B{row}",
  "Net или ++? С надбавками 192"),
 ("Питание в отелях вне названных ресторанов", 200, "на гостя",
  "=B{row}", "=B{row}",
  "Наша оценка на всю поездку: ужин 40–60, обед 25–35"),
 ("Полёт на шаре", 2500, "за корзину",
  "=B{row}/"+G, "=B{row}/"+G,
  "Корзина на 8–12. На 16 гостей, вероятно, нужны ДВЕ"),
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
 ("Прочее: Khufu's, Абу-Симбел на месте, meet & greet, чаевые вне судна, страховка", 0, "на гостя",
  "=B{row}", "=B{row}",
  "ЦЕНЫ НЕТ"),
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
ws3["A1"] = "ВОСЕМЬ ВОПРОСОВ, БЕЗ КОТОРЫХ СЧИТАТЬ НЕЛЬЗЯ"
ws3["A1"].font = Font(bold=True, size=13, color="5B46B8")
hdr(ws3, 3, ["№", "Вопрос", "Кому", "Сколько за этим стоит"])
qs = [
 ("«54 500 в день» — за ночь фрахта или за календарный день? Считается ли утро высадки оплачиваемым днём?",
  "Судовой оператор", "54 500, то есть 3 406 на гостя"),
 ("Наземная программа 22–25 января: гид, транспорт, билеты, GEM",
  "Принимающая компания", "Позиции в смете нет вообще"),
 ("Групповой тариф: Каир — Луксор и Асуан — Каир",
  "Билетный агент / EgyptAir", "Два рейса на всю группу"),
 ("Вместимость корзины шара; сколько корзин покрывают 2 500",
  "Оператор шара", "Вероятно 5 000 вместо 2 500"),
 ("Гиза: зоны, число человек в разрешении, длительность, съёмка; ночное дороже утреннего?",
  "Подрядчик спецдоступов", "7 000 за два посещения"),
 ("Four Seasons и Lucida: 250 и 150 — net или ++? Минимальный счёт за приватную зону?",
  "Отели и ресторан", "Около 1 800 на группу"),
 ("Филе: фиксируем курс? Входит ли лодка от Шеллала? Цена ужина на острове?",
  "Мара, Egypt & Africa Travel", "Разброс 1 100 плюс неизвестная"),
 ("Групповой блок номеров на январь: Giza Palace и Steigenberger",
  "Отделы продаж отелей", "Наши 325 и 170 — из интернета, ±30 %"),
]
rr = 4
for i, (q, who, money) in enumerate(qs, 1):
    ws3.cell(rr, 1, i).font = B
    ws3.cell(rr, 2, q).alignment = WRAP
    ws3.cell(rr, 3, who).alignment = WRAP
    c = ws3.cell(rr, 4, money); c.alignment = WRAP; c.fill = WARN
    ws3.row_dimensions[rr].height = 42
    rr += 1

wb.save("Смета_Египет_2027.xlsx")
print("saved")
