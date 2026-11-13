"""Light 'mint' pages: the homepage (Fresh & friendly layout) and the separate Get a free station page.
They use their own stylesheet (assets/mint.css) instead of the dark style.css, but share the same
footer markup, cookie banner, app modal, tracking and form logic (site.js) as the rest of the site."""
import html, json

GREEN, LIME = "#009245", "#9ef230"
FORM_URL = "/get-a-free-station/"


def nav(EX, APP_URL):
    links = [("/", "Home"), ("/stations/", "Stations"), ("/customers/", "Customers"), ("/areas/", "Areas"), ("/#how", "How it works"), ("/#faq", "FAQ")]
    a = "".join(f'<a href="{h}">{t}</a>' for h, t in links)
    mm = "".join(f'<a href="{h}">{t}</a>' for h, t in links)
    return f'''<div class="m-ann"><b>New</b>4,000+ venues across Ireland and the UK have used Jolt</div>
<header class="m-nav"><div class="m-wrap m-nav-in">
<a href="/" class="m-logo" aria-label="Jolt home"><img src="/assets/brand/jolt-logo-black.svg" alt="Jolt" width="436" height="142"></a>
<nav class="m-links">{a}</nav>
<div class="m-cta">{EX.nav_dropdown()}<a class="m-btn m-bg" href="{FORM_URL}">Get a free station</a><button class="m-burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button></div>
</div>
<nav class="m-menu mobile-menu" id="mobile-menu" hidden>{mm}<a href="{FORM_URL}">Get a free station</a><a class="app-link" href="{APP_URL}">Find a power bank</a>{EX.mobile_links()}</nav>
</header>'''


def shell(head_html, body, FOOTER, css_v):
    """head() output with the dark stylesheet swapped for mint.css, then body + shared footer."""
    h = head_html.replace('<link rel="stylesheet" href="/assets/style.css?v=', '<link rel="stylesheet" href="/assets/mint.css?v=' + css_v + '&amp;s=')
    h = h.replace('<meta name="theme-color" content="#050505">', '<meta name="theme-color" content="#f0fbe4">')
    h = h.replace("<body>", '<body class="mint">')
    return h + body + FOOTER


def marquee(logos):
    t = "".join(f'<div class="mql"><img src="/assets/venues/{n}.webp" alt=""></div>' for n in logos)
    return f'<div class="mq"><div class="mq-track">{t}{t}</div></div>'


def home(ctx):
    S, FAQ, EX, APP_URL = ctx["STATIONS"], ctx["FAQ"], ctx["EX"], ctx["APP_URL"]
    logos = EX.VENUE_LOGOS
    c4 = [("Get a free station", "A free Jolt station for your venue, installed and looked after by us.", "Get a station", FORM_URL, "countertop-8-white"),
          ("Events & nightlife", "High-capacity stations for clubs, gigs and festivals.", "Talk to us", FORM_URL, "tower-48"),
          ("Public spaces", "Stations for hospitals, stadiums and transport hubs.", "Talk to us", FORM_URL, "media-kiosk-48"),
          ("Charge my phone", "Find the nearest Jolt station in the app and rent a power bank.", "Find a station", APP_URL, "slim-kiosk-24")]
    cards = "".join(f'<div class="m-c"><div class="m-ci"><img src="/assets/stations/{s}-angle-sm.webp" alt=""></div><h3>{t}</h3><p>{d}</p>'
                    f'<a class="m-btn m-bg{" app-link" if h == APP_URL else ""}" href="{h}">{b}</a><a class="m-lm" href="/stations/{s}/">Learn more</a></div>' for t, d, b, h, s in c4)
    uses = [("🍺", "Pubs & bars", "Guests stay for another round instead of leaving to charge their phone."),
            ("🏥", "Hospitals", "Patients and visitors can stay in touch while they wait."),
            ("🏨", "Hotels", "A free station at reception, in the lobby or at the bar.")]
    faq = "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    body = nav(EX, APP_URL) + f'''
<main>
<section class="m-hero"><div class="m-wrap m-hero-in">
<div><h1>Charge your phone<br>on the go</h1><p>Free power bank rental stations for venues across Ireland and the UK. Your guests tap to rent, and your venue earns a share of every rental.</p>
<div class="m-btns"><a class="m-btn m-bg" href="{FORM_URL}">Get a free station</a><a class="m-btn m-bo app-link" href="{APP_URL}">Find a power bank</a></div></div>
<div class="m-hero-im"><img src="/assets/stations/countertop-12-angle.webp" alt="Jolt Countertop 12 power bank station" width="600" height="800"></div>
</div></section>

<section class="m-trust"><p>Trusted by venues across Ireland &amp; the UK</p>{marquee(logos)}</section>

<section class="m-news"><div class="m-wrap m-news-in">
<div><span class="m-tag">FREE</span><h2>A free station for your venue</h2><p>The station, power banks, installation and maintenance are free, and your venue earns a share of every rental.</p>
<div class="m-boxes"><div><b>€0</b><span>cost to install</span></div><div><b>7</b><span>station models</span></div><div><b>24/7</b><span>rent and return</span></div></div>
<a class="m-btn m-bg" href="{FORM_URL}">Get a free station</a> <a class="m-btn m-bo" href="/stations/">See the stations</a></div>
<div class="m-news-im"><img src="/assets/app/map-dublin-xwide.webp" alt="Jolt app map showing stations across Dublin and the east coast" loading="lazy"></div>
</div></section>

<section class="m-join"><div class="m-wrap"><h2>Join the Jolt network</h2><p>There are several ways to work with Jolt.</p><div class="m-c4">{cards}</div></div></section>

<section class="m-what" id="how"><div class="m-wrap m-what-in"><div class="m-what-im"><img src="/assets/app/map-dublin-wide.webp" alt="Jolt stations in and around Dublin" loading="lazy"></div>
<div><h2>What is Jolt?</h2><p>Jolt is a power bank rental network for venues in Ireland and the UK. Guests tap a card or phone on the station, take a power bank with Lightning, USB-C and Micro-USB cables built in, and return it to any Jolt station.</p>
<ol class="m-steps"><li><b>Tap</b> your card or phone on the station</li><li><b>Charge</b> your phone on the go</li><li><b>Return</b> it to any Jolt station</li></ol>
<a class="m-btn m-bg" href="/stations/">Check our products</a></div></div></section>

<section class="m-pres"><div class="m-wrap"><h2>Our presence</h2><p>Jolt stations across Ireland and the UK.</p>
<div class="m-maps"><figure><img src="/assets/app/map-dublin-xwide.webp" alt="Jolt stations around Dublin" loading="lazy"><figcaption>Dublin</figcaption></figure><figure><img src="/assets/app/map-london-wide.webp" alt="Jolt stations around London" loading="lazy"><figcaption>London</figcaption></figure><figure><img src="/assets/app/map-galway.webp" alt="Jolt stations in Galway" loading="lazy"><figcaption>Galway</figcaption></figure></div>
<div class="m-nums"><div><b>4,000+</b><span>venues have used Jolt</span></div><div><b>2</b><span>countries</span></div><div><b>7</b><span>station models</span></div></div>
<a class="m-btn m-bo" href="{FORM_URL}">Get a free station</a> <a class="m-btn m-bg app-link" href="{APP_URL}">Find a power bank</a></div></section>

<section class="m-uses" id="venues"><div class="m-wrap"><h2>Phone charging stations for every kind of venue</h2><div class="m-u3">{"".join(f'<div class="m-u"><div class="m-ic">{i}</div><h3>{t}</h3><p>{d}</p><a class="m-btn m-bg" href="{FORM_URL}">Get a free station</a></div>' for i, t, d in uses)}</div></div></section>

<section class="m-faq" id="faq"><div class="m-wrap m-narrow"><h2>Questions venues ask</h2>{faq}</div></section>
</main>'''
    return shell(ctx["head"](None), body, ctx["FOOTER"], ctx["MINT_V"])


def form_page(ctx):
    EX, APP_URL = ctx["EX"], ctx["APP_URL"]
    P = {"path": FORM_URL, "lang": "en-IE", "title": "Get a Free Power Bank Station for Your Venue | Jolt",
         "desc": "Tell us about your venue and get a free Jolt power bank station, installed and maintained at no cost, with a share of every rental."}
    body = nav(EX, APP_URL) + f'''
<main class="m-form-main">
<section class="m-form-sec"><div class="m-wrap m-form-in">
<div class="m-form-copy">
<span class="m-tag">FREE</span>
<h1>Get a free power bank station</h1>
<p>Answer four quick questions and we'll recommend the right station for your venue.</p>
<ul class="m-ticks"><li>Free station, installation and maintenance</li><li>Your venue earns a share of every rental</li><li>We keep it stocked and handle customer support</li><li>Every rental is secured with a card pre-authorisation</li></ul>
<div class="m-form-im"><img src="/assets/stations/countertop-8-white-angle-sm.webp" alt="Jolt Countertop 8 station" width="320" height="420"></div>
</div>
<div>{ctx["setup_card"]("")}</div>
</div></section>
<section class="m-trust"><p>Used by 4,000+ venues across Ireland &amp; the UK</p>{marquee(EX.VENUE_LOGOS)}</section>
</main>'''
    return shell(ctx["head"](None, P), body, ctx["FOOTER"], ctx["MINT_V"])
