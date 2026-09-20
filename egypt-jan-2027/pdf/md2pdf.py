#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Превращает рабочий markdown в фирменный PDF La Royal Event.
Запуск: python3 md2pdf.py <file.md> "<Заголовок>" "<Подзаголовок>" <out.pdf>"""
import html, re, subprocess, sys, os, tempfile

CHROME = "/opt/pw-browsers/chromium"
HERE = os.path.dirname(os.path.abspath(__file__))

HEAD = """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>{title}</title><link rel="stylesheet" href="brand-print-full.css">
<style>
h3{{font-size:10.5pt; font-weight:700; margin:8pt 0 3pt; color:var(--ink)}}
h4{{font-size:9.6pt; font-weight:700; margin:6pt 0 2pt; color:var(--ink2)}}
blockquote{{background:var(--soft); border-left:2pt solid var(--violet); border-radius:0 3pt 3pt 0;
  padding:6pt 8pt; margin:6pt 0; font-size:9pt; page-break-inside:avoid}}
blockquote p:last-child{{margin-bottom:0}}
hr{{border:0; border-top:.6pt solid var(--line); margin:10pt 0}}
code{{font-family:"DejaVu Sans Mono",monospace; font-size:8.6pt; background:var(--soft2);
  padding:.5pt 3pt; border-radius:2pt}}
pre{{background:var(--soft2); border:.6pt solid var(--line); border-radius:3pt; padding:6pt 8pt;
  font-size:8.4pt; overflow-wrap:break-word; white-space:pre-wrap; page-break-inside:avoid}}
td,th{{vertical-align:top}}
a{{color:var(--violet-d); text-decoration:none}}
</style></head><body>
<div class="cover">
  <img src="img/logo1.png" alt="La Royal Event">
  <p class="eyebrow">Внутренний рабочий документ · Египет 2027</p>
  <h1>{h1}</h1>
  <p class="sub">{sub}</p>
  <div class="band">
    <span style="background:var(--violet); width:62mm"></span>
    <span style="background:var(--lime); width:22mm"></span>
    <span style="background:var(--pink); width:12mm"></span>
  </div>
</div>
"""
FOOT = """<footer>La Royal Event · Египет, январь 2027 · внутренний рабочий документ ·
не передавать клиенту без правки</footer></body></html>"""

def inline(t):
    t = html.escape(t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t, flags=re.S)
    t = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', t)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    return t

def convert(md):
    out, i, lines = [], 0, md.split('\n')
    def flush_para(buf):
        if buf: out.append('<p>' + inline(' '.join(buf)) + '</p>')
    while i < len(lines):
        ln = lines[i]
        if ln.startswith('```'):                                   # код
            i += 1; blk = []
            while i < len(lines) and not lines[i].startswith('```'):
                blk.append(lines[i]); i += 1
            out.append('<pre>' + html.escape('\n'.join(blk)) + '</pre>'); i += 1; continue
        if re.match(r'^\s*\|', ln) and i + 1 < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i+1]):
            rows = []                                              # таблица
            while i < len(lines) and re.match(r'^\s*\|', lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            head, body = rows[0], rows[2:]
            t = ['<table><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr>']
            for r in body:
                t.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
            out.append(''.join(t) + '</table>'); continue
        if ln.startswith('>'):                                     # цитата: склеиваем строки
            blk = []
            while i < len(lines) and lines[i].startswith('>'):
                blk.append(lines[i].lstrip('>').strip()); i += 1
            paras, cur = [], []
            for b in blk:
                if b: cur.append(b)
                elif cur: paras.append(' '.join(cur)); cur = []
            if cur: paras.append(' '.join(cur))
            out.append('<blockquote>' + ''.join(f'<p>{inline(p)}</p>' for p in paras) + '</blockquote>')
            continue
        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lvl = len(m.group(1)); txt = inline(m.group(2))
            out.append(f'<h{lvl}>{txt}</h{lvl}>'); i += 1; continue
        if re.match(r'^\s*[-*]{3,}\s*$', ln):
            out.append('<hr>'); i += 1; continue
        m = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', ln)
        if m:                                                      # список с продолжениями
            tag = 'ol' if m.group(2)[0].isdigit() else 'ul'
            items = []
            while i < len(lines):
                mm = re.match(r'^(\s*)([-*]|\d+\.)\s+(.*)$', lines[i])
                if mm:
                    items.append([mm.group(3)]); i += 1
                elif items and lines[i].strip() and lines[i].startswith((' ', '\t')):
                    items[-1].append(lines[i].strip()); i += 1
                else:
                    break
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(" ".join(it))}</li>' for it in items) + f'</{tag}>')
            continue
        if not ln.strip():
            i += 1; continue
        buf = []                                                   # абзац
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|\s*\||>|```|\s*[-*]\s|\s*\d+\.\s)', lines[i]):
            buf.append(lines[i].strip()); i += 1
        flush_para(buf)
    return '\n'.join(out)

def build(src, title, sub, out_pdf):
    md = open(src, encoding='utf-8').read()
    md = re.sub(r'^#\s+.*\n(##\s+.*\n)?', '', md, count=1)         # убираем дублирующий заголовок
    doc = HEAD.format(title=html.escape(title), h1=html.escape(title), sub=html.escape(sub)) \
          + convert(md) + FOOT
    tmp = os.path.join(HERE, '_md_tmp.html')
    open(tmp, 'w', encoding='utf-8').write(doc)
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox', '--no-pdf-header-footer',
                    '--virtual-time-budget=9000', f'--print-to-pdf={out_pdf}', 'file://' + tmp],
                   capture_output=True)
    os.remove(tmp)
    return out_pdf

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print('готово:', sys.argv[4])
