# -*- coding: utf-8 -*-
"""Карточки шести команд для «Кода пирамид». A5, по странице на команду."""
import pathlib

TEAMS = [
    ("СКАРАБЕЙ", "scarab"),
    ("ГЛАЗ ГОРА", "eye"),
    ("ЛОТОС", "lotus"),
    ("АНУБИС", "anubis"),
    ("КОБРА", "cobra"),
    ("ВЕЕР", "fan"),
]

INK = "#4a2014"
RED = "#8d2f23"
GOLD = "#c08a2d"

def emblem(kind):
    if kind == "scarab":
        body = f'''<ellipse cx="60" cy="66" rx="20" ry="24" fill="{RED}"/>
<circle cx="60" cy="38" r="9" fill="{RED}"/>
<line x1="56" y1="31" x2="50" y2="22" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<line x1="64" y1="31" x2="70" y2="22" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>
<path d="M40 54 Q18 46 12 62" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M80 54 Q102 46 108 62" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M40 70 Q20 70 14 84" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M80 70 Q100 70 106 84" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>
<line x1="60" y1="46" x2="60" y2="88" stroke="#f6ead2" stroke-width="2.5"/>
<circle cx="60" cy="16" r="7" fill="{GOLD}"/>'''
        return body
    if kind == "eye":
        return f'''<path d="M14 58 Q60 28 106 58 Q60 82 14 58 Z" fill="none" stroke="{INK}" stroke-width="6"/>
<circle cx="60" cy="56" r="13" fill="{RED}"/>
<path d="M14 58 Q8 52 10 44" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M74 70 Q78 92 62 96" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>
<path d="M88 66 L104 90" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>
<path d="M16 40 Q60 18 104 40" stroke="{INK}" stroke-width="5" fill="none"/>'''
    if kind == "lotus":
        petals = []
        import math
        for i, ang in enumerate(range(-60, 61, 24)):
            a = math.radians(ang)
            x = 60 + 44*math.sin(a); y = 70 - 48*math.cos(a)
            col = RED if i % 2 == 0 else GOLD
            petals.append(f'<path d="M60 86 Q{60+20*math.sin(a-0.5)} {70-30*math.cos(a-0.5)} {x:.0f} {y:.0f} Q{60+20*math.sin(a+0.5)} {70-30*math.cos(a+0.5)} 60 86 Z" fill="{col}" stroke="{INK}" stroke-width="2"/>')
        return ''.join(petals) + f'<path d="M60 86 L60 104" stroke="{INK}" stroke-width="5"/>'
    if kind == "anubis":
        return f'''<path d="M44 26 L54 52 L50 58 Z" fill="{INK}"/>
<path d="M76 26 L66 52 L70 58 Z" fill="{INK}"/>
<path d="M50 50 Q60 42 70 50 L88 72 Q92 78 84 80 L60 84 L40 66 Q44 54 50 50 Z" fill="{RED}"/>
<circle cx="64" cy="62" r="3.5" fill="#f6ead2"/>
<path d="M44 82 Q60 92 84 84 L84 100 Q60 108 44 100 Z" fill="{GOLD}"/>
<line x1="44" y1="90" x2="84" y2="90" stroke="{INK}" stroke-width="2.5"/>'''
    if kind == "cobra":
        return f'''<path d="M60 18 Q34 26 34 52 Q34 74 52 80 L52 94 Q40 98 40 104 L80 104 Q80 96 68 93 L68 80 Q86 74 86 52 Q86 26 60 18 Z" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>
<path d="M60 30 Q46 36 46 52 Q46 66 58 70 L58 92 L66 92 L66 70 Q74 64 74 52 Q74 36 60 30 Z" fill="{RED}"/>
<circle cx="56" cy="48" r="3" fill="#f6ead2"/><circle cx="66" cy="48" r="3" fill="#f6ead2"/>
<path d="M58 58 Q61 62 64 58" stroke="#f6ead2" stroke-width="2.5" fill="none"/>'''
    if kind == "fan":
        import math
        rays = []
        for i, ang in enumerate(range(-66, 67, 22)):
            a = math.radians(ang)
            x = 60 + 46*math.sin(a); y = 66 - 50*math.cos(a)
            col = RED if i % 2 else GOLD
            rays.append(f'<path d="M60 76 L{x-8*math.cos(a):.0f} {y-8*math.sin(a):.0f} A10 10 0 0 1 {x+8*math.cos(a):.0f} {y+8*math.sin(a):.0f} Z" fill="{col}" stroke="{INK}" stroke-width="2"/>')
        return ''.join(rays) + f'<circle cx="60" cy="78" r="7" fill="{INK}"/><line x1="60" y1="84" x2="60" y2="104" stroke="{INK}" stroke-width="5"/>'
    return ''

def card(name, kind):
    rows = ''.join(f'<tr><td class="n">{i}</td><td></td><td></td><td class="st"></td></tr>' for i in range(1, 8))
    return f'''<section class="card">
  <div class="frame">
    <div class="head">
      <div class="quest">КОД ПИРАМИД</div>
      <div class="sub">экспедиция доктора Камаля · плато Гиза</div>
    </div>
    <div class="emblem"><svg viewBox="0 0 120 120" width="100%" height="100%">{emblem(kind)}</svg></div>
    <div class="team">КОМАНДА «{name}»</div>
    <div class="goal">
      <p><b>Ваша цель:</b> открыть коробку с гербом команды.</p>
      <p>Код разобран на <b>семь находок</b>. Четыре спрятаны во лжи дневника, пятую отмерьте шагами, шестую разбейте, седьмую увидите только во тьме.</p>
      <p>Каждая находка говорит: какую шестерёнку крутить, до какой цифры, и какая это буква слова по счёту. Семь букв — слово. Слово — ключ.</p>
    </div>
    <table>
      <tr><th>№ буквы</th><th>Шестерёнка</th><th>Цифра</th><th>Печать</th></tr>
      {rows}
    </table>
    <div class="foot">Фишки ставим до проверки, все вместе. Ошибиться можно, остаться без финала нельзя.</div>
  </div>
</section>'''

CSS = f'''
@page{{size:148mm 210mm;margin:0}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:"Golos Text",Arial,sans-serif;color:{INK}}}
.card{{width:148mm;height:210mm;overflow:hidden;padding:7mm;background:#f3e6c9;page-break-after:always;position:relative}}
.card:last-child{{page-break-after:auto}}
.frame{{height:100%;border:1.2mm solid {RED};outline:0.4mm solid {RED};outline-offset:1.6mm;padding:6mm 7mm;display:flex;flex-direction:column;background:
 radial-gradient(120% 90% at 50% 0%, rgba(192,138,45,.14), transparent 60%)}}
.head{{text-align:center;border-bottom:0.5mm solid {RED};padding-bottom:3mm}}
.quest{{font-family:"Spectral",Georgia,serif;font-size:19pt;letter-spacing:.14em;color:{RED}}}
.sub{{font-size:8pt;letter-spacing:.08em;color:{INK};opacity:.75;margin-top:1mm}}
.emblem{{width:29mm;height:29mm;margin:3mm auto 1mm;background:#fdf6e6;border-radius:50%;border:0.8mm solid {RED};padding:3mm}}
.team{{text-align:center;font-family:"Spectral",Georgia,serif;font-size:14pt;letter-spacing:.08em;margin:1mm 0 2.5mm;color:{INK}}}
.goal p{{font-size:9.2pt;line-height:1.45;margin:0 0 1.5mm}}
table{{width:100%;border-collapse:collapse;margin-top:2mm}}
th{{font-size:7.6pt;letter-spacing:.08em;text-transform:uppercase;color:{RED};border-bottom:0.5mm solid {RED};padding:0 0 1.2mm;text-align:left}}
td{{border-bottom:0.3mm solid {GOLD};height:8.2mm}}
td.n{{width:12mm;color:{RED};font-family:"Spectral",Georgia,serif;font-size:12pt}}
td.st{{width:20mm;border-left:0.3mm dotted {GOLD}}}
.foot{{margin-top:auto;padding-top:2mm;border-top:0.5mm solid {RED};font-size:8pt;text-align:center;opacity:.85}}
'''

html = ('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Карточки команд</title>'
        '<link rel="stylesheet" href="fonts/local.css"><style>' + CSS + '</style></head><body>'
        + ''.join(card(n, k) for n, k in TEAMS) + '</body></html>')
pathlib.Path('giza-kartochki-komand.html').write_text(html, encoding='utf-8')
print('html ok')
