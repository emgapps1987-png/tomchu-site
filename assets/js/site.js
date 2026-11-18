/* Tomchu Tattoo – site behaviour. Vanilla, no dependencies. */
(() => {
  const d = document, root = d.documentElement;
  const WA = '972542885771';
  const store = {
    get(k, f) { try { const v = localStorage.getItem(k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } }
  };
  const $ = (s, el = d) => el.querySelector(s);
  const $$ = (s, el = d) => [...el.querySelectorAll(s)];
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || root.classList.contains('a-still');
  const wa = (text) => `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;
  root.classList.remove('no-js');

  /* ---------- theme ---------- */
  const themeBtn = $('.theme-btn');
  const syncTheme = () => {
    const light = root.classList.contains('light');
    if (themeBtn) { themeBtn.setAttribute('aria-pressed', String(light)); themeBtn.setAttribute('aria-label', light ? 'מעבר לתצוגה כהה' : 'מעבר לתצוגה בהירה'); }
    const m = $('meta[name="theme-color"]'); if (m) m.content = light ? '#F7F3EE' : '#0B0A0D';
  };
  themeBtn?.addEventListener('click', () => { root.classList.toggle('light'); store.set('tt-theme', root.classList.contains('light') ? 'light' : 'dark'); syncTheme(); });
  syncTheme();

  /* ---------- accessibility panel ---------- */
  const A = ['a-big', 'a-contrast', 'a-font', 'a-links', 'a-still'];
  const aBtn = $('#a11y-btn'), aPanel = $('#a11y-panel');
  const aSync = () => $$('[data-a]', aPanel).forEach((b) => b.setAttribute('aria-pressed', String(root.classList.contains(b.dataset.a))));
  const aSave = () => store.set('tt-a11y', A.filter((c) => root.classList.contains(c)));
  const aOpen = (o) => { aPanel.hidden = !o; aBtn.setAttribute('aria-expanded', String(o)); if (o) $('button', aPanel).focus(); };
  if (aBtn && aPanel) {
    aSync();
    aBtn.addEventListener('click', () => aOpen(aPanel.hidden));
    $('.x', aPanel).addEventListener('click', () => { aOpen(false); aBtn.focus(); });
    $$('[data-a]', aPanel).forEach((b) => b.addEventListener('click', () => { root.classList.toggle(b.dataset.a); aSync(); aSave(); if (b.dataset.a === 'a-still') stopMarquee(root.classList.contains('a-still')); }));
    $('.reset', aPanel).addEventListener('click', () => { A.forEach((c) => root.classList.remove(c)); aSync(); aSave(); stopMarquee(false); });
    d.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !aPanel.hidden) { aOpen(false); aBtn.focus(); } });
    $$('[data-open-a11y]').forEach((b) => b.addEventListener('click', () => aOpen(true)));
  }

  /* ---------- drawer menu ---------- */
  const drawer = $('#drawer'), menuBtns = $$('[data-menu]');
  let lastFocus = null;
  const drawerOpen = (o) => {
    if (!drawer) return;
    drawer.classList.toggle('open', o); drawer.hidden = !o;
    menuBtns.forEach((b) => b.setAttribute('aria-expanded', String(o)));
    d.body.style.overflow = o ? 'hidden' : '';
    if (o) { lastFocus = d.activeElement; $('.drawer-close', drawer).focus(); } else if (lastFocus) lastFocus.focus();
  };
  menuBtns.forEach((b) => b.addEventListener('click', () => drawerOpen(true)));
  drawer?.addEventListener('click', (e) => { if (e.target.matches('.drawer-bg, .drawer-close, .drawer-close *')) drawerOpen(false); });
  drawer?.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') drawerOpen(false);
    if (e.key === 'Tab') trap(e, $('.drawer-panel', drawer));
  });
  function trap(e, box) {
    const f = $$('a[href], button:not([disabled]), input, select, textarea', box).filter((x) => x.offsetParent !== null);
    if (!f.length) return; const first = f[0], last = f[f.length - 1];
    if (e.shiftKey && d.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && d.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  /* ---------- new page always opens at the top (also inside preview frames) ---------- */
  if (!location.hash) {
    try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch (e) {}
    const toTop = () => { try { window.scrollTo(0, 0); d.body.scrollIntoView({ block: 'start', behavior: 'instant' }); } catch (e) { window.scrollTo(0, 0); } };
    toTop(); window.addEventListener('load', toTop, { once: true });
  }

  /* ---------- reveal on scroll ---------- */
  const rises = $$('.rise');
  if ('IntersectionObserver' in window && !reduced()) {
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px' });
    rises.forEach((el) => io.observe(el));
  } else rises.forEach((el) => el.classList.add('in'));

  /* ---------- marquee pause ---------- */
  const mq = $('.marquee'), mqBtn = $('.mq-pause');
  function stopMarquee(p) { if (!mq) return; mq.classList.toggle('paused', p); mqBtn.setAttribute('aria-pressed', String(p)); mqBtn.textContent = p ? 'הפעלת תנועה' : 'השהיית תנועה'; }
  mqBtn?.addEventListener('click', () => stopMarquee(!mq.classList.contains('paused')));
  if (root.classList.contains('a-still')) stopMarquee(true);

  /* ---------- gallery: filters + lightbox ---------- */
  const gal = $('#gallery');
  if (gal) {
    const items = $$('li', gal), live = $('#gal-live');
    $$('.filters button').forEach((b) => b.addEventListener('click', () => {
      const f = b.dataset.f;
      $$('.filters button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      let n = 0; items.forEach((li) => { const show = f === 'all' || li.dataset.tag === f; li.hidden = !show; if (show) n++; });
      if (live) live.textContent = `מוצגות ${n} עבודות`;
    }));
    const lb = $('#lightbox'), lbImg = $('img', lb), lbCap = $('.lb-cap', lb), lbPos = $('.lb-pos', lb);
    let cur = 0, opener = null;
    const visible = () => items.filter((li) => !li.hidden);
    const show = (i) => {
      const v = visible(); cur = (i + v.length) % v.length; const btn = $('button', v[cur]);
      lbImg.src = btn.dataset.full; lbImg.alt = btn.dataset.alt; lbCap.textContent = btn.dataset.alt; lbPos.textContent = `${cur + 1} מתוך ${v.length}`;
    };
    const open = (i, el) => { opener = el; lb.classList.add('open'); lb.hidden = false; d.body.style.overflow = 'hidden'; show(i); $('.close', lb).focus(); };
    const close = () => { lb.classList.remove('open'); lb.hidden = true; d.body.style.overflow = ''; lbImg.removeAttribute('src'); opener?.focus(); };
    items.forEach((li) => $('button', li).addEventListener('click', (e) => open(visible().indexOf(li), e.currentTarget)));
    $('.close', lb).addEventListener('click', close);
    $('.prev', lb).addEventListener('click', () => show(cur - 1));
    $('.next', lb).addEventListener('click', () => show(cur + 1));
    lb.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(cur - 1);
      else if (e.key === 'ArrowLeft') show(cur + 1);
      else if (e.key === 'Tab') trap(e, lb);
    });
    let sx = null;
    lb.addEventListener('touchstart', (e) => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(dx > 0 ? cur + 1 : cur - 1); sx = null; });
  }

  /* ---------- before / after ---------- */
  $$('.compare').forEach((c) => {
    const r = $('input', c), set = () => { c.style.setProperty('--x', r.value + '%'); r.setAttribute('aria-valuetext', `${100 - r.value}% אחרי, ${r.value}% לפני`); };
    r.addEventListener('input', set); set();
  });

  /* ---------- studio tour ---------- */
  const tour = $('.tour-track');
  if (tour) {
    const slides = $$('li', tour), pos = $('.tour-ctl .pos');
    const idx = () => { const x = tour.getBoundingClientRect().right; let best = 0, bd = 1e9; slides.forEach((s, i) => { const dd = Math.abs(s.getBoundingClientRect().right - x); if (dd < bd) { bd = dd; best = i; } }); return best; };
    const go = (i) => { i = Math.max(0, Math.min(slides.length - 1, i)); slides[i].scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'nearest', inline: 'start' }); };
    const upd = () => { if (pos) pos.textContent = `${idx() + 1} / ${slides.length}`; };
    $('[data-tour="prev"]')?.addEventListener('click', () => go(idx() - 1));
    $('[data-tour="next"]')?.addEventListener('click', () => go(idx() + 1));
    tour.addEventListener('scroll', () => requestAnimationFrame(upd), { passive: true }); upd();
  }

  /* ---------- guide: which tattoo fits me ---------- */
  const guide = $('#guide-form');
  if (guide) {
    const PLACES = {
      wrist: { n: 'פרק כף היד', pain: 3, size: 'עד 7 ס״מ', fit: ['fine', 'letter', 'tiny'], zone: 'z-wrist' },
      forearm: { n: 'אמה', pain: 2, size: '5–18 ס״מ', fit: ['fine', 'real', 'color', 'sketch', 'letter'], zone: 'z-forearm' },
      upperarm: { n: 'זרוע עליונה', pain: 2, size: '8–20 ס״מ', fit: ['real', 'color', 'sketch', 'fine'], zone: 'z-arm' },
      shoulder: { n: 'כתף / עורף', pain: 2, size: '6–15 ס״מ', fit: ['fine', 'color', 'sketch'], zone: 'z-shoulder' },
      ear: { n: 'מאחורי האוזן', pain: 3, size: 'עד 4 ס״מ', fit: ['tiny', 'fine', 'letter'], zone: 'z-ear' },
      collar: { n: 'עצם הבריח', pain: 4, size: '4–12 ס״מ', fit: ['fine', 'letter'], zone: 'z-collar' },
      ribs: { n: 'צלעות', pain: 5, size: '6–25 ס״מ', fit: ['fine', 'letter', 'real'], zone: 'z-ribs' },
      back: { n: 'גב', pain: 3, size: '10–40 ס״מ', fit: ['real', 'color', 'sketch', 'fine'], zone: 'z-back' },
      thigh: { n: 'ירך', pain: 2, size: '10–25 ס״מ', fit: ['real', 'color', 'sketch', 'fine'], zone: 'z-thigh' },
      ankle: { n: 'קרסול', pain: 4, size: 'עד 8 ס״מ', fit: ['fine', 'tiny', 'color'], zone: 'z-ankle' }
    };
    const STYLES = {
      fine: { n: 'Fine Line – קו עדין', tag: 'fine', t: 1 }, real: { n: 'ריאליזם', tag: 'fine', t: 1.6 }, color: { n: 'צבע עדין', tag: 'color', t: 1.3 },
      sketch: { n: 'סקיצה / איור', tag: 'sketch', t: 1.2 }, letter: { n: 'כיתוב', tag: 'fine', t: .8 }, cover: { n: 'קאבר או צלקת', tag: 'ba', t: 1.5 }, tiny: { n: 'מיני', tag: 'fine', t: .7 }
    };
    const SIZES = { xs: { n: 'מיני (עד 4 ס״מ)', h: [0.5, 1] }, s: { n: 'קטן (4–8 ס״מ)', h: [1, 2] }, m: { n: 'בינוני (8–15 ס״מ)', h: [2, 3.5] }, l: { n: 'גדול (15+ ס״מ)', h: [3.5, 6] } };
    const SAMPLES = JSON.parse($('#guide-samples').textContent);
    const out = $('#guide-out');
    const fmtH = (h) => h < 1 ? `${Math.round(h * 60)} דקות` : (Number.isInteger(h) ? `${h}` : h.toFixed(1).replace('.0', '').replace('.5', '½')) + (h === 1 ? ' שעה' : ' שעות');
    const dots = (n) => `<span class="pain" aria-hidden="true">${[1, 2, 3, 4, 5].map((i) => `<i class="${i <= n ? 'on' : ''}"></i>`).join('')}</span>`;
    const PAINW = ['', 'כמעט לא מורגש', 'עדין', 'בינוני', 'מורגש', 'מורגש מאוד'];
    $$('.body-map .zone').forEach((z) => z.addEventListener('click', () => { const r = guide.querySelector(`input[name="place"][value="${z.dataset.place}"]`); if (r) { r.checked = true; r.dispatchEvent(new Event('change', { bubbles: true })); } }));
    const calc = () => {
      const fd = new FormData(guide), st = fd.get('style'), sz = fd.get('size'), pl = fd.get('place'), first = fd.get('first') === 'yes';
      $$('.body-map .zone').forEach((z) => z.classList.toggle('on', !!pl && z.id === PLACES[pl]?.zone));
      if (!st || !sz || !pl) { out.innerHTML = `<h2>ההמלצה שלך</h2><p class="empty">בחרו סגנון, גודל ומיקום – וההמלצה תופיע כאן מיד.</p>`; return; }
      const P = PLACES[pl], S = STYLES[st], Z = SIZES[sz];
      let [a, b] = Z.h.map((h) => Math.round(h * S.t * 2) / 2); a = Math.max(.5, a); b = Math.max(a + .5, b);
      const multi = b > 5;
      const fits = P.fit.includes(st) || (st === 'cover');
      const tips = [];
      if (!fits) tips.push(`${S.n} על ${P.n} אפשרי, אבל לרוב עובד טוב יותר באזור עם יותר מקום – תום תציע התאמה.`);
      if ((sz === 'xs') && (st === 'real' || st === 'color')) tips.push('בגודל מיני פרטים עדינים עלולים להיטשטש עם השנים – שווה לחשוב על הגדלה קטנה.');
      if (sz === 'l' && ['wrist', 'ear', 'ankle', 'collar'].includes(pl)) tips.push(`המיקום הזה מתאים בדרך כלל לגודל של ${P.size}. אפשר לפרוס את העיצוב לאזור סמוך.`);
      if (P.pain >= 4) tips.push('אזור רגיש יותר – עושים הפסקות לפי הצורך, בלי לחץ של זמן.');
      if (first) tips.push('קעקוע ראשון? מתחילים בשיחה וקפה. כדאי לבוא אחרי ארוחה טובה ושינה.');
      if (st === 'cover') tips.push('קאברים וצלקות הם אהבה גדולה של תום – שלחו תמונה של האזור כדי לקבל הערכה.');
      if (!tips.length) tips.push('שילוב מצוין – הסגנון, הגודל והמיקום עובדים יפה יחד.');
      const num = (h) => String(h).replace('.5', '½').replace(/^0½$/, '½');
      const rng = a < 1 ? `${fmtH(a)}–${fmtH(b)}` : `${num(a)}–${num(b)} שעות`;
      const sess = multi ? `${rng} (כנראה בשני מפגשים)` : rng;
      const pics = (SAMPLES[S.tag] || SAMPLES.fine).slice(0, 3);
      const msg = `היי תום! מילאתי את המדריך באתר 🙂\nסגנון: ${S.n}\nגודל: ${Z.n}\nמיקום: ${P.n}\n${first ? 'זה הקעקוע הראשון שלי.\n' : ''}הרעיון שלי: `;
      out.innerHTML = `<h2>ההמלצה שלך</h2>
        <p><b>${S.n}</b> בגודל ${Z.n.split(' (')[0]} על ${P.n}${fits ? ' – התאמה טובה.' : '.'}</p>
        <dl><dt>זמן משוער</dt><dd>${sess}</dd><dt>תחושה</dt><dd>${dots(P.pain)} ${PAINW[P.pain]}</dd><dt>גודל מומלץ לאזור</dt><dd>${P.size}</dd><dt>החלמה</dt><dd>${P.pain >= 4 || pl === 'ankle' ? '2–4 שבועות, לשמור מחיכוך' : '2–3 שבועות'}</dd></dl>
        <ul class="prose" style="margin:0;padding-inline-start:20px;color:var(--muted)">${tips.map((t) => `<li>${t}</li>`).join('')}</ul>
        <div class="thumbs">${pics.map((p) => `<img src="${p.src}" alt="${p.alt}" loading="lazy" width="200" height="200">`).join('')}</div>
        <a class="btn btn-iri" href="${wa(msg)}" target="_blank" rel="noopener">לשלוח לתום בוואטסאפ<span class="sr"> (נפתח בחלון חדש)</span></a>
        <p class="note">ההערכה כללית ונועדה לעזור בהתחלה. כל גוף שונה – תום תיתן הערכה מדויקת בשיחה.</p>`;
    };
    guide.addEventListener('change', calc); calc();
  }

  /* ---------- contact: WhatsApp message builder ---------- */
  const cf = $('#wa-form');
  if (cf) {
    const pv = $('#wa-preview');
    const build = () => {
      const f = new FormData(cf), L = [];
      L.push(`היי תום! ${f.get('name') ? `כאן ${f.get('name').trim()}. ` : ''}אשמח לקבוע שיחת ייעוץ לקעקוע.`);
      if (f.get('idea')?.trim()) L.push(`הרעיון: ${f.get('idea').trim()}`);
      if (f.get('place')) L.push(`מיקום על הגוף: ${f.get('place')}`);
      if (f.get('size')) L.push(`גודל: ${f.get('size')}`);
      if (f.get('when')) L.push(`נוח לי: ${f.get('when')}`);
      if (f.get('first')) L.push('זה הקעקוע הראשון שלי.');
      return L.join('\n');
    };
    const upd = () => { pv.textContent = build(); };
    cf.addEventListener('input', upd); upd();
    cf.addEventListener('submit', (e) => { e.preventDefault(); window.open(wa(build()), '_blank', 'noopener'); });
  }

  /* ---------- prefilled WhatsApp links ---------- */
  $$('[data-wa]').forEach((a) => { a.href = wa(a.dataset.wa); });
  $$('[data-year]').forEach((s) => { s.textContent = new Date().getFullYear(); });

  /* ---------- gift voucher: same backend & approval flow as the app ---------- */
  const giftBox = $('#gift');
  if (giftBox) {
    const C = JSON.parse($('#gift-cfg').textContent), MIN = C.min || 200, D = ['קשת', 'אמרלד', 'פוקסיה'], PAY = { bit: 'ביט', pbx: 'פייבוקס' };
    // Live only on the real site; previews and local tests never create real vouchers.
    const DEMO = !C.endpoint || !/(^|\.)tomchu-tattoo\.co\.il$/.test(location.hostname);
    const esc = (t) => String(t || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const nis = (n) => '₪' + Number(n || 0).toLocaleString('he-IL');
    const okPhone = (p) => /^0?5\d{8}$|^9725\d{8}$/.test(String(p || '').replace(/\D/g, ''));
    const intl = (p) => { const x = String(p || '').replace(/\D/g, ''); return x.startsWith('972') ? x : '972' + x.replace(/^0/, ''); };
    const wa = (num, t) => `https://wa.me/${num}?text=${encodeURIComponent(t)}`;
    const link = (code) => `${C.app}#/gift/${code}`;
    const fresh = () => ({ step: 1, amt: '', design: 0, to: '', from: '', phone: '', msg: '', send: 'me', toPhone: '', pay: 'bit' });
    let g = fresh(), V = null, timer = null;
    const card = (x, extra = '') => `<div class="gv gv-${x.design || 0} ${extra}" role="img" aria-label="שובר מתנה${x.amount ? ' על סך ' + nis(x.amount) : ''}">
      <img class="gv-bird" src="assets/img/logo-dark.png" alt="">
      <div class="gv-top"><span class="gv-brand" lang="en">Tomchu Tattoo</span><span class="gv-kind">שובר מתנה לקעקוע</span></div>
      <div class="gv-main">${x.to ? `<div class="gv-to"><span class="gv-for">עבור</span> ${esc(x.to)}</div>` : ''}<div class="gv-amt" dir="ltr">${x.amount ? nis(x.amount) : '₪—'}</div>${x.msg ? `<div class="gv-msg">${esc(x.msg)}</div>` : ''}</div>
      <div class="gv-foot">${x.from ? `<span class="gv-from">באהבה, ${esc(x.from)}</span>` : ''}<span class="gv-code" dir="ltr">${x.code || 'TT-••••••'}</span></div>
      ${extra === 'gv-pending' ? '<span class="gv-stamp">ממתין לאישור תשלום</span>' : ''}</div>`;
    const liveOf = () => ({ amount: parseInt(g.amt, 10) || 0, design: g.design, to: g.to, from: g.from, msg: g.msg });
    const prog = () => `<div class="gift-prog" aria-hidden="true">${[1, 2, 3].map((i) => `<i class="${i <= g.step ? 'on' : ''}"></i>`).join('')}</div>`;
    const demoNote = DEMO ? '<p class="gift-demo">תצוגה מקדימה: כאן לא נשמר שובר ולא מתבצע תשלום.</p>' : '';
    function form() {
      const a = parseInt(g.amt, 10) || 0; let b = '';
      if (g.step === 1) b = `<div id="g-live">${card(liveOf())}</div>
        <div class="stack" style="gap:8px"><label class="lbl" for="g-amt">על איזה סכום השובר?</label>
          <div class="gift-amt" id="g-amt-box"><button type="button" class="gift-step" data-st="50" aria-label="הוספת 50 ש״ח">+</button>
          <span class="gift-amt-in"><span aria-hidden="true">₪</span><input id="g-amt" inputmode="numeric" autocomplete="off" placeholder="${MIN}" value="${esc(g.amt)}" aria-describedby="g-amt-h"></span>
          <button type="button" class="gift-step" data-st="-50" aria-label="הורדת 50 ש״ח">−</button></div>
          <p class="hint" id="g-amt-h" style="text-align:center">מינימום ${nis(MIN)} · כל סכום מעל זה</p><p class="err" id="g-amt-err" role="alert"></p></div>
        <div class="stack" style="gap:8px"><span class="lbl" id="g-des-l">עיצוב</span><div class="gift-designs" role="group" aria-labelledby="g-des-l">${D.map((n, i) => `<button type="button" data-des="${i}" aria-pressed="${g.design === i}"><span class="gv gv-${i} gv-mini"><img class="gv-bird" src="assets/img/logo-dark.png" alt=""></span>${n}</button>`).join('')}</div></div>`;
      if (g.step === 2) b = `<div id="g-live">${card(liveOf())}</div>
        <div class="stack" style="gap:6px"><label class="lbl" for="g-to">שם המקבל/ת</label><input class="fld" id="g-to" maxlength="40" value="${esc(g.to)}" autocomplete="off"><p class="err" id="g-to-err"></p></div>
        <div class="stack" style="gap:6px"><label class="lbl" for="g-from">השם שלך</label><input class="fld" id="g-from" maxlength="40" value="${esc(g.from)}" autocomplete="name"><p class="err" id="g-from-err"></p></div>
        <div class="stack" style="gap:6px"><label class="lbl" for="g-phone">הטלפון שלך</label><input class="fld" id="g-phone" type="tel" inputmode="tel" dir="ltr" maxlength="20" value="${esc(g.phone)}" autocomplete="tel" aria-describedby="g-phone-h"><p class="hint" id="g-phone-h">כדי שתום תזהה את ההעברה ותוכל לחזור אליך</p><p class="err" id="g-phone-err"></p></div>
        <div class="stack" style="gap:6px"><label class="lbl" for="g-msg">הקדשה (לא חובה)</label><textarea class="fld" id="g-msg" rows="2" maxlength="90">${esc(g.msg)}</textarea></div>
        <div class="stack" style="gap:8px"><span class="lbl" id="g-send-l">איך לשלוח את השובר?</span><div class="grid2" role="group" aria-labelledby="g-send-l">
          <button type="button" class="gift-opt" data-send="me" aria-pressed="${g.send === 'me'}"><b>אשלח בעצמי</b><small>תקבלו את השובר ותעבירו</small></button>
          <button type="button" class="gift-opt" data-send="them" aria-pressed="${g.send === 'them'}"><b>ישר אליה/יו</b><small>בוואטסאפ למקבל/ת</small></button></div>
          ${g.send === 'them' ? `<label class="lbl" for="g-tophone" style="margin-top:4px">הטלפון של המקבל/ת</label><input class="fld" id="g-tophone" type="tel" inputmode="tel" dir="ltr" maxlength="20" value="${esc(g.toPhone)}" autocomplete="off"><p class="err" id="g-tophone-err"></p>` : ''}</div>`;
      if (g.step === 3) b = `<div class="gift-rows"><div><span>שובר מתנה</span><b dir="ltr">${nis(a)}</b></div><div><span>למי</span><b>${esc(g.to)}</b></div><div><span>שליחה</span><b>${g.send === 'me' ? 'אליי' : 'ישר בוואטסאפ'}</b></div><div><span>תוקף</span><b>5 שנים מיום ההנפקה</b></div><div class="tot"><span>לתשלום</span><b dir="ltr">${nis(a)}</b></div></div>
        <div class="stack" style="gap:8px"><span class="lbl" id="g-pay-l">איך משלמים?</span><div class="gift-pay" role="group" aria-labelledby="g-pay-l">
          <button type="button" data-pay="bit" aria-pressed="${g.pay === 'bit'}"><span class="gp-ico gp-bit" lang="en">bit</span>ביט</button>
          <button type="button" data-pay="pbx" aria-pressed="${g.pay === 'pbx'}"><span class="gp-ico gp-pbx" lang="en">PayBox</span>פייבוקס</button></div></div>
        <div class="gift-how"><b>מה קורה עכשיו?</b><ol><li>השובר נשמר ומחכה לתשלום.</li><li>מעבירים את הסכום לתום באפליקציה שבחרתם.</li><li>תום רואה את ההעברה ומאשרת, והשובר נפתח.</li></ol></div>
        <details class="gift-how"><summary><b>תנאי השובר ופרטי העסק</b></summary><ul style="margin:8px 0 0;padding-inline-start:20px;color:var(--muted);display:grid;gap:4px">
          <li>השובר בתוקף 5 שנים מיום ההנפקה, וניתן לממש אותו בכל קעקוע או שירות בסטודיו, גם בזמן מבצעים, עד מלוא הסכום ששולם.</li>
          <li>אפשר לממש בכמה פעמים. אם נשארת יתרה של עד 5% מהסכום או 100 ₪ (הנמוך מביניהם) – היא מוחזרת במזומן.</li>
          <li>אפשר לבטל את הקנייה תוך 14 יום, בהודעה בוואטסאפ, בטלפון או במייל. ההחזר יינתן תוך 14 יום, בניכוי דמי ביטול של 5% או 100 ₪ (הנמוך מביניהם).</li>
          <li>${esc(C.name)}${C.biz ? ' · עוסק מס׳ ' + esc(C.biz) : ''} · ${esc(C.addr)} · <span dir="ltr">${esc(C.phone)}</span> · ${esc(C.mail)}</li>
        </ul></details>
        <p class="hint">הפרטים שמילאת נשמרים רק לצורך הנפקת השובר, זיהוי ההעברה ומשלוח השובר. <a href="privacy.html">מדיניות הפרטיות</a></p><p class="err" id="g-send-err" role="alert"></p>`;
      const nx = g.step === 1 ? (a ? `המשך · ${nis(a)}` : 'המשך') : g.step === 2 ? 'להמשך לתשלום' : 'אישור והמשך לתשלום';
      giftBox.innerHTML = `<div class="stack" style="gap:10px"><h2>${['', 'שובר מתנה', 'למי השובר?', 'תשלום'][g.step]}</h2>${prog()}</div>${b}
        <div class="stack" style="gap:10px"><button type="button" class="btn-gift" id="g-next">${nx}</button>${g.step > 1 ? '<button type="button" class="btn-out" id="g-prev">חזרה</button>' : ''}</div>${demoNote}`;
      bindForm();
    }
    const live = () => { const l = $('#g-live'); if (l) l.innerHTML = card(liveOf()); const a = parseInt(g.amt, 10) || 0; if (g.step === 1) $('#g-next').textContent = a ? `המשך · ${nis(a)}` : 'המשך'; };
    const bad = (id, t) => { const f = $('#' + id); f.setAttribute('aria-invalid', 'true'); $('#' + id + '-err').textContent = t; return f; };
    function bindForm() {
      $('#g-amt')?.addEventListener('input', (e) => { g.amt = e.target.value.replace(/\D/g, '').slice(0, 5); e.target.value = g.amt; $('#g-amt-box').classList.remove('bad'); $('#g-amt-err').textContent = ''; live(); });
      $$('[data-st]').forEach((b) => b.addEventListener('click', () => { g.amt = String(Math.max(MIN, (parseInt(g.amt, 10) || 0) + +b.dataset.st)); $('#g-amt').value = g.amt; live(); }));
      $$('[data-des]').forEach((b) => b.addEventListener('click', () => { g.design = +b.dataset.des; $$('[data-des]').forEach((x) => x.setAttribute('aria-pressed', String(x === b))); live(); }));
      [['g-to', 'to'], ['g-from', 'from'], ['g-phone', 'phone'], ['g-msg', 'msg'], ['g-tophone', 'toPhone']].forEach(([id, k]) => $('#' + id)?.addEventListener('input', (e) => { g[k] = e.target.value; e.target.removeAttribute('aria-invalid'); const er = $('#' + id + '-err'); if (er) er.textContent = ''; live(); }));
      $$('[data-send]').forEach((b) => b.addEventListener('click', () => { g.send = b.dataset.send; form(); }));
      $$('[data-pay]').forEach((b) => b.addEventListener('click', () => { g.pay = b.dataset.pay; $$('[data-pay]').forEach((x) => x.setAttribute('aria-pressed', String(x === b))); }));
      $('#g-prev')?.addEventListener('click', () => { g.step--; form(); });
      $('#g-next').addEventListener('click', next);
    }
    async function next() {
      const a = parseInt(g.amt, 10) || 0;
      if (g.step === 1) { if (a < MIN) { $('#g-amt-box').classList.add('bad'); $('#g-amt-err').textContent = a ? `הסכום המינימלי לשובר הוא ${nis(MIN)}` : 'כתבו סכום לשובר'; $('#g-amt').focus(); return; } g.step = 2; form(); giftBox.scrollIntoView({ block: 'start' }); return; }
      if (g.step === 2) {
        const errs = [];
        if (!g.to.trim()) errs.push(bad('g-to', 'כתבו למי השובר'));
        if (!g.from.trim()) errs.push(bad('g-from', 'כתבו את השם שלך'));
        if (!okPhone(g.phone)) errs.push(bad('g-phone', 'כתבו מספר טלפון תקין'));
        if (g.send === 'them' && !okPhone(g.toPhone)) errs.push(bad('g-tophone', 'כתבו מספר טלפון תקין'));
        if (errs.length) { errs[0].focus(); return; }
        g.step = 3; form(); giftBox.scrollIntoView({ block: 'start' }); return;
      }
      const btn = $('#g-next'); btn.disabled = true; btn.textContent = 'שומר את השובר…';
      const meta = { pay: g.pay, toPhone: g.send === 'them' ? g.toPhone : '' };
      try {
        let code;
        if (DEMO) { code = 'TT-' + Math.random().toString(36).slice(2, 8).toUpperCase(); V = { ok: true, code, status: 'pending', amount: a, design: g.design, to: g.to.trim(), from: g.from.trim(), msg: g.msg.trim() }; }
        else {
          const r = await fetch(C.endpoint, { method: 'POST', body: JSON.stringify({ kind: 'gift', amount: a, design: g.design, from: g.from.trim(), phone: g.phone, to: g.to.trim(), toPhone: meta.toPhone, msg: g.msg.trim(), pay: g.pay, src: 'site' }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } }).then((x) => x.json());
          if (!r.ok) throw new Error(r.error); code = r.code;
        }
        try { localStorage.setItem('tt-gift-meta-' + code, JSON.stringify(meta)); } catch (e) {}
        g = fresh(); history.replaceState(null, '', '#' + code.toLowerCase()); status(code);
      } catch (e) { btn.disabled = false; btn.textContent = 'אישור והמשך לתשלום'; $('#g-send-err').textContent = 'לא הצלחנו לשמור את השובר. בדקו את החיבור לאינטרנט ונסו שוב.'; }
    }
    async function status(code) {
      clearTimeout(timer); code = code.toUpperCase();
      let v = V && V.code === code ? V : null;
      if (!v && !DEMO) { try { v = await fetch(`${C.endpoint}?action=gift&code=${encodeURIComponent(code)}`).then((r) => r.json()); } catch (e) { v = { ok: false, net: true }; } }
      if (!v || !v.ok) { giftBox.innerHTML = `<h2>${v && v.net ? 'אין חיבור כרגע' : 'השובר לא נמצא'}</h2><p class="hint">אפשר לנסות שוב, או לכתוב לתום בוואטסאפ.</p><a class="btn-out" href="${wa(C.wa, 'היי תום, יש לי שאלה לגבי שובר מתנה ' + code)}" target="_blank" rel="noopener">וואטסאפ לתום</a><button type="button" class="btn-gift" id="g-new">לשובר חדש</button>`; $('#g-new').onclick = () => { history.replaceState(null, '', location.pathname); form(); }; return; }
      let meta = {}; try { meta = JSON.parse(localStorage.getItem('tt-gift-meta-' + code) || '{}'); } catch (e) {}
      if (v.status === 'pending') {
        const pay = PAY[meta.pay] || 'ביט / פייבוקס', url = (C.pay || {})[meta.pay] || '';
        giftBox.innerHTML = `<h2>כמעט שם!</h2>${card(v, 'gv-pending')}
          <div class="gift-status wait" role="status"><span class="dot" aria-hidden="true"></span><span>ממתין שתום תאשר את התשלום</span></div>
          <div class="gift-paybox stack" style="gap:10px"><p>מעבירים <b dir="ltr">${nis(v.amount)}</b> ב${pay} לתום גבע:</p>
            ${url ? `<a class="btn-gift" href="${esc(url)}" target="_blank" rel="noopener">לתשלום ב${pay}</a><p class="hint">אם האפליקציה לא נפתחה – אפשר להעביר ידנית למספר:</p>` : ''}
            <div class="gift-num"><b dir="ltr">${C.phone}</b><button type="button" class="btn-out sm" id="g-copy">העתקת המספר</button></div>
            <p class="hint">כדאי לכתוב בהערה להעברה: שובר <span dir="ltr">${v.code}</span></p></div>
          <p class="hint">אחרי שתום רואה את ההעברה היא מאשרת, והשובר נפתח כאן. אפשר לסגור את הדף ולחזור אחר כך מאותו קישור.</p>
          ${DEMO ? '<button type="button" class="btn-out" id="g-sim">תצוגה מקדימה: לדמות אישור של תום</button>' : '<button type="button" class="btn-out" id="g-check">לבדוק אם השובר אושר</button>'}${demoNote}`;
        $('#g-copy').onclick = async () => { try { await navigator.clipboard.writeText(C.phone.replace(/-/g, '')); $('#g-copy').textContent = 'הועתק ✓'; } catch (e) { $('#g-copy').textContent = C.phone; } };
        $('#g-check')?.addEventListener('click', () => status(code));
        $('#g-sim')?.addEventListener('click', () => { V.status = 'active'; status(code); });
        if (!DEMO) timer = setTimeout(() => status(code), 30000);
        return;
      }
      if (v.status === 'active') {
        const share = `${v.to ? v.to + ', ' : ''}קיבלת שובר מתנה לקעקוע אצל תום ב־Tomchu Tattoo 🎁\n${link(v.code)}`;
        giftBox.innerHTML = `<h2>השובר פעיל! 🎉</h2><div class="gv-reveal">${card(v)}</div>
          <div class="gift-status ok" role="status"><span class="dot" aria-hidden="true"></span><span>תום אישרה את התשלום. תודה!</span></div>
          ${meta.toPhone ? `<a class="btn-gift" href="${wa(intl(meta.toPhone), share)}" target="_blank" rel="noopener">לשלוח את השובר בוואטסאפ</a>` : `<a class="btn-gift" href="https://wa.me/?text=${encodeURIComponent(share)}" target="_blank" rel="noopener">להעביר את השובר בוואטסאפ</a>`}
          <a class="btn-out" href="${link(v.code)}" target="_blank" rel="noopener">לפתוח את השובר</a>${demoNote}`;
        return;
      }
      giftBox.innerHTML = `<h2>${{ used: 'השובר מומש', expired: 'תוקף השובר פג', cancel: 'השובר בוטל' }[v.status] || 'השובר'}</h2>${card(v, 'gv-off')}<a class="btn-out" href="${wa(C.wa, 'היי תום, לגבי שובר מתנה ' + code)}" target="_blank" rel="noopener">שאלה לתום בוואטסאפ</a>`;
    }
    const h = (location.hash || '').match(/^#(tt-[a-z0-9]{4,8})$/i);
    if (h && !DEMO) status(h[1]); else form();
  }

  /* ---------- health declaration (same questions + backend as the app) ---------- */
  if ($('#health-form')) {
    const H = JSON.parse($('#health-cfg').textContent), QS = H.questions, CONS = H.consents;
    const DEMO = !H.endpoint || !/(^|\.)tomchu-tattoo\.co\.il$/.test(location.hostname);
    const f = $('#health-form'), done = $('#health-done'), F = (n) => f.elements[n];
    const val = (n) => (F(n) && F(n).value || '').trim();
    const esc = (t) => String(t == null ? '' : t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const ageFrom = (iso) => { if (!iso) return null; const b = new Date(iso); if (isNaN(b)) return null; const t = new Date(); let a = t.getFullYear() - b.getFullYear(); if (t.getMonth() < b.getMonth() || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--; return a; };
    const validId = (v) => { const id = String(v || '').replace(/\D/g, ''); if (id.length < 5 || id.length > 9) return false; const p = id.padStart(9, '0'); let s = 0; for (let i = 0; i < 9; i++) { const x = Number(p[i]) * ((i % 2) + 1); s += x > 9 ? x - 9 : x; } return s % 10 === 0; };
    const validPhone = (v) => /^(?:0|\+?972-?)5\d-?\d{3}-?\d{4}$|^0\d{1,2}-?\d{7}$/.test(String(v || '').replace(/\s/g, ''));
    const today = () => { const x = new Date(); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 10); };
    if (!val('tdate')) F('tdate').value = today();
    const DRAFT = 'tt-health-draft';
    const saveDraft = () => { const o = {}; [...f.elements].forEach((el) => { if (!el.name || el.type === 'checkbox') return; if (el.type === 'radio') { if (el.checked) o[el.name] = el.value; } else o[el.name] = el.value; }); try { sessionStorage.setItem(DRAFT, JSON.stringify(o)); } catch (e) {} };
    try { const o = JSON.parse(sessionStorage.getItem(DRAFT) || 'null'); if (o) Object.keys(o).forEach((k) => { const el = F(k); if (!el) return; if (el.length && el[0] && el[0].type === 'radio') [...el].forEach((r) => { r.checked = r.value === o[k]; }); else el.value = o[k]; }); } catch (e) {}
    const setErr = (id, msg) => { const el = $('#' + id), er = $('#' + id + '-err'); if (er) er.textContent = msg; if (el) el.setAttribute('aria-invalid', msg ? 'true' : 'false'); return msg ? el : null; };
    const showQ = (q) => { const yes = (F(q.id).value || '') === 'כן'; $('#qn-' + q.id).hidden = !yes; $('#qdw-' + q.id).hidden = !yes; };
    QS.forEach(showQ);
    const minor = () => { const a = ageFrom(val('dob')); const m = a !== null && a < 18; $('#minor-note').hidden = !m; $('#parent-block').hidden = !m; $('#sig-who').textContent = m ? 'חתימת ההורה' : 'חתימה'; return m; };
    f.addEventListener('input', saveDraft);
    f.addEventListener('change', (e) => { saveDraft(); minor(); const q = QS.find((x) => x.id === e.target.name); if (q) { showQ(q); $('#fs-' + q.id).classList.remove('invalid'); } });

    /* signature */
    const cv = $('#sig'), ph = $('#sig-ph'), ctx = cv.getContext('2d'); let empty = true, drawing = false, last = null;
    const sizeSig = () => { const r = cv.getBoundingClientRect(); if (!r.width) return; const k = window.devicePixelRatio || 1; cv.width = Math.round(r.width * k); cv.height = Math.round(r.height * k); ctx.setTransform(k, 0, 0, k, 0, 0); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, r.width, r.height); ctx.lineWidth = 2.6; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = '#1E1A21'; empty = true; ph.hidden = false; };
    const pos = (e) => { const r = cv.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; };
    cv.addEventListener('pointerdown', (e) => { drawing = true; last = pos(e); cv.setPointerCapture(e.pointerId); ctx.beginPath(); ctx.arc(last.x, last.y, 1.2, 0, Math.PI * 2); ctx.fillStyle = '#1E1A21'; ctx.fill(); empty = false; ph.hidden = true; $('#h-sig-err').textContent = ''; });
    cv.addEventListener('pointermove', (e) => { if (!drawing) return; const p = pos(e); ctx.beginPath(); ctx.moveTo(last.x, last.y); ctx.lineTo(p.x, p.y); ctx.stroke(); last = p; });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach((t) => cv.addEventListener(t, () => { drawing = false; }));
    $('#sig-clear').addEventListener('click', sizeSig);

    let step = 1;
    const go = (n, quiet) => {
      step = Math.min(3, Math.max(1, n));
      $$('.hstep', f).forEach((s) => { s.hidden = Number(s.dataset.step) !== step; });
      $$('.hsteps li').forEach((li) => { const k = Number(li.dataset.s); li.classList.toggle('on', k === step); li.classList.toggle('ok', k < step); if (k === step) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); });
      $('#h-stepnow').textContent = `שלב ${step} מתוך 3`;
      $('#h-prev').hidden = step === 1;
      $('#h-next').textContent = step === 3 ? 'שליחה לתום' : 'המשך';
      if (step === 3) { minor(); requestAnimationFrame(sizeSig); }
      if (quiet) return;
      const top = $('.phead') || f; top.scrollIntoView({ block: 'start', behavior: reduced() ? 'auto' : 'smooth' });
    };
    $('#h-prev').addEventListener('click', () => go(step - 1));
    const validate = () => {
      const errs = [];
      if (step === 1) {
        errs.push(setErr('h-name', val('name').length >= 2 ? '' : 'נא למלא שם מלא'));
        errs.push(setErr('h-id', !val('idnum') || validId(val('idnum')) ? '' : 'מספר תעודת הזהות לא תקין'));
        const a = ageFrom(val('dob'));
        errs.push(setErr('h-dob', a === null ? 'נא לבחור תאריך לידה' : (a < 14 || a > 110) ? 'נא לבדוק את תאריך הלידה' : ''));
        errs.push(setErr('h-phone', validPhone(val('phone')) ? '' : 'נא למלא מספר טלפון תקין'));
        errs.push(setErr('h-address', val('address').length >= 4 ? '' : 'נא למלא כתובת מגורים'));
        errs.push(setErr('h-design', val('design').length >= 2 ? '' : 'ספרו בכמה מילים מה מקעקעים'));
        errs.push(setErr('h-ephone', !val('ephone') || validPhone(val('ephone')) ? '' : 'מספר הטלפון לא תקין'));
      }
      if (step === 2) {
        let first = null, msg = '';
        QS.forEach((q) => {
          const a = F(q.id).value || '', needs = a === 'כן' && q.level !== 'stop' && !val('d_' + q.id);
          $('#fs-' + q.id).classList.toggle('invalid', !a || needs);
          if (!a && !first) { first = F(q.id)[0]; msg = 'נא לענות על כל השאלות'; }
          if (needs && !first) { first = F('d_' + q.id); msg = 'סימנת "כן", נא לפרט בתיבה שמתחת לשאלה'; }
        });
        $('#h-q-err').textContent = msg; errs.push(first);
      }
      if (step === 3) {
        const m = minor();
        if (m) {
          errs.push(setErr('h-pname', val('pname').length >= 2 ? '' : 'נא למלא את שם ההורה'));
          errs.push(setErr('h-pid', validId(val('pid')) ? '' : 'מספר תעודת הזהות לא תקין'));
          errs.push(setErr('h-pphone', validPhone(val('pphone')) ? '' : 'נא למלא מספר טלפון תקין'));
        }
        const miss = CONS.filter((c) => c.required && (!c.minorOnly || m) && !F(c.id).checked);
        $('#h-c-err').textContent = miss.length ? 'נא לאשר את כל סעיפי החובה' : '';
        errs.push(miss.length ? F(miss[0].id) : null);
        $('#h-sig-err').textContent = empty ? 'נא לחתום' : '';
        errs.push(empty ? cv : null);
      }
      const first = errs.find(Boolean);
      if (first) { if (first.focus) first.focus(); if (first.scrollIntoView) first.scrollIntoView({ block: 'center' }); return false; }
      return true;
    };

    let rec = null;
    const record = () => {
      const age = ageFrom(val('dob')), m = age < 18, ans = (q) => F(q.id).value || '';
      const r = {
        submittedAt: new Date().toISOString(), submittedAtText: new Date().toLocaleString('he-IL', { dateStyle: 'short', timeStyle: 'short' }),
        name: val('name'), idnum: val('idnum'), dob: val('dob'), age, phone: val('phone'), email: val('email'),
        tattooDate: val('tdate'), area: val('area'), address: val('address'), design: val('design'),
        emergency: val('ename') || val('ephone') ? { name: val('ename'), phone: val('ephone') } : null,
        answers: QS.map((q) => ({ id: q.id, q: q.text, a: ans(q), detail: ans(q) === 'כן' ? val('d_' + q.id) : '' })),
        details: QS.filter((q) => ans(q) === 'כן' && val('d_' + q.id)).map((q) => `• ${q.text.replace(/\?$/, '')}: ${val('d_' + q.id)}`).join('\n'),
        consents: CONS.filter((c) => !c.minorOnly || m).map((c) => ({ id: c.id, text: c.text, ok: !!F(c.id).checked })),
        minor: m, parent: m ? { name: val('pname'), id: val('pid'), phone: val('pphone') } : null,
        signature: cv.toDataURL('image/png')
      };
      r.flags = QS.filter((q) => ans(q) === 'כן').map((q) => ({ level: q.level, q: q.text, note: q.note }));
      if (m) r.flags.push({ level: 'check', q: `קטין/ה (גיל ${age})`, note: 'לוודא שההורה נוכח/ת בסטודיו ומציג/ה תעודה מזהה.' });
      r.review = r.flags.some((x) => x.level === 'stop') ? 'stop' : r.flags.length ? 'check' : '';
      r.extraFields = [{ label: 'כתובת מגורים', value: r.address }, { label: 'מה מקעקעים', value: r.design },
        { label: 'איש קשר לחירום', value: r.emergency ? [r.emergency.name, r.emergency.phone].filter(Boolean).join(' · ') : '' }, { label: 'נשלח דרך', value: 'האתר' }].filter((x) => x.value);
      return r;
    };
    const summary = (r) => [`הצהרת בריאות – ${r.name}`, `טלפון: ${r.phone}`, `תאריך לידה: ${r.dob}`, `מה מקעקעים: ${r.design}`, '', ...r.answers.filter((a) => a.a === 'כן').map((a) => `כן: ${a.q}${a.detail ? ' – ' + a.detail : ''}`), r.answers.some((a) => a.a === 'כן') ? '' : 'כל התשובות: לא', '', '(החתימה לא נשלחת בוואטסאפ, אחתום שוב בסטודיו)'].join('\n');
    const showDone = (ok) => {
      const rv = rec.review;
      f.hidden = true; done.hidden = false;
      done.innerHTML = ok ? `<span class="hdone-ic" aria-hidden="true">✓</span><h2>ההצהרה נשלחה, <span class="iri-text">תודה!</span></h2>
        <p>ההצהרה החתומה הגיעה לתום. נתראה בסטודיו!</p>
        ${rv ? `<p class="qn qn-${rv}">${rv === 'stop' ? 'סימנת תשובה שבגללה לא מקעקעים עד בירור. תום תיצור איתך קשר.' : 'סימנת כמה תשובות שתום תעבור עליהן לפני התור. אם צריך, היא תיצור איתך קשר.'}</p>` : ''}
        <p class="hnote"><b>לפני שמגיעים:</b> לאכול ארוחה טובה, לשתות מים, ולא לשתות אלכוהול יום לפני.</p>
        ${DEMO ? '<p class="gift-demo">תצוגה מקדימה: ההצהרה לא נשלחה באמת.</p>' : ''}
        <div class="hacts"><a class="btn btn-soft" href="process.html">הוראות לפני ואחרי</a><a class="btn btn-iri" href="index.html">חזרה לאתר</a></div>`
        : `<span class="hdone-ic bad" aria-hidden="true">!</span><h2>לא הצלחנו לשלוח את ההצהרה</h2>
        <p>אולי אין כרגע אינטרנט. אפשר לנסות שוב, או לשלוח לתום את הסיכום בוואטסאפ.</p>
        <div class="hacts"><button type="button" class="btn btn-iri" id="h-retry">לנסות לשלוח שוב</button><a class="btn btn-soft" href="${wa(summary(rec))}" target="_blank" rel="noopener">שליחת סיכום בוואטסאפ<span class="sr"> (נפתח בחלון חדש)</span></a></div>`;
      done.focus(); done.scrollIntoView({ block: 'start' });
      const rt = $('#h-retry'); if (rt) rt.addEventListener('click', () => send());
    };
    const send = async () => {
      const btn = $('#h-next'); btn.disabled = true; btn.textContent = 'שולחים לתום…';
      let ok = true;
      if (!DEMO) {
        try {
          const r = await fetch(H.endpoint, { method: 'POST', body: JSON.stringify({ kind: 'health', ...rec }), headers: { 'Content-Type': 'text/plain;charset=utf-8' } });
          const j = await r.json().catch(() => ({ ok: true })); ok = r.ok && !(j && j.ok === false);
        } catch (e) { ok = false; }
      } else await new Promise((r) => setTimeout(r, 700));
      btn.disabled = false; btn.textContent = 'שליחה לתום';
      if (ok) { try { sessionStorage.removeItem(DRAFT); } catch (e) {} }
      showDone(ok);
    };
    f.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!validate()) return;
      if (step < 3) { go(step + 1); const n = $(`.hstep[data-step="${step}"] input, .hstep[data-step="${step}"] textarea`, f); if (n) setTimeout(() => n.focus({ preventScroll: true }), 50); return; }
      rec = record(); send();
    });
    window.addEventListener('resize', () => { if (step === 3 && empty) sizeSig(); });
    minor(); go(1, true);
  }

  /* ---------- promo of the month (same source as the app) ---------- */
  const pbar = $('#promo-bar');
  if (pbar && pbar.dataset.api) {
    const fmt = (iso) => { const [y, m, dd] = String(iso).split('-'); return `${dd}/${m}/${y}`; };
    const esc2 = (t) => String(t == null ? '' : t).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const today2 = () => { const x = new Date(); x.setMinutes(x.getMinutes() - x.getTimezoneOffset()); return x.toISOString().slice(0, 10); };
    const ctl = 'AbortController' in window ? new AbortController() : null; const tm = setTimeout(() => ctl && ctl.abort(), 8000);
    fetch(pbar.dataset.api + '?action=promo', { signal: ctl ? ctl.signal : undefined }).then((r) => r.json()).then((j) => {
      const p = j && j.ok && j.promo;
      if (!p || !p.title || !(p.until >= today2())) return;
      const link = wa(`היי תום, ראיתי באתר את מבצע החודש – "${p.title}". אשמח לקבוע תור 🙂`);
      const card = $('#promo-card');
      if (card) {
        const img = p.image && /^https:\/\//.test(p.image) ? `<img src="${esc2(p.image)}" alt="" loading="lazy">` : `<img src="assets/img/logo-ink.png" alt="" class="pc-logo">`;
        card.innerHTML = `<div class="pc-in"><div class="pc-img">${img}</div><div class="pc-txt"><span class="pc-badge">מבצע החודש</span><h2>${esc2(p.title)}</h2>${p.text ? `<p>${esc2(p.text).replace(/\n/g, '<br>')}</p>` : ''}</div><div class="pc-act"><a class="btn pc-wa brand-wa" href="${link}" target="_blank" rel="noopener">לקביעת תור במבצע<span class="sr"> (נפתח בחלון חדש)</span></a><span class="pc-until">בתוקף עד ${esc2(fmt(p.until))}</span></div></div>`;
        card.hidden = false;
        const im = $('.pc-img img', card); if (im) im.addEventListener('error', () => { im.src = 'assets/img/logo-ink.png'; im.className = 'pc-logo'; }, { once: true });
      } else if (store.get('tt-promo-bar-x') !== p.id) {
        pbar.innerHTML = `<div class="wrap"><span class="pb-t"><b>מבצע החודש:</b> ${esc2(p.title)}<span class="pb-until"> · עד ${esc2(fmt(p.until))}</span></span><a href="${pbar.dataset.home}">לפרטים</a><button type="button" class="pb-x" aria-label="סגירת הודעת המבצע">✕</button></div>`;
        pbar.hidden = false;
        $('.pb-x', pbar).addEventListener('click', () => { pbar.hidden = true; store.set('tt-promo-bar-x', p.id); });
      }
    }).catch(() => {}).finally(() => clearTimeout(tm));
  }
})();
