#!/usr/bin/env python3
"""Собирает производственное приложение из обвязки и сценарных карт."""
import os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CARDS = BASE

ORDER = [
    ('giza',         'Глава 1 · Код пирамид',                    'Гиза · 4 часа'),
    ('gem',          'Глава 2 · Последняя страница',             'Большой Египетский музей · 4 часа'),
    ('cairo',        'Глава 3 · Четыре руки, одно письмо',       'Исторический Каир · 4 часа'),
    ('dinner',       'Глава 4 · Последний кадр',                 'Каир или Шарм · 3 часа'),
    ('red_sea',      'Глава 5 · Ладья идёт за солнцем',          'Шарм-эль-Шейх · 8 часов'),
    ('desert',       'Глава 6 · Путь к звёздам',                 'Шарм-эль-Шейх · 6 часов'),
    ('sharm_museum', 'Глава 7 · Последняя запись археолога',     'Музей Шарм-эль-Шейха · 2,5 часа'),
    ('museum_alive', 'Глава 7б · Музей оживает',                 'Продолжение вечера · 1,5 часа'),
    ('ra',           'Глава 8 · Сокровища Ра',                   'Декорации · 90 минут'),
    ('pharaoh',      'Глава 9 · Фараон. Пропавшая экспедиция',   'Декорации · 100 минут'),
]

def demote(md):
    """Сдвигает все заголовки карты на один уровень вниз, чтобы главы встали под общий H1."""
    out = []
    for line in md.split('\n'):
        m = re.match(r'^(#{1,5}) (.*)$', line)
        if m:
            out.append('#' * (len(m.group(1)) + 1) + ' ' + m.group(2))
        else:
            out.append(line)
    return '\n'.join(out)

parts = [open(os.path.join(BASE, '_front.md'), encoding='utf-8').read()]

missing = []
toc = ['\n# Сценарные карты\n', '\n| Глава | Программа | Формат | Статус |', '|---|---|---|---|']
bodies = []
for key, title, fmt in ORDER:
    path = os.path.join(CARDS, key + '.md')
    if not os.path.exists(path):
        missing.append(key)
        toc.append(f'| {title.split("·")[0].strip()} | {title.split("·")[1].strip()} | {fmt} | карта готовится |')
        continue
    md = open(path, encoding='utf-8').read().strip()
    # убираем первый H1 карты, заменяем на единый заголовок главы
    md = re.sub(r'^#\s+.*\n', '', md, count=1).strip()
    words = len(md.split())
    toc.append(f'| {title.split("·")[0].strip()} | {title.split("·")[1].strip()} | {fmt} | готова |')
    bodies.append(f'\n\n---\n\n# {title}\n\n_{fmt}_\n\n' + demote(md))

parts.append('\n'.join(toc) + '\n')
parts.extend(bodies)
parts.append('\n\n' + open(os.path.join(BASE, '_back.md'), encoding='utf-8').read())

doc = '\n'.join(parts)
out = os.path.join(BASE, 'prilozhenie-dlya-organizatorov.md')
open(out, 'w', encoding='utf-8').write(doc)

print(f'собрано: {out}')
print(f'карт включено: {len(bodies)} из {len(ORDER)}')
if missing:
    print('не хватает:', ', '.join(missing))
print(f'слов всего: {len(doc.split())}')
print(f'размер: {os.path.getsize(out)//1024} КБ')
