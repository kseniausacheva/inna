# -*- coding: utf-8 -*-
"""Калькулятор сметы. Жёлтые ячейки — ввод, сиреневые — формулы.
Позиции, которые потребляет и команда La Royal, умножаются на (гости + команда)
и делятся на число гостей: расходы сопровождающих ложатся на цену гостя."""
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

# ═══════════ Лист 1: Калькулятор ═══════════
ws = wb.active; ws.title = "Калькулятор"
for col, w in zip("ABCDEF", (46, 13, 16, 13, 13, 50)): ws.column_dimensions[col].width = w

ws["A1"] = "СМЕТА НА ОДНОГО ГОСТЯ · Египет, январь 2027 · La Royal Event"
ws["A1"].font = Font(bold=True, size=14, color="5B46B8")
ws["A2"] = "Жёлтое меняем руками, сиреневое считается само. Цены поставщиков названы устно; цены отелей взяты из открытых источников и предложением не являются."
ws["A2"].font = I

ws["A4"] = "ИСХОДНЫЕ ДАННЫЕ"; ws["A4"].font = SUB
params = [
    ("Гостей",                       16, "чел",  "На это число делится всё"),
    ("Команда La Royal в поездке",    4, "чел",  "Их номера, перелёты и питание ложатся на цену гостя"),
    ("Команда: человек в номере",     2, "чел",  "2 = селим по двое. 1 = одноместно, дороже"),
    ("Дней фрахта, вариант A",        4, "дней", "25–29 января"),
    ("Дней фрахта, вариант B",        5, "дней", "25–30 января"),
    ("Фрахт за день, USD",        54500, "USD",  "ПРОВЕРИТЬ: за ночь фрахта или за календарный день"),
    ("Курс EUR/USD",            1.1489, "",      "На 20.09.2026. На дату платежа будет другим"),
    ("Вознаграждение La Royal",   0.15, "доля",  "Наценка на себестоимость"),
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
G, S, PER, DA, DB, DAY, RATE, MARG = [f"$B${p0+i}" for i in range(8)]
T   = f"({G}+{S})"                       # всего людей в пути
SR  = f"ROUNDUP({S}/{PER},0)"            # номеров/кают под команду

r += 1
ws.cell(r, 1, "РАСЧЁТ").font = SUB
ws.cell(r, 6, "Колонка «×» показывает, на скольких человек берётся позиция").font = I
r += 1
hdr(ws, r, ["Статья", "Цена", "Единица", "A, на гостя", "B, на гостя", "Что уточнить"]); r += 1
start = r

# (название, цена, единица, формула A, формула B, комментарий)
rows = [
 ("Фрахт судна", None, "за день",
  f"={DAY}*{DA}/{G}", f"={DAY}*{DB}/{G}",
  "ПРОВЕРИТЬ: «в день» — за ночь или за календарный день. И входят ли каюты команды"),
 ("Филе: визит и показ", 15000, "EUR за группу",
  "=B{row}*"+RATE+"/"+G, "=B{row}*"+RATE+"/"+G,
  "Договор в евро. Входит ли лодка от Шеллала"),
 ("Ужин на острове Филе", 0, "за группу",
  "=B{row}/"+G, "=B{row}/"+G,
  "ЦЕНЫ НЕТ. Плюсом к 15 000 EUR"),
 ("Гиза: приватный доступ, одно посещение", 3500, "за посещение",
  "=B{row}*2/"+G, "=B{row}*2/"+G,
  "Нужно два. Ночное может быть дороже утреннего"),
 ("Абу-Симбел самолётом", 470, "на человека",
  "=B{row}*"+T+"/"+G, "=B{row}*"+T+"/"+G,
  "Только перелёт. Билеты и транспорт на месте — отдельно"),
 ("Giza Palace, ночь", 325, "за номер за ночь",
  f"=B{{row}}*({G}*2+{SR}*2)/{G}", f"=B{{row}}*({G}*2+{SR}*2)/{G}",
  "Открытые источники 222–349. Запросить групповой тариф"),
 ("Steigenberger Nile Palace, ночь", 170, "за номер за ночь",
  f"=B{{row}}*({G}+{SR})/{G}", f"=B{{row}}*({G}+{SR})/{G}",
  "Открытые источники 120–176. Запросить групповой тариф"),
 ("Four Seasons Cairo, ночь", 570, "на человека",
  f"=B{{row}}*({G}+{SR})/{G}", f"=B{{row}}*({G}+{SR})/{G}",
  "Названо отелем, все налоги включены"),
 ("Ужин в Four Seasons", 250, "на человека",
  "=B{row}*"+T+"/"+G, "=0",
  "Net или ++? С надбавками 319. Только вариант A"),
 ("Ужин в Lucida или руфтоп", 150, "на человека",
  "=B{row}*"+T+"/"+G, "=B{row}*"+T+"/"+G,
  "Net или ++? С надбавками 192"),
 ("Питание в отелях вне названных ресторанов", 200, "на человека",
  "=B{row}*"+T+"/"+G, "=B{row}*"+T+"/"+G,
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
  "ЦЕНЫ НЕТ. Гид, транспорт, билеты, GEM на 20 человек. Крупнейшая дыра"),
 ("Перелёты Каир–Луксор и Асуан–Каир", 0, "на человека",
  "=B{row}*"+T+"/"+G, "=B{row}*"+T+"/"+G,
  "ЦЕНЫ НЕТ. Групповой тариф на 20 мест"),
 ("Прочее: Khufu's, Абу-Симбел на месте, meet & greet, чаевые вне судна, страховка", 0, "на человека",
  "=B{row}*"+T+"/"+G, "=B{row}*"+T+"/"+G,
  "ЦЕНЫ НЕТ"),
]
for name, price, unit, fa, fb, note in rows:
    ws.cell(r, 1, name).alignment = WRAP
    c = ws.cell(r, 2, f"={DAY}" if price is None else price)
    c.fill = CALC if price is None else INP
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
r += 1
ws.cell(r, 1, "Расходы команды La Royal сидят в СЕБЕСТОИМОСТИ, а не в вознаграждении. Иначе 15 % съедаются на четверть.").font = Font(bold=True, color="A85CB0")

# ═══════════ Лист 2: Команда ═══════════
ws2 = wb.create_sheet("Команда и каюты")
for col, w in zip("ABCD", (46, 15, 15, 52)): ws2.column_dimensions[col].width = w
ws2["A1"] = "КОМАНДА LA ROYAL: СКОЛЬКО СТОИТ И СКОЛЬКО КАЮТ"
ws2["A1"].font = Font(bold=True, size=13, color="5B46B8")
ws2["A2"] = "Четыре-пять человек сопровождают группу всю поездку. Для клиента это главное отличие от турпакета, для сметы — отдельная строка."
ws2["A2"].font = I
hdr(ws2, 4, ["Показатель", "Значение", "", "Комментарий"])
items = [
 ("Гостей", f"=Калькулятор!{G}", ""),
 ("Команда La Royal", f"=Калькулятор!{S}", ""),
 ("Всего человек в пути", f"=Калькулятор!{G}+Калькулятор!{S}", "Столько мест в самолётах и столько ртов"),
 ("Кают и номеров под команду", f"=ROUNDUP(Калькулятор!{S}/Калькулятор!{PER},0)", "При размещении по двое"),
 ("ВСЕГО КАЮТ НА СУДНЕ", f"=Калькулятор!{G}+ROUNDUP(Калькулятор!{S}/Калькулятор!{PER},0)",
  "Гости одноместно + команда. ЭТО ТРЕБОВАНИЕ К БОРТУ"),
 ("Номера: Giza Palace 2 ночи", f"=ROUNDUP(Калькулятор!{S}/Калькулятор!{PER},0)*2*325", ""),
 ("Номера: Луксор 1 ночь", f"=ROUNDUP(Калькулятор!{S}/Калькулятор!{PER},0)*170", ""),
 ("Номера: Four Seasons 1 ночь", f"=ROUNDUP(Калькулятор!{S}/Калькулятор!{PER},0)*570", ""),
 ("Абу-Симбел самолётом", f"=Калькулятор!{S}*470", ""),
 ("Ужины Lucida и Four Seasons", f"=Калькулятор!{S}*400", ""),
 ("Питание в отелях", f"=Калькулятор!{S}*200", ""),
]
rr = 5
for name, f, note in items:
    ws2.cell(rr, 1, name).font = B if "ВСЕГО" in name else Font()
    c = ws2.cell(rr, 2, f); c.border = BOX
    c.number_format = MON
    c.fill = FIN if "ВСЕГО" in name else CALC
    nc = ws2.cell(rr, 4, note); nc.alignment = WRAP; nc.font = I
    if "ТРЕБОВАНИЕ" in note: nc.fill = WARN
    rr += 1
ws2.cell(rr, 1, "ИТОГО расходы на команду, USD").font = B
c = ws2.cell(rr, 2, f"=SUM(B{rr-6}:B{rr-1})"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
rr += 1
ws2.cell(rr, 1, "На одного гостя").font = B
c = ws2.cell(rr, 2, f"=B{rr-1}/Калькулятор!{G}"); c.number_format = MON; c.fill = TOT; c.font = B; c.border = BOX
rr += 2
ws2.cell(rr, 1, "Внутренние перелёты команды сюда не входят: цены пока нет.").font = Font(bold=True, color="A85CB0")

# ═══════════ Лист 3: Вопросы ═══════════
ws3 = wb.create_sheet("Вопросы поставщикам")
for col, w in zip("ABCD", (5, 58, 26, 46)): ws3.column_dimensions[col].width = w
ws3["A1"] = "ДЕВЯТЬ ВОПРОСОВ, БЕЗ КОТОРЫХ СЧИТАТЬ НЕЛЬЗЯ"
ws3["A1"].font = Font(bold=True, size=13, color="5B46B8")
hdr(ws3, 3, ["№", "Вопрос", "Кому", "Сколько за этим стоит"])
qs = [
 ("«54 500 в день» — за ночь фрахта или за календарный день? Считается ли утро высадки оплачиваемым днём?",
  "Судовой оператор", "54 500, то есть 3 406 на гостя"),
 ("18–19 кают при 16 гостях и 21 при 18. Входят ли каюты и питание 4–5 сопровождающих в цену или это доплата?",
  "Судовой оператор", "Определяет, какие борта вообще подходят"),
 ("Наземная программа 22–25 января на 20 человек: гид, транспорт, билеты, GEM",
  "Принимающая компания", "Позиции в смете нет вообще"),
 ("Групповой тариф на 20 мест: Каир — Луксор и Асуан — Каир",
  "Билетный агент / EgyptAir", "Три рейса × 20 мест"),
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
