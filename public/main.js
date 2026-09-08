(function () {
  'use strict';
  var D = window.SITE || {};
  var $ = function (sel, root) { return (root || document).querySelector(sel); };

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') n.className = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
      else if (k === 'html') n.innerHTML = attrs[k];
      else if (k === 'style') n.style.cssText = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }

  // Медиа-слот: картинка, видео или плейсхолдер
  function media(item, ratio, label) {
    var box = el('div', { class: 'media', style: 'aspect-ratio:' + (ratio || '1/1') });
    var src = item && item.src;
    if (src && item.video) {
      var v = el('video', { src: src, muted: '', autoplay: '', loop: '', playsinline: '', preload: 'metadata' });
      v.muted = true;
      if (item.poster) v.setAttribute('poster', item.poster);
      box.appendChild(v);
    } else if (src) {
      box.appendChild(el('img', { src: src, alt: (item && item.title) || label || '', loading: 'lazy', decoding: 'async' }));
    } else {
      box.className += ' is-placeholder';
      box.setAttribute('data-label', label || '');
      box.setAttribute('role', 'img');
      box.setAttribute('aria-label', label || '');
    }
    return box;
  }

  // ---- Reel
  var reel = $('#reel');
  if (reel && D.reel) D.reel.forEach(function (it) {
    var m = media(it, it.ratio, it.placeholder);
    m.style.flexBasis = it.w; m.style.width = it.w;
    if (it.align) m.className += ' align-' + it.align;
    reel.appendChild(m);
  });

  // ---- Portrait
  var portrait = $('#portrait');
  if (portrait) portrait.appendChild(media(D.portrait || {}, '3/4', (D.portrait && D.portrait.placeholder) || 'Портрет'));

  // ---- Works
  var works = $('#works');
  if (works && D.rows) D.rows.forEach(function (row) {
    var strip = el('div', { class: 'work-strip' });
    (row.items || []).forEach(function (it) {
      var fig = el('figure', { style: 'width:' + row.w + ';--w:' + row.w });
      fig.appendChild(media(it, row.ratio, it.placeholder || row.placeholder));
      fig.appendChild(el('figcaption', null, [
        el('span', { text: it.title || '' }),
        el('span', { class: 'meta', text: it.meta || row.meta || '' })
      ]));
      strip.appendChild(fig);
    });
    works.appendChild(el('div', { class: 'work-row' }, [
      el('div', { class: 'work-head' }, [
        el('div', { class: 'work-num', text: row.num }),
        el('h3', { class: 'work-title', text: row.title }),
        el('p', { class: 'work-desc', text: row.desc })
      ]),
      strip
    ]));
  });

  // ---- Reviews + clients
  var rl = $('#reviews-list');
  if (rl && D.reviews) D.reviews.forEach(function (r) {
    var f = el('footer');
    f.appendChild(el('b', { text: r.name }));
    f.appendChild(document.createElement('br'));
    f.appendChild(document.createTextNode(r.role || ''));
    rl.appendChild(el('blockquote', { class: 'review' }, [el('p', { text: r.text }), f]));
  });
  var cl = $('#clients');
  if (cl && D.clients) D.clients.forEach(function (c) { cl.appendChild(el('span', { text: c })); });

  // ---- Prices (флаг showPrices)
  var pricesSec = $('#prices');
  if (pricesSec) {
    if (D.showPrices === false) {
      pricesSec.hidden = true;
      var pl = $('[data-prices-link]'); if (pl) pl.hidden = true;
    } else if (D.prices) {
      var list = $('#prices-list');
      D.prices.forEach(function (p) {
        list.appendChild(el('div', { class: 'price' }, [
          el('div', null, [el('div', { class: 'price-name', text: p.name }), el('div', { class: 'price-desc', text: p.desc })]),
          el('div', { class: 'price-value', text: p.price })
        ]));
      });
    }
  }

  // ---- Contacts / footer
  var c = D.contacts || {};
  var bc = $('#brief-contacts');
  if (bc) {
    if (c.email) bc.appendChild(el('a', { href: 'mailto:' + c.email, text: c.email }));
    if (c.telegram) bc.appendChild(el('a', { href: 'https://t.me/' + c.telegram, target: '_blank', rel: 'noopener', text: 'Telegram — @' + c.telegram }));
  }
  var fl = $('#footer-links');
  if (fl) {
    var links = [['Behance', c.behance], ['Telegram', c.telegram ? 'https://t.me/' + c.telegram : null], ['Instagram', c.instagram]];
    links.forEach(function (l) {
      if (!l[1] || l[1] === '#') return;
      fl.appendChild(el('a', { href: l[1], target: '_blank', rel: 'noopener', text: l[0] }));
    });
  }

  // ---- Chips (single-select toggle)
  var chips = $('#type-chips'), typeVal = $('#type-value');
  var currentType = null;
  if (chips && D.types) D.types.forEach(function (label) {
    var b = el('button', { type: 'button', class: 'chip', 'aria-pressed': 'false', text: label });
    b.addEventListener('click', function () {
      currentType = currentType === label ? null : label;
      Array.prototype.forEach.call(chips.children, function (ch) {
        ch.setAttribute('aria-pressed', ch.textContent === currentType ? 'true' : 'false');
      });
      typeVal.value = currentType || '';
    });
    chips.appendChild(b);
  });

  // ---- Form: loading / error / sent
  var form = $('#brief-form'), btn = $('#submit-btn'), errBox = $('#form-error'), thanks = $('#thanks');
  var ENDPOINT = (form && form.getAttribute('data-endpoint')) || '/api/brief';

  function showError(msg) { errBox.textContent = msg; errBox.hidden = false; }
  function hideError() { errBox.hidden = true; errBox.textContent = ''; }
  function setLoading(on) {
    btn.disabled = on; btn.classList.toggle('is-loading', on);
    form.setAttribute('aria-busy', on ? 'true' : 'false');
  }

  function validate() {
    var bad = [];
    ['name', 'contact', 'about'].forEach(function (n) {
      var f = form.elements[n];
      var ok = f.value.trim().length > 0;
      f.classList.toggle('is-invalid', !ok);
      if (!ok) bad.push(f);
    });
    if (bad.length) { bad[0].focus(); showError('Заполните, пожалуйста, имя, контакт и пару слов о проекте.'); }
    return bad.length === 0;
  }

  if (form) {
    ['name', 'contact', 'about'].forEach(function (n) {
      form.elements[n].addEventListener('input', function () { this.classList.remove('is-invalid'); if (!errBox.hidden) hideError(); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      hideError();
      if (!validate()) return;

      var payload = {
        name: form.elements.name.value.trim(),
        contact: form.elements.contact.value.trim(),
        type: currentType || '',
        about: form.elements.about.value.trim(),
        budget: form.elements.budget.value.trim(),
        website: form.elements.website.value, // honeypot
        page: location.href
      };

      setLoading(true);
      var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
      var timer = ctrl && setTimeout(function () { ctrl.abort(); }, 20000);

      fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(payload),
        signal: ctrl ? ctrl.signal : undefined
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          if (!res.ok || !data.ok) throw new Error(data.error || ('HTTP ' + res.status));
          form.hidden = true;
          thanks.hidden = false;
          thanks.setAttribute('tabindex', '-1'); thanks.focus();
        });
      }).catch(function (err) {
        var msg = err && err.name === 'AbortError'
          ? 'Сервер долго не отвечает. Попробуйте ещё раз или напишите напрямую' + (c.email ? ': ' + c.email : '.')
          : 'Не удалось отправить бриф' + (err && err.message && !/^HTTP|Failed to fetch|NetworkError/i.test(err.message) ? ': ' + err.message.replace(/[.\s]+$/, '') : '') + '. Попробуйте ещё раз или напишите напрямую' + (c.email ? ': ' + c.email : '.');
        showError(msg);
      }).then(function () {
        if (timer) clearTimeout(timer);
        setLoading(false);
      });
    });
  }
})();
