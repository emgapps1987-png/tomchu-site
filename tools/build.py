#!/usr/bin/env python3
"""Static site generator for tomchu-tattoo.co.il.
Run from repo root: python3 tools/build.py  → writes *.html, journal/*.html, sitemap.xml, robots.txt, manifest."""
import json, os, html
from datetime import date
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
C = json.load(open(os.path.join(ROOT, 'tools', 'content.json'), encoding='utf-8'))
CFG = C['CONFIG']
SITE = 'https://www.tomchu-tattoo.co.il'
APP = 'https://emgapps1987-png.github.io/tomchu-tattoo-app/'
PLAY = 'https://play.google.com/apps/testing/com.tomchutattoo.app'
IOS = APP + 'install.html'
BIZ_ID = CFG.get('businessId', '')  # מספר עוסק של תום – חובה להשלים לפני מכירת שוברים באתר
MOOVIT = 'https://moovit.com/?to=%D7%A7%D7%93%D7%A8%D7%95%D7%9F+48%2C+%D7%90%D7%9C%D7%A4%D7%99+%D7%9E%D7%A0%D7%A9%D7%94&tll=32.1801435_35.0132961&metroId=1'
WA = 'https://wa.me/972542885771'
TODAY = date.today()
VER = __import__('datetime').datetime.now().strftime('%Y%m%d%H%M')
e = html.escape

# ---------------------------------------------------------------- images
DIM = {}
for i in range(1, 30):
    DIM[i] = Image.open(os.path.join(ROOT, f'assets/img/works/work{i}.jpg')).size
DIM['12a'] = Image.open(os.path.join(ROOT, 'assets/img/works/work12a.jpg')).size
WORK = {w['id']: w for w in C['WORKS']}

def pic(n, alt, sizes='(max-width: 600px) 50vw, 300px', cls='', eager=False, extra=''):
    w, h = DIM[n]
    small = min(600, w)
    base = f'{{R}}assets/img/works/work{n}'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{base}-600.webp {small}w, {base}-1000.webp {w}w" sizes="{sizes}">'
            f'<img src="{base}.jpg" width="{w}" height="{h}" alt="{e(alt)}" {load} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}{extra}></picture>')

# ---------------------------------------------------------------- icons
ICONS = {
 'wa': '<path d="M5 27l1.6-5.2A11 11 0 1 1 10.4 25.6z"/><path d="M12.4 11.2c.4 3.9 3.6 7.6 8 8.3l1.3-1.8-2.4-1.3-1.1 1c-1.5-.7-2.8-2-3.5-3.5l1-1.1-1.3-2.4z"/>',
 'phone': '<path d="M9 4h4l2 6-3 2a15 15 0 0 0 8 8l2-3 6 2v4a3 3 0 0 1-3 3A21 21 0 0 1 6 7a3 3 0 0 1 3-3z"/>',
 'mail': '<rect x="4" y="7" width="24" height="18" rx="3"/><path d="M5 9l11 8 11-8"/>',
 'pin': '<path d="M16 29s-9-8.4-9-15a9 9 0 0 1 18 0c0 6.6-9 15-9 15z"/><circle cx="16" cy="14" r="3.4"/>',
 'nav': '<path d="M27 5L5 14.5l9.5 3 3 9.5z"/>',
 'map': '<path d="M4 8l8-3 8 3 8-3v19l-8 3-8-3-8 3z"/><path d="M12 5v19M20 8v19"/>',
 'ig': '<rect x="5" y="5" width="22" height="22" rx="6.5"/><circle cx="16" cy="16" r="5"/><circle cx="22.6" cy="9.4" r=".9" fill="currentColor"/>',
 'fb': '<path d="M18.5 28V17h3.6l.6-4.2h-4.2v-2.6c0-1.2.4-2 2.1-2h2.2V4.5a29 29 0 0 0-3.2-.2c-3.2 0-5.3 1.9-5.3 5.5v3H11V17h3.3v11"/>',
 'tt': '<path d="M18 4v15.5a4.5 4.5 0 1 1-4.5-4.5"/><path d="M18 4c.6 3.6 3 6 6.5 6.3"/>',
 'home': '<path d="M5 15L16 5l11 10"/><path d="M8 13v13h16V13"/><path d="M13 26v-7h6v7"/>',
 'grid': '<rect x="5" y="5" width="9" height="9" rx="2"/><rect x="18" y="5" width="9" height="9" rx="2"/><rect x="5" y="18" width="9" height="9" rx="2"/><rect x="18" y="18" width="9" height="9" rx="2"/>',
 'spark': '<path d="M16 3l2.6 7.4L26 13l-7.4 2.6L16 23l-2.6-7.4L6 13l7.4-2.6z"/><path d="M25 21l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/>',
 'chat': '<path d="M6 7h20a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H13l-6 5v-5H6a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2z"/>',
 'menu': '<path d="M5 9h22M5 16h22M5 23h22"/>',
 'close': '<path d="M8 8l16 16M24 8L8 24"/>',
 'sun': '<circle cx="16" cy="16" r="5.5"/><path d="M16 3v3M16 26v3M3 16h3M26 16h3M6.8 6.8l2.1 2.1M23.1 23.1l2.1 2.1M6.8 25.2l2.1-2.1M23.1 8.9l2.1-2.1"/>',
 'moon': '<path d="M26 19.5A11 11 0 0 1 12.5 6 11 11 0 1 0 26 19.5z"/>',
 'a11y': '<circle cx="16" cy="6" r="2.4" fill="currentColor"/><path d="M6 11l10 2 10-2M16 13v7M11 29l5-9 5 9"/>',
 'arrow': '<path d="M20 7l-9 9 9 9"/>',
 'health': '<path d="M16 27s-10-6.2-10-13.2A5.6 5.6 0 0 1 16 10.4a5.6 5.6 0 0 1 10 3.4C26 20.8 16 27 16 27z"/><path d="M8.5 16.5h4l1.6-3 2.6 6 1.8-3h5"/>',
 'care': '<path d="M16 28c-6-4-10-8.5-10-13.5C6 8 11 4 16 4s10 4 10 10.5C26 19.5 22 24 16 28z"/><path d="M12 15l3 3 5-6"/>',
 'gift': '<rect x="6" y="13" width="20" height="13" rx="2"/><path d="M4.5 13h23M16 13v13"/><path d="M16 13c-2.2-4.5-7.5-5-7.5-1.6C8.5 13 12 13 16 13zM16 13c2.2-4.5 7.5-5 7.5-1.6 0 1.6-3.5 1.6-7.5 1.6z"/>',
 'camera': '<rect x="4.5" y="9" width="23" height="16" rx="3"/><path d="M11 9l1.6-3h6.8L21 9"/><circle cx="16" cy="17" r="4.5"/>',
 'idea': '<path d="M12 22.5c0-2-3-3.6-3-7.5a7 7 0 0 1 14 0c0 3.9-3 5.5-3 7.5z"/><path d="M12.5 25.5h7M14 28h4"/>',
 'android': '<path d="M8 13h16v10a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2z"/><path d="M9 12a7 7 0 0 1 14 0M11 5l2 3M21 5l-2 3M5 14v6M27 14v6M12 25v3M20 25v3"/>',
 'apple': '<path d="M21.5 4.5c.2 2.2-1.6 4.3-3.8 4.2-.2-2.1 1.7-4.1 3.8-4.2z"/><path d="M25.5 21.5c-1 2.4-2.6 5-4.6 5-1.7 0-2.2-1-4.2-1s-2.6 1-4.2 1c-2 0-4.4-3.7-5.3-7-1.3-4.9.9-9.5 4.6-9.5 1.8 0 3 1.1 4.6 1.1s2.6-1.1 4.7-1.1c1.4 0 3.1.7 4.2 2.2-3.6 2-3.1 7.5.2 9.3z"/>',
 'clock': '<circle cx="16" cy="16" r="11.5"/><path d="M16 9v7l5 3"/>',
 'swap': '<path d="M11 10l-5 6 5 6M21 10l5 6-5 6"/>',
 'chev': '<path d="M20 7l-9 9 9 9"/>',
}
def ic(name, cls=''):
    return f'<svg class="i {cls}" viewBox="0 0 32 32" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

NAV = [('works.html', 'עבודות', 'גלריה, סינון ולפני/אחרי'), ('guide.html', 'המדריך', 'איזה קעקוע מתאים לי?'), ('studio.html', 'הסטודיו', 'סיור לפני שמגיעים'),
       ('tom.html', 'תום', 'הסיפור וההמלצות'), ('process.html', 'איך זה עובד', 'מרעיון ועד החלמה'), ('gift.html', 'שובר מתנה', 'סכום חופשי, ביט או פייבוקס'),
       ('journal.html', 'מאמרים', 'לפני הקעקוע הראשון'), ('app.html', 'האפליקציה', 'הצהרת בריאות, החלמה, מתנה'), ('faq.html', 'שאלות', 'כאב, מחיר, חניה')]

def head(title, desc, path, R, og_img='assets/img/og.jpg', ld=None, robots='index,follow'):
    url = SITE + '/' + ('' if path == 'index.html' else path)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    return f'''<!doctype html>
<html lang="he" dir="rtl" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B0A0D">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="Tomchu Tattoo">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og_img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{R}favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="{R}assets/img/favicon-192.png">
<link rel="icon" type="image/png" sizes="96x96" href="{R}assets/img/favicon-96.png">
<link rel="icon" type="image/png" sizes="48x48" href="{R}assets/img/favicon-48.png">
<link rel="apple-touch-icon" href="{R}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{R}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amatic+SC:wght@700&family=Heebo:wght@400;500;600;700&family=Rubik:wght@500;700;800&display=swap">
<link rel="stylesheet" href="{R}assets/css/site.css?v={VER}">
<script>(function(){{var r=document.documentElement;try{{if(JSON.parse(localStorage.getItem('tt-theme'))==='light')r.classList.add('light');(JSON.parse(localStorage.getItem('tt-a11y'))||[]).forEach(function(c){{r.classList.add(c)}})}}catch(e){{}}}})();</script>
{lds}
</head>'''

def header(cur, R):
    items = ''.join(f'<li><a href="{R}{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""}>{t}</a></li>' for h, t, _ in NAV)
    ditems = ''.join(f'<li><a href="{h if h.startswith("http") else R + h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""}><span>{t}</span></a></li>' for h, t in [('index.html', 'בית'), ('works.html', 'עבודות'), ('guide.html', 'איזה קעקוע מתאים לי?'), ('tom.html', 'תום והסטודיו'), ('process.html', 'לפני שמגיעים'), ('process.html#care', 'טיפול בקעקוע חדש'), ('health.html', 'הצהרת בריאות'), ('gift.html', 'שובר מתנה'), ('app.html', 'האפליקציה')])
    API, WA = CFG.get('healthEndpoint', ''), CFG['whatsapp']
    return f'''<body>
<a class="skip" href="#main">דילוג לתוכן הראשי</a>
<div id="promo-bar" class="promo-bar" hidden data-api="{API}" data-wa="{WA}" data-home="{R}index.html#promo-card"></div>
<header class="hdr">
  <div class="wrap">
    <button type="button" class="menu-btn" data-menu aria-expanded="false" aria-controls="drawer">{ic("menu")}<span>תפריט</span></button>
    <a class="brand" href="{R}index.html"><img class="lg-d" src="{R}assets/img/logo-96.png" width="44" height="44" alt=""><img class="lg-l" src="{R}assets/img/logo-light-96.png" width="44" height="44" alt=""><span>Tomchu Tattoo</span><span class="sr"> – לעמוד הבית</span></a>
    <nav class="mainnav" aria-label="ניווט ראשי"><ul>{items}</ul></nav>
    <div class="hdr-act">
      <button type="button" class="icon-btn theme-btn" aria-pressed="false" aria-label="מעבר לתצוגה בהירה">{ic("moon", "moon")}{ic("sun", "sun")}</button>
      <a class="btn btn-iri btn-sm" href="{R}contact.html">קביעת תור</a>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="drawer-bg"></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="תפריט האתר">
    <div class="drawer-top"><b>תפריט</b><button type="button" class="icon-btn drawer-close" aria-label="סגירת התפריט">{ic("close")}</button></div>
    <nav aria-label="תפריט מלא"><ul>{ditems}</ul></nav>
    <a class="drawer-cta" href="{R}contact.html">קביעת תור</a>
  </div>
</div>
<main id="main" tabindex="-1">'''

def footer(cur, R):
    tabs = [('index.html', 'בית', 'home'), ('works.html', 'עבודות', 'grid'), ('guide.html', 'המדריך', 'spark'), ('contact.html', 'קביעת תור', 'chat')]
    t = ''.join(f'<a href="{R}{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == cur else ""}><i>{ic(i)}</i>{n}</a>' for h, n, i in tabs)
    return f'''</main>
<footer class="ftr">
  <div class="wrap">
    <div class="cols">
      <div><a class="brand" href="{R}index.html"><img class="lg-d" src="{R}assets/img/logo-96.png" width="44" height="44" alt=""><img class="lg-l" src="{R}assets/img/logo-light-96.png" width="44" height="44" alt=""><span>Tomchu Tattoo</span></a>
        <p>סטודיו פרטי לקעקועים של תום גבע.<br>Fine Line, ריאליזם וקאברים.<br>{CFG["address"]} · בתיאום מראש</p></div>
      <div><h2>דברו עם תום</h2><ul>
        <li><a class="soc-pill" href="{WA}" target="_blank" rel="noopener">{ic("wa")}וואטסאפ<span class="sr"> (נפתח בחלון חדש)</span></a></li>
        <li><a href="tel:+972542885771">054-288-5771</a></li>
        <li><a href="mailto:{CFG["email"]}">{CFG["email"]}</a></li></ul></div>
      <div><h2>באתר</h2><ul>
        <li><a href="{R}works.html">עבודות</a></li><li><a href="{R}guide.html">איזה קעקוע מתאים לי?</a></li><li><a href="{R}journal.html">מאמרים</a></li><li><a href="{R}gift.html">שובר מתנה</a></li><li><a href="{R}app.html">האפליקציה</a></li></ul></div>
      <div><h2>עוקבים ומגיעים</h2><ul class="socials">
        <li><a href="{CFG["instagram"]}" target="_blank" rel="noopener">{ic("ig")}Instagram<span class="sr"> (נפתח בחלון חדש)</span></a></li>
        <li><a href="{CFG["facebook"]}" target="_blank" rel="noopener">{ic("fb")}Facebook<span class="sr"> (נפתח בחלון חדש)</span></a></li>
        <li><a href="{CFG["tiktok"]}" target="_blank" rel="noopener">{ic("tt")}TikTok<span class="sr"> (נפתח בחלון חדש)</span></a></li>
        <li><a href="{CFG["waze"]}" target="_blank" rel="noopener">{ic("nav")}ניווט ב־Waze<span class="sr"> (נפתח בחלון חדש)</span></a></li>
        <li><a href="{MOOVIT}" target="_blank" rel="noopener">{ic("pin")}תחבורה ציבורית ב־Moovit<span class="sr"> (נפתח בחלון חדש)</span></a></li></ul></div>
    </div>
    <p class="seo-links">אזורים: <a href="{R}tattoo-alfei-menashe.html">אלפי מנשה</a> · <a href="{R}tattoo-kfar-saba.html">כפר סבא</a> · <a href="{R}tattoo-raanana.html">רעננה</a> · <a href="{R}tattoo-hod-hasharon.html">הוד השרון</a> · <a href="{R}tattoo-karnei-shomron.html">קרני שומרון</a> · <a href="{R}tattoo-tzur-yigal.html">צור יגאל</a> · <a href="{R}tattoo-tzofim.html">צופים</a> · <a href="{R}tattoo-kochav-yair.html">כוכב יאיר</a><br>סגנונות: <a href="{R}fine-line-tattoo.html">פיין ליין</a> · <a href="{R}cover-up-tattoo.html">קאבר וחידוש</a> · <a href="{R}color-tattoo.html">צבע עדין</a></p>
    <div class="legal"><span>© <span data-year>{TODAY.year}</span> Tomchu Tattoo · תום גבע</span><span><a href="{R}accessibility.html">הצהרת נגישות</a> · <a href="{R}privacy.html">מדיניות פרטיות</a></span></div>
  </div>
</footer>
<nav class="tabs" aria-label="פעולות מהירות"><a class="tb-book" href="{R}contact.html">{ic("chat")}קביעת תור</a><a class="tb-wa brand-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}וואטסאפ<span class="sr"> (נפתח בחלון חדש)</span></a></nav>
<button type="button" class="a11y-btn" id="a11y-btn" aria-expanded="false" aria-controls="a11y-panel" aria-label="תפריט נגישות">{ic("a11y")}</button>
<div class="a11y-panel" id="a11y-panel" role="dialog" aria-labelledby="a11y-h" hidden>
  <div class="hd"><h2 id="a11y-h">התאמות נגישות</h2><button type="button" class="x" aria-label="סגירת תפריט הנגישות">✕</button></div>
  <div class="grid">
    <button type="button" data-a="a-big" aria-pressed="false">הגדלת טקסט</button>
    <button type="button" data-a="a-contrast" aria-pressed="false">ניגודיות גבוהה</button>
    <button type="button" data-a="a-font" aria-pressed="false">גופן קריא</button>
    <button type="button" data-a="a-links" aria-pressed="false">הדגשת קישורים</button>
    <button type="button" data-a="a-still" aria-pressed="false">עצירת אנימציות</button>
    <button type="button" class="reset">איפוס הכול</button>
  </div>
  <a href="{R}accessibility.html">להצהרת הנגישות</a>
</div>
<script src="{R}assets/js/site.js?v={VER}" defer></script>
<script>if(/(^|\\.)tomchu-tattoo\\.co\\.il$/.test(location.hostname)){{var s=document.createElement('script');s.defer=1;s.src='https://static.cloudflareinsights.com/beacon.min.js';s.setAttribute('data-cf-beacon','{{"token": "618c5c9de5fb46e09ffd3922cdc57781"}}');document.body.appendChild(s)}}</script>
</body>
</html>
'''

def crumbs(items, R):
    li = ''.join((f'<li><a href="{R}{h}">{t}</a></li>' if h else f'<li aria-current="page">{t}</li>') for h, t in items)
    return f'<nav class="crumbs" aria-label="פירורי לחם"><ol>{li}</ol></nav>'

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, **({"item": SITE + '/' + (h if h != 'index.html' else '')} if h else {})} for i, (h, t) in enumerate(items)]}

KEEP_LEAD=False
def phead(title_html, lead, cr, R, label=None):
    return f'''<div class="phead"><div class="wrap">{crumbs(cr, R)}<h1>{title_html}</h1>{f'<p class="lead">{lead}</p>' if lead and KEEP_LEAD else ''}</div></div>'''

BUSINESS = {
    "@context": "https://schema.org", "@type": "TattooParlor", "@id": SITE + "/#studio", "name": "Tomchu Tattoo – תום גבע",
    "alternateName": "טומצ'ו טאטו", "url": SITE + "/", "image": SITE + "/assets/img/og.jpg", "logo": SITE + "/assets/img/icon-512.png",
    "telephone": "+972-54-288-5771", "email": CFG['email'], "priceRange": "₪₪",
    "description": "סטודיו פרטי לקעקועים באלפי מנשה: Fine Line, ריאליזם וקאברים. עיצוב אישי, ציוד חד־פעמי ואווירה רגועה.",
    "address": {"@type": "PostalAddress", "streetAddress": "קדרון 48", "addressLocality": "אלפי מנשה", "addressCountry": "IL"},
    "geo": {"@type": "GeoCoordinates", "latitude": 32.1801435, "longitude": 35.0132961},
    "areaServed": ["אלפי מנשה", "כפר סבא", "רעננה", "הוד השרון", "קרני שומרון", "צור יגאל"],
    "founder": {"@type": "Person", "name": "תום גבע", "jobTitle": "מקעקעת"},
    "sameAs": [CFG['instagram'], CFG['facebook'], CFG['tiktok']],
    "hasMap": CFG['maps'],
}

def ext(href, text, cls='btn btn-ghost', icon=None):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{ic(icon) if icon else ""}{text}<span class="sr"> (נפתח בחלון חדש)</span></a>'

def mark_app_links(html):
    import re as _re
    html = _re.sub(r'href="([^"]*?)studio\.html"', r'href="\1tom.html#studio"', html)
    html = _re.sub(r'href="([^"]*?)faq\.html"', r'href="\1process.html#faq"', html)
    BR = [('instagram.com', 'brand-ig'), ('facebook.com', 'brand-fb'), ('tiktok.com', 'brand-tt'), ('wa.me/', 'brand-wa'), ('waze.com', 'brand-wz'), ('moovit.com', 'brand-mv')]
    def fix(m):
        tag = m.group(0)
        hm = _re.search(r'href="([^"]*)"', tag)
        if not hm or 'brand-' in tag: return tag
        k = next((c for d, c in BR if d in hm.group(1)), None)
        if not k: return tag
        if 'class="' in tag: return tag.replace('class="', f'class="{k} ', 1)
        return tag.replace('<a ', f'<a class="{k}" ', 1)
    return _re.sub(r'<a [^>]*>', fix, html)

def page(path, title, desc, body, R='', ld=None, robots='index,follow'):
    out = head(title, desc, path, R, ld=ld, robots=robots) + header(path, R) + body.replace('{R}', R) + footer(path, R)
    out = mark_app_links(out)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(out)
    PAGES.append(path)

PAGES = []
TAGN = {'fine': 'קו עדין', 'color': 'צבע', 'sketch': 'סקיצה', 'studio': 'בסטודיו'}

# ================================================================ HOME
# appended into build.py: SVG art per tile
def _svg(key, inner, vb='0 0 120 72'):
    return (f'<span class="tart tart-{key}" aria-hidden="true"><svg viewBox="{vb}" focusable="false">'
            f'<defs><linearGradient id="ig-{key}" gradientUnits="userSpaceOnUse" x1="10" y1="6" x2="110" y2="66"><stop offset="0" stop-color="#18B58A"/><stop offset=".3" stop-color="#16B3C2"/>'
            f'<stop offset=".55" stop-color="#4C82E6"/><stop offset=".78" stop-color="#9B5BD6"/><stop offset="1" stop-color="#E8467F"/></linearGradient></defs>'
            f'{inner}</svg></span>')
def _st(key): return f'stroke="url(#ig-{key})"'
SPARK = 'M0 -5L1.1 -1.1 5 0 1.1 1.1 0 5-1.1 1.1-5 0-1.1-1.1Z'
TILE_ART = {
 'guide': _svg('guide',
    f'<g fill="none" {_st("guide")} stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
    f'<path class="ln mo mo1" pathLength="1" d="M66 15A21 21 0 1 0 66 57 16.5 16.5 0 1 1 66 15Z"/>'
    f'<path class="ln mo mo2" pathLength="1" d="M60 64C60 52 58 44 60 35M60 35C53 28 53 17 60 12 67 17 67 28 60 35 54 30 45 30 41 35 46 41 54 40 60 35 66 30 75 30 79 35 74 41 66 40 60 35M60 53C65 48 71 47 75 49 71 54 66 55 60 53"/>'
    f'<path class="ln mo mo3" pathLength="1" d="M60 60C42 48 36 39 39 29 42 19 55 19 60 30 65 19 78 19 81 29 84 39 78 48 60 60Z"/></g>'
    f'<g fill="url(#ig-guide)"><g transform="translate(28 18)"><path class="tw tw1" d="{SPARK}"/></g><g transform="translate(94 50) scale(.8)"><path class="tw tw2" d="{SPARK}"/></g><g transform="translate(96 16) scale(.6)"><path class="tw tw3" d="{SPARK}"/></g></g>'),
 'contact': _svg('contact',
    '<g fill="none" stroke="currentColor" stroke-width="1.4" class="faint"><rect x="32" y="11" width="56" height="52" rx="7"/><path d="M32 23H88M46 6V15M74 6V15"/></g>'
    '<g fill="currentColor" class="faint">' + ''.join(f'<circle cx="{40 + 10 * c}" cy="{32 + 10 * r}" r="1.7"/>' for r in range(3) for c in range(5) if not (r == 1 and c == 3)) + '</g>'
    f'<g fill="none" {_st("contact")} stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle class="ln cal-ring" pathLength="1" cx="70" cy="42" r="6.6" transform="rotate(-90 70 42)"/><path class="ln cal-ok" pathLength="1" d="M67 42.2L69.2 44.4 73.4 39.8"/></g>'),
 'process': _svg('process',
    '<path d="M14 50C30 50 30 22 46 22S62 50 74 50 90 22 106 22" fill="none" stroke="currentColor" class="faint" stroke-width="1.3" stroke-dasharray="2 4"/>'
    f'<path class="ln pr-line" pathLength="1" d="M14 50C30 50 30 22 46 22S62 50 74 50 90 22 106 22" fill="none" {_st("process")} stroke-width="2" stroke-linecap="round"/>'
    + ''.join(f'<circle cx="{x}" cy="{y}" r="5.2" fill="var(--surface)" stroke="currentColor" class="faint-s" stroke-width="1.3"/><circle class="pr-dot pr-d{i}" cx="{x}" cy="{y}" r="5.2" fill="url(#ig-process)"/>' for i, (x, y) in enumerate([(14, 50), (46, 22), (74, 50), (106, 22)]))
    + '<circle class="pr-ping" cx="106" cy="22" r="5.2" fill="none" stroke="#E8467F" stroke-width="1.2"/>'),
 'faq': _svg('faq',
    f'<g class="fq-b1"><path d="M62 10H98A8 8 0 0 1 106 18V30A8 8 0 0 1 98 38H96L100 45 89 38H62A8 8 0 0 1 54 30V18A8 8 0 0 1 62 10Z" fill="none" {_st("faq")} stroke-width="1.6" stroke-linejoin="round"/>'
    f'<path d="M76 19.5C76 16 84 16 84 20.5 84 23.5 80 23.6 80 27M80 31.2V31.4" fill="none" {_st("faq")} stroke-width="1.9" stroke-linecap="round"/></g>'
    '<g class="fq-b2"><path d="M22 32H54A8 8 0 0 1 62 40V52A8 8 0 0 1 54 60H33L22 67 26 60H22A8 8 0 0 1 14 52V40A8 8 0 0 1 22 32Z" fill="none" stroke="currentColor" class="faint-s" stroke-width="1.5" stroke-linejoin="round"/>'
    '<g fill="currentColor" class="fq-dots"><circle class="fd fd1" cx="30" cy="46" r="2.2"/><circle class="fd fd2" cx="38" cy="46" r="2.2"/><circle class="fd fd3" cx="46" cy="46" r="2.2"/></g>'
    f'<path class="ln fq-ok" pathLength="1" d="M31 46.5L36 51 46 40.5" fill="none" {_st("faq")} stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"/></g>'),
 'app': _svg('app',
    '<defs><clipPath id="ap-clip"><rect x="47.5" y="13" width="25" height="48" rx="2.5"/></clipPath></defs>'
    f'<rect x="44" y="5" width="32" height="63" rx="7" fill="none" {_st("app")} stroke-width="1.6"/><path d="M56 9.4H64" stroke="currentColor" class="faint" stroke-width="1.6" stroke-linecap="round"/>'
    '<g clip-path="url(#ap-clip)"><g class="ap-feed">' + ''.join(f'<rect x="49.5" y="{15 + 14 * i}" width="21" height="11" rx="2.6" fill="url(#ig-app)" opacity="{.75 if i % 4 == 0 else .3}"/><rect x="52" y="{18 + 14 * i}" width="{9 + (i * 5) % 8}" height="1.6" rx=".8" fill="#fff" opacity=".85"/>' for i in range(8)) + '</g></g>'
    '<circle cx="76" cy="6" r="3.6" fill="#E8467F" class="ap-badge"/><circle cx="76" cy="6" r="3.6" fill="none" stroke="#E8467F" stroke-width="1.1" class="ap-ping"/>'
    f'<g fill="url(#ig-app)"><g transform="translate(28 44) scale(.7)"><path class="tw tw2" d="{SPARK}"/></g><g transform="translate(94 30) scale(.55)"><path class="tw tw3" d="{SPARK}"/></g></g>'),
 'journal': _svg('journal',
    '<g fill="none" stroke-linejoin="round" stroke-linecap="round">'
    '<path d="M60 18C50 12 36 12 22 16V60C36 56 50 56 60 62Z" stroke="currentColor" class="faint-s" stroke-width="1.5"/>'
    '<path d="M60 18C70 12 84 12 98 16V60C84 56 70 56 60 62Z" stroke="currentColor" class="faint-s" stroke-width="1.5"/>'
    '<path d="M29 25H52M29 32H50M29 39H52M29 46H45" stroke="currentColor" class="faint" stroke-width="1.3"/>'
    f'<path class="ln jl jl1" pathLength="1" d="M68 25H91" {_st("journal")} stroke-width="1.6"/><path class="ln jl jl2" pathLength="1" d="M68 32H89" {_st("journal")} stroke-width="1.6"/>'
    f'<path class="ln jl jl3" pathLength="1" d="M68 39H91" {_st("journal")} stroke-width="1.6"/><path class="ln jl jl4" pathLength="1" d="M68 46H82" {_st("journal")} stroke-width="1.6"/>'
    f'<path class="jl-page" d="M60 18C70 12 84 12 98 16V60C84 56 70 56 60 62Z" fill="var(--surface2)" {_st("journal")} stroke-width="1.3"/>'
    '<path d="M60 18V62" stroke="currentColor" class="faint-s" stroke-width="1.5"/></g>'),
 'tom': _svg('tom',
    '<path class="ln tm-heart" pathLength="1" d="M60 62C40 49 33 39 37 28 41 17 55 17 60 29 65 17 79 17 83 28 87 39 80 49 60 62Z" fill="none" stroke="url(#ig-tom)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<path class="ln tm-line" pathLength="1" d="M18 58C30 58 34 44 44 44S56 60 66 54 80 36 102 40" fill="none" {_st("tom")} stroke-width="1.6" stroke-linecap="round"/>'),
}

TILE_ART['works'] = _svg('works',
    '<g fill="none" stroke="currentColor" class="faint-s" stroke-width="1.3"><rect x="8" y="14" width="30" height="40" rx="3"/><rect x="45" y="6" width="30" height="40" rx="3"/><rect x="82" y="18" width="30" height="40" rx="3"/></g>'
    '<path d="M2 66H118" stroke="currentColor" class="faint" stroke-width="1.2"/>'
    f'<g fill="none" {_st("works")} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path class="ln wk wk1" pathLength="1" d="M23 48C23 40 22 36 23 30M23 30C19 26 19 21 23 18 27 21 27 26 23 30M23 40C26 37 29 37 31 38 29 41 26 41 23 40"/>'
    '<path class="ln wk wk2" pathLength="1" d="M50 30C54 22 58 22 60 28S66 36 70 26M52 38C56 34 60 34 63 37S68 40 70 36"/>'
    '<path class="ln wk wk3" pathLength="1" d="M97 50C88 44 85 39 87 34 89 29 95 29 97 35 99 29 105 29 107 34 109 39 106 44 97 50Z"/></g>')
TILE_ART['studio'] = _svg('studio',
    '<path d="M4 64H116" stroke="currentColor" class="faint" stroke-width="1.2"/>'
    '<g class="st-lamp"><path d="M26 0V14" stroke="currentColor" class="faint-s" stroke-width="1.2"/>'
    f'<path d="M18 22C18 17 21.5 14 26 14S34 17 34 22Z" fill="none" {_st("studio")} stroke-width="1.5" stroke-linejoin="round"/>'
    '<path class="st-cone" d="M19 23L8 60H44L33 23Z" fill="url(#ig-studio)" opacity=".16"/></g>'
    f'<path class="ln st-neon" pathLength="1" d="M70 40C62 34 59 30 61 25 63 20 68 20 70 25 72 20 77 20 79 25 81 30 78 34 70 40Z" fill="none" stroke="#F0457F" stroke-width="2" stroke-linejoin="round"/>'
    f'<g fill="none" {_st("studio")} stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M96 64L94 52H106L104 64Z"/>'
    '<path class="ln st-leaf" pathLength="1" d="M100 52C100 44 98 40 94 36M100 52C101 45 104 41 108 39M100 50C100 42 101 36 101 30"/></g>')

TILE_ART['gift'] = _svg('gift',
    f'<g fill="none" {_st("gift")} stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round"><rect x="42" y="34" width="36" height="30" rx="3"/><path d="M60 34V64"/>'
    '<g class="gf-lid"><rect x="39" y="26" width="42" height="9" rx="2.5"/><path d="M60 26C54 16 46 18 49 23S60 26 60 26C66 16 74 18 71 23S60 26 60 26"/></g></g>'
    f'<g fill="url(#ig-gift)"><g transform="translate(34 20)"><path class="tw tw1" d="{SPARK}"/></g><g transform="translate(88 18) scale(.7)"><path class="tw tw2" d="{SPARK}"/></g></g>')
TILE_KEY = {'gift.html': 'gift', 'works.html': 'works', 'studio.html': 'studio', 'guide.html': 'guide', 'contact.html': 'contact', 'process.html': 'process', 'faq.html': 'faq', 'app.html': 'app', 'journal.html': 'journal', 'tom.html': 'tom'}
XF = {}

tiles = [
    ('works.html', 'עבודות', 'קיר העבודות, סינון לפי סגנון ולפני/אחרי', '#2FC4CF', 'big', None),
    ('guide.html', 'איזה קעקוע מתאים לי?', 'סגנון, גודל ומיקום – והמלצה מיידית', '#F0457F', '', None),
    ('contact.html', 'קביעת תור', 'וואטסאפ, טלפון והגעה לסטודיו', '#22C08F', '', None),
    ('studio.html', 'הסטודיו שלי', 'סיור בתמונות לפני שמגיעים', '#A46BE6', '', None),
    ('tom.html', 'קצת עליי, תום', 'הסיפור, ההמלצות, האנשים', '#5B95EE', '', None),
    ('process.html', 'איך זה עובד', 'מרעיון ועד החלמה – 4 שלבים', '#2FC4CF', '', None),
    ('faq.html', 'שאלות ותשובות', 'כאב, מחיר, חניה, קאברים', '#F0457F', '', None),
    ('app.html', 'האפליקציה', 'הצהרת בריאות, יומן החלמה ושובר מתנה', '#22C08F', '', None),
    ('journal.html', 'מאמרים', 'כל מה שכדאי לדעת לפני', '#A46BE6', '', None),
    ('gift.html', 'שובר מתנה', 'סכום חופשי, תשלום בביט או בפייבוקס', '#F0457F', 'wide', None),
]
th = ''
for k, (h, t, s, c, cls, img) in enumerate(tiles):
    im = pic(img, '', sizes='(max-width: 900px) 100vw, 600px') if img else ''
    xf = ''.join(f'<span class="xf xf{j + 1}">{pic(n2, "", sizes="(max-width: 900px) 100vw, 600px")}</span>' for j, n2 in enumerate(XF.get(h, [])))
    art = TILE_ART.get(TILE_KEY.get(h, ''), '')
    th += f'<a class="tile rise {cls} t-{h[:-5]}" style="--k:{k % 4};--c:{c}" href="{{R}}{h}">{im}{xf}<span class="tile-top"><span class="tile-n">{k + 1:02d}</span><span class="tile-go" aria-hidden="true">←</span></span>{art}<span><b>{t}</b></span></a>'

feat = [8, 9, 5, 20, 13, 17]
featured = ''.join(f'<li class="rise" style="--k:{k}"><a href="{{R}}works.html" class="frame" style="display:block;aspect-ratio:4/5">{pic(n, WORK["w" + str(n)]["alt"], sizes="(max-width: 600px) 50vw, 200px")}</a></li>' for k, n in enumerate(feat))

REVIEWS = [
    ('אסתאר', 'הייטקיסטית', 'מודה על היחס האישי, הסבלנות והאירוח בסטודיו – מרוצה מהתוצאה ומתכננת לחזור.'),
    ('רבקה', 'גננת', 'מספרת על סבלנות, הקשבה ותחושה בטוחה לאורך כל התהליך, ועל קעקוע שיצא בדיוק כמו שרצתה.'),
    ('א.', 'כוחות הביטחון', 'הרגישה נוח ובטוחה בקעקוע הראשון שלה, בזכות היחס האישי והסבלנות – ומתכוונת לחזור.'),
    ('ליבי קאופמן', 'קעקוע ליום הולדת 18', 'הרגישה שמקשיבים לה באמת; התוצאה מדויקת ויפה והאווירה נעימה.'),
    ('אורית קן דרור', 'מורה', 'מודה על קעקועים מושלמים, על ההקשבה, המקצועיות והעדינות – וכבר מתכננת את הבא.'),
    ('מיכל', 'מורה ליוגה', 'נהנתה מהאווירה ומהעדינות של תום; הזמן עבר בקלות והיא מחכה למפגש הבא.'),
    ('מייקל מוסקוביץ', '', 'הגיע עם רעיון ישן שלא ידע איך לממש – הסבלנות והכישרון של תום הפכו אותו למציאות.'),
    ('נועה בן דור טלמור', 'מורה', 'סטודיו חם ונעים, תום מקצועית ורגישה, והקעקוע יצא בדיוק כמו שרצתה. ממליצה בחום.'),
    ('אורלי', 'מורה', 'מתארת קבלה חמה, מקום אסתטי ונעים וקעקוע מושלם.'),
    ('שני אסרף', 'מורה', 'עשתה אצל תום שלושה קעקועים, ובעלה עשה אצלה את הראשון שלו; מדגישה מקצועיות, יצירתיות וקשב.'),
]
def rev_cards(lst):
    return ''.join(f'<article class="card rev rise" style="--k:{k % 3}"><span class="mark iri-text" aria-hidden="true">״</span><p>{t}</p><footer><b>{n}</b>{f"<span>{r}</span>" if r else ""}</footer></article>' for k, (n, r, t) in enumerate(lst))

home = f'''
<section class="hero-ink" aria-labelledby="hero-h">
  <svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><filter id="goo"><feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b"/><feColorMatrix in="b" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 22 -9"/></filter></svg>
  <div class="wrap hi-in">
    <div class="hi-orb" aria-hidden="true"><div class="hi-goo"><span class="hi-core"></span><i style="--s:70px;--c:#18B58A;--a:0deg;--r:92px;--d:.25s;--t:14s"></i><i style="--s:54px;--c:#16B3C2;--a:60deg;--r:100px;--d:.32s;--t:11s"></i><i style="--s:76px;--c:#4C82E6;--a:130deg;--r:88px;--d:.38s;--t:16s"></i><i style="--s:48px;--c:#9B5BD6;--a:195deg;--r:104px;--d:.3s;--t:12s"></i><i style="--s:66px;--c:#E8467F;--a:255deg;--r:94px;--d:.36s;--t:15s"></i><i style="--s:40px;--c:#2A5FC4;--a:310deg;--r:110px;--d:.42s;--t:10s"></i></div><img class="hi-logo lg-d" src="{{R}}assets/img/logo-ink.png" width="512" height="512" alt=""><img class="hi-logo lg-l" src="{{R}}assets/img/logo-light3.png" width="512" height="512" alt=""></div>
    <div class="hi-text">
      <span class="hi-eye">סטודיו פרטי לקעקועים · אלפי מנשה</span>
      <h1 id="hero-h"><span class="hi-w" style="--d:1.75s">הכל</span> <span class="hi-w" style="--d:1.95s">מתחיל</span> <span class="hi-w iri-flow" style="--d:2.15s">בקעקוע</span></h1>
      <p class="lead hi-rv" style="--d:2.5s">Fine Line, ריאליזם וקאברים.</p>
      <div class="reel hero-reel hi-rv" style="--d:2.6s" aria-label="תום מקעקעת בסטודיו – סרטונים קצרים"><figure><video class="reel-v" muted loop playsinline preload="none" poster="{{R}}assets/video/reel-A.jpg"><source src="{{R}}assets/video/reel-A.mp4" type="video/mp4"></video></figure><figure><video class="reel-v" muted loop playsinline preload="none" poster="{{R}}assets/video/reel-B.jpg"><source src="{{R}}assets/video/reel-B.mp4" type="video/mp4"></video></figure><figure><video class="reel-v" muted loop playsinline preload="none" poster="{{R}}assets/video/reel-C.jpg"><source src="{{R}}assets/video/reel-C.mp4" type="video/mp4"></video></figure></div>
      <div class="ctas hi-rv" style="--d:2.9s"><a class="btn btn-iri" href="{{R}}contact.html">{ic("chat")}לקביעת שיחת ייעוץ</a><a class="btn btn-ghost" href="{{R}}guide.html">{ic("spark")}איזה קעקוע מתאים לי?</a></div>
    </div>
  </div>
  <div class="wrap"><div id="promo-card" class="promo-card" hidden></div></div>
  <div class="wrap"><div class="tom-c hi-rv" style="--d:3s"><div class="ph"><img src="assets/img/tom-studio-1400.webp" srcset="assets/img/tom-studio-700.webp 700w, assets/img/tom-studio-1400.webp 1400w" sizes="(max-width:960px) 100vw, 960px" width="1400" height="788" alt="תום מקעקעת לקוחה בסטודיו שלה באלפי מנשה"></div><div class="tc-row"><h2>אמנית, אמא, <span class="iri-text">ומקעקעת עם נשמה</span></h2><a class="btn btn-ghost" href="tom.html">הסיפור של תום</a></div></div></div>
  <div class="wrap"><div class="motto" id="motto"><p><span class="w" style="--i:0">״אצלי</span> <span class="w" style="--i:1">אין</span> <span class="w" style="--i:2">חוקים</span><br><span class="w" style="--i:3">רק</span> <span class="w" style="--i:4">חלומות</span> <span class="w" style="--i:5">שמתגשמים.״</span></p><span class="sig">תום גבע</span></div></div>
</section>
<section aria-labelledby="tiles-h">
  <div class="wrap">
    <div class="sec-head"><h2 id="tiles-h">בוחרים <span class="iri-text">מאיפה להתחיל</span></h2></div>
    <div class="tiles">{th}</div>
  </div>
</section>
<section aria-labelledby="rev-h" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2 id="rev-h">מה מספרים <span class="iri-text">אחרי</span></h2></div>
    <div class="cards">{rev_cards(REVIEWS[:3])}</div>
    <p style="margin-top:18px"><a href="{{R}}tom.html#reviews">לכל ההמלצות</a></p>
  </div>
</section>
<section style="padding-top:0"><div class="wrap"><div class="band rise">
  <div><h2>יש לך רעיון? בואו נדבר עליו</h2></div>
  <div class="ctas"><a class="btn btn-light" href="{{R}}contact.html">{ic("wa")}כתבו לתום</a><a class="btn btn-line" href="tel:+972542885771">{ic("phone")}054-288-5771</a></div>
</div></div></section>
'''
WEBSITE_LD = {"@context": "https://schema.org", "@type": "WebSite", "name": "Tomchu Tattoo", "url": SITE + "/", "inLanguage": "he"}
page('index.html', 'Tomchu Tattoo | סטודיו לקעקועים באלפי מנשה – תום גבע',
     'סטודיו פרטי לקעקועים באלפי מנשה, ליד כפר סבא, רעננה והוד השרון. Fine Line, ריאליזם וקאברים – עיצוב אישי, ציוד חד־פעמי ואווירה רגועה.',
     home, ld=[BUSINESS, WEBSITE_LD])

# ================================================================ WORKS
gal_items = [w for w in C['WORKS'] if w['tag'] in TAGN]
counts = {t: sum(1 for w in gal_items if w['tag'] == t) for t in TAGN}
filters = f'<button type="button" data-f="all" aria-pressed="true">הכל<span class="c">({len(gal_items)})</span></button>' + ''.join(f'<button type="button" data-f="{t}" aria-pressed="false">{n}<span class="c">({counts[t]})</span></button>' for t, n in TAGN.items())
gl = ''
for w in gal_items:
    n = int(w['id'][1:])
    gl += f'<li data-tag="{w["tag"]}"><button type="button" data-full="{{R}}assets/img/works/work{n}-1000.webp" data-alt="{e(w["alt"])}" aria-label="{TAGN[w["tag"]]}: {e(w["alt"])} – הגדלה">{pic(n, w["alt"], sizes="(max-width: 520px) 100vw, (max-width: 1000px) 50vw, 290px")}<span class="cap" aria-hidden="true">{TAGN[w["tag"]]}</span></button></li>'
cr = [('index.html', 'בית'), (None, 'עבודות')]
works = phead('קו עדין. <span class="iri-text">הרבה נשמה.</span>', 'מבחר עבודות של תום – Fine Line, צבע עדין, סקיצות ורגעים מהסטודיו. לוחצים על תמונה כדי להגדיל, ואפשר לדפדף עם החיצים או בהחלקה.', cr, '') + f'''
<section aria-labelledby="gal-h">
  <div class="wrap">
    <h2 id="gal-h" class="sr">גלריית עבודות</h2>
    <div class="filters" role="group" aria-label="סינון לפי סגנון">{filters}</div>
    <p class="sr" aria-live="polite" id="gal-live"></p>
    <ul class="masonry" id="gallery">{gl}</ul>
  </div>
</section>
<section aria-labelledby="ba-h" style="padding-top:0">
  <div class="wrap split">
    <div class="stack rise">
      
      <h2 id="ba-h">גם קעקוע ישן<br>יכול <span class="iri-text">לקבל חיים חדשים</span></h2>
      
      <div class="ctas"><a class="btn btn-iri" href="{{R}}contact.html">לשלוח תמונה של קעקוע ישן</a></div>
    </div>
    <div class="compare rise" style="--k:2">
      {pic("12a", "דג הזהב לפני החידוש – קווים דהויים", sizes="460px")}
      <div class="after">{pic(11, "דג הזהב אחרי החידוש – קווים חדים וצבעים חיים", sizes="460px")}</div>
      <span class="tag r" aria-hidden="true">אחרי</span><span class="tag l" aria-hidden="true">לפני</span>
      <div class="handle"><span class="knob">{ic("swap")}</span></div>
      <input type="range" dir="ltr" min="0" max="100" value="50" aria-label="השוואת לפני ואחרי – הזזה ימינה מציגה יותר ״לפני״">
    </div>
  </div>
</section>
<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="תצוגת תמונה מוגדלת" hidden>
  <div class="lb-top"><p><span class="lb-cap"></span> · <span class="lb-pos"></span></p><button type="button" class="close" aria-label="סגירה">✕</button></div>
  <div class="lb-stage"><img alt=""></div>
  <button type="button" class="prev" aria-label="התמונה הקודמת">›</button><button type="button" class="next" aria-label="התמונה הבאה">‹</button>
</div>'''
page('works.html', 'עבודות – גלריית קעקועים | Tomchu Tattoo', 'גלריית קעקועים של תום גבע: Fine Line, צבע עדין, סקיצות, לפני ואחרי של חידושים וקאברים. סטודיו פרטי באלפי מנשה.', works, ld=[crumbs_ld(cr)])

# CSS for compare 'after' wrapper: picture inside .after needs absolute
# ================================================================ STUDIO
TOUR = [(24, 'מבט כללי', 'חלל אחד, מואר ומסודר: עמדת העבודה, מיטת הקעקוע והציורים של תום על הקיר.'),
        (25, 'פינת ההמתנה', 'כורסאות טורקיז, שולחן קפה ומראה – לנשום רגע לפני שמתחילים, וגם למי שבא ללוות.'),
        (26, 'פינת העיצוב', 'מסכים, כיסא נוח ושלטי ניאון – כאן הרעיון שלך הופך לסקיצה.'),
        (27, 'הציורים של תום', 'קוליברי, כבשים צבעוניות ודיוקנאות – ציורים מקוריים של תום שמקשטים את הסטודיו.'),
        (28, 'קיר הכבשים', 'הכבשים הצבעוניות של תום כבר הפכו לסמל של המקום.')]
tl = ''.join(f'<li><figure>{pic(n, WORK["w" + str(n)]["alt"], sizes="(max-width: 600px) 84vw, 560px")}<figcaption><b>{t}</b><span>{s}</span></figcaption></figure></li>' for n, t, s in TOUR)
STUDIO_SECTIONS = f'''<div id="studio" class="anchor"></div>
<section aria-labelledby="studio-h" style="padding-bottom:0"><div class="wrap"><div class="sec-head"><h2 id="studio-h">הסטודיו <span class="iri-text">שלי</span></h2></div></div></section>
<section aria-labelledby="tour-h">
  <div class="wrap">
    <h2 id="tour-h" class="sr">סיור בתמונות</h2>
    <div class="tour">
      <ul class="tour-track" tabindex="0" aria-label="סיור בסטודיו – גוללים הצידה">{tl}</ul>
      <div class="tour-ctl"><button type="button" class="icon-btn" data-tour="prev" aria-label="התמונה הקודמת">{ic("arrow")}</button><button type="button" class="icon-btn" data-tour="next" aria-label="התמונה הבאה" style="transform:scaleX(-1)">{ic("arrow")}</button><span class="pos" aria-hidden="true"></span></div>
    </div>
  </div>
</section>
<section aria-labelledby="day-h" style="padding-top:0">
  <div class="wrap split">
    <div class="stack rise">
      
      <h2 id="day-h">מה מחכה לך <span class="iri-text">בסטודיו</span></h2>
      <ul class="prose" style="padding-inline-start:20px;display:grid;gap:8px;color:var(--muted);margin:0">
        <li>מתחילים בקפה ובשיחה קצרה – עוברים יחד על הסקיצה ומדייקים מיקום וגודל.</li>
        <li>מחטים ודיו חד־פעמיים שנפתחים מול העיניים, ומשטחים מחוטאים לפני כל לקוח.</li>
        <li>אין לחץ של זמן: אם צריך – עוצרים, נושמים, שותים משהו וממשיכים.</li>
        <li>בסוף מקבלים הסבר על הטיפול, ויומן החלמה באפליקציה מלווה אותך יום אחרי יום.</li>
      </ul>
    </div>
    <div class="place-card rise" style="--k:2">
      {pic(25, "פינת ההמתנה בסטודיו", sizes="(max-width: 900px) 100vw, 520px")}
      <div class="in"><b style="font:700 1.2rem var(--f-d)">Tomchu Tattoo</b><span class="muted">{CFG["address"]} · בתיאום מראש בלבד</span><span class="muted">חניה בשפע ובחינם ליד הסטודיו</span>
        <div class="ctas" style="margin-top:6px">{ext(CFG["waze"], "Waze", "btn btn-ghost btn-sm", "nav")}{ext(CFG["maps"], "Google Maps", "btn btn-ghost btn-sm", "map")}{ext(MOOVIT, "Moovit", "btn btn-ghost btn-sm", "pin")}</div></div>
    </div>
  </div>
</section>'''

# ================================================================ TOM
cr = [('index.html', 'בית'), (None, 'תום והסטודיו')]
tom = phead('היי, <span class="iri-text">אני תום</span>', 'תום גבע · מקעקעת · אלפי מנשה', cr, '') + f'''
<section aria-labelledby="about-h">
  <div class="wrap split">
    <div class="frame rise" style="aspect-ratio:4/5"><picture><source type="image/webp" srcset="{{R}}assets/img/tom-studio-700.webp 700w, {{R}}assets/img/tom-studio-1400.webp 1400w" sizes="(max-width: 900px) 100vw, 480px"><img src="{{R}}assets/img/tom-studio.jpg" width="1400" height="788" alt="תום מקעקעת לקוחה בסטודיו שלה" style="object-position:28% 40%"></picture></div>
    <div class="stack rise" style="--k:2">
      <h2 id="about-h">קצת עליי</h2>
      <p class="lead">אני בת 38, נשואה לאייל ואמא לשלושה בנים מדהימים. התשוקה שלי לציור הובילה אותי ליצור על נייר, על נעליים ועל כל חפץ אפשרי. עבורי, האמנות היא דרך לביטוי עצמי ולבריחה לעולם שבו הכל אפשרי.</p>
      <ul class="facts"><li><b class="iri-text">21</b><span>הגיל של הקעקוע הראשון שלי</span></li><li><b class="iri-text">30+</b><span>קעקועים על הגוף שלי</span></li><li><b class="iri-text">3</b><span>בנים: תאי, ניו וסאן</span></li></ul>
      <p class="quote">״אצלי אין חוקים – רק חלומות שמתגשמים.״</p>
    </div>
  </div>
</section>
<section aria-labelledby="why-h" style="padding-top:0">
  <div class="wrap">
    <h2 id="why-h" class="sr">איך אני עובדת</h2>
    <div class="cards">
      <article class="card rise"><h3>למה קעקועים?</h3><p>קעקועים הם הרבה יותר מדיו על העור – הם סיפור חיים, זיכרון, ודרך לתת לנשמה לדבר. מאז הקעקוע הראשון שלי העולם הזה הפך לאהבה גדולה, וכל אחד מהקעקועים שלי מחזיק בתוכו רגע בזמן.</p></article>
      <article class="card rise" style="--k:1"><h3>איך אני עובדת</h3><p>לא צריך להגיע עם ציור מוכן. נשב יחד על כוס קפה, אקשיב לסיפור שלך, נבין איזה סגנון מרגש אותך – ואעצב סקיצה אישית שתהיה רק שלך.</p></article>
      <article class="card rise" style="--k:2"><h3>מה מרגש אותי במיוחד</h3><p>קאברים (Cover Up) וקעקועים על צלקות. יש משהו מרפא בלקחת זיכרון ישן או צלקת ולהפוך אותם למשהו חדש ויפה שמחזיר את הביטחון העצמי.</p></article>
    </div>
    <div class="stack" style="margin-top:22px"><h3>הסגנונות שלי</h3><ul class="chips"><li>Fine Line</li><li>ריאליזם</li><li>קאברים</li><li>סקיצה</li><li>עיצוב אישי</li></ul></div>
  </div>
</section>
{STUDIO_SECTIONS}
<section id="reviews" aria-labelledby="rev-h" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2 id="rev-h">מה מספרים <span class="iri-text">אחרי</span></h2></div>
    <div class="cards">{rev_cards(REVIEWS)}</div>
  </div>
</section>
<section style="padding-top:0"><div class="wrap"><div class="band rise">
  <div><h2>מחכה לך באהבה בסטודיו</h2><p>אני מזמינה אותך לבוא, לשבת איתי על כוס קפה, לדבר, להרגיש – ולהפוך יחד את הסיפור שלך ליצירת אמנות שתלווה אותך תמיד. תום</p></div>
  <div class="ctas"><a class="btn btn-light" href="{{R}}contact.html">בואו נדבר על הקעקוע שלך</a>{ext(CFG["instagram"], "Instagram", "btn btn-line", "ig")}</div>
</div></div></section>'''
page('tom.html', 'תום והסטודיו – הסיפור וסיור בסטודיו | Tomchu Tattoo', 'תום גבע, מקעקעת ואמנית מאלפי מנשה: הסיפור, הסגנונות, סיור בתמונות בסטודיו הפרטי, חניה בחינם והמלצות של לקוחות.', tom,
     ld=[crumbs_ld(cr), {"@context": "https://schema.org", "@type": "Person", "name": "תום גבע", "jobTitle": "מקעקעת", "worksFor": {"@id": SITE + "/#studio"}, "sameAs": [CFG['instagram'], CFG['facebook'], CFG['tiktok']]}])

# ================================================================ PROCESS
STEPS = [('רעיון', 'שולחים לתום בוואטסאפ מה בראש – תמונה, מילה, תחושה. לא בטוחים? המדריך באתר והרעיונות באפליקציה יעזרו.', 'guide.html', 'למדריך', False),
         ('סקיצה', 'תום מעצבת סקיצה מקורית רק בשבילך – ואפשר לראות איך היא תיראה על הגוף עוד לפני שמחליטים.', APP + '#/tryon', 'להדמיה על הגוף', True),
         ('יום הקעקוע', 'ממלאים הצהרת בריאות דיגיטלית מראש, מגיעים לסטודיו, ושותים קפה לפני שמתחילים.', 'health.html', 'למילוי הצהרת הבריאות', False),
         ('החלמה', 'יומן החלמה יום אחרי יום עם תזכורות – כדי שהקעקוע יישאר חד ויפה לשנים.', APP + '#/care', 'ליומן ההחלמה', True)]
sl = ''
for k, (t, p, h, b, x) in enumerate(STEPS):
    btn = ext(h, b, 'btn btn-soft btn-sm') if x else f'<a class="btn btn-soft btn-sm" href="{{R}}{h}">{b}</a>'
    sl += f'<li class="step rise" style="--k:{k}"><span class="n" aria-hidden="true">{k + 1:02d}</span><h3><span class="sr">שלב {k + 1}: </span>{t}</h3><p>{p}</p>{btn}</li>'
care = C['CARE']
cs = ''.join(f'<article class="card rise" style="--k:{k % 3}"><span class="muted" style="font-weight:600">{e(s["when"])}</span><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></article>' for k, s in enumerate(care['steps']))
fq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{e(f["q"])}</summary><p>{e(f["a"])}</p></details>' for i, f in enumerate(C['FAQ']))
cr = [('index.html', 'בית'), (None, 'לפני שמגיעים')]
process = phead('לפני <span class="iri-text">שמגיעים</span>', 'מהרגע שיש רעיון ועד שהקעקוע מחלים – תום איתך בכל שלב, וכל שלב מחובר לאפליקציה.', cr, '') + f'''
<section aria-labelledby="steps-h"><div class="wrap"><h2 id="steps-h" class="sr">ארבעה שלבים</h2><ol class="steps">{sl}</ol></div></section>
<section id="care" aria-labelledby="care-h" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><h2 id="care-h">מדריך <span class="iri-text">ההחלמה</span></h2></div>
    <div class="cards">{cs}</div>
    <div class="split" style="margin-top:22px;align-items:start">
      <div class="card"><h3>כן</h3><ul class="prose" style="padding-inline-start:20px;margin:0;color:var(--muted)">{"".join(f"<li>{e(x)}</li>" for x in care["dos"])}</ul></div>
      <div class="card"><h3>לא</h3><ul class="prose" style="padding-inline-start:20px;margin:0;color:var(--muted)">{"".join(f"<li>{e(x)}</li>" for x in care["donts"])}</ul></div>
    </div>
    <p class="card" style="margin-top:16px;border-color:var(--acc2)"><b>חשוב:</b> {e(care["warning"])}</p>
    <div class="ctas" style="margin-top:20px">{ext(APP + "#/care", "יומן ההחלמה באפליקציה", "btn btn-iri", "care")}</div>
  </div>
</section>
<section id="faq" aria-labelledby="faq-h" style="padding-top:0"><div class="wrap"><div class="sec-head"><h2 id="faq-h">שאלות <span class="iri-text">ותשובות</span></h2></div></div><div class="wrap split" style="align-items:start">
  <div class="faq">{fq}</div>
  <div class="card rise" style="position:sticky;top:90px"><h2 style="font-size:1.4rem">עוד שאלה?</h2><p>הכי מהיר בוואטסאפ – אפשר לצרף תמונה של הרעיון או של האזור.</p><div class="ctas"><a class="btn btn-iri" href="{WA}" data-wa="היי תום! יש לי שאלה לפני קעקוע: " target="_blank" rel="noopener">{ic("wa")}לשאול את תום<span class="sr"> (נפתח בחלון חדש)</span></a><a class="btn btn-soft" href="{{R}}guide.html">למדריך ההתאמה</a></div></div>
</div></section>'''
page('process.html', 'לפני שמגיעים – איך זה עובד ושאלות ותשובות | Tomchu Tattoo', 'ארבעה שלבים לקעקוע אצל תום, מדריך החלמה, ותשובות לשאלות הנפוצות: כאב, מחיר, סטריליות, חניה וקאברים.', process, ld=[crumbs_ld(cr), {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['a']}} for f in C['FAQ']]}])

# ================================================================ GUIDE
def opts(name, items):
    out = ''
    for v, b, s, pain in items:
        pd = f' <span class="pain" aria-hidden="true">{"".join(f"<i class={chr(34)}{"on" if i <= pain else ""}{chr(34)}></i>" for i in range(1, 6))}</span><span class="sr"> – רגישות {pain} מתוך 5</span>' if pain else ''
        out += f'<div class="opt"><input type="radio" name="{name}" id="{name}-{v}" value="{v}"><label for="{name}-{v}"><b>{b}{pd}</b>{f"<small>{s}</small>" if name=="size" else ""}</label></div>'
    return out
styles = [('fine', 'Fine Line', 'קווים דקים ועדינים', 0), ('real', 'ריאליזם', 'הצללות ועומק כמו תמונה', 0), ('color', 'צבע עדין', 'צבעי מים ופסטל', 0),
          ('sketch', 'סקיצה / איור', 'מראה של ציור יד', 0), ('letter', 'כיתוב', 'מילה, משפט, תאריך', 0), ('tiny', 'מיני', 'סמל קטן ועדין', 0), ('cover', 'קאבר / צלקת', 'חידוש או קאבר על ישן', 0)]
sizes = [('xs', 'מיני', 'עד 4 ס״מ', 0), ('s', 'קטן', '4–8 ס״מ', 0), ('m', 'בינוני', '8–15 ס״מ', 0), ('l', 'גדול', '15 ס״מ ומעלה', 0)]
places = [('wrist', 'פרק כף היד', 'עד 7 ס״מ', 3), ('forearm', 'אמה', '5–18 ס״מ', 2), ('upperarm', 'זרוע עליונה', '8–20 ס״מ', 2), ('shoulder', 'כתף / עורף', '6–15 ס״מ', 2), ('ear', 'מאחורי האוזן', 'עד 4 ס״מ', 3),
          ('collar', 'עצם הבריח', '4–12 ס״מ', 4), ('ribs', 'צלעות', '6–25 ס״מ', 5), ('back', 'גב', '10–40 ס״מ', 3), ('thigh', 'ירך', '10–25 ס״מ', 2), ('ankle', 'קרסול', 'עד 8 ס״מ', 4)]
samples = {
    'fine': [8, 13, 4], 'color': [9, 6, 20], 'sketch': [19, 5, 14], 'ba': [12, 11, 6]}
samples_js = json.dumps({k: [{'src': f'{{R}}assets/img/works/work{n}-600.webp', 'alt': WORK['w' + str(n)]['alt']} for n in v] for k, v in samples.items()}, ensure_ascii=False)
BODY = '''<figure class="body-fig"><svg class="body-map" viewBox="0 0 280 410" aria-hidden="true" focusable="false">
<defs><linearGradient id="skin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="var(--sk1)"/><stop offset="1" stop-color="var(--sk2)"/></linearGradient>
<radialGradient id="zon"><stop offset="0" stop-color="#FF6FA5"/><stop offset=".6" stop-color="#E8467F"/><stop offset="1" stop-color="#9B5BD6"/></radialGradient>
<filter id="zglow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<ellipse cx="210" cy="402" rx="34" ry="4" class="shadow"/><ellipse cx="70" cy="402" rx="34" ry="4" class="shadow"/>
<path class="sil" d="M210.0 6.0C213.3 6.0 217.2 6.2 220.0 8.0C222.8 9.8 225.2 13.3 226.5 17.0C227.8 20.7 227.7 25.8 227.5 30.0C227.3 34.2 226.6 38.5 225.5 42.0C224.4 45.5 222.3 48.7 221.0 51.0C219.7 53.3 218.0 53.8 217.5 56.0C217.0 58.2 216.1 61.7 218.0 64.0C219.9 66.3 225.2 68.2 229.0 70.0C232.8 71.8 237.8 72.8 241.0 75.0C244.2 77.2 246.7 79.5 248.5 83.0C250.3 86.5 251.2 91.2 252.0 96.0C252.8 100.8 252.9 106.7 253.5 112.0C254.1 117.3 254.8 123.2 255.5 128.0C256.2 132.8 256.7 136.2 257.5 141.0C258.3 145.8 259.6 151.7 260.5 157.0C261.4 162.3 262.2 168.0 263.0 173.0C263.8 178.0 264.2 183.2 265.0 187.0C265.8 190.8 267.2 192.5 268.0 196.0C268.8 199.5 269.8 204.3 269.5 208.0C269.2 211.7 267.8 216.5 266.5 218.0C265.2 219.5 262.7 218.8 261.5 217.0C260.3 215.2 260.2 210.7 259.5 207.0C258.8 203.3 258.5 199.8 257.5 195.0C256.5 190.2 254.8 183.8 253.5 178.0C252.2 172.2 250.8 165.7 249.5 160.0C248.2 154.3 247.0 149.3 246.0 144.0C245.0 138.7 244.4 133.7 243.5 128.0C242.6 122.3 241.2 111.3 240.5 110.0C239.8 108.7 239.5 115.0 239.0 120.0C238.5 125.0 238.2 133.3 237.5 140.0C236.8 146.7 234.5 153.3 234.5 160.0C234.5 166.7 236.5 173.3 237.5 180.0C238.5 186.7 240.1 192.7 240.5 200.0C240.9 207.3 240.5 215.7 240.0 224.0C239.5 232.3 238.5 241.7 237.5 250.0C236.5 258.3 234.8 267.3 234.0 274.0C233.2 280.7 232.8 284.0 233.0 290.0C233.2 296.0 235.1 302.0 235.0 310.0C234.9 318.0 233.8 328.3 232.5 338.0C231.2 347.7 228.0 361.0 227.0 368.0C226.0 375.0 225.7 376.2 226.5 380.0C227.3 383.8 231.3 388.0 232.0 391.0C232.7 394.0 232.8 396.8 230.5 398.0C228.2 399.2 220.6 400.0 218.5 398.0C216.4 396.0 217.9 390.7 218.0 386.0C218.1 381.3 219.0 377.3 219.0 370.0C219.0 362.7 217.9 351.7 218.0 342.0C218.1 332.3 219.6 320.3 219.5 312.0C219.4 303.7 217.9 298.0 217.5 292.0C217.1 286.0 217.2 282.7 217.0 276.0C216.8 269.3 217.0 260.3 216.5 252.0C216.0 243.7 215.1 232.7 214.0 226.0C212.9 219.3 211.3 212.0 210.0 212.0C208.7 212.0 207.1 219.3 206.0 226.0C204.9 232.7 204.0 243.7 203.5 252.0C203.0 260.3 203.2 269.3 203.0 276.0C202.8 282.7 202.9 286.0 202.5 292.0C202.1 298.0 200.6 303.7 200.5 312.0C200.4 320.3 201.9 332.3 202.0 342.0C202.1 351.7 201.0 362.7 201.0 370.0C201.0 377.3 201.9 381.3 202.0 386.0C202.1 390.7 203.6 396.0 201.5 398.0C199.4 400.0 191.8 399.2 189.5 398.0C187.2 396.8 187.3 394.0 188.0 391.0C188.7 388.0 192.7 383.8 193.5 380.0C194.3 376.2 194.0 375.0 193.0 368.0C192.0 361.0 188.8 347.7 187.5 338.0C186.2 328.3 185.1 318.0 185.0 310.0C184.9 302.0 186.8 296.0 187.0 290.0C187.2 284.0 186.8 280.7 186.0 274.0C185.2 267.3 183.5 258.3 182.5 250.0C181.5 241.7 180.5 232.3 180.0 224.0C179.5 215.7 179.1 207.3 179.5 200.0C179.9 192.7 181.5 186.7 182.5 180.0C183.5 173.3 185.5 166.7 185.5 160.0C185.5 153.3 183.2 146.7 182.5 140.0C181.8 133.3 181.5 125.0 181.0 120.0C180.5 115.0 180.2 108.7 179.5 110.0C178.8 111.3 177.4 122.3 176.5 128.0C175.6 133.7 175.0 138.7 174.0 144.0C173.0 149.3 171.8 154.3 170.5 160.0C169.2 165.7 167.8 172.2 166.5 178.0C165.2 183.8 163.5 190.2 162.5 195.0C161.5 199.8 161.2 203.3 160.5 207.0C159.8 210.7 159.7 215.2 158.5 217.0C157.3 218.8 154.8 219.5 153.5 218.0C152.2 216.5 150.8 211.7 150.5 208.0C150.2 204.3 151.2 199.5 152.0 196.0C152.8 192.5 154.2 190.8 155.0 187.0C155.8 183.2 156.2 178.0 157.0 173.0C157.8 168.0 158.6 162.3 159.5 157.0C160.4 151.7 161.7 145.8 162.5 141.0C163.3 136.2 163.8 132.8 164.5 128.0C165.2 123.2 165.9 117.3 166.5 112.0C167.1 106.7 167.2 100.8 168.0 96.0C168.8 91.2 169.7 86.5 171.5 83.0C173.3 79.5 175.8 77.2 179.0 75.0C182.2 72.8 187.2 71.8 191.0 70.0C194.8 68.2 200.1 66.3 202.0 64.0C203.9 61.7 203.0 58.2 202.5 56.0C202.0 53.8 200.3 53.3 199.0 51.0C197.7 48.7 195.6 45.5 194.5 42.0C193.4 38.5 192.7 34.2 192.5 30.0C192.3 25.8 192.2 20.7 193.5 17.0C194.8 13.3 197.2 9.8 200.0 8.0C202.8 6.2 206.7 6.0 210.0 6.0Z"/><path class="sil" d="M70.0 6.0C73.3 6.0 77.2 6.2 80.0 8.0C82.8 9.8 85.2 13.3 86.5 17.0C87.8 20.7 87.7 25.8 87.5 30.0C87.3 34.2 86.6 38.5 85.5 42.0C84.4 45.5 82.3 48.7 81.0 51.0C79.7 53.3 78.0 53.8 77.5 56.0C77.0 58.2 76.1 61.7 78.0 64.0C79.9 66.3 85.2 68.2 89.0 70.0C92.8 71.8 97.8 72.8 101.0 75.0C104.2 77.2 106.7 79.5 108.5 83.0C110.3 86.5 111.2 91.2 112.0 96.0C112.8 100.8 112.9 106.7 113.5 112.0C114.1 117.3 114.8 123.2 115.5 128.0C116.2 132.8 116.7 136.2 117.5 141.0C118.3 145.8 119.6 151.7 120.5 157.0C121.4 162.3 122.2 168.0 123.0 173.0C123.8 178.0 124.2 183.2 125.0 187.0C125.8 190.8 127.2 192.5 128.0 196.0C128.8 199.5 129.8 204.3 129.5 208.0C129.2 211.7 127.8 216.5 126.5 218.0C125.2 219.5 122.7 218.8 121.5 217.0C120.3 215.2 120.2 210.7 119.5 207.0C118.8 203.3 118.5 199.8 117.5 195.0C116.5 190.2 114.8 183.8 113.5 178.0C112.2 172.2 110.8 165.7 109.5 160.0C108.2 154.3 107.0 149.3 106.0 144.0C105.0 138.7 104.4 133.7 103.5 128.0C102.6 122.3 101.2 111.3 100.5 110.0C99.8 108.7 99.5 115.0 99.0 120.0C98.5 125.0 98.2 133.3 97.5 140.0C96.8 146.7 94.5 153.3 94.5 160.0C94.5 166.7 96.5 173.3 97.5 180.0C98.5 186.7 100.1 192.7 100.5 200.0C100.9 207.3 100.5 215.7 100.0 224.0C99.5 232.3 98.5 241.7 97.5 250.0C96.5 258.3 94.8 267.3 94.0 274.0C93.2 280.7 92.8 284.0 93.0 290.0C93.2 296.0 95.1 302.0 95.0 310.0C94.9 318.0 93.8 328.3 92.5 338.0C91.2 347.7 88.0 361.0 87.0 368.0C86.0 375.0 85.7 376.2 86.5 380.0C87.3 383.8 91.3 388.0 92.0 391.0C92.7 394.0 92.8 396.8 90.5 398.0C88.2 399.2 80.6 400.0 78.5 398.0C76.4 396.0 77.9 390.7 78.0 386.0C78.1 381.3 79.0 377.3 79.0 370.0C79.0 362.7 77.9 351.7 78.0 342.0C78.1 332.3 79.6 320.3 79.5 312.0C79.4 303.7 77.9 298.0 77.5 292.0C77.1 286.0 77.2 282.7 77.0 276.0C76.8 269.3 77.0 260.3 76.5 252.0C76.0 243.7 75.1 232.7 74.0 226.0C72.9 219.3 71.3 212.0 70.0 212.0C68.7 212.0 67.1 219.3 66.0 226.0C64.9 232.7 64.0 243.7 63.5 252.0C63.0 260.3 63.2 269.3 63.0 276.0C62.8 282.7 62.9 286.0 62.5 292.0C62.1 298.0 60.6 303.7 60.5 312.0C60.4 320.3 61.9 332.3 62.0 342.0C62.1 351.7 61.0 362.7 61.0 370.0C61.0 377.3 61.9 381.3 62.0 386.0C62.1 390.7 63.6 396.0 61.5 398.0C59.4 400.0 51.8 399.2 49.5 398.0C47.2 396.8 47.3 394.0 48.0 391.0C48.7 388.0 52.7 383.8 53.5 380.0C54.3 376.2 54.0 375.0 53.0 368.0C52.0 361.0 48.8 347.7 47.5 338.0C46.2 328.3 45.1 318.0 45.0 310.0C44.9 302.0 46.8 296.0 47.0 290.0C47.2 284.0 46.8 280.7 46.0 274.0C45.2 267.3 43.5 258.3 42.5 250.0C41.5 241.7 40.5 232.3 40.0 224.0C39.5 215.7 39.1 207.3 39.5 200.0C39.9 192.7 41.5 186.7 42.5 180.0C43.5 173.3 45.5 166.7 45.5 160.0C45.5 153.3 43.2 146.7 42.5 140.0C41.8 133.3 41.5 125.0 41.0 120.0C40.5 115.0 40.2 108.7 39.5 110.0C38.8 111.3 37.4 122.3 36.5 128.0C35.6 133.7 35.0 138.7 34.0 144.0C33.0 149.3 31.8 154.3 30.5 160.0C29.2 165.7 27.8 172.2 26.5 178.0C25.2 183.8 23.5 190.2 22.5 195.0C21.5 199.8 21.2 203.3 20.5 207.0C19.8 210.7 19.7 215.2 18.5 217.0C17.3 218.8 14.8 219.5 13.5 218.0C12.2 216.5 10.8 211.7 10.5 208.0C10.2 204.3 11.2 199.5 12.0 196.0C12.8 192.5 14.2 190.8 15.0 187.0C15.8 183.2 16.2 178.0 17.0 173.0C17.8 168.0 18.6 162.3 19.5 157.0C20.4 151.7 21.7 145.8 22.5 141.0C23.3 136.2 23.8 132.8 24.5 128.0C25.2 123.2 25.9 117.3 26.5 112.0C27.1 106.7 27.2 100.8 28.0 96.0C28.8 91.2 29.7 86.5 31.5 83.0C33.3 79.5 35.8 77.2 39.0 75.0C42.2 72.8 47.2 71.8 51.0 70.0C54.8 68.2 60.1 66.3 62.0 64.0C63.9 61.7 63.0 58.2 62.5 56.0C62.0 53.8 60.3 53.3 59.0 51.0C57.7 48.7 55.6 45.5 54.5 42.0C53.4 38.5 52.7 34.2 52.5 30.0C52.3 25.8 52.2 20.7 53.5 17.0C54.8 13.3 57.2 9.8 60.0 8.0C62.8 6.2 66.7 6.0 70.0 6.0Z"/>
<g class="det"><path d="M184 74Q198 70 207 75M236 74Q222 70 213 75"/><path d="M188 100Q198 110 209 104M232 100Q222 110 211 104"/><path d="M210 110V170"/><path d="M202 128H218M202 143H218M203 157H217"/><circle cx="210" cy="168" r="1.2"/><path d="M188 180Q200 196 210 208M232 180Q220 196 210 208"/><path d="M191 282q4 5 8 0M229 282q-4 5 -8 0"/><path d="M70 60V205"/><path d="M46 88Q54 112 64 108M94 88Q86 112 76 108"/><path d="M46 164Q58 176 68 172M94 164Q82 176 72 172"/><path d="M68 196Q56 218 44 206M72 196Q84 218 96 206"/><path d="M52 296q4 -4 8 0M88 296q-4 -4 -8 0"/></g>
<ellipse class="zone" id="z-collar" data-place="collar" cx="223" cy="72" rx="11" ry="3.6" transform="rotate(10 223 72)"/><ellipse class="zone" id="z-arm" data-place="upperarm" cx="250" cy="112" rx="6.2" ry="17" transform="rotate(-6 250 112)"/><ellipse class="zone" id="z-forearm" data-place="forearm" cx="257" cy="161" rx="5.6" ry="15" transform="rotate(-11 257 161)"/><ellipse class="zone" id="z-wrist" data-place="wrist" cx="262.5" cy="190" rx="5" ry="3.2" transform="rotate(-14 262.5 190)"/><ellipse class="zone" id="z-ribs" data-place="ribs" cx="230" cy="134" rx="6.5" ry="15" transform="rotate(4 230 134)"/><ellipse class="zone" id="z-thigh" data-place="thigh" cx="226" cy="238" rx="10" ry="23" transform="rotate(-3 226 238)"/><ellipse class="zone" id="z-ankle" data-place="ankle" cx="223" cy="374" rx="5.5" ry="4.2"/><ellipse class="zone" id="z-ear" data-place="ear" cx="54.5" cy="33" rx="3.2" ry="6"/><ellipse class="zone" id="z-shoulder" data-place="shoulder" cx="48" cy="76" rx="12" ry="6" transform="rotate(14 48 76)"/><ellipse class="zone" id="z-back" data-place="back" cx="70" cy="128" rx="19" ry="32"/>
</svg><figcaption><span>מלפנים</span><span>מאחור</span></figcaption></figure>'''
cr = [('index.html', 'בית'), (None, 'איזה קעקוע מתאים לי?')]
guide = phead('איזה קעקוע <span class="iri-text">מתאים לי?</span>', 'שלוש בחירות קצרות – וקבלו המלצה מיידית: גודל מומלץ למיקום, זמן משוער, רמת רגישות ודוגמאות מהעבודות של תום. בסוף אפשר לשלוח הכול לתום בוואטסאפ בלחיצה.', cr, '') + f'''
<section aria-label="המדריך">
  <div class="wrap guide">
    <form id="guide-form" onsubmit="return false">
      <fieldset class="q"><legend><span class="n" aria-hidden="true">1</span>איזה סגנון מושך אותך?</legend><div class="opts">{opts("style", styles)}</div></fieldset>
      <fieldset class="q"><legend><span class="n" aria-hidden="true">2</span>באיזה גודל?</legend><div class="opts">{opts("size", sizes)}</div></fieldset>
      <fieldset class="q"><legend><span class="n" aria-hidden="true">3</span>איפה על הגוף?</legend><div class="opts">{opts("place", places)}</div></fieldset>
      <fieldset class="q"><legend><span class="n" aria-hidden="true">4</span>זה הקעקוע הראשון?</legend><div class="opts">{opts("first", [("yes", "כן, הראשון", "מתרגשים!", 0), ("no", "כבר יש לי", "מכירים את התחושה", 0)])}</div></fieldset>
    </form>
    <aside class="stack" aria-label="תוצאה">
      {BODY}
      <div class="result" id="guide-out" aria-live="polite"><h2>ההמלצה שלך</h2><p class="empty">בחרו סגנון, גודל ומיקום – וההמלצה תופיע כאן מיד.</p></div>
    </aside>
  </div>
  <script type="application/json" id="guide-samples">{samples_js}</script>
</section>'''
page('guide.html', 'איזה קעקוע מתאים לי? מדריך אינטראקטיבי | Tomchu Tattoo', 'מדריך קצר לבחירת קעקוע: בוחרים סגנון, גודל ומיקום ומקבלים גודל מומלץ, זמן משוער, רמת רגישות ודוגמאות – ושולחים לתום בוואטסאפ.', guide, ld=[crumbs_ld(cr)])


# ================================================================ GIFT VOUCHER (same backend + approval flow as the app)
GIFT_CFG = json.dumps({'biz': BIZ_ID, 'name': 'תום גבע · Tomchu Tattoo', 'addr': CFG['address'], 'mail': CFG['email'], 'endpoint': CFG.get('healthEndpoint', ''), 'min': CFG.get('giftMin', 200), 'pay': CFG.get('payLinks', {}), 'phone': CFG['phoneDisplay'], 'wa': CFG['whatsapp'], 'app': APP}, ensure_ascii=False)
cr = [('index.html', 'בית'), (None, 'שובר מתנה')]
giftb = phead('מתנה <span class="iri-text">שנשארת לתמיד</span>', None, cr, '') + f"""
<section aria-label="קניית שובר מתנה" style="padding-top:8px"><div class="wrap"><div class="gift-page" id="gift" aria-live="polite"><noscript><p>כדי לקנות שובר צריך JavaScript. אפשר גם לכתוב לתום בוואטסאפ.</p></noscript></div></div>
<script type="application/json" id="gift-cfg">{GIFT_CFG}</script></section>"""
page('gift.html', 'שובר מתנה לקעקוע | Tomchu Tattoo', 'שובר מתנה לקעקוע אצל תום: בוחרים סכום ועיצוב, משלמים בביט או בפייבוקס, והשובר נשלח בוואטסאפ.', giftb, ld=[crumbs_ld(cr)])

# ================================================================ HEALTH DECLARATION (same questions + backend as the app)
QS, CONS = C['QUESTIONS'], C['CONSENTS']
def _hq(q):
    return f"""<fieldset class="hq" id="fs-{q['id']}"><legend>{e(q['text'])}</legend>
  <div class="yn"><label><input type="radio" name="{q['id']}" value="לא"><span>לא</span></label><label><input type="radio" name="{q['id']}" value="כן"><span>כן</span></label></div>
  <p class="qn qn-{q['level']}" id="qn-{q['id']}" hidden>{e(q['note'])}</p>
  <div class="field" id="qdw-{q['id']}" hidden><label for="qd-{q['id']}">פירוט{' (לא חובה)' if q['level'] == 'stop' else ''}</label><textarea id="qd-{q['id']}" name="d_{q['id']}" rows="2"></textarea></div>
</fieldset>"""
def _hc(c):
    star = ' <span class="req" aria-hidden="true">*</span>' if c.get('required') else ''
    return f'<label class="hchk"><input type="checkbox" name="{c["id"]}"{" required" if c.get("required") and not c.get("minorOnly") else ""}><span>{e(c["text"])}{star}</span></label>'
def _f(id_, name, label, req=False, typ='text', extra='', hint=''):
    star = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    return f'<div class="field"><label for="{id_}">{label}{star}</label><input id="{id_}" name="{name}" type="{typ}"{" required" if req else ""} aria-describedby="{id_}-err"{extra}><span class="err" id="{id_}-err"></span></div>'
HCFG = json.dumps({'endpoint': CFG.get('healthEndpoint', ''), 'wa': CFG['whatsapp'], 'questions': QS, 'consents': CONS}, ensure_ascii=False)
cr = [('index.html', 'בית'), (None, 'הצהרת בריאות')]
healthb = phead('הצהרת <span class="iri-text">בריאות</span>', None, cr, '') + f"""
<section aria-label="טופס הצהרת בריאות" style="padding-top:8px"><div class="wrap hgrid">
<div class="hmain">
<form id="health-form" novalidate>
  <ol class="hsteps" aria-label="שלבי הטופס"><li data-s="1"><span>1</span> פרטים אישיים</li><li data-s="2"><span>2</span> שאלות בריאות</li><li data-s="3"><span>3</span> אישור וחתימה</li></ol>
  <p class="sr" id="h-stepnow" aria-live="polite"></p>
  <div class="hstep" data-step="1">
    {_f('h-name', 'name', 'שם מלא', True, extra=' autocomplete="name"')}
    <div class="g2">{_f('h-dob', 'dob', 'תאריך לידה', True, 'date')}{_f('h-phone', 'phone', 'טלפון', True, 'tel', ' autocomplete="tel" inputmode="tel"')}</div>
    {_f('h-address', 'address', 'כתובת מגורים', True, extra=' autocomplete="street-address" placeholder="רחוב, מספר ועיר"')}
    {_f('h-design', 'design', 'מה מקעקעים?', True, extra=' placeholder="למשל: פרח בקו עדין, 6 ס״מ, שחור"')}
    <div class="g2">{_f('h-date', 'tdate', 'תאריך הקעקוע', False, 'date')}{_f('h-area', 'area', 'אזור הקעקוע', False, extra=' placeholder="למשל: אמה"')}</div>
    <div class="g2">{_f('h-id', 'idnum', 'תעודת זהות (לא חובה)', False, 'text', ' inputmode="numeric" maxlength="9"')}{_f('h-email', 'email', 'אימייל (לא חובה)', False, 'email', ' autocomplete="email"')}</div>
    <fieldset class="hgroup"><legend>איש קשר לחירום (לא חובה)</legend><div class="g2">{_f('h-ename', 'ename', 'שם')}{_f('h-ephone', 'ephone', 'טלפון', False, 'tel', ' inputmode="tel"')}</div></fieldset>
    <p class="hnote">בסטודיו נבקש לראות תעודה מזהה לאימות גיל.</p>
    <p class="hnote" id="minor-note" hidden>מתחת לגיל 18 נדרשים פרטי הורה או אפוטרופוס וחתימתו, בשלב האחרון.</p>
  </div>
  <div class="hstep" data-step="2" hidden>
    <div class="hqs">{''.join(_hq(q) for q in QS)}</div>
    <p class="err" id="h-q-err" role="alert"></p>
  </div>
  <div class="hstep" data-step="3" hidden>
    <div id="parent-block" hidden>
      <p class="hnote">ממלא/ת ההצהרה מתחת לגיל 18: נדרשים פרטי הורה או אפוטרופוס, והחתימה למטה היא של ההורה.</p>
      {_f('h-pname', 'pname', 'שם ההורה', True)}
      <div class="g2">{_f('h-pid', 'pid', 'ת״ז ההורה', True, 'text', ' inputmode="numeric" maxlength="9"')}{_f('h-pphone', 'pphone', 'טלפון ההורה', True, 'tel', ' inputmode="tel"')}</div>
      {''.join(_hc(c) for c in CONS if c.get('minorOnly'))}
    </div>
    <div class="hchks">{''.join(_hc(c) for c in CONS if not c.get('minorOnly'))}</div>
    <p class="err" id="h-c-err" role="alert"></p>
    <div class="field"><span class="flabel" id="sig-label"><span id="sig-who">חתימה</span> <span class="req" aria-hidden="true">*</span></span>
      <div class="sig-wrap"><canvas id="sig" role="img" aria-labelledby="sig-label"></canvas><span class="sig-ph" id="sig-ph">חתמו כאן עם האצבע או העכבר</span></div>
      <div class="sig-row"><span class="err" id="h-sig-err" role="alert"></span><button type="button" class="link-btn" id="sig-clear">ניקוי חתימה</button></div>
    </div>
    <p class="hlock">ההצהרה נשלחת ישירות לתום ואינה נשמרת באתר. <a href="{{R}}privacy.html">מדיניות פרטיות</a></p>
  </div>
  <div class="hacts"><button type="button" class="btn btn-soft" id="h-prev" hidden>חזרה</button><button type="submit" class="btn btn-iri" id="h-next">המשך</button></div>
</form>
<div id="health-done" class="hdone" hidden tabindex="-1"></div>
</div>
<aside class="hside" aria-label="מידע על ההצהרה">
  <h2>3 דקות, פעם אחת</h2>
  <ol><li>פרטים אישיים</li><li>14 שאלות קצרות, כן או לא</li><li>אישור וחתימה, עם האצבע או העכבר</li></ol>
  <p class="hnote">עונים בכנות. תשובת "כן" לא אומרת שלא נקעקע, רק שתום תבדוק לפני התור.</p>
  {ext('https://wa.me/' + CFG['whatsapp'], 'שאלה? לכתוב לתום בוואטסאפ', 'btn btn-ghost', 'wa')}
</aside>
</div>
<noscript><div class="wrap"><p>כדי למלא את ההצהרה צריך JavaScript. אפשר גם למלא אותה בסטודיו.</p></div></noscript>
<script type="application/json" id="health-cfg">{HCFG}</script></section>"""
page('health.html', 'הצהרת בריאות לפני קעקוע | Tomchu Tattoo', 'הצהרת בריאות דיגיטלית לפני הקעקוע אצל תום: פרטים, שאלות קצרות וחתימה. נשלחת ישירות לתום.', healthb, ld=[crumbs_ld(cr)])

# ================================================================ JOURNAL
posts = ''
for k, a in enumerate(C['ARTICLES']):
    posts += f'<a class="post rise" style="--k:{k % 3}" href="{{R}}journal/{a["id"]}.html"><span class="tag">{e(a["tag"])}</span><h2>{e(a["title"])}</h2><span class="more">לקריאה ←</span></a>'
cr = [('index.html', 'בית'), (None, 'מאמרים')]
journal = phead('מאמרים <span class="iri-text">מהסטודיו</span>', 'כל מה שכדאי לדעת לפני, בזמן ואחרי הקעקוע – בשפה פשוטה, מתום.', cr, '') + f'<section aria-label="רשימת מאמרים"><div class="wrap"><div class="posts">{posts}</div></div></section>'
page('journal.html', 'מאמרים על קעקועים – מדריכים מתום | Tomchu Tattoo', 'מאמרים ומדריכים: 10 דברים לפני קעקוע ראשון, איך בוחרים קעקוע, סגנונות, היסטוריה ומכונות קעקוע.', journal, ld=[crumbs_ld(cr)])
for a in C['ARTICLES']:
    cr = [('index.html', 'בית'), ('journal.html', 'מאמרים'), (None, a['title'])]
    secs = ''.join(f'<h2>{e(s["h"])}</h2>' + (f'<p>{e(s["p"])}</p>' if s.get('p') else '') + ('<ul>' + ''.join(f'<li>{e(x)}</li>' for x in s['list']) + '</ul>' if s.get('list') else '') for s in a['sections'])
    others = ''.join(f'<li><a href="{{R}}journal/{o["id"]}.html">{e(o["title"])}</a></li>' for o in C['ARTICLES'] if o['id'] != a['id'])
    body = phead(e(a['title']), None, cr, '../') + f'<div class="wrap"><p class="lead" style="margin:0 0 8px">{e(a["intro"])}</p></div>' + f'''
<section aria-label="המאמר"><div class="wrap split artgrid">
  <article class="prose">{secs}<div class="band" style="margin-top:28px"><div><h2 style="margin:0">רוצים לדבר על זה עם תום?</h2></div><div class="ctas"><a class="btn btn-light" href="{{R}}contact.html">לקביעת שיחה</a></div></div></article>
  <aside class="card"><h2 style="font-size:1.15rem">עוד מאמרים</h2><ul class="prose" style="padding-inline-start:18px;margin:0">{others}</ul></aside>
</div></section>'''
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a['title'], "description": a['intro'], "inLanguage": "he",
          "author": {"@type": "Person", "name": "תום גבע"}, "publisher": {"@id": SITE + "/#studio"}, "image": SITE + "/assets/img/og.jpg", "mainEntityOfPage": f"{SITE}/journal/{a['id']}.html"}
    page(f'journal/{a["id"]}.html', f'{a["title"]} | Tomchu Tattoo', a['intro'][:155], body, R='../', ld=[crumbs_ld(cr), ld])

# ================================================================ CONTACT
cr = [('index.html', 'בית'), (None, 'קביעת תור')]
place_opts = ''.join(f'<option>{p[1]}</option>' for p in places) + '<option>עוד לא יודע/ת</option>'
contact = phead('בואו נדבר על <span class="iri-text">הקעקוע שלך</span>', 'הדרך הכי מהירה היא וואטסאפ. ממלאים כמה פרטים – וההודעה לתום מוכנה לשליחה. שום מידע לא נשמר באתר.', cr, '') + f'''
<section aria-label="יצירת קשר"><div class="wrap split" style="align-items:start">
  <form class="form card" id="wa-form" aria-labelledby="wa-h">
    <h2 id="wa-h" style="font-size:1.4rem">הודעה מוכנה לתום</h2>
    <div class="two">
      <div class="field"><label for="f-name">שם</label><input id="f-name" name="name" autocomplete="given-name"></div>
      <div class="field"><label for="f-when">מתי נוח לך?</label><select id="f-when" name="when"><option value="">לא משנה</option><option>בוקר</option><option>צהריים</option><option>ערב</option><option>סוף שבוע</option></select></div>
    </div>
    <div class="field"><label for="f-idea">מה הרעיון?</label><textarea id="f-idea" name="idea" aria-describedby="f-idea-h"></textarea><span class="hint" id="f-idea-h">מילה, תחושה, השראה. תמונות אפשר לצרף בוואטסאפ.</span></div>
    <div class="two">
      <div class="field"><label for="f-place">איפה על הגוף?</label><select id="f-place" name="place"><option value="">עוד לא החלטתי</option>{place_opts}</select></div>
      <div class="field"><label for="f-size">גודל משוער</label><select id="f-size" name="size"><option value="">לא בטוח/ה</option><option>מיני (עד 4 ס״מ)</option><option>קטן (4–8 ס״מ)</option><option>בינוני (8–15 ס״מ)</option><option>גדול (15+ ס״מ)</option></select></div>
    </div>
    <div class="opt" style="max-width:320px"><input type="checkbox" id="f-first" name="first" value="1"><label for="f-first"><b>זה הקעקוע הראשון שלי</b></label></div>
    <div class="field"><span style="font-weight:600" id="wa-pv-l">כך תיראה ההודעה</span><div class="preview" id="wa-preview" aria-labelledby="wa-pv-l"></div></div>
    <button class="btn btn-iri brand-wa" type="submit">{ic("wa")}פתיחה בוואטסאפ<span class="sr"> (נפתח בחלון חדש)</span></button>
  </form>
  <div class="stack">
    <ul class="channels">
      <li><a href="{WA}" target="_blank" rel="noopener"><span class="ic">{ic("wa")}</span><span><b>וואטסאפ</b><small>הכי מהיר · אפשר לשלוח תמונות</small></span><span class="sr"> (נפתח בחלון חדש)</span></a></li>
      <li><a href="tel:+972542885771"><span class="ic">{ic("phone")}</span><span><b>054-288-5771</b><small>שיחה עם תום</small></span></a></li>
      <li><a href="mailto:{CFG["email"]}"><span class="ic">{ic("mail")}</span><span><b>{CFG["email"]}</b><small>למי שמעדיף מייל</small></span></a></li>
    </ul>
    <div class="place-card">
      {pic(24, "מבט כללי על הסטודיו", sizes="(max-width: 900px) 100vw, 520px")}
      <div class="in"><b style="font:700 1.2rem var(--f-d)">{CFG["address"]}</b><span class="muted">בתיאום מראש בלבד · חניה בחינם</span>
        <div class="ctas" style="margin-top:6px">{ext(CFG["waze"], "Waze", "btn btn-ghost btn-sm", "nav")}{ext(CFG["maps"], "Google Maps", "btn btn-ghost btn-sm", "map")}{ext(MOOVIT, "Moovit", "btn btn-ghost btn-sm", "pin")}</div></div>
    </div>
    <ol class="steps" style="grid-template-columns:1fr;gap:10px">
      <li class="step"><h3>1 · שולחים רעיון</h3><p>מילה, תמונה, תחושה – הכול מתאים.</p></li>
      <li class="step"><h3>2 · שיחת ייעוץ</h3><p>מדברים על גודל, מיקום ומחיר. בלי התחייבות.</p></li>
      <li class="step"><h3>3 · קובעים תאריך</h3><p>תום מכינה סקיצה מקורית לקראת היום.</p></li>
    </ol>
  </div>
</div></section>'''
page('contact.html', 'קביעת תור לקעקוע – וואטסאפ, טלפון והגעה | Tomchu Tattoo', 'קובעים שיחת ייעוץ לקעקוע אצל תום באלפי מנשה: הודעת וואטסאפ מוכנה, טלפון 054-288-5771, מייל, Waze ו־Google Maps. חניה בחינם.', contact, ld=[crumbs_ld(cr), BUSINESS])

# ================================================================ APP
FE = [('health', 'הצהרת בריאות', 'ממלאים מהטלפון לפני שמגיעים', '#/health', '#2FC4CF'), ('care', 'יומן החלמה', 'תזכורות והוראות יום אחרי יום', '#/care', '#22C08F'),
      ('gift', 'שובר מתנה', 'לפנק מישהו בקעקוע, בביט או בפייבוקס', '#/gift', '#F0457F'), ('camera', 'הדמיה על הגוף', 'מעלים תמונה ורואים איך ייראה', '#/tryon', '#A46BE6')]
fl = ''.join(f'<li><a href="{APP}{h}" target="_blank" rel="noopener" style="--c:{c}"><span class="ic">{ic(i)}</span><span><b>{t}</b></span><span class="sr"> (נפתח בחלון חדש)</span></a></li>' for i, t, s, h, c in FE)
cr = [('index.html', 'בית'), (None, 'האפליקציה')]
app = phead('הסטודיו של תום <span class="iri-text">בכיס</span>', 'כל מה שצריך לפני ואחרי הקעקוע – באפליקציה אחת, בחינם, לאנדרואיד ולאייפון.', cr, '') + f'''
<section aria-label="האפליקציה"><div class="wrap"><div class="app-card rise">
  <div class="stack">
    <ul class="feats">{fl}</ul>
    <div class="ctas">{ext(PLAY, "להורדה לאנדרואיד", "btn btn-iri", "android")}{ext(IOS, "התקנה באייפון", "btn btn-ghost", "apple")}</div>
    <p class="note">באנדרואיד האפליקציה בשלב בדיקה ב־Google Play. באייפון מוסיפים למסך הבית מהדפדפן – ההוראות בקישור.</p>
    <p><a href="{APP}" target="_blank" rel="noopener">לפתוח את האפליקציה בדפדפן<span class="sr"> (נפתח בחלון חדש)</span></a></p>
  </div>
  <div class="phone" aria-hidden="true">
    <div class="pt"><img class="lg-d" src="{{R}}assets/img/logo-96.png" alt="" width="22" height="22"><img class="lg-l" src="{{R}}assets/img/logo-light-96.png" alt="" width="22" height="22"><span dir="ltr">Tomchu Tattoo</span></div>
    <div class="ph"><img src="{{R}}assets/img/works/work23-600.webp" alt="" width="600" height="400"></div>
    <div class="g"><span>הצהרת בריאות</span><span>וואטסאפ לתום</span><span class="w">שובר מתנה – לפנק מישהו בקעקוע</span><span>הדמיה על הגוף</span><span>רעיונות</span></div>
  </div>
</div></div></section>'''
page('app.html', 'אפליקציית Tomchu Tattoo – הצהרת בריאות, החלמה ושובר מתנה', 'האפליקציה של תום: הצהרת בריאות דיגיטלית, יומן החלמה עם תזכורות, שובר מתנה והדמיה של קעקוע על הגוף. לאנדרואיד ולאייפון.', app, ld=[crumbs_ld(cr)])

# ================================================================ ACCESSIBILITY
cr = [('index.html', 'בית'), (None, 'הצהרת נגישות')]
acc = phead('הצהרת נגישות', None, cr, '') + f'''
<section aria-label="הצהרת נגישות"><div class="wrap prose">
<p>ב־Tomchu Tattoo חשוב לנו שכל אחת ואחד יוכלו להכיר את הסטודיו, לראות עבודות ולפנות לתום בקלות – כולל אנשים עם מוגבלות. האתר הונגש בהתאם לתקנות שוויון זכויות לאנשים עם מוגבלות (התאמות נגישות לשירות), התשע״ג–2013, ולתקן הישראלי ת״י 5568, המבוסס על הנחיות WCAG 2.0 ברמה AA.</p>
<h2>מה עשינו באתר</h2>
<ul>
<li>תפריט נגישות קבוע (הכפתור הכחול בפינה): הגדלת טקסט, ניגודיות גבוהה, גופן קריא, הדגשת קישורים ועצירת אנימציות. הבחירה נשמרת בדפדפן.</li>
<li>ניווט מלא במקלדת, קישור ״דילוג לתוכן הראשי״ ומסגרת פוקוס ברורה.</li>
<li>תמיכה בקוראי מסך: מבנה כותרות היררכי, תיאור טקסטואלי לתמונות, פירורי לחם ותוויות לכל שדה וכפתור.</li>
<li>ניגודיות צבעים לפי רמה AA במצב כהה ובמצב בהיר, ומידע שלא מועבר בצבע בלבד.</li>
<li>כיבוד הגדרת ״הפחתת תנועה״ של המכשיר, וכפתור ״עצירת אנימציות״ בתפריט הנגישות.</li>
<li>גלריה ותצוגה מוגדלת שעובדות עם מקלדת (חיצים ו־Esc), השוואת לפני/אחרי עם מקלדת, ותפריטים שנסגרים ב־Esc.</li>
<li>התאמה לטלפון, לטאבלט ולמחשב, וכפתורים גדולים ונוחים ללחיצה.</li>
</ul>
<h2>מגבלות ידועות</h2>
<p>קישורים לאתרים חיצוניים (רשתות חברתיות, Waze, Google Maps וחנות האפליקציות) אינם בשליטתנו ועשויים שלא להיות נגישים במלואם.</p>
<h2>נגישות הסטודיו</h2>
<p>הסטודיו נמצא ברחוב קדרון 48, אלפי מנשה, וחניה זמינה בסמוך. הכניסה לסטודיו היא דרך שער, ללא מדרגות. רוחב השער 115 ס״מ, ורוחב דלת הסטודיו 78 ס״מ. צריכים התאמה? ספרו לתום מראש ונדאג לכם.</p>
<h2>נתקלתם בבעיה?</h2>
<p>אם משהו באתר לא נגיש לכם – נשמח לשמוע ולתקן. רכזת הנגישות: תום גבע · טלפון <a href="tel:+972542885771">054-288-5771</a> · <a href="mailto:{CFG["email"]}">{CFG["email"]}</a>. נשתדל לחזור תוך 5 ימי עבודה.</p>
<p class="muted">ההצהרה עודכנה בתאריך {TODAY.strftime("%d.%m.%Y")}.</p>
</div></section>'''
page('accessibility.html', 'הצהרת נגישות | Tomchu Tattoo', 'הצהרת הנגישות של אתר Tomchu Tattoo לפי ת״י 5568 ו־WCAG 2.0 AA: התאמות באתר, נגישות הסטודיו ופרטי רכזת הנגישות.', acc, ld=[crumbs_ld(cr)])

# ================================================================ PRIVACY
cr = [('index.html', 'בית'), (None, 'מדיניות פרטיות')]
priv = phead('מדיניות פרטיות', None, cr, '') + f'''
<section aria-label="מדיניות פרטיות"><div class="wrap prose">
<p>מדיניות זו מסבירה איזה מידע אישי נאסף באתר של Tomchu Tattoo (תום גבע, {CFG["address"]}), למה, ומה הזכויות שלך. באתר אין עוגיות פרסום ואין מעקב אחרי מבקרים מסוימים.</p>
<h2>הצהרת בריאות</h2>
<p>בהצהרת הבריאות נאספים: שם, תאריך לידה, טלפון, כתובת מגורים, תיאור הקעקוע, תשובות לשאלות בריאות, אישורים וחתימה. תעודת זהות, אימייל ואיש קשר לחירום אינם חובה. לקטינים נאספים גם פרטי הורה או אפוטרופוס. את הפרטים נדרש לתעד לפי המפרט של משרד הבריאות לעסקי קעקוע. מסירתם היא מרצונך, אבל בלי הצהרה חתומה אי אפשר לבצע את הקעקוע.</p>
<p>זהו מידע רפואי רגיש. ההצהרה נשלחת בחיבור מוצפן (HTTPS) ישירות לחשבון Google של העסק, שם נוצר ממנה קובץ PDF חתום שנשלח למייל של תום ונשמר בתיקייה ובגיליון פרטיים. האתר עצמו לא שומר את ההצהרה. עד השליחה, הפרטים שמילאת נשמרים זמנית רק בדפדפן שלך ונמחקים כשסוגרים את הלשונית. רק תום ניגשת למידע, והוא לא מועבר לאף אחד.</p>
<p>הצהרות נשמרות עד שנה מיום הקעקוע, כנדרש בהנחיות משרד הבריאות, ונמחקות בתום התקופה. הצהרה שלא בוצע בעקבותיה קעקוע נמחקת לפי בקשה מיד.</p>
<h2>קניית שובר מתנה</h2>
<p>כשקונים שובר מתנה באתר נאספים: השם שלך, הטלפון שלך, שם המקבל/ת, הטלפון של המקבל/ת (רק אם בחרת לשלוח ישירות), ההקדשה, הסכום ואמצעי התשלום שבחרת. אין חובה חוקית למסור את המידע, אבל בלעדיו אי אפשר להנפיק שובר.</p>
<p>המידע משמש רק כדי להנפיק את השובר, לזהות את ההעברה, לשלוח את השובר, לאפשר את מימושו ולחזור אליך בנושא. הוא נשמר בחשבון Google של העסק (Google Sheets), נגיש לתום בלבד, לא נמכר ולא מועבר לאחרים לשום מטרה אחרת, ונשמר כל עוד השובר בתוקף ועוד שנה אחרי – אלא אם הדין מחייב לשמור יותר.</p>
<p>התשלום עצמו נעשה באפליקציית ביט או פייבוקס, והאתר לא רואה ולא שומר פרטי אשראי או חשבון בנק.</p>
<h2>מה נשמר במכשיר שלך</h2>
<p>הבחירות שלך בתפריט הנגישות ובמצב התצוגה (כהה/בהיר), וקוד השובר שקנית, נשמרים בדפדפן שלך בלבד (localStorage). אפשר למחוק אותם בכל רגע דרך הגדרות הדפדפן.</p>
<h2>הודעות וואטסאפ</h2>
<p>הטופס בעמוד ״קביעת תור״ והמדריך ״איזה קעקוע מתאים לי״ רק מכינים טקסט ופותחים את וואטסאפ. ההודעה נשלחת רק אם תלחצו ״שלח״ בוואטסאפ, וממנה והלאה חלים תנאי השימוש של WhatsApp.</p>
<h2>שירותים חיצוניים</h2>
<p>האתר טוען גופנים מ־Google Fonts, ולכן הדפדפן פונה לשרתים של Google. קישורים ל־Instagram, Facebook, TikTok, Waze, Google Maps, Moovit ולאפליקציה מובילים לשירותים חיצוניים עם מדיניות פרטיות משלהם.</p>
<h2>סטטיסטיקת כניסות</h2>
<p>כדי לדעת כמה אנשים נכנסים לאתר ולאילו עמודים, האתר משתמש ב־Cloudflare Web Analytics. הכלי לא משתמש בעוגיות, לא שומר כתובת IP ולא מזהה מבקרים מסוימים. הוא מודד רק נתונים כלליים: מספר הכניסות, העמודים שנצפו, סוג המכשיר, המדינה ומאיזה אתר הגעת.</p>
<h2>הזכויות שלך</h2>
<p>אפשר לבקש לעיין במידע שנשמר עליך, לתקן אותו או למחוק אותו (כל עוד אין שובר פעיל שתלוי בו, או הצהרה שחובה לשמור לפי הנחיות משרד הבריאות), בפנייה ל־<a href="mailto:{CFG["email"]}">{CFG["email"]}</a> או בטלפון {CFG["phoneDisplay"]}. נחזור אליך תוך 30 יום.</p>
<p class="muted">עודכן בתאריך {TODAY.strftime("%d.%m.%Y")}.</p>
</div></section>'''
page('privacy.html', 'מדיניות פרטיות | Tomchu Tattoo', 'מדיניות הפרטיות של אתר Tomchu Tattoo: איזה מידע נאסף בהצהרת בריאות ובקניית שובר מתנה, איך הוא נשמר, ומה הזכויות שלך.', priv, ld=[crumbs_ld(cr)])

# ================================================================ 404
nf = f'''<section><div class="wrap stack" style="align-items:flex-start;min-height:50vh;justify-content:center">
<span class="label">שגיאה 404</span><h1>הדף <span class="iri-text">לא נמצא</span></h1><p class="lead">אולי הקישור השתנה במעבר לאתר החדש. אפשר לחזור לעמוד הבית או לראות עבודות.</p>
<div class="ctas"><a class="btn btn-iri" href="/index.html">לעמוד הבית</a><a class="btn btn-ghost" href="/works.html">לעבודות</a></div></div></section>'''
page('404.html', 'הדף לא נמצא | Tomchu Tattoo', 'הדף לא נמצא.', nf, R='/', robots='noindex')
PAGES.remove('404.html')


# ================================================================ redirects from the old SITE123 addresses
OLD = {'קצת-עליי': 'tom.html', 'קצת-עליי/זאת-אני': 'tom.html', 'קצת-עליי/עבודות': 'works.html', 'קצת-עליי/ה-סטודיו': 'tom.html#studio',
       'לקוחות-ממליצים': 'tom.html#reviews', 'לינקים': 'app.html', 'שאלות-ותשובות': 'process.html#faq', 'מאמרים': 'journal.html',
       'שלחו-הודעה-ואני-אחזור-אליכם': 'contact.html',
       'מאמרים/10-דברים-שכדאי-לדעת-לפני-שעושים-קעקוע-במיוחד-אם-זה-הראשון-שלכם': 'journal/ten.html',
       'מאמרים/איך-לבחור-את-הקעקוע-הראשון-שלך': 'journal/first.html',
       'מאמרים/המדריך-המלא-לסגנונות-קעקועים-איזה-סגנון-הכי-מתאים-לך': 'journal/styles.html',
       'מאמרים/היסטורית-עולם-הקעקועים': 'journal/history.html',
       'מאמרים/המדריך-השלם-למכונות-קעקועים-סוגים-יתרונות-ומה-כדאי-לדעת': 'journal/machines.html'}
for f_, t_ in [('studio.html', 'tom.html#studio'), ('faq.html', 'process.html#faq')]:
    open(os.path.join(ROOT, f_), 'w', encoding='utf-8').write(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Tomchu Tattoo</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{t_}"><meta http-equiv="refresh" content="0; url={t_}"><script>location.replace({json.dumps(t_)})</script></head><body><p>העמוד עבר: <a href="{t_}">להמשך</a></p></body></html>')
for f_, up_, tg_ in ((os.path.join('health', 'index.html'), '../', 'health.html'), (os.path.join('הצהרה', 'index.html'), '../', 'health.html'), (os.path.join('care', 'index.html'), '../', 'process.html#care'), (os.path.join('טיפול', 'index.html'), '../', 'process.html#care')):
    os.makedirs(os.path.dirname(os.path.join(ROOT, f_)), exist_ok=True)
    open(os.path.join(ROOT, f_), 'w', encoding='utf-8').write(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Tomchu Tattoo</title><meta name="robots" content="noindex"><link rel="canonical" href="{SITE}/{tg_.split('#')[0]}"><meta http-equiv="refresh" content="0; url={up_}{tg_}"></head><body><a href="{up_}{tg_}">המשך</a></body></html>')
for old, new in OLD.items():
    d = os.path.join(ROOT, old); os.makedirs(d, exist_ok=True)
    up = '../' * (old.count('/') + 1); tgt = up + new; full = SITE + '/' + new
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Tomchu Tattoo</title><meta name="robots" content="noindex"><link rel="canonical" href="{full}"><meta http-equiv="refresh" content="0; url={tgt}"><script>location.replace({json.dumps(tgt)})</script></head><body><p>העמוד עבר: <a href="{tgt}">להמשך</a></p></body></html>')

# ================================================================ SEO landing pages
def _gal(tags, n=6):
    items = [w for w in C['WORKS'] if w['tag'] in tags][:n]
    li = ''.join(f'<li data-tag="{w["tag"]}"><button type="button" data-full="{{R}}assets/img/works/work{int(w["id"][1:])}-1000.webp" data-alt="{e(w["alt"])}" aria-label="{e(w["alt"])} – הגדלה">{pic(int(w["id"][1:]), w["alt"], sizes="(max-width: 520px) 100vw, 290px")}</button></li>' for w in items)
    return f'<ul class="masonry" id="gallery">{li}</ul>'
LB = '''<div class="lb" id="lightbox" role="dialog" aria-modal="true" aria-label="תצוגת תמונה מוגדלת" hidden><div class="lb-top"><p><span class="lb-cap"></span> · <span class="lb-pos"></span></p><button type="button" class="close" aria-label="סגירה">✕</button></div><div class="lb-stage"><img alt=""></div><button type="button" class="prev" aria-label="התמונה הקודמת">›</button><button type="button" class="next" aria-label="התמונה הבאה">‹</button></div>'''
def _faq(qs):
    return ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qs)
CITIES = [
 ('tattoo-alfei-menashe', 'אלפי מנשה', 'ממש כאן, בקדרון 48'),
 ('tattoo-kfar-saba', 'כפר סבא', 'נסיעה קצרה מכפר סבא'),
 ('tattoo-raanana', 'רעננה', 'נסיעה קצרה מרעננה'),
 ('tattoo-hod-hasharon', 'הוד השרון', 'נסיעה קצרה מהוד השרון'),
 ('tattoo-karnei-shomron', 'קרני שומרון', 'נסיעה קצרה מקרני שומרון'),
 ('tattoo-tzur-yigal', 'צור יגאל', 'נסיעה קצרה מצור יגאל'),
 ('tattoo-tzofim', 'צופים', 'נסיעה קצרה מצופים'),
 ('tattoo-kochav-yair', 'כוכב יאיר', 'נסיעה קצרה מכוכב יאיר'),
]
STYLES = [
 ('fine-line-tattoo', 'קעקוע פיין ליין (Fine Line)', ['fine'], 'קווים דקים ומדויקים, פרטים קטנים ועדינים – הסגנון שתום הכי אוהבת לעבוד בו.',
  [('כמה זמן מחזיק קעקוע פיין ליין?', 'קו דק שנעשה נכון ובעומק הנכון נשאר יפה לאורך שנים. חשוב לשמור עליו בשבועות הראשונים ולהגן מהשמש.'),
   ('מה הגודל המינימלי?', 'תלוי בכמות הפרטים. בשיחת הייעוץ תום תתאים את הגודל כך שהקווים לא יתחברו עם הזמן.')]),
 ('cover-up-tattoo', 'קאבר וחידוש קעקוע ישן', ['ba'], 'קעקוע ישן שדהה או שכבר לא מתאים? אפשר לחדש אותו או לעצב מעליו משהו חדש.',
  [('אפשר לכסות כל קעקוע?', 'לא תמיד, וזה תלוי בגודל ובכהות של הקעקוע הקיים. שולחים תמונה בוואטסאפ ותום אומרת בכנות מה אפשר.'),
   ('חידוש או כיסוי – מה ההבדל?', 'בחידוש מחזקים את הקווים והצבעים של אותו עיצוב. בכיסוי מעצבים עיצוב חדש שמסתיר את הישן.')]),
 ('color-tattoo', 'קעקוע צבעוני עדין', ['color'], 'צבע רך ומדויק שמשתלב עם קו עדין – פרחים, ציפורים ועיצובים אישיים.',
  [('צבע דוהה מהר?', 'כל קעקוע מתבהר מעט עם השנים. הגנה מהשמש ולחות שומרות על הצבע הרבה יותר זמן.')]),
]
BASEQ = [(f['q'], f['a']) for f in C['FAQ'][:3]]
def _land(slug, h1, lead, tags, qs, crumb):
    cr = [('index.html', 'בית'), (None, crumb)]
    body = phead(h1, '', cr, '') + f'''
<section><div class="wrap stack"><p class="lead" style="max-width:60ch">{lead}</p>
<div class="ctas"><a class="btn btn-iri" href="{WA}" target="_blank" rel="noopener">לשיחת ייעוץ בוואטסאפ</a><a class="btn btn-ghost" href="{{R}}works.html">לכל העבודות</a></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>עבודות של תום</h2>{_gal(tags)}</div></section>
<section style="padding-top:0"><div class="wrap stack"><h2>שאלות נפוצות</h2><div class="faq">{_faq(qs)}</div></div></section>
<section style="padding-top:0"><div class="wrap stack"><h2>איפה הסטודיו</h2><p>סטודיו פרטי בקדרון 48, אלפי מנשה. חניה בשפע ובחינם, בתיאום מראש.</p>
<div class="ctas"><a class="btn btn-ghost" href="{{R}}contact.html">הגעה וקביעת תור</a></div></div></section>{LB}'''
    ld = [crumbs_ld(cr), {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}]
    return body, ld
for slug, city, near in CITIES:
    lead = f'מחפשים מקעקעת ב{city} והסביבה? {near} נמצא הסטודיו הפרטי של תום גבע – Fine Line, צבע עדין וקאברים, בעיצוב אישי, עם ציוד חד־פעמי ואווירה רגועה.'
    body, ld = _land(slug, f'קעקועים <span class="iri-text">ב{city}</span> והסביבה', lead, ['fine', 'color', 'sketch'], BASEQ, f'קעקועים ב{city}')
    page(f'{slug}.html', f'קעקועים ב{city} – סטודיו של תום גבע | Tomchu Tattoo', lead[:155], body, ld=ld)
for slug, name, tags, lead, qs in STYLES:
    body, ld = _land(slug, f'<span class="iri-text">{name}</span>', lead + ' בסטודיו פרטי באלפי מנשה, קרוב לכפר סבא, רעננה והוד השרון.', tags, qs + BASEQ[:1], name)
    page(f'{slug}.html', f'{name} – תום גבע | Tomchu Tattoo', (lead + ' סטודיו פרטי באלפי מנשה.')[:155], body, ld=ld)

# ================================================================ sitemap, robots, manifest
pri = {'index.html': '1.0', 'works.html': '0.9', 'contact.html': '0.9', 'guide.html': '0.8', 'studio.html': '0.8', 'tom.html': '0.8'}
urls = ''.join(f'<url><loc>{SITE}/{"" if p == "index.html" else p}</loc><lastmod>{TODAY.isoformat()}</lastmod><priority>{pri.get(p, "0.6")}</priority></url>' for p in PAGES)
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
json.dump({"name": "Tomchu Tattoo", "short_name": "Tomchu", "lang": "he", "dir": "rtl", "start_url": "/", "display": "standalone",
           "background_color": "#0B0A0D", "theme_color": "#0B0A0D",
           "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]},
          open(os.path.join(ROOT, 'site.webmanifest'), 'w'), ensure_ascii=False, indent=1)
open(os.path.join(ROOT, 'CNAME'), 'w').write('www.tomchu-tattoo.co.il\n')
open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
print('built', len(PAGES) + 1, 'pages')
