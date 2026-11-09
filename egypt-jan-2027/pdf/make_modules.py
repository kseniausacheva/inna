#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собирает modules.json для приложения «Программы по дням»:
модуль «Каир» (из cairo.json — перенос откатанной программы Ксении),
четыре модуля «Нил» (вырезаны из programmes.json: речные дни четырёх программ)
и таблица готовых комбинаций «Каир N дней + Нил M ночей».

Запуск: python3 make_modules.py  → modules.json, затем python3 build_programmes.py
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
progs = json.load(io.open(os.path.join(HERE, 'programmes.json'), encoding='utf-8'))
cairo_path = os.path.join(HERE, 'cairo.json')
cairo = json.load(io.open(cairo_path, encoding='utf-8')) if os.path.exists(cairo_path) else None

CAIRO_WORDS = ('Каир', 'Гиз', 'пирамид', 'музе', 'Хан-эль', 'Khufu', 'Саккар', 'отел')

def not_cairo(items):
    return [x for x in items if not any(w in x for w in CAIRO_WORDS)]

def cut_before(days, idx, time_prefix):
    """Убирает из дня idx строки до первой строки, чьё время начинается с time_prefix."""
    rows = days[idx]['rows']
    for i, r in enumerate(rows):
        if r['time'].startswith(time_prefix):
            days[idx]['rows'] = rows[i:]
            return
    raise SystemExit('не нашёл строку %s в %s' % (time_prefix, days[idx]['label']))

FLIGHT_LINE = 'Перелёт из Каира утром дня посадки и рейс в Каир в день выезда — в комбинациях с каирским модулем; при прямом международном рейсе в Луксор или Асуан эти строки заменяются встречей в аэропорту'

def module(key, title, subtitle, intro, days, src, extra_included=(), extra_note=None):
    inc = not_cairo(src['included']) + [FLIGHT_LINE] + list(extra_included)
    ext = not_cairo(src['extra'])
    ntk = not_cairo(src['need_to_know'])
    if extra_note:
        ntk.append(extra_note)
    return {'key': key, 'title': title, 'subtitle': subtitle, 'intro': intro, 'days': days,
            'need_to_know': ntk, 'included': inc, 'extra': ext}

p1, p2, p3, p4 = progs

# ── Нил 4 ночи: понедельник — пятница (дни 2..6 программы 1) ──
d = json.loads(json.dumps(p1['days'][2:7]))
cut_before(d, 0, '≈07:00')
d[0]['label'] = 'Понедельник · Луксор'
d[0]['heading'] = 'Прилёт из Каира, Карнак, посадка'
d[0]['summary'] = 'Утренний рейс из Каира прилетает в 08:20. Посадка на судно с 12:00, поэтому Карнак смотрим до посадки, пока там свет и прохлада. При прямом рейсе в Луксор день строится так же от времени прилёта.'
nile4 = module('nile4', 'Нил 4 ночи: понедельник — пятница',
               'Из Луксора в Асуан · Soleil или Le Fayan Suites · регулярное отправление по понедельникам',
               'Классическая речная часть: Луксор, западный берег, Эдфу, Ком-Омбо, два дня в Асуане. Сетка оператора: посадка в понедельник с 12:00, ночи в Луксоре, Эдфу, Асуане и Асуане, выезд в пятницу до 08:00. Абу-Симбел по желанию ставим на утро четверга, как и оператор, тогда в пятницу вся группа летит в Каир одним утренним рейсом. До 50 гостей — Le Fayan Suites или Soleil, 70 — Soleil (35 кают по двое).',
               d, p1)

# ── Нил 3 ночи: пятница — понедельник (дни 2..5 программы 2) ──
d = json.loads(json.dumps(p2['days'][2:6]))
cut_before(d, 0, '≈06:30')
d[0]['label'] = 'Пятница · Асуан'
d[0]['heading'] = 'Прилёт из Каира, Филе, посадка'
d[0]['summary'] = 'Утренний рейс из Каира прилетает в Асуан около 08:00. До посадки в 12:00 успеваем Филе, плотину и обелиск. Абу-Симбел в этот день не помещается: его рейс уходит в 06:55, когда группа ещё летит из Каира.'
nile3 = module('nile3', 'Нил 3 ночи: пятница — понедельник',
               'Из Асуана в Луксор · Soleil или Le Fayan Suites · регулярное отправление по пятницам',
               'Самый ходовой формат на Ниле: три ночи вниз по течению, от Асуана к Луксору. Посадка в пятницу с 12:00, суббота на два храма и переход, воскресенье целиком на Луксор, выезд в понедельник до 08:00. До 40 гостей — Le Fayan Suites, больше — Soleil. День отправления из Асуана подтверждаем у оператора под дату: на его сайте одна из таблиц подписана иначе.',
               d, p2)

# ── Нил 7 ночей: понедельник — понедельник (программа 3 целиком) ──
d = json.loads(json.dumps(p3['days']))
cut_before(d, 0, '08:20')
nile7 = module('nile7', 'Нил 7 ночей: понедельник — понедельник',
               'Кольцо Луксор — Асуан — Луксор · Soleil или Le Fayan Suites · одно судно всю неделю',
               p3['intro'], d, p3)

# ── Lumière 5 ночей (программа 4 целиком) ──
d = json.loads(json.dumps(p4['days']))
lum = module('lumiere', 'Lumière 5 ночей: из Луксора в Асуан с островами',
             'Дахабия только под вашу группу · 8 кают, 16 гостей · день посадки любой',
             p4['intro'], d, p4)
lum['extra'] = [x for x in lum['extra'] if 'Каирский модуль' not in x] + \
               ['Каирский модуль 1–3 дня до посадки: см. раздел «Каир», перелёт Каир — Луксор утром дня посадки']

combos = [
    {'n': '1', 'name': 'Каир 2 дня + Нил 4 ночи', 'days': 'суббота → пятница', 'total': '7 дней', 'boat': 'Soleil или Le Fayan Suites', 'group': '30–70',
     'chain': 'Сб прилёт в Каир · Вс Гиза и квест · Пн утренний рейс в Луксор, посадка · Пт выезд, рейс в Каир и домой'},
    {'n': '2', 'name': 'Каир 3 дня + Нил 4 ночи', 'days': 'пятница → пятница', 'total': '8 дней', 'boat': 'Soleil или Le Fayan Suites', 'group': '30–70',
     'chain': 'Пт прилёт · Сб Гиза и квест · Вс Большой музей, конференция, яхта (или пустыня Эль-Файюм) · Пн рейс в Луксор, посадка · Пт выезд'},
    {'n': '3', 'name': 'Каир 2 дня + Нил 3 ночи', 'days': 'среда → понедельник', 'total': '6 дней', 'boat': 'Soleil или Le Fayan Suites', 'group': '20–70',
     'chain': 'Ср прилёт · Чт Гиза и квест · Пт утренний рейс в Асуан, Филе, посадка · Пн выезд, рейс в Каир и домой'},
    {'n': '4', 'name': 'Только Нил 7 ночей', 'days': 'понедельник → понедельник', 'total': '8 дней', 'boat': 'Soleil или Le Fayan Suites', 'group': '30–70',
     'chain': 'Пн прилёт в Луксор, посадка · неделя по кольцу без переездов · Пн выезд. Каир можно добавить 1–3 днями до посадки'},
    {'n': '5', 'name': 'Каир 0–2 дня + Lumière 5 ночей', 'days': 'любой день недели', 'total': '6–8 дней', 'boat': 'Lumière, весь борт', 'group': 'до 16',
     'chain': 'Каир по желанию · день 1 прилёт в Луксор, посадка · острова Фавза, Бесау, Хербиаб · день 6 Абу-Симбел по желанию и выезд из Асуана'},
]

out = {'cairo': cairo, 'nile': [nile4, nile3, nile7, lum], 'combos': combos}
io.open(os.path.join(HERE, 'modules.json'), 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print('modules.json:', 'Каир' if cairo else 'без Каира', '+', len(out['nile']), 'речных модулей,', sum(len(m['days']) for m in out['nile']), 'дней')
