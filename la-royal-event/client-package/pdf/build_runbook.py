# -*- coding: utf-8 -*-
"""Подробная механика Гизы для команды. Один источник, два языка."""
import html, pathlib

def T(ru, en): return {"ru": ru, "en": en}
def esc(s): return html.escape(s, quote=False)

L = "ru"
def t(x): return esc(x[L]) if isinstance(x, dict) else esc(x)
def raw(x): return x[L] if isinstance(x, dict) else x

# ---------- блоки ----------
def h2(x): return f'<h2>{t(x)}</h2>'
def eyebrow(x): return f'<div class="mono eyebrow">{t(x)}</div>'
def p(x): return f'<p>{raw(x) if isinstance(x,dict) else x}</p>'
def ul(items): return '<ul>' + ''.join(f'<li>{raw(i)}</li>' for i in items) + '</ul>'
def ol(items): return '<ol>' + ''.join(f'<li>{raw(i)}</li>' for i in items) + '</ol>'
def table(head, rows):
    h = '<tr>' + ''.join(f'<th>{t(c)}</th>' for c in head) + '</tr>' if head else ''
    r = ''.join('<tr>' + ''.join(f'<td>{raw(c)}</td>' for c in row) + '</tr>' for row in rows)
    return f'<table>{h}{r}</table>'
def box(label, inner, kind=""):
    lab = f'<div class="mono lbl">{t(label)}</div>' if label else ''
    return f'<div class="box {kind}">{lab}{inner}</div>'
def warn(label, inner): return box(label, inner, "warn")
def dark(label, inner): return box(label, inner, "dark")
def say(who, line):
    return (f'<div class="say"><span class="who">{t(who)}</span>'
            f'<span class="line">«{raw(line)}»</span></div>')
def steps(rows):
    return '<div class="mins">' + ''.join(
        f'<div class="m"><span class="tm">{t(a)}</span><span class="tx">{raw(b)}</span></div>'
        for a, b in rows) + '</div>'

# ---------- содержание ----------
def build():
    P = []

    # 1. обложка
    P.append(('cover', f'''
  <div>
    <div class="mono">{t(T("La Royal Event · плато Гиза · только для команды","La Royal Event · Giza plateau · staff only"))}</div>
    <h1>{t(T("Код пирамид","Code of the Pyramids"))}</h1>
    <p class="lead">{t(T("Подробная механика для команды. Что делает каждый человек, минута за минутой, с готовыми репликами. Здесь есть ответы и код замка.","Full run-book for the team. What each person does, minute by minute, with scripted lines. It contains the answers and the lock code."))}</p>
    <div class="strip">
      <div><b>4 {t(T("часа","hours"))}</b><span>{t(T("на плато","on the plateau"))}</span></div>
      <div><b>30</b><span>{t(T("гостей, 6 команд","guests, 6 teams"))}</span></div>
      <div><b>3 {t(T("потока","flows"))}</b><span>{t(T("по 10 человек","of 10 guests"))}</span></div>
      <div><b>10</b><span>{t(T("человек штата","staff on duty"))}</span></div>
    </div>
  </div>
  <div class="foot"><span>{t(T("Ксения Усачёва · La Royal Event","Kseniia Usacheva · La Royal Event"))}</span><span>{t(T("Гостям и подрядчикам не отдаём","Never handed to guests or contractors"))}</span></div>'''))

    # 2. суть + ответы
    P.append(('', eyebrow(T("1 · Суть игры","1 · What the game is"))
      + h2(T("Проверить можно только то, что стоит перед глазами","Only what stands in front of you can be counted"))
      + p(T("Гостям выдают полевой дневник археолога. В нём двенадцать страниц: шесть настоящих и шесть переписанных человеком, который на плато не был. На шести точках команды проверяют написанное собственными глазами. Четыре наблюдения дают число, два не дают. Числа открывают замок.",
            "Guests are given an archaeologist's field diary. It holds twelve pages: six genuine and six rewritten by someone who never stood on the plateau. At six stops the teams check what is written against what they can see. Four observations produce a number, two do not. The numbers open the lock."))
      + warn(T("Ответы. Вслух до финала не произносим","The answers. Never said aloud before the closing session"),
          p(T("<b>Код замка: 2 – 2 – 3 – 4.</b> Числа выстраиваются от меньшего к большему.",
              "<b>Lock code: 2 – 2 – 3 – 4.</b> The numbers are ordered from smallest to largest."))
        + p(T("<b>Признак подделки:</b> настоящие страницы называют стороны света: «северная грань», «у восточной грани». Поддельные пишут «справа от входа», «слева по дороге». Человек, который не стоял на месте, описывает картинку, а не местность.",
              "<b>How the forgery shows:</b> genuine pages name compass directions, \"the north face\", \"by the east face\". The forged ones say \"to the right of the entrance\", \"on the left along the road\". Someone who was never there describes a picture, not a place."))
        + p(T("<b>Второй признак:</b> настоящие страницы никогда не называют число. Поддельные называют, и всегда неверное.",
              "<b>Second tell:</b> genuine pages never state a number. Forged ones always do, and always wrongly."))
        + p(T("<b>Кто переписывал:</b> курьер, который утром сам передаёт группе ларец и едет с ней весь день. Ему нужен не ларец, а бумага с подписями тридцати человек, заверяющая его версию маршрута.",
              "<b>Who rewrote it:</b> the courier who hands the group the lock box in the morning and stays with them all day. He does not want the box. He wants a sheet of paper signed by thirty people that certifies his version of the route.")))
      + eyebrow(T("2 · Кто работает в смене","2 · Who works the shift"))
      + table([T("Кто","Who"), T("Чей","Whose"), T("Что делает","What they do")], [
          [T("Ведущая","Lead host"), T("наш","ours"), T("Ведёт весь день. Пролог, правила, сигналы смены станций, финал, замок, номинации. Старшая на маршруте.","Runs the day. Prologue, rules, stop-change signals, closing session, the lock, the awards. Senior on the route.")],
          [T("Помощники, 3","Assistants, 3"), T("наши","ours"), T("По одному на две команды. Читают задание, держат время, принимают ставки, выдают конверты, ставят печати, снимают фото.","One per two teams. Read the task, keep time, take the bets, hand out envelopes, apply the stamps, take photographs.")],
          [T("Координатор","Coordinator"), T("наш","ours"), T("Автобус, вода, туалеты, площадка финала, печать листов в дороге. Он же играет курьера.","Coach, water, toilets, closing venue, printing on the move. He also plays the courier.")],
          [T("Гиды, 3","Guides, 3"), T("партнёр","partner"), T("По одному на поток. Ведут историю. Объясняют только после ставки команды.","One per flow. They carry the history. They explain only after the team has bet.")],
          [T("Координатор площадки","Site coordinator"), T("партнёр","partner"), T("Билеты, проход, стоянки автобуса, связь с администрацией плато.","Tickets, entry, coach standing points, liaison with the plateau administration.")],
      ])
      + p(T("<b>Актёры не обязательны.</b> В базовой версии курьера играет координатор: он ничего не изображает, просто дважды произносит написанный текст. Отдельный актёр покупает подачу, а не развязку.",
            "<b>Actors are optional.</b> In the base version the coordinator plays the courier. He acts nothing out, he simply delivers two written lines. A hired actor buys presentation, not the plot."))))

    # 3. личные карточки
    P.append(('', eyebrow(T("3 · Личные карточки","3 · Personal cards"))
      + h2(T("Каждому свой список дел","One list of duties each"))
      + box(T("Ведущая","Lead host"),
          ol([T("В автобусе: перекличка, шесть папок, роли, правила, пролог. Тексты на странице 5.","On the coach: roll call, six folders, roles, rules, prologue. Scripts on page 5."),
              T("Принимает ларец от курьера при гостях и ставит его на переднее сиденье, на виду. Весь день ларец виден.","Takes the lock box from the courier in front of the guests and puts it on the front seat, in plain sight. The box stays visible all day."),
              T("На контроле решает, идут потоки по порядку или по кругу. Сообщает гидам одной фразой по рации.","At the gate she decides whether flows go in order or in a circle. She tells the guides in one radio sentence."),
              T("На каждой станции даёт сигнал старта и сигнал смены. Следит за временем по сетке, а не по ощущению.","At each stop she gives the start signal and the change signal. She watches the grid, not her feeling of time."),
              T("Раз за программу произносит запланированную неправду у Сфинкса. Подробности на странице 10.","Once during the day she delivers the planned false statement at the Sphinx. Details on page 10."),
              T("Ведёт финал целиком: полоски, спор с курьером, набор кода, письмо, номинации.","Runs the whole closing session: the strips, the argument with the courier, the code, the letter, the awards."),
              T("Носит с собой кофр: дубль всех бумаг, запасная дужка и ключ от замка.","Carries the case: duplicates of every document, a spare shackle and the lock key.")]))
      + box(T("Помощник, каждый ведёт две команды","Assistant, each runs two teams"),
          ol([T("Приходит на точку раньше своих команд и находит место, где две пятёрки встают, не перекрывая проход.","Arrives at the stop ahead of his teams and finds where two groups of five can stand without blocking the path."),
              T("Читает задание станции дословно. Текст короткий, его не пересказывают своими словами.","Reads the task for the stop word for word. The text is short and is never paraphrased."),
              T("Держит время вслух: «пять минут», «две минуты». Команда должна слышать, сколько осталось.","Calls the time aloud: \"five minutes\", \"two minutes\". The team must hear how long is left."),
              T("Принимает ставку: жетоны ложатся на угол бланка, все вместе, одним движением. После ставки пересчитывать нельзя.","Takes the bet: tokens go on the corner of the sheet, all together, in one movement. After the bet nothing is recounted."),
              T("Только теперь разрешает вскрыть конверт проверки.","Only now does he let them open the check envelope."),
              T("Ставит печать в бланк. Заверяет то, что команда назвала своими глазами, даже если число неверное.","Stamps the evidence sheet. He certifies what the team saw with their own eyes, even when the number is wrong."),
              T("Снимает фото команды на станции. Оно уйдёт в лист, который печатается в автобусе.","Photographs the team at the stop. The picture goes onto the sheet printed on the coach.")]))
      + box(T("Координатор, он же курьер","Coordinator, also the courier"),
          ol([T("До выезда: вода, аптечка, радиогиды заряжены, реквизит по кофрам.","Before departure: water, first aid kit, charged radio guides, props packed by case."),
              T("Утром передаёт ведущей ларец и дневники при гостях и читает записку. Текст на странице 5.","In the morning he hands the host the box and the diaries in front of the guests and reads the note. Script on page 5."),
              T("Весь день держится рядом с группой и ничего не объясняет. На вопросы отвечает: «Я выполняю поручение».","He stays near the group all day and explains nothing. To questions he answers: \"I am carrying out an instruction.\""),
              T("Во время четвёртого блока уезжает вперёд и готовит зону финала: столы, схема на стене, ларец на центральном столе.","During the fourth block he drives ahead and sets up the closing area: tables, the chart on the wall, the box on the centre table."),
              T("Печатает в автобусе шесть листов «Восстановленный маршрут» с фотографиями команд.","On the coach he prints six route sheets with the team photographs."),
              T("В финале входит с конвертом на 13-й минуте и произносит свой текст. Больше ничего не добавляет.","In the closing session he enters with the envelope at minute 13 and delivers his lines. He adds nothing.")]))
      + box(T("Гид партнёра","Partner guide"),
          ol([T("Ведёт свой поток из десяти человек весь день и отвечает на вопросы по истории.","Leads his flow of ten all day and answers questions on the history."),
              T("Молчит, пока команда наблюдает и спорит. Это самое трудное правило и самое важное.","Stays silent while the team observes and argues. This is the hardest rule and the most important one."),
              T("Рассказывает историю целиком только после того, как команда поставила жетоны и вскрыла конверт.","Gives the full explanation only after the team has placed its tokens and opened the envelope."),
              T("Получает пакет со всеми станциями и ответами на брифинге накануне, лично.","Receives the full station pack with answers at the briefing the day before, in person.")])))
    )

    # 4. до выезда
    P.append(('', eyebrow(T("4 · До выезда","4 · Before departure"))
      + h2(T("Три проверки, которые нельзя пропустить","Three checks that are never skipped"))
      + table([T("Когда","When"), T("Что делаем","What we do"), T("Кто","Who")], [
          [T("Накануне, днём","The day before, daytime"), T("Брифинг гидов партнёра: час в помещении, час пешком по маршруту. Каждый гид получает пакет станций и проходит свои точки ногами.","Briefing for the partner guides: one hour in a room, one hour walking the route. Each guide receives the station pack and walks his own stops."), T("Ведущая","Host")],
          [T("Накануне, вечером","The day before, evening"), T("Комплектация: шесть папок собраны и подписаны номерами команд. Проверяем, что в каждой папке лежат все конверты и полоска правила.","Packing: six folders assembled and numbered. Check that every folder holds all its envelopes and its rule strip."), T("Помощники","Assistants")],
          [T("Накануне, вечером","The day before, evening"), T("Замок: набираем код 2–2–3–4 и открываем три раза подряд. Запасная дужка и ключ в кофр.","The lock: enter 2–2–3–4 and open it three times in a row. Spare shackle and key into the case."), T("Ведущая","Host")],
          [T("За 3 часа","3 hours before"), T("Радиогиды заряжены и проверены на всех каналах. Вода загружена: 1,5 литра на гостя плюс запас.","Radio guides charged and tested on every channel. Water loaded: 1.5 litres per guest plus reserve."), T("Координатор","Coordinator")],
          [T("За 45 минут","45 minutes before"), T("Штат на месте. Ведущая раздаёт рации, называет порядок точек и подтверждает, кто из гидов ведёт какой поток.","Staff on site. The host hands out radios, states the order of stops and confirms which guide leads which flow."), T("Все","Everyone")],
      ])
      + warn(T("Без чего не выезжаем","We do not depart without these"),
          ul([T("Разведка пройдена и четыре числа кода подтверждены на месте.","The reconnaissance is done and the four code numbers are confirmed on site."),
              T("Материалы напечатаны под подтверждённые числа, а не под прошлые.","Materials are printed against the confirmed numbers, not last time's."),
              T("Фотографии в конвертах проверки сняты с тех точек, где реально встанут команды.","The photographs in the check envelopes were taken from the exact spots the teams will stand on."),
              T("Зона финала подтверждена письменно: шесть столов, центральный стол, место под схему.","The closing venue is confirmed in writing: six tables, a centre table, space for the chart."),
              T("Письмо экспедиции отпечатано с названием компании заказчика.","The expedition letter is printed with the client's company name in it.")]))
      + eyebrow(T("5 · Деление на команды","5 · Dividing the group"))
      + p(T("Команды складываем заранее, по списку заказчика, а не на месте. Шесть конвертов с именами, по пять имён в каждом. Так начальники расходятся по разным командам и не уходит пять минут на разговор «а можно я с Олей».",
            "Teams are composed in advance from the client's list, never on site. Six envelopes with names, five names in each. That way senior people end up in different teams and no five minutes are lost to \"can I be with Olga\"."))
      + table([T("Роль","Role"), T("Что в руках","What they hold"), T("Что делает только она","What only they may do")], [
          [T("Читатель","Reader"), T("Дневник экспедиции","The expedition diary"), T("Читает страницы вслух, по одной на станцию. Дневник держит только он.","Reads the pages aloud, one per stop. Only they hold the diary.")],
          [T("Наблюдатель","Observer"), T("Карточка-видоискатель","The viewfinder card"), T("Считает и называет вслух то, что видит. Число идёт в бланк с его голоса.","Counts and says aloud what they see. The number enters the sheet in their voice.")],
          [T("Картограф","Mapper"), T("План плато и компас","The plateau plan and compass"), T("Определяет стороны света и ведёт команду вдоль дорожки.","Determines the compass directions and leads the team along the path.")],
          [T("Проверяющий","Checker"), T("Запечатанные конверты","The sealed envelopes"), T("Вскрывает конверт после ставки. До ставки конверт лежит печатью вверх.","Opens the envelope after the bet. Until then it lies seal upwards.")],
          [T("Представитель","Speaker"), T("Бланк свидетельств","The evidence sheet"), T("Говорит с помощником, объявляет ставку, в финале крутит диск замка.","Speaks to the assistant, announces the bet, turns a dial at the closing session.")],
      ])
      + p(T("Роли сдвигаются по кругу после второй и после четвёртой станции и ещё раз перед финалом. Сигнал даёт ведущая.",
            "Roles rotate one position after the second and after the fourth stop, and once more before the closing session. The host gives the signal.")))
    )

    # 5. автобус
    P.append(('', eyebrow(T("6 · В автобусе","6 · On the coach"))
      + h2(T("Двадцать минут, которые задают весь день","The twenty minutes that set up the day"))
      + steps([
          (T("До выезда","Before departure"), T("Перекличка. Координатор раздаёт воду. Помощники раздают шесть папок, по одной в руки хранителю команды.","Roll call. The coordinator hands out water. The assistants give out six folders, one into the hands of each team's keeper.")),
          (T("Минута 1","Minute 1"), T("Курьер передаёт ведущей ларец и дневники. При гостях, молча, с запиской.","The courier hands the host the box and the diaries. In front of the guests, in silence, with a note.")),
          (T("Минуты 2–4","Minutes 2–4"), T("Роли. Команда распределяет пять ролей сама, вслух. Помощники помогают тем, кто медлит.","Roles. Each team assigns its five roles itself, aloud. Assistants help anyone who hesitates.")),
          (T("Минуты 5–7","Minutes 5–7"), T("Правила и пролог ведущей.","The rules and the host's prologue.")),
      ])
      + say(T("Ведущая читает записку курьера","The host reads the courier's note"),
            T("Передаю по поручению. Тетрадь и ларец принадлежат экспедиции доктора Амира Камаля. Просьба вернуть решение до захода солнца.",
              "Delivered on instruction. The notebook and the box belong to Doctor Amir Kamal's expedition. A decision is requested before sunset."))
      + say(T("Правила, ведущая, дословно","The rules, host, word for word"),
            T("Правил у нас пять, и все короткие. Первое: смотрим с обычных дорожек, там видно ровно то, что нам сегодня нужно. Второе: всё, к чему сегодня можно прикоснуться, наш реквизит, он для этого и сделан. Третье: перед каждой проверкой команда ставит жетоны на свою версию, и ставит вся вместе, одним движением. Четвёртое: ошибиться можно, остаться без развязки нельзя, ларец сегодня откроется в любом случае. И пятое: один раз за эти четыре часа кто-то из нас уверенно скажет вам неправду. Команда, которая поймает нас на слове, получит жетон. Договорились?",
              "We have five rules and all of them are short. One: we look from the ordinary visitor paths, and from there you can see exactly what we need today. Two: everything you may touch today is our own prop, made for that purpose. Three: before every check the team places its tokens on its version, all together, in one movement. Four: getting it wrong is allowed, going home without the ending is not, the box opens today no matter what. And five: once in these four hours one of us will tell you something untrue, and tell it confidently. The team that catches us gets a token. Agreed?"))
      + say(T("Пролог, ведущая, дословно","The prologue, host, word for word"),
            T("Друзья, тетрадь у вас в руках — полевой дневник доктора Амира Камаля. Час назад его вместе с этим ларцом передал нам человек, который поедет с нами весь день. Он говорит, что выполняет поручение. Чьё, не говорит.<br><br>В дневнике беда. Весной Камаль заметил, что в его записях появились чужие страницы. Кто-то переписывал его наблюдения и вставлял свои. Камаль сделал одну вещь: он вынес настоящий маршрут из дневника наружу, в шесть наблюдений, которые можно пересчитать прямо на плато. Числа он записал на последней странице и запер вот здесь. Замок на четыре диска, кода не знает никто, включая меня.<br><br>Экспедиция после этого замолчала. Молчит до сих пор.<br><br>Четыре часа, шесть наблюдений, шесть команд. Свидетели у нас лучшие из возможных: они стоят здесь четыре с половиной тысячи лет и ни разу никому не соврали. Откройте дневник на первой странице. Там их две, и они об одном и том же. Какая из них написана человеком, который здесь стоял?",
              "Friends, the notebook in your hands is the field diary of Doctor Amir Kamal. An hour ago a man handed it to us together with this box, and he is travelling with us all day. He says he is carrying out an instruction. Whose instruction, he does not say.<br><br>There is a problem with the diary. In the spring Kamal noticed that pages he had not written had appeared in it. Someone was copying his observations and inserting their own. So Kamal did one thing: he took the real route out of the diary and turned it into six observations that can be counted here on the plateau. He wrote the numbers on the last page and locked it in this box. Four dials, and nobody knows the code, myself included.<br><br>After that the expedition went silent. It is silent still.<br><br>Four hours, six observations, six teams. Our witnesses are the best available: they have stood here for four and a half thousand years and have never lied to anyone. Open the diary at the first page. There are two of them, and they describe the same thing. Which one was written by someone who actually stood here?"))
      + warn(T("Что помощники держат при себе весь день","What assistants keep to themselves all day"),
          p(T("Две станции из шести не дают числа. Команды должны обнаружить это только в финале. Ни словом, ни намёком, ни интонацией. Печать в бланк ставим одинаково на всех шести станциях.",
              "Two of the six stops produce no number. The teams must discover this only at the closing session. Not a word, not a hint, not a change of tone. The stamp goes into the sheet identically at all six stops.")))))

    # 6. станция 1
    P.append(('', eyebrow(T("7 · Станция 1 · северная грань Хеопса · 20 минут","7 · Stop 1 · north face of Khufu · 20 minutes"))
      + h2(T("Две работы","Two different jobs"))
      + table([], [[T("Где","Where"), T("Площадка у северной грани, в стороне от очереди ко входу внутрь. Три потока встают вдоль грани с интервалом 30–50 метров, лицом к пирамиде.","The area by the north face, away from the queue for the inner passage. The three flows line up along the face 30 to 50 metres apart, facing the pyramid.")],
          [T("Реквизит на команду","Props per team"), T("Дневник, страницы 1 и 1-бис. Карточка-видоискатель. Бланк. Карандаш. Шесть жетонов. Запечатанный конверт с фотографией северной грани, на которой обведены два отверстия. Печать «ВХОДЫ» у помощника.","Diary, pages 1 and 1-bis. Viewfinder card. Evidence sheet. Pencil. Six tokens. A sealed envelope with a photograph of the north face with two openings circled. The assistant carries the ENTRANCES stamp.")]])
      + say(T("Помощник, дословно","Assistant, word for word"),
            T("Друзья, в дневнике сказано: проём в этой грани один, и сделали его строители. Наблюдатель, посмотрите на грань и скажите вслух, сколько отверстий вы видите?",
              "Friends, the diary says there is one opening in this face and that the builders made it. Observer, look at the face and say out loud how many openings you can see."))
      + steps([
          (T("0–2","0–2"), T("Помощник читает задание. Читатель читает вслух обе страницы дневника, настоящую и поддельную.","The assistant reads the task. The reader reads both diary pages aloud, the genuine one and the forged one.")),
          (T("2–6","2–6"), T("Наблюдатель через окно видоискателя ведёт по грани и называет число отверстий вслух, без объяснений. Остальные считают за ним.","The observer scans the face through the viewfinder window and says the number of openings aloud, with no explanation. The others count after them.")),
          (T("6–10","6–10"), T("Команда описывает края каждого отверстия. Одно обрамлено ровной каменной кладкой, другое рваный пролом с осыпью под ним.","The team describes the edges of each opening. One is framed by even stonework, the other is a ragged breach with rubble below it.")),
          (T("10–12","10–12"), T("Вывод: на ровную раму строитель тратит недели, тот, кто ищет чужое, не тратит. Значит, отверстия делали разные люди и в разное время.","The conclusion: an even frame costs a builder weeks, and someone searching for another man's treasure spends nothing on it. So the two openings were made by different people at different times.")),
          (T("12–13","12–13"), T("<b>Ставка.</b> Представитель объявляет, жетоны ложатся на угол бланка. Ставят на число и на то, какое отверстие древнее.","<b>The bet.</b> The speaker announces it, the tokens go on the corner of the sheet. They bet on the number and on which opening is older.")),
          (T("13–15","13–15"), T("<b>Проверка.</b> Проверяющий вскрывает конверт, команда сама сверяет фотографию с гранью.","<b>The check.</b> The checker opens the envelope and the team compares the photograph with the face themselves.")),
          (T("15–18","15–18"), T("<b>Гид.</b> Верхний проём с ровной рамой это древний вход. Нижний пролом связывают с работами халифа аль-Мамуна в девятом веке, когда искали внутренние камеры. Отсюда и разница краёв.","<b>The guide.</b> The upper opening with the even frame is the ancient entrance. The lower breach is associated with Caliph al-Ma'mun's ninth-century works, when the inner chambers were being searched for. That is where the difference in edges comes from.")),
          (T("18–20","18–20"), T("Помощник спрашивает: «Кто считал и сколько раз?» — и заверяет строку печатью.","The assistant asks: \"Who counted, and how many times?\" and stamps the line.")),
      ])
      + box(T("Ответ","The answer"),
          p(T("Отверстий два. Древнее верхнее, с ровной рамой. Настоящая страница дневника та, где грань названа северной. <b>В бланк: ВХОДОВ — 2.</b>",
              "There are two openings. The older is the upper one with the even frame. The genuine diary page is the one that calls the face the north face. <b>Into the sheet: ENTRANCES — 2.</b>"))
        + p(T("<b>Подсказка 1.</b> «Сначала посчитайте, потом объясняйте». <b>Подсказка 2.</b> «Посмотрите на края. Кто из двоих торопился?»",
              "<b>Hint 1.</b> \"Count first, explain afterwards.\" <b>Hint 2.</b> \"Look at the edges. Which of the two was in a hurry?\"")))
      + p(T("<b>Если второй проём плохо читается</b> с разрешённой точки, станция переносится на остатки облицовки у основания грани: сколько рядов сохранилось. Это меняет число, а вместе с ним код замка и полоски правила, поэтому решение принимается на разведке, а не в день программы.",
            "<b>If the second opening reads badly</b> from the permitted spot, the stop moves to the remains of casing at the base of the face: how many courses survive. That changes the number, and with it the lock code and the rule strips, so the decision is taken at the reconnaissance and never on the day."))))

    # 7. станция 2
    P.append(('', eyebrow(T("8 · Станция 2 · панорама · 25 минут","8 · Stop 2 · the panorama · 25 minutes"))
      + h2(T("Где стоял фотограф","Where the photographer stood"))
      + table([], [[T("Где","Where"), T("Официальная панорамная точка с видом на три пирамиды и разрешённый отрезок дорожки рядом. Точка людная: помощник сразу уводит свои две команды на 40–50 метров в сторону от торговцев и верблюдов.","The official panorama point with the view of the three pyramids, and the permitted stretch of path beside it. It is a busy spot: the assistant immediately takes his two teams 40 to 50 metres away from the vendors and the camels.")],
          [T("Реквизит","Props"), T("Дневник, страницы 3 и 3-бис. Снимок панорамы 15 × 20 см. План с шестью пронумерованными точками. Видоискатель. Запечатанная справка с высотами. Бланк, жетоны. Печать «ПАНОРАМА».","Diary, pages 3 and 3-bis. A 15 by 20 cm print of the panorama. A plan with six numbered points. Viewfinder. A sealed note with the heights. Sheet, tokens. The PANORAMA stamp.")]])
      + say(T("Помощник, дословно","Assistant, word for word"),
            T("Друзья, в дневнике лежит снимок этой панорамы и подпись: снято отсюда, и отсюда видно, что средняя пирамида выше всех. Картограф, найдите место, с которого сделан снимок, а мы пока поверим подписи.",
              "Friends, the diary holds a photograph of this panorama with a caption: taken from here, and from here you can see that the middle pyramid is the tallest. Mapper, find the spot the photograph was taken from. In the meantime we shall believe the caption."))
      + steps([
          (T("0–3","0–3"), T("Задание и чтение обеих страниц. Команда сравнивает вид со снимком: вершины выстроены иначе.","The task and both pages. The team compares the view with the photograph: the summits line up differently.")),
          (T("3–5","3–5"), T("Первое голосование глазами: какая пирамида кажется выше? Помощник записывает ответ карандашом и вслух не комментирует. Почти все команды называют среднюю.","A first vote by eye: which pyramid looks taller? The assistant writes the answer in pencil and says nothing. Almost every team names the middle one.")),
          (T("5–14","5–14"), T("Картограф ведёт команду вдоль дорожки по шести отмеченным точкам. На каждой наблюдатель через видоискатель сверяет взаимное положение трёх вершин со снимком.","The mapper walks the team along the path through the six marked points. At each one the observer uses the viewfinder to compare the relative position of the three summits with the photograph.")),
          (T("14–16","14–16"), T("Команда называет точку, с которой снимок совпадает, и формулирует, что сделал автор снимка: он не придумал ни слова, он выбрал место.","The team names the point where the photograph matches and puts into words what its author did: he invented nothing, he chose where to stand.")),
          (T("16–17","16–17"), T("<b>Ставка</b> на номер точки.","<b>The bet</b> on the number of the point.")),
          (T("17–20","17–20"), T("<b>Проверка.</b> Проверяющий вскрывает справку с высотами и отметками оснований, команда читает её вслух.","<b>The check.</b> The checker opens the note with the heights and base levels and the team reads it aloud.")),
          (T("20–23","20–23"), T("<b>Гид.</b> Хуфу выше как сооружение, 146,6 метра против 143,5, но стоит ниже. Основание Хафры лежит на скале примерно на десять метров выше, грани круче, на вершине сохранилась облицовка. Поэтому её макушка действительно выше над уровнем моря и она кажется больше почти с любой точки плато.","<b>The guide.</b> Khufu is the taller structure, 146.6 metres against 143.5, but it stands lower. Khafre's base sits on bedrock about ten metres higher, its faces are steeper and casing survives at the top. So its apex really is higher above sea level and it looks bigger from almost anywhere on the plateau.")),
          (T("23–25","23–25"), T("Помощник заверяет строку печатью и снимает командное фото с панорамой.","The assistant stamps the line and takes the team photograph against the panorama.")),
      ])
      + box(T("Ответ","The answer"),
          p(T("Впечатление не измеряет высоту. Выше как сооружение Хуфу, выше над уровнем моря вершина Хафры, и это разные утверждения. <b>В бланк: ВПЕЧАТЛЕНИЕ — НЕ ИЗМЕРЕНИЕ.</b> Числа станция не даёт, и в финале это окажется важным.",
              "An impression does not measure height. Khufu is the taller structure, Khafre's apex is higher above sea level, and those are two different statements. <b>Into the sheet: IMPRESSION IS NOT MEASUREMENT.</b> This stop yields no number, and at the closing session that turns out to matter."))
        + p(T("<b>Подсказка 1.</b> «Пройдите двадцать шагов вдоль дорожки и посмотрите на вершины снова». <b>Подсказка 2.</b> «Посмотрите, на какой высоте начинается каждая пирамида».",
              "<b>Hint 1.</b> \"Walk twenty paces along the path and look at the summits again.\" <b>Hint 2.</b> \"Look at the height each pyramid starts from.\"")))
      + p(T("Это самая обсуждаемая мысль дня у корпоративной группы, и она про отчёты и презентации, а не про пирамиды. Ложь высокого класса делается не выдумкой, а выбранной точкой зрения. Гид может сказать это вслух.",
            "For a corporate group this is the most discussed idea of the day, and it is about reports and presentations rather than pyramids. First-class deception is not invention, it is a chosen point of view. The guide may say so aloud."))))

    # 8. станция 3
    P.append(('', eyebrow(T("9 · Станция 3 · у Хефрена · 20 минут","9 · Stop 3 · at Khafre · 20 minutes"))
      + h2(T("Ключ, которого нет в папке","The key that is not in the folder"))
      + table([], [[T("Где","Where"), T("Обзорная точка у пирамиды Хефрена, откуда одновременно видны Хефрен и восточная грань Хеопса с малыми пирамидами у подножия.","The viewpoint by Khafre from which both Khafre and the east face of Khufu with the subsidiary pyramids at its foot are visible.")],
          [T("Реквизит","Props"), T("Дневник, страницы 2 и 2-бис. Бумажная печать из восьми знаков. Три трафарета с прорезями. Компас. Видоискатель. Запечатанная справка об именах правителя. Бланк, жетоны. Печать «СПУТНИЦЫ».","Diary, pages 2 and 2-bis. A paper seal of eight signs. Three cut-out stencils. Compass. Viewfinder. A sealed note about the ruler's names. Sheet, tokens. The SUBSIDIARIES stamp.")]])
      + say(T("Помощник, дословно","Assistant, word for word"),
            T("Друзья, в дневнике лежит печать из восьми знаков и записка: ключ я не записал, он стоит перед вами и не менялся четыре тысячи лет. Читатель, прочтите записку ещё раз и скажите, где нам искать ключ?",
              "Friends, the diary holds a seal of eight signs and a note: I did not write the key down, it stands in front of you and has not changed in four thousand years. Reader, read the note again and tell us where to look for the key."))
      + steps([
          (T("0–2","0–2"), T("Задание. Команда обнаруживает, что ключа в папке нет.","The task. The team discovers that the key is not in the folder.")),
          (T("2–6","2–6"), T("Наблюдатель находит у подножия большой пирамиды ряд малых и пересчитывает их вслух. Поддельная страница называет число на единицу больше, поэтому пересчитывать приходится дважды.","The observer finds the row of small pyramids at the foot of the great one and counts them aloud. The forged page states one more than there are, so they count twice.")),
          (T("6–11","6–11"), T("Ключ. Три трафарета закрывают часть знаков печати, и осмысленное слово получается только при одном порядке наложения: в том, в каком три главные пирамиды стоят с севера на юг. Порядок определяет картограф по компасу.","The key. Three stencils cover part of the seal, and a readable word appears in only one order of overlay: the order in which the three main pyramids stand from north to south. The mapper works it out with the compass.")),
          (T("11–12","11–12"), T("Команда читает печать: открытыми остаются четыре знака, они складываются в имя ХУФУ.","The team reads the seal: four signs stay uncovered and spell the name KHUFU.")),
          (T("12–13","12–13"), T("<b>Ставка</b> на число малых пирамид и на прочитанное имя.","<b>The bet</b> on the number of small pyramids and on the name read from the seal.")),
          (T("13–16","13–16"), T("<b>Проверка.</b> В справке: Хуфу это египетское имя царя, Хеопс его греческая передача. Два документа, одно имя, один человек. Дальше в программе говорим только «Хуфу».","<b>The check.</b> The note says: Khufu is the king's Egyptian name, Cheops the Greek rendering of it. Two documents, one name, one man. For the rest of the day we say only Khufu.")),
          (T("16–18","16–18"), T("<b>Гид.</b> Малые пирамиды у восточной грани это гробницы цариц, часть того же замысла, что и большая. Лишними их считали ещё в девятнадцатом веке, когда планы плато рисовали по памяти.","<b>The guide.</b> The small pyramids by the east face are queens' tombs, part of the same design as the great one. They were treated as surplus as late as the nineteenth century, when plateau plans were drawn from memory.")),
          (T("18–20","18–20"), T("Помощник заверяет строку печатью.","The assistant stamps the line.")),
      ])
      + warn(T("Число, от которого зависит весь день","The number the whole day depends on"),
          p(T("Сколько малых пирамид уверенно пересчитывается именно с этой точки, подтверждается на разведке. <b>Это число идёт в код замка.</b> Если на месте видно другое количество, меняются код и все шесть полосок правила. Менять что-либо в день программы нельзя.",
              "How many small pyramids can be counted with confidence from this exact spot is confirmed at the reconnaissance. <b>This number goes into the lock code.</b> If a different count is visible on site, the code and all six rule strips change. Nothing here may be changed on the day.")))
      + box(T("Ответ","The answer"),
          p(T("Малых пирамид три. Порядок трафаретов с севера на юг. На печати ХУФУ. <b>В бланк: СПУТНИЦ — 3.</b>",
              "There are three small pyramids. The stencil order runs north to south. The seal reads KHUFU. <b>Into the sheet: SUBSIDIARIES — 3.</b>"))
        + p(T("<b>Подсказка 1.</b> «Ваш ключ не в папке. Он перед вами». <b>Подсказка 2.</b> «Поставьте фигуры в том порядке, в каком стоят три пирамиды с севера на юг, и прочтите печать заново».",
              "<b>Hint 1.</b> \"Your key is not in the folder. It is in front of you.\" <b>Hint 2.</b> \"Place the shapes in the order the three pyramids stand in from north to south, and read the seal again.\"")))))

    # 9. станции 4 и 5
    P.append(('', eyebrow(T("10 · Станции 4 и 5 · блок Сфинкса · по 14 минут","10 · Stops 4 and 5 · the Sphinx block · 14 minutes each"))
      + h2(T("Потоки меняются местами по сигналу ведущей","The flows swap over on the host's signal"))
      + p(T("Две станции работают одновременно: одна у храма в долине, вторая на террасе перед Сфинксом. Через четырнадцать минут ведущая даёт сигнал, и потоки меняются местами.",
            "The two stops run at the same time: one at the valley temple, the other on the terrace in front of the Sphinx. After fourteen minutes the host gives the signal and the flows swap over."))
      + box(T("Станция 4. Куда ведёт дорога","Stop 4. Where the road leads"),
          say(T("Помощник","Assistant"),
              T("Друзья, вот настоящие камни того самого пути, а в дневнике его цепочка переписана, и в неё вписано лишнее. Наблюдатель, где здесь ниже, где выше и куда уходит дорога?",
                "Friends, these are the real stones of that road, and in the diary its sequence has been rewritten with extra links added. Observer, where is the low ground here, where is the high ground, and where does the road go?"))
        + steps([
              (T("0–2","0–2"), T("Задание и чтение двух страниц.","The task and both pages.")),
              (T("2–6","2–6"), T("Наблюдатель и картограф определяют рельеф и направление: где вода была ближе, где начинается подъём, куда он ведёт.","The observer and the mapper work out the relief and the direction: where the water was closer, where the climb begins, where it leads.")),
              (T("6–9","6–9"), T("Команда выкладывает на схему только те карточки, что образуют непрерывный путь. Две карточки лишние, и они правдоподобны: такие постройки в комплексах были, но в путь от воды к пирамиде не входят.","The team lays out only the cards that form an unbroken road. Two cards are surplus and they are plausible: such buildings existed in the complexes, but they are not part of the road from the water to the pyramid.")),
              (T("9–10","9–10"), T("<b>Ставка</b> на число звеньев.","<b>The bet</b> on the number of links.")),
              (T("10–12","10–12"), T("<b>Проверка</b> и разбор.","<b>The check</b> and the discussion.")),
              (T("12–14","12–14"), T("<b>Гид.</b> Храм в долине, дорога, заупокойный храм, пирамида. С востока на запад, от воды в пустыню. Путь фараона повторяет путь солнца.","<b>The guide.</b> Valley temple, causeway, mortuary temple, pyramid. East to west, from the water into the desert. The pharaoh's road repeats the road of the sun.")),
          ])
        + p(T("<b>Ответ.</b> Звеньев четыре. Направление с востока на запад. <b>В бланк: ЗВЕНЬЕВ — 4.</b> Подсказки: «Начните со звена, к которому можно было приплыть» и «Две карточки описывают постройки, которые нужны живым, а не мёртвым».",
              "<b>The answer.</b> Four links. East to west. <b>Into the sheet: LINKS — 4.</b> Hints: \"Start with the link you could have sailed to\" and \"Two cards describe buildings the living need, not the dead.\"")))
      + box(T("Станция 5. Что видно, а что известно","Stop 5. What is visible and what is known"),
          say(T("Помощник","Assistant"),
              T("Друзья, про этого свидетеля в дневнике три утверждения. Проверяющий, прочтите их вслух и скажите, какое из трёх мы можем проверить отсюда, своими глазами?",
                "Friends, the diary makes three claims about this witness. Checker, read them aloud and tell us which of the three we can verify from here, with our own eyes."))
        + p(T("<b>Три утверждения, все правдоподобны.</b> А: по внешнему виду можно определить, чьё это лицо. Б: по внешнему виду можно определить, сколько существ соединено в одном образе. В: по внешнему виду можно определить, когда его высекли.",
              "<b>Three claims, all plausible.</b> A: the face can be identified by appearance. B: the number of creatures combined in the figure can be established by appearance. C: the date it was carved can be established by appearance."))
        + p(T("Команда проверяет каждое утверждение собственным наблюдением по чек-листу. Голова человека и тело льва различимы с террасы, значит Б проверяемо. Чьё лицо и когда высечено, отсюда не устанавливается. Ставка на букву и на число существ, потом проверка, потом гид: соединённый образ это знак царской силы, а не портрет зверя; стела между лапами поставлена Тутмосом Четвёртым примерно через тысячу лет после самого Сфинкса.",
              "The team tests each claim by its own observation against a checklist. A human head and a lion's body are distinguishable from the terrace, so B is verifiable. Whose face it is and when it was carved cannot be established from here. They bet on the letter and on the number of creatures, then the check, then the guide: the combined figure is a sign of royal power rather than a portrait of an animal; the stela between the paws was set up by Thutmose the Fourth roughly a thousand years after the Sphinx itself."))
        + p(T("<b>Ответ.</b> Верно Б. Существ два. <b>В бланк: СУЩЕСТВ — 2.</b>",
              "<b>The answer.</b> B is correct. Two creatures. <b>Into the sheet: CREATURES — 2.</b>")))
      + warn(T("Здесь стоит единственная запланированная неправда дня","This is where the day's one planned untruth belongs"),
          p(T("Гид на подходе к террасе уверенно говорит: «Сфинкса сложили из блоков, как пирамиду». В настоящей странице дневника написано, что страж вырублен из одной скалы и это видно по слоям. Команда, поймавшая противоречие, получает жетон и номинацию. Если за три минуты никто не поймал, гид произносит фразу второй раз, громче.",
              "As the flow approaches the terrace the guide says confidently: \"The Sphinx was built up out of blocks, like a pyramid.\" The genuine diary page states that the guardian was cut from a single rock and that this is visible in the layers. The team that catches the contradiction gets a token and an award. If nobody has caught it within three minutes, the guide repeats the sentence, louder.")))))

    # 10. станция 6
    P.append(('', eyebrow(T("11 · Станция 6 · в автобусе · 15 минут","11 · Stop 6 · on the coach · 15 minutes"))
      + h2(T("Отчёт о месте, где вы не были","A report on a place you never visited"))
      + p(T("Станция идёт на переезде к площадке финала, после туалетов и воды. Команды сидят вместе, папки на коленях. Свет над креслами должен работать: гости читают текст.",
            "This stop runs on the transfer to the closing venue, after the toilets and the water. Teams sit together with folders on their laps. The reading lights must work: the guests read a text."))
      + say(T("Ведущая, после того как курьер передал конверт на стоянке","Host, after the courier hands over the envelope at the standing point"),
            T("Это доставили пять минут назад. Отчёт о третьей пирамиде, о той, к которой мы сегодня не подходили. Просят решение до финала. Друзья, у вас пятнадцать минут: этот отчёт можно принять?",
              "This was delivered five minutes ago. A report on the third pyramid, the one we did not approach today. They are asking for a decision before the closing session. Friends, you have fifteen minutes: can this report be accepted?"))
      + steps([
          (T("0–2","0–2"), T("Помощники раздают отчёты и запечатанные полоски правила со словами: «Это не читаем до зала».","The assistants hand out the reports and the sealed rule strips, saying: \"We do not read this until the room.\"")),
          (T("2–9","2–9"), T("Команда разбирает отчёт своим методом дня: на чём стоит каждое утверждение, на пересчитанном, на измеренном или на впечатлении. Читатель подчёркивает всё, что можно пересчитать.","The team works through the report with the method of the day: what does each statement rest on, something counted, something measured, or an impression. The reader underlines everything that could be counted.")),
          (T("9–11","9–11"), T("Выбор варианта: принять, отклонить, отсюда проверить нельзя. <b>Ставка.</b>","They choose: accept, reject, or cannot be verified from here. <b>The bet.</b>")),
          (T("11–13","11–13"), T("Помощник собирает листы решения. Конверта проверки здесь нет: проверка придёт в финале, из письма экспедиции.","The assistant collects the decision sheets. There is no check envelope here: the check arrives at the closing session, in the expedition's letter.")),
          (T("13–15","13–15"), T("Помощник заверяет строку печатью «РЕШЕНИЕ». Заверяется сам факт решения, любого из трёх.","The assistant stamps the line DECISION. What is certified is the act of deciding, whichever of the three it was.")),
      ])
      + box(T("Ответ","The answer"),
          p(T("«Отсюда проверить нельзя» — и это лучший ответ, за него полный балл и отдельная номинация. Команда, дописавшая рядом, чем именно это можно было бы проверить, получает жетон сверх. <b>В бланк: ПРОВЕРИТЬ НЕЛЬЗЯ.</b> Числа станция не даёт.",
              "\"It cannot be verified from here\" is the best answer, and it takes full marks and an award of its own. A team that writes beside it how it could be verified gets an extra token. <b>Into the sheet: CANNOT BE VERIFIED.</b> This stop yields no number."))
        + p(T("<b>Подсказка 1.</b> «Подчеркните в отчёте всё, что можно пересчитать. Сколько подчёркиваний получилось?» <b>Подсказка 2.</b> «Сегодня вы четыре раза отказались верить красивой странице. Это пятая».",
              "<b>Hint 1.</b> \"Underline everything in the report that can be counted. How many underlinings did you get?\" <b>Hint 2.</b> \"Four times today you refused to believe a well-written page. This is the fifth.\"")))
      + p(T("Для корпоративной группы это самая ценная минута программы: «я не знаю» это профессиональный ответ, а не слабость. Она же объясняет правило финала, поэтому сокращать эту станцию нельзя. Если дорога короче пятнадцати минут, станция переносится на первые минуты в зале, до рассадки.",
            "For a corporate group this is the most valuable minute of the programme: \"I do not know\" is a professional answer, not a weakness. It also explains the closing rule, so this stop is never shortened. If the drive is under fifteen minutes, the stop moves to the first minutes in the room, before seating."))))

    # 11. финал
    P.append(('', eyebrow(T("12 · Финал · 50 минут","12 · The closing session · 50 minutes"))
      + h2(T("Замок помнит только то, что можно пересчитать","The lock remembers only what can be counted"))
      + p(T("Шесть столов по числу команд, центральный стол под ларец, на стене большая схема плато с шестью пустыми окнами. Кода никто не выдаёт. Правило чтения разрезано на шесть полосок, по одной на команду, и собирается только сообща.",
            "Six tables, one per team, a centre table for the box, and on the wall a large plateau chart with six empty windows. Nobody is given the code. The reading rule is cut into six strips, one per team, and can only be assembled together."))
      + steps([
          (T("00–06","00–06"), T("Рассадка, вода. Каждая команда крепит свои шесть заверенных свидетельств в своё окно на схеме. Сразу видно, что у кого-то числа расходятся с соседями. Ведущая это не комментирует.","Seating, water. Each team pins its six certified findings into its window on the chart. It is immediately visible that somebody's numbers differ from their neighbours'. The host does not comment.")),
          (T("06–13","06–13"), T("Ведущая ставит ларец на центральный стол: «Свидетельств шесть, дисков четыре. Правило чтения было на последней странице дневника, и он её вырвал, а потом разрезал». Команды вскрывают полоски и выкладывают их на центральный стол. Собранное правило: «Замок помнит только то, что можно пересчитать. От меньшего к большему».","The host puts the box on the centre table: \"Six findings, four dials. The reading rule was on the last page of the diary, and he tore it out and then cut it up.\" The teams open their strips and lay them on the centre table. Assembled, the rule reads: \"The lock remembers only what can be counted. From smallest to largest.\"")),
          (T("13–21","13–21"), T("Входит курьер с конвертом. Он приносит готовый код 1–3–4–5 и лист «Восстановленный маршрут» своей версии, на подпись представителей. Ведущая в спор не вмешивается до 19-й минуты. К 21-й команды называют, какие числа пересчитали лично, и признак почерка: стороны света против «справа и слева».","The courier enters with an envelope. He brings a ready-made code, 1–3–4–5, and his own version of the route sheet for the speakers to sign. The host stays out of the argument until minute 19. By minute 21 the teams state which numbers they counted themselves, and the tell in the handwriting: compass directions against \"right\" and \"left\".")),
          (T("21–28","21–28"), T("Отбор. Счётные: 2, 2, 3, 4. Несчётные: «впечатление не измерение» и «проверить нельзя», ровно те две станции, где команда училась не доверять. По возрастанию: 2–2–3–4. Две одинаковые двойки всегда вызывают спор, не гасите его.","Sorting. Countable: 2, 2, 3, 4. Uncountable: \"impression is not measurement\" and \"cannot be verified\", precisely the two stops where the team learned not to trust. In ascending order: 2–2–3–4. The two identical twos always start an argument. Do not shut it down.")),
          (T("28–35","28–35"), T("Набор кода. Жребий: четыре команды крутят по диску, две оставшиеся выходят к ларцу и вслух называют, что в код не вошло и почему. Если хоть одно число чужое, дужка не отходит, и две минуты вся группа сверяет бланки между столами. Это лучший командный момент дня.","Entering the code. By lot, four teams each turn one dial and the remaining two come to the box and say aloud what did not go into the code and why. If even one number is wrong the shackle stays shut and for two minutes the whole group compares sheets between tables. This is the best team moment of the day.")),
          (T("35–43","35–43"), T("Ведущая достаёт из ларца последнюю страницу дневника и письмо экспедиции и читает письмо вслух. Под письмом тридцать фрагментов солнечной печати, по одному каждому. Координатор раздаёт шесть листов «Восстановленный маршрут», отпечатанных в дороге.","The host takes the diary's last page and the expedition's letter out of the box and reads the letter aloud. Under the letter lie thirty fragments of the sun seal, one for each guest. The coordinator hands out the six route sheets printed on the way.")),
          (T("43–50","43–50"), T("Номинации без баллов и общая фотография у открытого ларца: шесть рук на четырёх дисках и Хеопс за спинами.","Awards without scores, and a group photograph at the open box: six hands on four dials with Khufu behind them.")),
      ])
      + say(T("Ведущая перед открытием, дословно","The host before the opening, word for word"),
            T("Друзья, вам сегодня четыре раза предлагали поверить красивой странице, и один раз готовый код. Вы вместо этого посчитали сами. Четыре числа, четыре диска, шесть команд. Кто крутит первым?",
              "Friends, four times today you were offered a well-written page to believe, and once a ready-made code. Instead you counted for yourselves. Four numbers, four dials, six teams. Who turns first?"))
      + warn(T("Предохранитель","The safety catch"),
          p(T("Если после набора дужка не отошла, ведущая говорит: «Одно число чужое. Две минуты, сверьте бланки между столами, вслух». Через две минуты, чем бы это ни кончилось, она набирает верный код сама со словами: «Значит, это число он оставил мне», и открывает ларец. Развязку получают все шесть команд при любом раскладе.",
              "If the shackle does not release, the host says: \"One number is wrong. Two minutes, compare your sheets between tables, out loud.\" After two minutes, however it has gone, she enters the correct code herself with the words \"So that is the number he left for me\" and opens the box. All six teams get the ending whatever happens."))
        + p(T("<b>Если полоска правила потеряна:</b> у ведущей лежит полный дубль. Она выкладывает недостающую молча, без объяснений, и продолжает.",
              "<b>If a rule strip is lost:</b> the host carries a full duplicate. She lays the missing strip down in silence, without explanation, and carries on."))
        + p(T("<b>Если группа подписала лист курьера:</b> ничего не переигрываем. В письме экспедиции это прямо предусмотрено, и ведущая читает письмо как есть. Ошибка группы становится частью развязки.",
              "<b>If the group signed the courier's sheet:</b> nothing is replayed. The expedition's letter allows for exactly this, and the host reads it as written. The group's mistake becomes part of the ending.")))))

    # 12. аварийные + после
    P.append(('', eyebrow(T("13 · Если что-то пошло не так","13 · When something goes wrong"))
      + h2(T("Решения приняты заранее, чтобы не думать на месте","The decisions are made in advance so nobody has to think on site"))
      + table([T("Что случилось","What happened"), T("Что делаем","What we do")], [
          [T("Очередь на входе длиннее обычного","The queue at the gate is longer than usual"), T("Внутри блока заложено десять минут. Если не хватает, режем разговор гида на второй станции, а не финал.","There are ten minutes of slack in the block. If that is not enough, cut the guide's talk at the second stop, never the closing session.")],
          [T("На точке толпа","The stop is crowded"), T("Потоки идут по кругу. Ведущая объявляет по рации одной фразой: «Круг, поток В с Хефрена». На код порядок не влияет.","The flows go round in a circle. The host announces it in one radio sentence: \"Circle, flow C starts at Khafre.\" The order does not affect the code.")],
          [T("Жара","Heat"), T("Станция сокращается до наблюдения, ставки и проверки. Рассказ гида переносим в тень на следующем переезде.","The stop shrinks to observation, bet and check. The guide's talk moves into the shade at the next transfer.")],
          [T("Точка перекрыта","A spot is closed off"), T("Работает запасной вариант, согласованный на разведке. Подменять незаметно нельзя: если меняется число, меняется код.","The fallback agreed at the reconnaissance is used. It is never swapped quietly: if the number changes, the code changes.")],
          [T("Команда не нашла деталь","A team cannot find the detail"), T("Помощник считает вслух вместе с командой и заверяет число как своё. В финале никто не отличит.","The assistant counts aloud with the team and certifies the number as his own. At the closing session nobody can tell the difference.")],
          [T("Команда пересчитала неверно","A team counted wrongly"), T("Не исправляем. Ошибка доедет до финала, и там её ищет вся группа. Это лучшая минута дня.","We do not correct it. The error travels to the closing session and the whole group hunts for it there. It is the best minute of the day.")],
          [T("Опоздание больше 20 минут","More than 20 minutes behind"), T("Снимаем одну станцию целиком, а не сокращаем все. Финалу отдаём его пятьдесят минут полностью.","Drop one stop entirely rather than trimming all of them. The closing session keeps its full fifty minutes.")],
          [T("Ларец не открылся","The box will not open"), T("Предохранитель, запасная дужка и ключ лежат в кофре ведущей.","The safety catch, the spare shackle and the key are in the host's case.")],
          [T("Гость плохо себя чувствует","A guest feels unwell"), T("Координатор уводит в тень, вода, аптечка. Команда продолжает: роли распределены так, что пятеро не обязаны стоять вместе.","The coordinator takes them into the shade, water, first aid kit. The team continues: the roles are arranged so the five need not stand together.")],
      ])
      + eyebrow(T("14 · После программы","14 · After the programme"))
      + table([T("Когда","When"), T("Что","What"), T("Кто","Who")], [
          [T("Сразу","Straight away"), T("Пересчитать реквизит по списку. Ларец, печати, трафареты и схема уезжают с координатором. Гостям ничего из этого не достаётся.","Count the props against the list. The box, the stamps, the stencils and the chart leave with the coordinator. None of it goes to the guests.")],
          [T("В тот же вечер","The same evening"), T("Ведущая пишет одну страницу: что шло дольше плана, где команды спорили, какой неверный вариант выбирали чаще всего.","The host writes one page: what ran over, where the teams argued, which wrong answer came up most often.")],
          [T("На следующий день","The next day"), T("Заказчику: фотографии, скан собранного листа и короткий отчёт, сколько команд дошло до верного кода.","To the client: photographs, a scan of the assembled sheet and a short report on how many teams reached the correct code.")],
          [T("В течение недели","Within the week"), T("Правки в эту инструкцию. Всё, что пришлось решать на месте, должно оказаться здесь до следующей группы.","Corrections to this run-book. Everything that had to be decided on site belongs here before the next group.")],
      ])
      + dark(T("Одно правило важнее остальных","One rule matters more than the rest"),
          p(T("Гость приезжает, чтобы самому увидеть и самому посчитать. Всё, что мы делаем в этот день, существует ради минуты, когда он говорит: «Подождите, а давайте пересчитаем». Любой из нас, кто отвечает раньше этой минуты, отнимает у него весь день.",
              "The guest comes to see for themselves and count for themselves. Everything we do that day exists for the moment when they say: \"Hold on, let us count that again.\" Any one of us who answers before that moment takes the whole day away from them.")))))
    return P

CSS_EXTRA = '''
.say{display:grid;grid-template-columns:32mm 1fr;gap:4mm;margin:0 0 3.5mm;padding:3mm 0 0;border-top:1px solid var(--rule)}
.say .who{font-family:"JetBrains Mono",monospace;font-size:6.8pt;letter-spacing:.12em;text-transform:uppercase;color:var(--violet);padding-top:.6mm}
.say .line{font-family:"Spectral",Georgia,serif;font-size:10.5pt;line-height:1.4;color:var(--ink)}
.mins{margin:0 0 3.5mm}
.m{display:grid;grid-template-columns:20mm 1fr;gap:4mm;padding:1.8mm 0;border-bottom:1px solid var(--rule)}
.m .tm{font-family:"JetBrains Mono",monospace;font-size:7.6pt;color:var(--violet);padding-top:.4mm}
.m .tx{color:var(--ink-2)}
.box .mins .m:last-child{border-bottom:none}
h2{margin-bottom:3mm}
'''

def render(lang, out):
    global L
    L = lang
    pages = build()
    title = "Код пирамид — механика" if lang == "ru" else "Code of the Pyramids — run-book"
    foot = "Код пирамид · механика для команды" if lang == "ru" else "Code of the Pyramids · team run-book"
    body = []
    n = 1
    for kind, inner in pages:
        cls = "page cover" if kind == "cover" else "page"
        pn = "" if kind == "cover" else f'<div class="pn"><span>{foot}</span><span>{n}</span></div>'
        body.append(f'<section class="{cls}">{inner}{pn}</section>')
        n += 1
    doc = ('<!doctype html><html lang="' + lang + '"><head><meta charset="utf-8"><title>' + title +
           '</title><link rel="stylesheet" href="fonts/local.css"><link rel="stylesheet" href="doc.css">'
           '<style>' + CSS_EXTRA + '</style></head><body>' + ''.join(body) + '</body></html>')
    pathlib.Path(out).write_text(doc, encoding='utf-8')
    print(out, len(pages), 'страниц')

render('ru', 'giza-mehanika-ru.html')
render('en', 'giza-runbook-en.html')
