#!/usr/bin/env python3
"""Generira statične stranice za pularental.com.
Pokretanje iz korijena repozitorija:  python3 _src/gen.py
Cijene se mijenjaju SAMO u _src/prices.json (koristi ih i cjenik i kalkulator)."""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, '_src', 'prices.json'), encoding='utf-8'))

SITE = 'https://www.pularental.com'
WA = '385994089624'
WA_TXT = 'Hello%2C%20I%20would%20like%20to%20rent%20'
EMAIL = 'mdsegway@gmail.com'
AW = 'AW-18300638741'

LOC = [
    dict(id='verudela', name='Verudela, Pula', addr='Verudela 11, 52100 Pula', note='Near the Pula Aquarium',
         phones=['+385994089624', '+385989409522'], maps='https://www.google.com/maps/search/?api=1&query=Verudela+11+Pula'),
    dict(id='stoja', name='Camp Arena Stoja, Pula', addr='Stoja 37, 52100 Pula', note='SUP boards and kayaks available here',
         phones=['+385994089624', '+385989409522'], maps='https://www.google.com/maps/search/?api=1&query=Camp+Arena+Stoja+Pula'),
    dict(id='medulin', name='Camp Arena Medulin', addr='Osipovica 30, 52203 Medulin', note='Morning and evening tours from here',
         phones=['+385916077252', '+385994089624'], maps='https://www.google.com/maps/search/?api=1&query=Camp+Arena+Medulin+Osipovica+30'),
]

NAV = [('/', 'Home'), ('/book-now', 'Book Now'), ('/prices', 'Prices'), ('/toursgallery', 'Tours & Gallery'),
       ('/blog-list', 'Blog'), ('/contact', 'Contact')]

ICON_WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.13c-.24.68-1.42 1.3-1.95 1.34-.5.05-.97.23-3.27-.68-2.77-1.09-4.52-3.92-4.66-4.1-.13-.18-1.11-1.48-1.11-2.83 0-1.35.71-2.01.96-2.29.25-.27.55-.34.73-.34l.52.01c.17 0 .39-.06.61.47.24.56.79 1.92.86 2.06.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.94 1.93 1.23 2.2 1.37.27.14.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.34Z"/></svg>'
ICON_TEL = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.33.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2Z"/></svg>'


def fmt_tel(p):
    d = p.replace('+385', '0')
    return f'{d[:3]} {d[3:6]} {d[6:]}'


def euro(v):
    return (f'{v:.2f}'.rstrip('0').rstrip('.') if v % 1 else f'{int(v)}') + ' €'


def page(path, title, desc, body, extra_head='', ld=None):
    canon = SITE + (path if path != '/' else '/')
    nav = ''.join(f'<a href="{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/i/og.jpg">
<meta name="theme-color" content="#0b6e74">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={AW}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{AW}');</script>
{ldj}
{extra_head}
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Pula Rental home"><img src="/i/logo-192.png" alt="Pula Rental logo" width="44" height="44"><span>Pula Rental</span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="btn btn-wa btn-sm hide-sm" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a>
    <button class="menu" aria-label="Open menu" aria-expanded="false" onclick="document.body.classList.toggle('nav-open');this.setAttribute('aria-expanded',document.body.classList.contains('nav-open'))"><span></span><span></span><span></span></button>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <strong>Pula Rental</strong><br>Bike, e-bike, e-scooter, SUP and kayak rental in Pula and Medulin.<br>
      Open every day 9 AM – 9 PM.
    </div>
    <div>
      <strong>Contact</strong><br>
      WhatsApp / phone: <a href="tel:+385994089624">+385 99 408 9624</a><br>
      Medulin: <a href="tel:+385916077252">+385 91 607 7252</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
    <div>
      <strong>Follow us</strong><br>
      <a href="https://www.instagram.com/mdsegway" target="_blank" rel="noopener">Instagram</a> ·
      <a href="https://www.facebook.com/share/1E3GsqCAwR/" target="_blank" rel="noopener">Facebook</a> ·
      <a href="https://g.page/r/CVAbX9tgbK7REBM/review" target="_blank" rel="noopener">Google reviews</a>
    </div>
  </div>
  <div class="wrap copy">© 2017–2026 MD Segway · pularental.com · <a href="/privacy">Privacy</a></div>
</footer>
<div class="mbar">
  <a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp</a>
  <a class="btn btn-main" href="/book-now">Check price</a>
</div>
</body>
</html>
'''


def write(path, content):
    fp = os.path.join(ROOT, path.strip('/'), 'index.html') if path != '/' else os.path.join(ROOT, 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(content)


def redirect(path, to):
    fp = os.path.join(ROOT, path.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Pula Rental</title><link rel="canonical" href="{SITE}{to}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"></head><body><a href="{to}">Continue</a></body></html>')


# ---------- zajednički dijelovi ----------
ITEMS = P['items']
TIER_LABEL = {'30m': '30 minutes', '1h': '1 hour', '2h': '2 hours', '3h': '3 hours', '1d': '1 day', '2d': '2 days', '3d': '3 days', '4d': '4+ days, per day'}


def price_table(item, compact=False):
    rows = ''
    for k in ['30m', '1h', '2h', '3h', '1d', '2d', '3d', '4d']:
        v = item['official'].get(k)
        if v is None:
            continue
        extra = ''
        if k in ('2d', '3d'):
            n = int(k[0])
            extra = f' <span class="per">({euro(round(v / n, 2))}/day)</span>'
        rows += f'<tr><td>{TIER_LABEL[k]}</td><td>{euro(v)}{extra}</td></tr>'
    return f'<table class="pt"><tbody>{rows}</tbody></table>'


def cta_row(extra=''):
    return f'''<div class="cta">
  <a class="btn btn-main" href="/book-now">Check price &amp; availability</a>
  <a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}Book via WhatsApp</a>{extra}
</div>'''


FAQ = [
    ('How much does it cost to rent a bike in Pula?', 'A regular bike costs 15 € for 3 hours or 22 € for one day. Multi-day rentals are cheaper per day: 17 € per day for 2 days, 15 € per day for 3 days and 13 € per day for 4 or more days. E-bikes start at 33 € for 3 hours or 39 € per day, e-scooters at 11 € for 30 minutes or 34 € per day. Children\'s bikes are 50% of the regular price.'),
    ('How do I book?', 'Choose the dates and what you want to rent on the <a href="/book-now">Book Now</a> page. You will see the price straight away. Send us the request by WhatsApp or e-mail and we confirm availability. You pay when you pick up the equipment.'),
    ('Do I pay online?', 'No. There is no online payment. You pay on arrival, by card (Mastercard, Visa) or in cash.'),
    ('Where can I rent a bike in Pula and Medulin?', 'We have three locations: Verudela (near the Aquarium) and Camp Arena Stoja in Pula, and Camp Arena Medulin in Medulin.'),
    ('Is a helmet and lock included?', 'Yes. Every rental includes a helmet and a lock free of charge.'),
    ('Do I need to leave a deposit?', 'No deposit is required. You only need to show a valid photo ID (identity card, passport or driver\'s licence) when you pick up your rental.'),
    ('Can I rent an e-bike or e-scooter?', 'Yes, e-bikes and e-scooters are available at all three locations. E-bikes are perfect for longer rides to Cape Kamenjak or along the Medulin coast.'),
    ('Do you rent SUP boards and kayaks?', 'Yes, SUP boards and kayaks are available at Camp Arena Stoja in Pula.'),
    ('Can children rent bikes?', 'Yes. Children\'s bikes are 50% of the regular price, and child seats are available for 4 €.'),
    ('Do you deliver?', 'Delivery is free for bike and e-scooter rentals of 2 or more days, or for bookings of 4 or more vehicles. Mention your accommodation in the request.'),
    ('Do I need to book in advance?', 'Walk-ins are welcome, but in July and August we recommend sending a request in advance so we can keep the equipment for you.'),
    ('What are your opening hours?', 'We are open every day from 9 AM to 9 PM at all locations.'),
    ('What if the bike breaks down?', 'We provide free support on the road. Call us and we will repair or replace your bike as quickly as possible anywhere in the Pula and Medulin area.'),
    ('What if it rains?', 'You can reschedule or cancel free of charge if the weather makes riding unsafe.'),
    ('Can I return the bike to a different location?', 'Yes. You can pick up at Verudela and return at Camp Stoja or Camp Arena Medulin – just let us know in advance.'),
    ('Do you offer guided tours?', 'Yes. We run guided tours from Verudela to Cape Kamenjak and to the Šijana forest, plus sunrise and sunset rides. Private tours for families and groups are available on request.'),
]


def faq_html():
    return ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)


import re
def strip_tags(s):
    return re.sub('<[^>]+>', '', s)


BUSINESS_LD = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Pula Rental (MD Segway)", "url": SITE + "/",
         "logo": SITE + "/i/logo.png", "email": EMAIL, "telephone": "+385994089624",
         "sameAs": ["https://www.instagram.com/mdsegway", "https://www.facebook.com/share/1E3GsqCAwR/"]},
    ] + [
        {"@type": "BikeStore" if l['id'] != 'stoja' else "SportingGoodsStore", "@id": f"{SITE}/#{l['id']}",
         "name": f"Pula Rental – {l['name']}", "url": SITE + "/contact",
         "image": SITE + "/i/hero.jpg", "telephone": l['phones'][0], "email": EMAIL,
         "priceRange": "€",
         "address": {"@type": "PostalAddress", "streetAddress": l['addr'].split(',')[0],
                     "addressLocality": "Medulin" if l['id'] == 'medulin' else "Pula",
                     "postalCode": "52203" if l['id'] == 'medulin' else "52100", "addressCountry": "HR"},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                        "opens": "09:00", "closes": "21:00"}],
         "parentOrganization": {"@id": SITE + "/#org"}} for l in LOC
    ] + [
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in FAQ]}
    ]
}

# ---------- POČETNA ----------
fleet = [
    ('mtb-red', 'Mountain bikes', 'Cube Aim and BRB 29" hardtails with hydraulic disc brakes and front suspension. Sizes XS to L, city version with basket.', 'bike'),
    ('ebike-easy', 'E-bikes', 'Bosch-powered Cube Reaction Hybrid (600 Wh), Radon E-MTB, LIQBike Comfort Wave and MBM Nefele city e-bike. Easy entry frames available.', 'ebike'),
    ('escooter', 'E-scooters', 'VSETT e-scooters for quick trips around Pula, from 30 minutes to several days.', 'escooter'),
]
home_cards = ''.join(f'''<article class="card">
  <img src="/i/{img}.jpg" alt="{t} for rent in Pula" loading="lazy" width="800" height="450">
  <div class="card-b"><h3>{t}</h3><p>{d}</p>
  <p class="from">from <b>{euro(min(v for v in ITEMS[k]['official'].values()))}</b></p>
  <a class="link" href="/book-now?i={k}">Check price →</a></div>
</article>''' for img, t, d, k in fleet)

loc_html = ''.join(f'''<div class="loc">
  <h3>{l['name']}</h3><p>{l['addr']}<br><span class="muted">{l['note']}</span></p>
  <p>Every day 9 AM – 9 PM<br>{' · '.join(f'<a href="tel:{p}">{fmt_tel(p)}</a>' for p in l['phones'])}</p>
  <a class="link" href="{l['maps']}" target="_blank" rel="noopener">Open in Google Maps →</a>
</div>''' for l in LOC)

home = f'''
<section class="hero">
  <div class="wrap hero-g">
    <div>
      <p class="eyebrow">Pula · Verudela · Stoja · Medulin</p>
      <h1>Rent bikes, e-bikes and e-scooters in Pula, Croatia</h1>
      <p class="lead">Pick your dates, see the price instantly and send us a request. We confirm availability and you pay on arrival. Helmet, lock and road support included.</p>
      {cta_row()}
      <ul class="ticks"><li>Pay on arrival – card or cash</li><li>No deposit, just a photo ID</li><li>Free delivery for 2+ days or 4+ vehicles</li></ul>
    </div>
    <div class="hero-img"><img src="/i/hero.jpg" alt="Group of cyclists with rental bikes on the coast near Pula" width="1400" height="933" fetchpriority="high"></div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sh"><h2>Rentals &amp; prices</h2><p>Same prices at all three locations. The longer you ride, the less you pay per day.</p></div>
    <div class="cards3">{home_cards}</div>
    <div class="sub-row">
      <div class="mini"><h3>SUP &amp; kayak</h3><p>At Camp Arena Stoja. From {euro(ITEMS['sup']['official']['1h'])} per hour.</p><a class="link" href="/book-now?i=sup">Check price →</a></div>
      <div class="mini"><h3>Kids' bikes</h3><p>50% of the regular price. Child seats 4 €.</p><a class="link" href="/book-now?i=kids">Check price →</a></div>
      <div class="mini"><h3>Full price list</h3><p>All rentals and accessories in one place.</p><a class="link" href="/prices">See prices →</a></div>
    </div>
  </div>
</section>

<section class="how">
  <div class="wrap">
    <div class="sh"><h2>How booking works</h2></div>
    <ol class="steps">
      <li><b>Choose dates and equipment</b><span>Mark the days in the calendar and pick what you need.</span></li>
      <li><b>See the price</b><span>The total is calculated straight away from our price list.</span></li>
      <li><b>Send the request</b><span>By WhatsApp or e-mail. We reply and confirm availability.</span></li>
      <li><b>Pay on arrival</b><span>Card or cash when you pick up. No online payment.</span></li>
    </ol>
    <div class="cta center"><a class="btn btn-main" href="/book-now">Start booking</a></div>
  </div>
</section>

<section>
  <div class="wrap tours-teaser">
    <div><img src="/i/kamenjak-group.jpg" alt="Guided bike tour group at Cape Kamenjak" loading="lazy" width="1400" height="933"></div>
    <div>
      <h2>Guided bike tours</h2>
      <p>Ride with a local guide to Cape Kamenjak, through the shady Šijana forest or along the coast at sunrise and sunset. Classic bikes and e-bikes available. Private tours for families and groups on request.</p>
      <a class="btn btn-main btn-sm" href="/toursgallery">See tours</a>
    </div>
  </div>
</section>

<section class="locs-s">
  <div class="wrap">
    <div class="sh"><h2>Our locations</h2><p>Pick up at one location and return at another – just let us know in advance.</p></div>
    <div class="locs">{loc_html}</div>
  </div>
</section>

<section>
  <div class="wrap narrow">
    <div class="sh"><h2>Frequently asked questions</h2></div>
    <div class="faq">{faq_html()}</div>
    <p class="center"><a class="btn btn-ghost btn-sm" href="https://g.page/r/CVAbX9tgbK7REBM/review" target="_blank" rel="noopener">⭐ Read our Google reviews</a></p>
  </div>
</section>
'''
write('/', page('/', 'Bike, E-Bike & Scooter Rental Pula & Medulin | Pula Rental',
               'Rent bikes, e-bikes, e-scooters, SUP boards and kayaks in Pula and Medulin. Check the price online, pay on arrival. Helmet and lock included. Verudela, Camp Stoja, Camp Arena Medulin.',
               home, ld=BUSINESS_LD))

# ---------- CJENIK ----------
blocks = ''
for k in ['bike', 'ebike', 'escooter', 'kids', 'sup', 'kayak']:
    it = ITEMS[k]
    note = f'<p class="muted">{it["note"]}</p>' if it.get('note') else ''
    blocks += f'<div class="pblock"><h2>{it["name"]}</h2>{note}{price_table(it)}<a class="link" href="/book-now?i={k}">Calculate my price →</a></div>'
acc = ''.join(f'<tr><td>{a["name"]}</td><td>{euro(a["price"])}</td></tr>' for a in P['extras'])
prices = f'''
<section class="page-h"><div class="wrap"><h1>Price list</h1><p class="lead">All prices in euro, the same at all three locations. Helmet and lock included with every rental. You pay on arrival.</p>{cta_row()}</div></section>
<section><div class="wrap"><div class="pgrid">{blocks}
<div class="pblock"><h2>Accessories</h2><table class="pt"><tbody>{acc}</tbody></table></div>
</div>
<p class="muted">Free delivery for bike and e-scooter rentals of 2 or more days, or for bookings of 4 or more vehicles.</p></div></section>
'''
write('/prices', page('/prices', 'Prices – Bike, E-Bike, E-Scooter, SUP & Kayak Rental Pula | Pula Rental',
                      'Price list for bike, e-bike, e-scooter, SUP and kayak rental in Pula and Medulin. Bike from 13 € per day, e-bike from 28 € per day. Pay on arrival.',
                      prices))

# ---------- REZERVACIJA ----------
opts = ''.join(f'<option value="{l["id"]}">{l["name"]}</option>' for l in LOC)
book = f'''
<section class="page-h"><div class="wrap"><h1>Check price &amp; send a booking request</h1>
<p class="lead">Mark your days in the calendar, choose what you want to rent and see the total. Send the request and we confirm availability. <b>You pay on arrival</b> – no online payment.</p></div></section>
<section class="bk-s"><div class="wrap">
<form id="bk" class="bk" novalidate>
  <div class="bk-main">
    <div class="tabs" role="tablist">
      <button type="button" class="tab on" data-mode="rent" role="tab" aria-selected="true">Rental</button>
      <button type="button" class="tab" data-mode="tour" role="tab" aria-selected="false">Guided tour</button>
    </div>

    <fieldset class="step">
      <legend><span>1</span>Pick-up location</legend>
      <select id="loc" name="location" required>{opts}</select>
      <p class="hint" id="locHint"></p>
    </fieldset>

    <fieldset class="step">
      <legend><span>2</span><b id="calTitle">Select your days</b></legend>
      <p class="hint" id="calHint">Click the first day and the last day you need the equipment. For a few hours, click one day twice.</p>
      <div class="cal" id="cal" aria-live="polite"></div>
      <div class="dur" id="durBox" hidden>
        <label for="dur">How long?</label>
        <select id="dur">
          <option value="30m">30 minutes</option><option value="1h">1 hour</option><option value="2h">2 hours</option>
          <option value="3h">3 hours</option><option value="1d" selected>Whole day</option>
        </select>
      </div>
      <div class="time"><label for="time">Pick-up time</label>
        <select id="time" name="time">{''.join(f'<option{" selected" if h == 10 else ""}>{h:02d}:00</option>' for h in range(9, 21))}</select></div>
    </fieldset>

    <fieldset class="step" id="itemsStep">
      <legend><span>3</span>What would you like to rent?</legend>
      <div id="items" class="items"></div>
      <details class="extras"><summary>Accessories</summary><div id="extras" class="items"></div></details>
    </fieldset>

    <fieldset class="step" id="tourStep" hidden>
      <legend><span>3</span>Which tour?</legend>
      <div id="tours" class="tour-opts"></div>
      <div class="items">
        <div class="row"><div><b>People</b></div><div class="qty"><button type="button" data-t="-">−</button><output id="tourN">2</output><button type="button" data-t="+">+</button></div></div>
      </div>
      <label class="chk"><input type="checkbox" id="tourE"> We would like e-bikes for the tour</label>
      <p class="hint">Tour prices are confirmed in our reply.</p>
    </fieldset>

    <fieldset class="step">
      <legend><span>4</span>Your details</legend>
      <div class="f2">
        <label>Name*<input id="nm" name="name" autocomplete="name" required></label>
        <label>Phone / WhatsApp<input id="ph" name="phone" autocomplete="tel" inputmode="tel"></label>
        <label>E-mail<input id="em" name="email" type="email" autocomplete="email"></label>
        <label>Accommodation (for delivery)<input id="acc" name="accommodation" placeholder="Apartment / hotel / camp"></label>
      </div>
      <label>Message<textarea id="msg" name="message" rows="3" placeholder="Height of riders, bike sizes, questions…"></textarea></label>
      <label class="chk"><input type="checkbox" id="dlv"> I would like delivery to my accommodation</label>
    </fieldset>
  </div>

  <aside class="bk-sum" id="sum">
    <h2>Your request</h2>
    <div id="sumBody"><p class="muted">Select dates and equipment to see the price.</p></div>
    <div class="total"><span>Total</span><b id="tot">0 €</b></div>
    <p class="pay">Pay on arrival · card or cash · no deposit</p>
    <p class="err" id="err" role="alert"></p>
    <button type="button" class="btn btn-wa wide" id="sendWa">{ICON_WA}Send request via WhatsApp</button>
    <button type="button" class="btn btn-main wide" id="sendEm">Send request by e-mail</button>
    <p class="ok" id="ok" role="status" hidden></p>
    <p class="fine">We reply as soon as possible during opening hours (9 AM – 9 PM). The booking is confirmed only after our reply. Your details are used only to answer this request – see <a href="/privacy">privacy</a>.</p>
  </aside>
</form>
</div></section>
<script>window.PR_PRICES={json.dumps(P, ensure_ascii=False)};window.PR_WA="{WA}";window.PR_MAIL="{EMAIL}";</script>
<script src="/js/booking.js" defer></script>
'''
write('/book-now', page('/book-now', 'Book a Bike, E-Bike or E-Scooter in Pula – Check Price | Pula Rental',
                        'Choose dates and equipment, see the rental price instantly and send a booking request. Pay on arrival at Verudela, Camp Stoja or Camp Arena Medulin.',
                        book))
for p in ['/book-your-ride', '/book-your-ride-1', '/book-your-ride-2']:
    redirect(p, '/book-now')

# ---------- TURE I GALERIJA ----------
tours = ''.join(f'''<article class="tour" id="{t['id']}">
  <img src="/i/{t['img']}.jpg" alt="{t['name']} – guided bike tour Pula" loading="lazy" width="1400" height="788">
  <div><h2>{t['name']}</h2><p>{t['desc']}</p>
  <a class="btn btn-main btn-sm" href="/book-now?tour={t['id']}">Send tour request</a></div>
</article>''' for t in P['tours'])
gal = ['hero', 'kamenjak-group', 'arena-group', 'group-park', 'city-tour', 'sunset-ride', 'pano-1', 'pano-2', 'radon-emtb', 'escooter', 'cube-aim-yellow', 'ebike-city']
gal_html = ''.join(f'<figure><img src="/i/{g}.jpg" alt="Pula Rental – {g.replace("-", " ")}" loading="lazy"></figure>' for g in gal)
tg = f'''
<section class="page-h"><div class="wrap"><h1>Guided bike tours in Pula &amp; Kamenjak</h1>
<p class="lead">Guided rides with helmets and water included. Classic bikes or e-bikes. Private tours for families and groups on request.</p></div></section>
<section><div class="wrap tours">{tours}</div></section>
<section class="gal-s"><div class="wrap"><div class="sh"><h2>Gallery</h2></div><div class="gal">{gal_html}</div></div></section>
'''
write('/toursgallery', page('/toursgallery', 'Bike Tours – Kamenjak, Šijana Forest & Sunset Rides | Pula Rental',
                            'Guided bike and e-bike tours from Pula: Cape Kamenjak, Šijana forest, sunrise and sunset rides along the coast. Send a request and pay on arrival.', tg))

# ---------- KONTAKT ----------
contact = f'''
<section class="page-h"><div class="wrap"><h1>Contact &amp; locations</h1>
<p class="lead">The fastest way to reach us is WhatsApp. Need help during your rental? Call us any time.</p>
<div class="cta"><a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON_WA}WhatsApp +385 99 408 9624</a>
<a class="btn btn-ghost" href="tel:+385994089624">{ICON_TEL}Call</a>
<a class="btn btn-ghost" href="mailto:{EMAIL}">{EMAIL}</a></div></div></section>
<section><div class="wrap"><div class="locs">{loc_html}</div></div></section>
'''
write('/contact', page('/contact', 'Contact & Locations – Pula (Verudela, Stoja) & Medulin | Pula Rental',
                       'Pula Rental locations: Verudela 11 and Camp Arena Stoja in Pula, Camp Arena Medulin. Open every day 9 AM – 9 PM. WhatsApp +385 99 408 9624.', contact, ld=BUSINESS_LD))

# ---------- BLOG (Soro) ----------
blog = '''
<section class="page-h"><div class="wrap"><h1>Cycling in Pula &amp; Istria – routes and tips</h1></div></section>
<section><div class="wrap"><div id="soro-blog"></div></div></section>
<script src="https://app.trysoro.com/api/embed/b053aa41-6469-4c6a-87a8-ef26bdab1c5c" defer></script>
'''
write('/blog-list', page('/blog-list', 'Cycling Istria – Bike Routes & Tips | Pula Rental',
                         'Bike routes, e-scooter tips and trip ideas for Pula, Medulin, Premantura and Cape Kamenjak.', blog))

# ---------- PRIVATNOST ----------
priv = f'''
<section class="page-h"><div class="wrap narrow"><h1>Privacy</h1>
<p>When you send a booking request by e-mail from this website, we receive your name, contact details, chosen dates, equipment and message. We use them only to answer your request and arrange the rental, and we do not pass them on for marketing.</p>
<p>E-mail requests are delivered through the FormSubmit service (formsubmit.co). Requests sent via WhatsApp are handled by WhatsApp under its own terms.</p>
<p>This website uses Google Ads measurement (Google tag) to see how visitors find us.</p>
<p>To ask about or delete your data, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p class="muted">MD Segway, Pula, Croatia</p></div></section>
'''
write('/privacy', page('/privacy', 'Privacy | Pula Rental', 'How Pula Rental handles booking request data.', priv))

# ---------- 404 ----------
nf = page('/404', 'Page not found | Pula Rental', 'Page not found.',
          '<section class="page-h"><div class="wrap"><h1>Page not found</h1><p class="lead">The page you are looking for does not exist.</p>' + cta_row() + '</div></section>')
open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8').write(nf.replace('<link rel="canonical" href="https://www.pularental.com/404">', '<meta name="robots" content="noindex">'))

# ---------- sitemap ----------
urls = ['/', '/book-now', '/prices', '/toursgallery', '/contact', '/blog-list', '/privacy']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(sm)
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print('OK')
