# -*- coding: utf-8 -*-
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
H   = Font(bold=True, size=11, color="FFFFFF")
HF  = PatternFill("solid", fgColor="5B46B8")
SUB = Font(bold=True, size=11, color="5B46B8")
INP = PatternFill("solid", fgColor="FFF2CC")   # жёлтый = вводим руками
CALC= PatternFill("solid", fgColor="EFECFB")   # сиреневый = формула
TOT = PatternFill("solid", fgColor="C3E850")
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

# ─────────── Лист 1: Калькулятор ───────────
ws = wb.active; ws.title = "Калькулятор"
for col, w in zip("ABCDEF", (44, 14, 14, 14, 13, 52)): ws.column_dimensions[col].width = w

ws["A1"] = "СМЕТА НА ОДНОГО ГОСТЯ · Египет, январь 2027 · La Royal Event"
ws["A1"].font = Font(bold=True, size=14, color="5B46B8")
ws["A2"] = "Жёлтые ячейки меняем руками. Всё остальное считается формулами. Цены названы поставщиками устно и требуют письменного подтверждения."
ws["A2"].font = I

ws["A4"] = "ИСХОДНЫЕ ДАННЫЕ"; ws["A4"].font = SUB
base = [
    ("Число гостей",                    16,    "чел",   "Фрахт делится на это число"),
    ("Дней фрахта, вариант A",           4,    "дней",  "25–29 января, четыре ночи"),
    ("Дней фрахта, вариант B",           5,    "дней",  "25–30 января, пять ночей"),
    ("Цена фрахта за день, USD",     54500,    "USD",   "ВКЛЮЧАЕТ налоги, чаевые, питание, напитки, гида, билеты — со слов оператора"),
    ("Курс EUR/USD",                1.1489,    "",      "Курс на 20.09.2026. На дату платежа будет другим"),
]
r = 5
hdr(ws, r, ["Параметр", "Значение", "Ед.", "", "", "Комментарий"]); r += 1
first_input = r
for name, val, unit, note in base:
    ws.cell(r, 1, name).font = B
    c = ws.cell(r, 2, val); c.fill = INP; c.border = BOX
    c.number_format = '0.0000' if name.startswith("Курс") else MON
    ws.cell(r, 3, unit)
    ws.cell(r, 6, note).alignment = WRAP; ws.cell(r, 6).font = I
    r += 1
N, DA, DB, DAY, RATE = [f"$B${first_input+i}" for i in range(5)]

r += 1
ws.cell(r, 1, "РАСЧЁТ ПО НАЗВАННЫМ ЦЕНАМ").font = SUB; r += 1
hdr(ws, r, ["Статья", "Цена", "Единица", "Вариант A, на гостя", "Вариант B, на гостя", "Что уточнить"]); r += 1
start = r

rows = [
    ("Фрахт судна", None, "за день",
     f"={DAY}*{DA}/{N}", f"={DAY}*{DB}/{N}",
     "«В день» — за ночь фрахта или за календарный день? Разница 54 500"),
    ("Филе: приватный визит и показ", 15000, "EUR за группу",
     "=B{row}*"+RATE+"/"+N, "=B{row}*"+RATE+"/"+N,
     "Договор в евро. Входит ли моторная лодка от Шеллала"),
    ("Ужин на острове Филе", 0, "за группу",
     "=B{row}/"+N, "=B{row}/"+N,
     "ЦЕНА НЕ НАЗВАНА. Плюсом к 15 000 EUR. Запросить у Мары"),
    ("Гиза: приватный доступ, одно посещение", 3500, "за посещение",
     "=B{row}*2/"+N, "=B{row}*2/"+N,
     "Нужно ДВА: до открытия и ночью. Ночное может стоить дороже"),
    ("Ужин в Four Seasons", 250, "на человека",
     "=B{row}", "=0",
     "Net или ++? С 12% сервиса и 14% НДС будет 319. Только вариант A"),
    ("Ужин в Lucida или руфтоп", 150, "на человека",
     "=B{row}", "=B{row}",
     "Net или ++? С надбавками будет 192"),
    ("Полёт на шаре", 2500, "за корзину",
     "=B{row}/"+N, "=B{row}/"+N,
     "Корзина вмещает 8–12. На 16 гостей, вероятно, нужны ДВЕ"),
    ("Гала-ужин на борту, вариант B", 0, "за группу",
     "=0", "=B{row}/"+N,
     "ЦЕНА НЕ НАЗВАНА. Меню, декор, музыка сверх пансиона"),
    ("Наземная программа 22–25 января", 0, "за группу",
     "=B{row}/"+N, "=B{row}/"+N,
     "ЦЕНА НЕ НАЗВАНА. Гид, транспорт, билеты, GEM до посадки на судно"),
    ("Отели: Giza Palace, Steigenberger, Four Seasons", 0, "за группу",
     "=B{row}/"+N, "=B{row}/"+N,
     "ЦЕНА НЕ НАЗВАНА. 18 номеров × 4 ночи суммарно"),
    ("Внутренние перелёты", 0, "на человека",
     "=B{row}", "=B{row}",
     "ЦЕНА НЕ НАЗВАНА. CAI–LXR, ASW–ABS–ASW, ASW–CAI"),
    ("Прочее: Khufu's, Абу-Симбел на месте, meet & greet, чаевые вне судна", 0, "на человека",
     "=B{row}", "=B{row}",
     "ЦЕНА НЕ НАЗВАНА"),
]
for name, price, unit, fa, fb, note in rows:
    ws.cell(r, 1, name).alignment = WRAP
    if price is None:
        c = ws.cell(r, 2, f"={DAY}"); c.fill = CALC
    else:
        c = ws.cell(r, 2, price); c.fill = INP
    c.border = BOX; c.number_format = MON
    ws.cell(r, 3, unit).font = I
    for col, f in ((4, fa), (5, fb)):
        cc = ws.cell(r, col, f.format(row=r)); cc.number_format = MON; cc.fill = CALC; cc.border = BOX
    nc = ws.cell(r, 6, note); nc.alignment = WRAP; nc.font = I
    if "НЕ НАЗВАНА" in note: nc.fill = WARN
    r += 1
end = r - 1

ws.cell(r, 1, "СЕБЕСТОИМОСТЬ НА ГОСТЯ").font = B
for col in (4, 5):
    c = ws.cell(r, col, f"=SUM({chr(64+col)}{start}:{chr(64+col)}{end})")
    c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
cost_row = r; r += 1

ws.cell(r, 1, "Вознаграждение La Royal, %").font = B
m = ws.cell(r, 2, 0.15); m.fill = INP; m.number_format = '0%'; m.border = BOX
for col in (4, 5):
    c = ws.cell(r, col, f"={chr(64+col)}{cost_row}*$B${r}")
    c.number_format = MON; c.fill = CALC; c.border = BOX
marg_row = r; r += 1

ws.cell(r, 1, "ЦЕНА ДЛЯ КЛИЕНТА НА ГОСТЯ").font = Font(bold=True, size=12, color="5B46B8")
for col in (4, 5):
    c = ws.cell(r, col, f"={chr(64+col)}{cost_row}+{chr(64+col)}{marg_row}")
    c.number_format = MON; c.fill = TOT; c.font = Font(bold=True, size=12); c.border = BOX
r += 2
ws.cell(r, 1, "ВНИМАНИЕ: пока в столбце «Что уточнить» есть розовые строки, итог занижен и клиенту не называется.").font = Font(bold=True, color="A85CB0")

# ─────────── Лист 2: Чувствительность ───────────
ws2 = wb.create_sheet("Чувствительность")
for col, w in zip("ABCDE", (40, 15, 15, 15, 15)): ws2.column_dimensions[col].width = w
ws2["A1"] = "КАК ЦЕНА МЕНЯЕТСЯ ОТ ЧИСЛА ГОСТЕЙ"; ws2["A1"].font = Font(bold=True, size=13, color="5B46B8")
ws2["A2"] = "Только по названным ценам. Фрахт — фиксированная сумма, поэтому каждый недобравшийся гость дорожает поездку для остальных."
ws2["A2"].font = I
hdr(ws2, 4, ["Число гостей", "14", "16", "18", ""])
labels = [("Фрахт, вариант A", "=Калькулятор!$B$9*Калькулятор!$B$7/{n}"),
          ("Фрахт, вариант B", "=Калькулятор!$B$9*Калькулятор!$B$8/{n}"),
          ("Филе, визит и показ", "=15000*Калькулятор!$B$10/{n}"),
          ("Гиза, два посещения", "=7000/{n}"),
          ("Шар, одна корзина", "=2500/{n}")]
rr = 5
for name, f in labels:
    ws2.cell(rr, 1, name)
    for col, n in ((2, 14), (3, 16), (4, 18)):
        c = ws2.cell(rr, col, f.format(n=n)); c.number_format = MON; c.fill = CALC; c.border = BOX
    rr += 1
ws2.cell(rr, 1, "Итого по известному, вариант A").font = B
for col in (2, 3, 4):
    L = chr(64 + col)
    c = ws2.cell(rr, col, f"={L}5+{L}7+{L}8+{L}9+250+150"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
ra = rr; rr += 1
ws2.cell(rr, 1, "Итого по известному, вариант B").font = B
for col in (2, 3, 4):
    L = chr(64 + col)
    c = ws2.cell(rr, col, f"={L}6+{L}7+{L}8+{L}9+150"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
rb = rr; rr += 2
ws2.cell(rr, 1, "Разница между 18 и 14 гостями, вариант A").font = B
c = ws2.cell(rr, 2, f"=B{ra}-D{ra}"); c.number_format = MON; c.fill = WARN; c.border = BOX
rr += 1
ws2.cell(rr, 1, "Цена пятого дня на гостя при 16").font = B
c = ws2.cell(rr, 2, f"=C{rb}-C{ra}"); c.number_format = MON; c.fill = WARN; c.border = BOX

# ─────────── Лист 3: Вопросы ───────────
ws3 = wb.create_sheet("Вопросы поставщикам")
for col, w in zip("ABCD", (6, 56, 26, 60)): ws3.column_dimensions[col].width = w
ws3["A1"] = "СЕМЬ ВОПРОСОВ, БЕЗ КОТОРЫХ СЧИТАТЬ НЕЛЬЗЯ"; ws3["A1"].font = Font(bold=True, size=13, color="5B46B8")
hdr(ws3, 3, ["№", "Вопрос", "Кому", "Сколько денег за этим стоит"])
qs = [
 ("«54 500 в день» — за ночь фрахта или за календарный день? Считается ли утро высадки оплачиваемым днём?",
  "Судовой оператор", "54 500 USD, то есть 3 406 на гостя при 16"),
 ("Входят ли береговые экскурсии: транспорт, сопровождение, носильщики? И отдельно: дни 22–25 января до посадки в фрахт не входят вовсе",
  "Судовой оператор + принимающая компания", "Отдельная строка на 4 дня × 18 человек, сейчас её в смете нет"),
 ("Вместимость корзины шара; сколько корзин покрывают 2 500; летят ли корзины вместе",
  "Оператор шара", "Вероятно 5 000 вместо 2 500: +156 на гостя"),
 ("Гиза: какие зоны, на сколько человек разрешение, длительность окна, съёмка; ночное посещение дороже утреннего?",
  "Подрядчик спецдоступов", "3 500 за посещение, двух посещений — 7 000"),
 ("Four Seasons и Lucida: цена net или ++ (12 % сервис, 14 % НДС)? Есть ли минимальный счёт за приватную зону сверх меню?",
  "Отели и ресторан", "250→319 и 150→192: около 1 800 на группу"),
 ("Филе: фиксируем ли курс EUR/USD; входит ли моторная лодка от Шеллала; цена ужина на острове",
  "Мара, Egypt & Africa Travel", "Валютный разброс 1 100 на группу + цена ужина"),
 ("Что именно входит в «напитки включены»: алкоголь или только безалкогольные?",
  "Судовой оператор", "Тысячи долларов на 5 днях и 16 гостях"),
]
rr = 4
for i, (q, who, money) in enumerate(qs, 1):
    ws3.cell(rr, 1, i).font = B
    ws3.cell(rr, 2, q).alignment = WRAP
    ws3.cell(rr, 3, who).alignment = WRAP
    c = ws3.cell(rr, 4, money); c.alignment = WRAP; c.fill = WARN
    ws3.row_dimensions[rr].height = 44
    rr += 1

wb.save("Смета_Египет_2027.xlsx")
print("saved")
