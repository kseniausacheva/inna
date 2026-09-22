# -*- coding: utf-8 -*-
"""Единственный источник цифр сметы.

Меняешь цену здесь — она меняется в клиентском предложении, во внутренней смете
и в таблице размеров группы одновременно. Раньше числа лежали в трёх файлах
руками и разошлись: строки клиентской таблицы давали 302 064, а в итоге
стояло 303 504.

Правило структуры: то, что оплачивается за группу, лежит в GROUP; то, что
по головам, — в PERHEAD. Команда La Royal потребляет те же позиции, что и гость,
и идёт одной строкой, а не растворяется в строках гостей.
"""
import math

GUESTS = 16
TEAM_GROUND = 2        # человек команды, которые потребляют платные позиции наравне с гостями
FEE = 0.15             # вознаграждение La Royal, наценка на себестоимость
EUR_USD = 1.14893      # курс, по которому переведены 15 000 EUR за Филе

# ─────────── за группу целиком ───────────
CHARTER_DAY   = 54_500
NIGHTS        = {'A': 4, 'B': 5}
PHILAE_EUR    = 15_000
GIZA_OPENING  = 3_500          # за один приватный вход, их два
ENSEMBLE      = 650
BASKET        = 2_500          # корзина шара, до 8 человек

# ─────────── на человека ───────────
GIZA_PALACE   = 325            # за ночь, две ночи
SONESTA       = 222            # Sonesta St. George Luxor, single BB, письмо отеля 22.09
ASWAN_29      = 250            # вариант A, остров Элефантина
FOURSEASONS   = 570            # вариант B, ночь 30 января
ABU_SIMBEL    = 470
GIZA_TICKET   = 180            # за посещение, их два
FLIGHTS       = 250            # два внутренних перелёта
FAREWELL      = 250            # вариант A; в B ужин на борту и денег не стоит
HOTEL_MEALS   = 200            # питание в отелях вне названных ресторанов, за всю поездку
LUCIDA        = 150
PHILAE_DINNER = 150
GEM           = 120
KHUFU         = 90
TEAM_OWN_ROOM = 90             # свой отель в Каире, за ночь, две ночи
TEAM_MEALS    = 240            # питание команды на берегу


def baskets(people):
    """Корзин шара: в одну помещается восемь человек."""
    return math.ceil(people / 8)


def group_fixed(v, n=GUESTS):
    """Позиции, которые стоят одинаково при любом числе гостей."""
    return {
        'charter':  CHARTER_DAY * NIGHTS[v],
        'philae':   round(PHILAE_EUR * EUR_USD),
        'giza_open': GIZA_OPENING * 2,
        'balloon':  BASKET * baskets(n),
        'ensemble': ENSEMBLE,
    }


def per_head(v):
    """Стоимость одного человека — что гостя, что члена команды на берегу."""
    d = {
        'giza_palace': GIZA_PALACE * 2,
        'sonesta':     SONESTA,
        'abu_simbel':  ABU_SIMBEL,
        'giza_ticket': GIZA_TICKET * 2,
        'flights':     FLIGHTS,
        'hotel_meals': HOTEL_MEALS,
        'lucida':      LUCIDA,
        'philae_din':  PHILAE_DINNER,
        'gem':         GEM,
        'khufu':       KHUFU,
    }
    if v == 'A':
        d['hotel_29'] = ASWAN_29
        d['farewell'] = FAREWELL
    else:
        d['hotel_30'] = FOURSEASONS
        d['farewell'] = 0
    return d


def team(v):
    """Команда: свой отель в Каире и питание на берегу вместо гостевых,
    всё остальное — как у гостя. Абу-Симбел: летят не все, считаем двоих."""
    p = per_head(v)
    one = (TEAM_OWN_ROOM * 2 + TEAM_MEALS
           + p['sonesta'] + p.get('hotel_29', 0) + p.get('hotel_30', 0)
           + p['abu_simbel'] + p['giza_ticket'] + p['flights'] + p['farewell']
           + p['lucida'] + p['philae_din'] + p['gem'] + p['khufu'])
    return one


def total(v, n=GUESTS, team_n=TEAM_GROUND, charter_day=None):
    """Себестоимость для клиента. Расходы нашей команды сюда НЕ входят:
    это наши расходы, и они покрываются из вознаграждения."""
    g = group_fixed(v, n)
    if charter_day is not None:
        g['charter'] = charter_day * NIGHTS[v]
    return sum(g.values()) + sum(per_head(v).values()) * n


def our_costs(v, team_n=TEAM_GROUND):
    """Что поездка стоит нам самим: содержание команды на месте."""
    return team(v) * team_n


def net_fee(v, n=GUESTS, team_n=TEAM_GROUND):
    """Что остаётся нам после содержания команды."""
    return with_fee(total(v, n)) - total(v, n) - our_costs(v, team_n)


def with_fee(cost):
    return round(cost * (1 + FEE))


def ru(x):
    """1234567 → '1 234 567' с неразрывными пробелами."""
    return '{:,}'.format(int(round(x))).replace(',', '\u00a0')


# ─────────── строки клиентской таблицы ───────────
# (заголовок, сумма A, сумма B, статус, комментарий)
def client_rows(n=GUESTS, team_n=TEAM_GROUND):
    ga, gb = group_fixed('A', n), group_fixed('B', n)
    pa, pb = per_head('A'), per_head('B')
    R = []
    add = lambda *a: R.append(a)
    add('<b>Частный фрахт судна</b>, 4 или 5 ночей', ga['charter'], gb['charter'], '~',
        'Названо оператором. Экипаж, полный пансион, напитки, гид, портовые сборы')
    add('<b>Приватный вечер на острове Филе</b>', ga['philae'], gb['philae'], '✓',
        'Подтверждено письменно. 15 000 EUR')
    add('Отель в Каире, 2 ночи', pa['giza_palace'] * n, pb['giza_palace'] * n, '≈',
        'Giza Palace. Групповой тариф запрошен')
    add('Абу-Симбел самолётом', pa['abu_simbel'] * n, pb['abu_simbel'] * n, '~',
        'Уточняем, что входит кроме перелёта')
    add('<b>Плато Гизы</b>, два приватных открытия для группы', ga['giza_open'], gb['giza_open'], '✓',
        'Персональное разрешение и доступ во все зоны. По 3 500 за визит')
    add('Входные билеты на плато, два посещения', pa['giza_ticket'] * n, pb['giza_ticket'] * n, '✓',
        '180 за билет на человека, оплачиваются сверх открытия')
    add('Полёт на шаре, две корзины', ga['balloon'], gb['balloon'], '✓',
        'Названо оператором. В корзину помещается восемь человек')
    add('Отель 29 января (A) или 30 января (B)', pa['hotel_29'] * n, pb['hotel_30'] * n, '≈',
        'A: остров Элефантина, Асуан. B: Four Seasons, 570 названо отелем')
    add('Внутренние перелёты', pa['flights'] * n, pb['flights'] * n, '≈',
        'По открытым тарифам. Групповой запрошен')
    add('Прощальный ужин', pa['farewell'] * n, None, '~',
        'A: площадка в Асуане. B: верхняя палуба судна, входит во фрахт')
    add('<b>Отель в Луксоре</b>, 1 ночь', pa['sonesta'] * n, pb['sonesta'] * n, '✓',
        'Sonesta St. George. 222 за номер, завтрак, сервис и НДС включены')
    add('Питание в отелях вне названных ресторанов', pa['hotel_meals'] * n, pb['hotel_meals'] * n, '≈',
        'Ужин 40–60, обед 25–35 на человека')
    add('Ужин в Lucida', pa['lucida'] * n, pb['lucida'] * n, '✓',
    'Подтверждено. Включены два бокала вина или пива на человека')
    add('Ужин на острове Филе', pa['philae_din'] * n, pb['philae_din'] * n, '≈',
        '150 на человека, сверх приватного вечера')
    add('Большой Египетский музей, индивидуальная экскурсия', pa['gem'] * n, pb['gem'] * n, '✓',
        '120 на человека, с трансфером')
    add('Завтрак в Khufu’s у пирамиды', pa['khufu'] * n, pb['khufu'] * n, '✓', '90 на человека')
    add('Живая музыка на прощальном вечере', ga['ensemble'], gb['ensemble'], '≈', 'Запрошено')
    R.sort(key=lambda r: -(r[1] or 0))
    return R


if __name__ == '__main__':
    for v in ('A', 'B'):
        c = total(v)
        print('Вариант %s: клиенту %s (себестоимость %s), на гостя %s'
              % (v, ru(with_fee(c)), ru(c), ru(with_fee(c) / GUESTS)))
        print('   наши расходы на команду %s, чистое вознаграждение %s'
              % (ru(our_costs(v)), ru(net_fee(v))))
    rows = client_rows()
    sa = sum(r[1] or 0 for r in rows)
    sb = sum(r[2] or 0 for r in rows)
    print('сумма строк таблицы: A %s  B %s' % (ru(sa), ru(sb)))
    assert sa == total('A') and sb == total('B'), 'таблица не сходится с итогом'
    print('таблица сходится')
    for n in (16, 20, 30):
        c = total('A', n, team_n=2 if n < 30 else 3)
        print('  %d гостей: кают %d, всего %s, на гостя %s'
              % (n, n + (2 if n < 30 else 3), ru(with_fee(c)), ru(with_fee(c) / n)))
