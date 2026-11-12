"""Jolt website examples: eight alternative homepage designs, each laid out like a reference site
but using only Jolt's own name, logo, colours, photos and facts. Written into /examples/<slug>/.
Called from build.py: examples.build(write, STATIONS, IOS_URL, ANDROID_URL)."""
import html

LIME, GREEN = "#9ef230", "#009245"          # from Jolt's logo colour guide
LOGO_W, LOGO_B = "/assets/brand/jolt-logo-white.svg", "/assets/brand/jolt-logo-black.svg"
FORM = "/#setup-card"                        # the real quote form on the main site

EXAMPLES = [  # slug, label shown in the dropdown, layout reference
    ("blue-wave",    "1 · Gradient hero",      "chargeFUZE"),
    ("bold-colour",  "2 · Bold colour block",  "Joos Power"),
    ("clean-navy",   "3 · Clean navy",         "ChargedUp"),
    ("pill-play",    "4 · Rounded & playful",  "Naki"),
    ("fresh-green",  "5 · Fresh & friendly",   "ChargerGoGo"),
    ("night-out",    "6 · Night-out energy",   "Chimpy"),
    ("city-lights",  "7 · Dark cinematic",     "ChargeSPOT"),
    ("neon-dark",    "8 · Black & neon",       "voozaa"),
]

VENUE_LOGOS = ["rds", "tesco-express-temple-bar", "the-george", "whelan-s", "temple-bar-hotel-dublin", "o-donoghues-bar-dublin",
               "st-vincent-s-university-hospital", "copper-face-jacks", "jameson-distillery-bow-st", "the-workman-s-club",
               "clayton-hotel-ballsbridge", "slattery-s", "caf-en-seine", "the-harbour-bar", "harcourt-hotel", "pawn-shop"]

FONTS = {
    "poppins": [400, 600, 700, 800], "montserrat": [400, 600, 800], "open-sans": [400, 600, 700, 800],
    "plus-jakarta-sans": [400, 500, 700], "barlow-condensed": [700, 800], "afacad": [400, 600, 700],
}


def font_css(*names):
    out = []
    for n in names:
        fam = n.replace("-", " ").title()
        for w in FONTS[n]:
            out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-display:swap;src:url(/assets/fonts/ex/{n}-latin-{w}-normal.woff2) format('woff2')}}")
        if n == "barlow-condensed":
            out.append("@font-face{font-family:'Barlow Condensed';font-weight:800;font-style:italic;font-display:swap;src:url(/assets/fonts/ex/barlow-condensed-latin-800-italic.woff2) format('woff2')}")
    return "".join(out)


EXBAR_CSS = """
.exbar{position:relative;z-index:9999;display:flex;align-items:center;justify-content:space-between;gap:.8rem;padding:.45rem 1rem;background:#050505;color:#cfd8cf;font:500 12px/1.2 Inter,system-ui,sans-serif;letter-spacing:.02em;border-bottom:1px solid #1d231d}
.exbar a{color:#9ef230;text-decoration:none}
.exbar select{background:#111511;color:#fff;border:1px solid #2c352c;border-radius:8px;padding:.35rem .5rem;font:inherit;max-width:60vw}
"""


def exbar(cur):
    opts = "".join(f'<option value="/examples/{s}/"{" selected" if s == cur else ""}>{html.escape(l)} (layout: {r})</option>' for s, l, r in EXAMPLES)
    return (f'<div class="exbar"><span>Jolt website example · <a href="/">back to main site</a></span>'
            f'<select aria-label="Switch example" onchange="location.href=this.value">{opts}</select></div>')


def page(cur, title, fonts, css, body, light=True):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>{html.escape(title)} | Jolt example</title>
<link rel="icon" href="/assets/brand/jolt-logo-black.svg">
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(/assets/fonts/inter-latin-400-normal.woff2) format('woff2')}}
@font-face{{font-family:Inter;font-weight:600;src:url(/assets/fonts/inter-latin-600-normal.woff2) format('woff2')}}
{font_css(*fonts)}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;overflow-x:hidden}}body{{margin:0;-webkit-font-smoothing:antialiased;overflow-x:hidden}}img{{max-width:100%;display:block}}a{{color:inherit}}
.wrap{{width:min(1180px,92vw);margin:0 auto}}
{EXBAR_CSS}
[hidden]{{display:none!important}}
img[src*="/assets/stations/"]:not(.nb){{mix-blend-mode:multiply}}
{css}
</style></head><body>
{exbar(cur)}
{body}
<script>
// "Find a power bank" buttons open the right app store
document.querySelectorAll('[data-app]').forEach(a=>{{const ua=navigator.userAgent;a.href=/android/i.test(ua)?'{{AND}}':'{{IOS}}';a.target='_blank';a.rel='noopener'}});
</script>
</body></html>"""


def logos_html(cls="lg"):
    return "".join(f'<div class="{cls}"><img src="/assets/venues/{n}.webp" alt=""></div>' for n in VENUE_LOGOS)


def st_img(slug, view="angle", sm=True):
    return f"/assets/stations/{slug}-{view}{'-sm' if sm else ''}.webp"


def cap(x):
    return f'{x["banks"]} power banks' if x.get("banks") else f'{x["bays"]} compartments'


PHONE = """<div class="phone"><div class="notch"></div><img src="/assets/app/map-dublin-hero.webp" alt="Jolt app map showing stations across Dublin"></div>"""
PHONE_CSS = """.phone{position:relative;width:min(300px,70vw);aspect-ratio:9/19;border-radius:44px;background:#0b0b0b;padding:12px;box-shadow:0 40px 80px rgba(0,0,0,.35)}
.phone img{width:100%;height:100%;object-fit:cover;border-radius:34px}
.phone .notch{position:absolute;top:22px;left:50%;transform:translateX(-50%);width:90px;height:24px;border-radius:20px;background:#0b0b0b;z-index:2}"""

STEPS = [("Tap", "Tap your card or phone on the station to rent a power bank."),
         ("Charge", "Each 6000mAh power bank has Lightning, USB-C and Micro-USB cables built in."),
         ("Return", "Drop it back into any Jolt station when you're done.")]
VENUE_TYPES = ["Pubs & bars", "Restaurants & cafés", "Hotels", "Nightclubs & events", "Gyms & leisure", "Hospitals, stadiums & transport"]
FACTS = [("4,000+", "venues have used Jolt"), ("€0", "cost to install"), ("6000mAh", "power banks"), ("24/7", "rent and return")]
BENEFITS = [("Free station", "The station, power banks, installation and maintenance are free."),
            ("Revenue share", "Your venue receives a share of the rental income from the station."),
            ("Nothing to manage", "Jolt installs it, keeps it stocked and handles customer support."),
            ("No lost stock", "Every rental is secured with a card pre-authorisation, so unreturned banks never cost you.")]


# ---------------------------------------------------------------- 1. Gradient hero (chargeFUZE layout)
def ex_blue_wave(S):
    css = PHONE_CSS + f"""
body{{font-family:Poppins,sans-serif;color:#0b1a12;background:#fff}}
.nav{{position:sticky;top:0;z-index:50;background:linear-gradient(90deg,{GREEN},#1aa64a 55%,#58c43a);}}
.nav .wrap{{display:flex;align-items:center;gap:2rem;height:72px}}.nav img{{height:26px}}
.nav nav{{display:flex;gap:1.8rem;margin-left:auto;font-weight:600;font-size:.9rem;color:#fff}}.nav nav a{{text-decoration:none}}
.nav .cta{{background:#fff;color:#0b1a12;padding:.8rem 1.2rem;border-radius:6px;font-weight:700;font-size:.8rem;text-decoration:none;letter-spacing:.04em}}
.hero{{position:relative;background:linear-gradient(160deg,{GREEN} 0%,#21a84b 45%,{LIME} 100%);color:#fff;overflow:hidden}}
.hero:after{{content:"";position:absolute;left:-10%;right:-10%;bottom:-120px;height:240px;background:#fff;border-radius:50%}}
.hero .wrap{{position:relative;z-index:1;display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:2rem;padding:5rem 0 9rem}}
.hero h1{{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1.08;margin:0 0 1.2rem;font-weight:700}}
.hero p{{font-size:1.05rem;max-width:30rem;opacity:.95}}
.btns{{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.6rem}}
.b{{display:inline-block;padding:1rem 1.4rem;border-radius:6px;font-weight:700;font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}}
.b-dark{{background:#08140d;color:#fff}}.b-light{{background:#fff;color:#08140d}}
.hero .art{{display:flex;justify-content:center;align-items:center;gap:0}}
.hero .art .st{{width:220px;margin-left:-60px;filter:drop-shadow(0 30px 40px rgba(0,0,0,.25));border-radius:18px;background:#fff;padding:10px}}
.logos{{padding:3rem 0}}.logos .wrap{{display:grid;grid-template-columns:.8fr 1.2fr;align-items:center;gap:2rem}}
.logos h2{{font-size:1.8rem;margin:0}}.strip{{display:flex;gap:1rem;overflow:hidden;mask:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}}
.lg{{flex:none;width:120px;height:64px;display:grid;place-items:center;border:1px solid #e6efe8;border-radius:10px;padding:8px}}.lg img{{max-height:44px;object-fit:contain}}
.find .wrap{{padding:3rem 0}}.find .top{{display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:end;margin-bottom:2rem}}
.find h2,.join h2,.max h2{{font-size:clamp(2rem,3.6vw,3rem);line-height:1.1;margin:0}}
.cards3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}}
.card{{border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 12px 30px rgba(0,60,25,.12)}}
.card .im{{height:240px;background:linear-gradient(180deg,#f3fbee,#e2f4d6);display:flex;align-items:center;justify-content:center;overflow:hidden}}.card .im img{{height:215px;width:auto;object-fit:contain}}
.card .im.map img{{height:100%;width:100%;object-fit:cover}}
.card .t{{display:flex;gap:1rem;padding:1.2rem 1.3rem}}.card b{{color:{GREEN};font-size:1.3rem;min-width:5.5rem}}.card p{{margin:0;font-size:.9rem;color:#3d5246}}
.where{{position:relative;margin-top:4rem;background:linear-gradient(180deg,{GREEN},#06703a);color:#fff;overflow:hidden}}
.where:before{{content:"";position:absolute;inset:0;background:url(/assets/app/map-dublin-area.webp) center/cover;opacity:.18;mix-blend-mode:luminosity}}
.where .wrap{{position:relative;padding:5rem 0}}.where h2{{font-size:3rem;margin:0 0 2rem}}
.stat{{border-bottom:1px solid rgba(255,255,255,.35);padding:1rem 0;max-width:320px}}.stat b{{display:block;font-size:2.6rem;font-weight:600}}.stat span{{font-size:.85rem;opacity:.85}}
.join .wrap{{padding:5rem 0}}.join .ey{{color:#557264;font-size:.85rem}}.join h2{{margin:.4rem 0 2rem}}
.card h3{{margin:1.2rem 1.3rem .4rem;font-size:1.15rem}}.card .d{{margin:0 1.3rem 1.2rem;font-size:.9rem;color:#3d5246}}
.card .pill{{display:inline-block;margin:0 1.3rem 1.4rem;background:#08140d;color:#fff;border-radius:30px;padding:.8rem 1.4rem;font-size:.75rem;font-weight:700;letter-spacing:.06em;text-decoration:none}}
.band{{background:#06150c;padding:2.4rem 0}}.band .strip .lg{{background:#fff;border:0}}
.max{{background:#fcfcfc;position:relative;overflow:hidden}}.max:before{{content:"";position:absolute;right:-200px;top:-200px;width:800px;height:800px;border-radius:50%;background:repeating-radial-gradient(circle,transparent 0 60px,rgba(0,146,69,.08) 61px 62px)}}
.max .wrap{{position:relative;padding:5rem 0}}.max .ey{{color:{GREEN};font-size:.85rem;font-weight:600}}
.cols4{{display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;margin-top:2.5rem}}.cols4 h3{{color:{GREEN};font-size:1.05rem;margin:0 0 .5rem}}.cols4 p{{margin:0;font-size:.9rem;color:#3d5246}}
.cta{{background:linear-gradient(90deg,{GREEN},#58c43a);color:#fff;text-align:center;padding:4rem 1rem}}.cta h2{{font-size:2.4rem;margin:0 0 1.4rem}}
footer{{background:#06150c;color:#b8c8bd;padding:3rem 0;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:center}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav{{display:none}}.hero .wrap,.logos .wrap,.find .top{{grid-template-columns:1fr}}.cards3,.cols4{{grid-template-columns:1fr}}.hero .art .st{{display:none}}}}
"""
    cards = "".join(f'<div class="card"><div class="im{" map" if i == 1 else ""}"><img src="{src}" alt=""></div><div class="t"><b>{t}</b><p>{d}</p></div></div>'
                    for i, ((t, d), src) in enumerate(zip(STEPS, [st_img("countertop-12", sm=False), "/assets/app/map-dublin.webp", st_img("slim-kiosk-24", sm=False)])))
    join = [("Pubs & bars", "Keep guests in for one more round instead of leaving to find a charge.", "countertop-8-black"),
            ("Hotels & venues", "A free station for reception, lobby or bar, kept stocked by Jolt.", "countertop-8-white"),
            ("Events & stadiums", "High-capacity floor-standing stations for big crowds.", "media-kiosk-48")]
    jcards = "".join(f'<div class="card"><div class="im"><img src="{st_img(s, sm=False)}" alt=""></div><h3>{t}</h3><p class="d">{d}</p><a class="pill" href="{FORM}">GET A FREE STATION →</a></div>' for t, d, s in join)
    body = f"""
<header class="nav"><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><nav><a href="#how">How it works</a><a href="#venues">Venues</a><a href="/stations/">Stations</a></nav><a class="cta" href="{FORM}">TALK TO US</a></div></header>
<section class="hero"><div class="wrap"><div><h1>Stay connected, charge on the go!</h1><p>Rent a power bank at thousands of venues across Ireland and the UK, and return it to any Jolt station.</p>
<div class="btns"><a class="b b-dark" href="{FORM}">Get a free station</a><a class="b b-light" data-app href="#">Find a power bank</a></div></div>
<div class="art">{PHONE}<img class="st nb" src="{st_img('countertop-8-black', 'front', False)}" alt="Jolt Countertop 8 station"></div></div></section>
<section class="logos"><div class="wrap"><h2>Jolt powers 4,000+ venues across Ireland &amp; the UK</h2><div class="strip">{logos_html()}</div></div></section>
<section class="find" id="how"><div class="wrap"><div class="top"><h2>Find a power bank near you</h2><div><p>Stay powered up wherever you go. Use the Jolt app to find a station near you.</p><a class="b b-dark" data-app href="#">Download the app</a></div></div><div class="cards3">{cards}</div></div></section>
<section class="where"><div class="wrap"><h2>Where to find us</h2>{"".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in FACTS)}<div class="btns"><a class="b b-dark" data-app href="#">Get the app</a><a class="b b-light" href="{FORM}">Get a free station</a></div></div></section>
<section class="join" id="venues"><div class="wrap"><span class="ey">For venues</span><h2>Join the network</h2><div class="cards3">{jcards}</div></div></section>
<section class="band"><div class="wrap"><div class="strip">{logos_html()}</div></div></section>
<section class="max"><div class="wrap"><span class="ey">Why Jolt</span><h2>Make more of every visit<br>with Jolt</h2><div class="cols4">{"".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in BENEFITS)}</div></div></section>
<section class="cta"><h2>Ready for a free station?</h2><a class="b b-dark" href="{FORM}">Get a free station</a></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Power bank rental stations for venues across Ireland and the UK.</span></div></footer>"""
    return page("blue-wave", "Gradient hero", ["poppins"], css, body)


# ---------------------------------------------------------------- 2. Bold colour block (Joos Power layout)
def ex_bold_colour(S):
    css = f"""
body{{font-family:'Open Sans',sans-serif;color:#1d1d1d;background:#fff}}
.nav{{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid #eee}}.nav .wrap{{display:flex;align-items:center;height:70px;gap:2rem}}.nav img{{height:26px}}
.nav nav{{margin-left:auto;display:flex;gap:1.8rem;font-size:.9rem}}.nav nav a{{text-decoration:none}}
.nav .cta{{background:{GREEN};color:#fff;padding:.75rem 1.1rem;border-radius:4px;font-weight:700;font-size:.85rem;text-decoration:none}}
.hero{{background:radial-gradient(ellipse at 20% 30%,{LIME} 0%,#3fbf3f 35%,{GREEN} 80%);color:#fff;overflow:hidden}}
.hero .wrap{{display:grid;grid-template-columns:1fr 1fr;align-items:center;min-height:620px}}
.hero h1{{font-size:clamp(2.8rem,6vw,5rem);line-height:1.02;font-weight:800;margin:0 0 1.2rem}}.hero p{{font-size:1.1rem;max-width:26rem;font-weight:600}}
.hero .art{{position:relative;height:100%;display:flex;align-items:flex-end;justify-content:center}}
.hero .art img{{height:560px;width:auto;filter:drop-shadow(0 40px 60px rgba(0,0,0,.35));background:#fff;border-radius:24px 24px 0 0;padding:20px 20px 0}}
.trusted{{text-align:center;padding:3rem 0 2rem}}.trusted em{{font-size:.85rem;color:#888}}
.grid-logos{{display:grid;grid-template-columns:repeat(8,1fr);gap:1.4rem 2rem;align-items:center;margin-top:1.4rem}}.grid-logos .lg img{{max-height:46px;margin:auto;object-fit:contain;filter:grayscale(1);opacity:.8}}
.prod{{padding:2rem 0 4rem}}.panel{{border:1px solid #eee;border-radius:12px;padding:1.4rem;box-shadow:0 10px 40px rgba(0,0,0,.06)}}
.tabs{{display:flex;gap:.4rem;align-items:center;margin-bottom:1.2rem}}.tab{{padding:.55rem .9rem;border-radius:6px;font-size:.85rem;background:transparent;border:0;cursor:pointer}}.tab.on{{background:#f2f2f2}}
.tabs .demo{{margin-left:auto;background:{GREEN};color:#fff;padding:.65rem 1rem;border-radius:4px;text-decoration:none;font-size:.85rem;font-weight:700}}
.prods{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}.pc{{text-decoration:none}}.pc .im{{background:#eefbe6;border-radius:10px;height:260px;display:flex;align-items:center;justify-content:center;padding:1rem}}.pc .im img{{height:225px;width:auto;object-fit:contain}}
.pc small{{display:block;color:#888;font-size:.75rem;margin-top:.8rem}}.pc h3{{margin:.1rem 0 .3rem;font-size:1.2rem}}.pc p{{margin:0;font-size:.85rem;color:#555}}.pc .n{{color:{GREEN};font-size:.8rem;font-weight:700;margin-top:.4rem;display:block}}
.how{{background:{GREEN};padding:5rem 0}}.how .row{{display:grid;grid-template-columns:1.6fr 1fr;gap:1rem;align-items:stretch;margin-bottom:1rem}}.how .row.r{{grid-template-columns:1fr 1.6fr}}
.how .ph{{border-radius:6px;overflow:hidden;background:#0d2a17 url(/assets/app/map-dublin.webp) center/cover;min-height:260px;opacity:.95}}
.how .bx{{background:#111;color:#fff;border-radius:6px;padding:1.6rem;font-size:1.05rem;font-weight:600}}.how .bx h3{{font-size:1.6rem;font-weight:800;margin:0 0 .6rem;text-transform:uppercase}}
.stats{{padding:4rem 0;background:#f6f6f6}}.stats h2{{font-weight:600;font-size:1.4rem;margin:0 0 1.4rem}}.sgrid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}
.sc{{background:#fff;border-radius:10px;padding:1.6rem}}.sc b{{display:block;font-size:2rem;font-weight:600}}.sc span{{font-size:.8rem;color:#666}}
.spaces{{padding:5rem 0}}.spaces h2{{color:{GREEN};font-size:1.8rem;margin:0 0 1.6rem;font-weight:600}}
.vt{{display:grid;grid-template-columns:240px 1fr;border:1px solid #eee;border-radius:10px;overflow:hidden;background:#fafafa}}
.vt .list button{{display:block;width:100%;text-align:left;padding:1.2rem 1rem;border:0;border-bottom:1px solid #eee;background:none;font:inherit;font-size:.9rem;cursor:pointer}}.vt .list button.on{{background:#fff;color:{GREEN};font-weight:700;border-left:3px solid {GREEN}}}
.vt .pane{{display:grid;grid-template-columns:1fr 1fr;gap:1.6rem;padding:1.6rem;background:#fff}}.vt .pane .im{{border-radius:8px;background:#eefbe6;display:flex;align-items:center;justify-content:center;height:320px}}.vt .pane .im img{{height:290px;width:auto}}
.vt h3{{color:{GREEN};margin:.2rem 0 .3rem}}.vt p{{font-size:.9rem;color:#555}}
.about{{padding:4rem 0 6rem}}.about .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:3rem}}.about .tag{{display:inline-block;border:1px solid #ccc;border-radius:20px;padding:.3rem .8rem;font-size:.75rem;margin-bottom:1rem}}.about h2{{font-size:2.6rem;margin:0;line-height:1.1;font-weight:600}}
footer{{background:#111;color:#bbb;padding:3rem 0;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav{{display:none}}.hero .wrap,.how .row,.how .row.r,.vt,.vt .pane,.about .wrap{{grid-template-columns:1fr}}.hero .art img{{height:360px}}.prods,.sgrid{{grid-template-columns:1fr 1fr}}.grid-logos{{grid-template-columns:repeat(4,1fr)}}}}
"""
    prods = "".join(f'<a class="pc" href="/stations/{x["slug"]}/" data-t="{x["type"]}"><div class="im"><img src="{st_img(x["slug"])}" alt=""></div><small>{x["type"]}</small><h3>{x["name"]}{" · " + x["finish"] if x["slug"].startswith("countertop-8") else ""}</h3><p>{x["tag"]}</p><span class="n">{cap(x)}</span></a>' for x in S)
    spaces = [("Hospitality", "Pubs, bars, restaurants, hotels", "Guests stay longer when they don't have to leave to charge their phone. A free Jolt station sits on the bar or beside reception.", "countertop-8-black"),
              ("Nightlife & events", "Nightclubs, festivals, gigs", "High-capacity stations so a full room can stay charged all night.", "tower-48"),
              ("Healthcare", "Hospitals and clinics", "A station in waiting areas and A&E so patients and visitors can stay in touch.", "secure-locker-24"),
              ("Leisure", "Gyms, leisure centres, stadiums", "Floor-standing stations for busy public spaces.", "media-kiosk-48")]
    vtl = "".join(f'<button type="button" class="{"on" if i == 0 else ""}" data-i="{i}">{t}</button>' for i, (t, *_ ) in enumerate(spaces))
    vtp = "".join(f'<div class="pane" data-p="{i}"{"" if i == 0 else " hidden"}><div class="im"><img src="{st_img(s, sm=False)}" alt=""></div><div><h3>{t}</h3><small>{sub}</small><p>{d}</p><a href="{FORM}" style="color:{GREEN};font-weight:700;font-size:.85rem">Get a free station »</a></div></div>' for i, (t, sub, d, s) in enumerate(spaces))
    body = f"""
<header class="nav"><div class="wrap"><img src="{LOGO_B}" alt="Jolt"><nav><a href="/">Home</a><a href="#venues">Venues</a><a href="/stations/">Stations</a><a href="/areas/">Areas</a></nav><a class="cta" href="{FORM}">Talk to the Jolt team</a></div></header>
<section class="hero"><div class="wrap"><div><h1>Stay charged,<br>stay connected</h1><p>Free power bank rental stations for venues across Ireland and the UK. Installed and looked after by Jolt.</p></div><div class="art"><img class="nb" src="{st_img('slim-kiosk-24', 'angle', False)}" alt="Jolt Slim Kiosk 24"></div></div></section>
<section class="trusted"><div class="wrap"><em>Trusted by</em><div class="grid-logos">{logos_html()}</div></div></section>
<section class="prod" id="stations"><div class="wrap"><div class="panel"><div class="tabs"><button class="tab on" data-f="">All</button><button class="tab" data-f="Countertop">Countertop</button><button class="tab" data-f="Floor-standing">Floor-standing</button><a class="demo" href="{FORM}">Get a free station</a></div><div class="prods">{prods}</div></div></div></section>
<section class="how" id="how"><div class="wrap"><div class="row"><div class="ph"></div><div class="bx"><h3>How to rent</h3>Tap your card or phone on the station and take a power bank.</div></div><div class="row r"><div class="bx"><h3>How to return</h3>Slot the power bank back into any Jolt station. You can return it 24/7.</div><div class="ph" style="background-image:url(/assets/app/map-london.webp)"></div></div></div></section>
<section class="stats"><div class="wrap"><h2>Chosen by thousands of venues</h2><div class="sgrid">{"".join(f'<div class="sc"><b>{n}</b><span>{l}</span></div>' for n, l in FACTS)}</div></div></section>
<section class="spaces" id="venues"><div class="wrap"><h2>Charging for every kind of venue</h2><div class="vt"><div class="list">{vtl}</div><div>{vtp}</div></div></div></section>
<section class="about"><div class="wrap"><div><span class="tag">About Jolt</span><h2>Free charging stations built for busy venues</h2></div><p>Jolt installs and maintains power bank rental stations for pubs, hotels, hospitals and venues across Ireland and the UK. Your guests rent a power bank with a tap, and your venue earns a share of every rental.</p></div></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Ireland &amp; the UK</span></div></footer>
<script>
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>{{document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on',x===t));document.querySelectorAll('.pc').forEach(p=>p.hidden=!!t.dataset.f&&p.dataset.t!==t.dataset.f)}});
document.querySelectorAll('.vt .list button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.vt .list button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('.vt .pane').forEach(p=>p.hidden=p.dataset.p!==b.dataset.i)}});
</script>"""
    return page("bold-colour", "Bold colour block", ["open-sans"], css, body)


# ---------------------------------------------------------------- 3. Clean navy (ChargedUp layout)
def ex_clean_navy(S):
    NAVY = "#0c1f33"
    css = PHONE_CSS + f"""
body{{font-family:'Plus Jakarta Sans',sans-serif;color:{NAVY};background:#fff}}
.nav{{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(10px)}}.nav .wrap{{display:flex;align-items:center;height:68px;gap:2rem}}.nav img{{height:24px}}
.nav nav{{margin-left:auto;display:flex;gap:1.6rem;font-size:.85rem}}.nav nav a{{text-decoration:none}}
.pill{{display:inline-block;border-radius:40px;padding:.85rem 1.4rem;font-weight:700;font-size:.85rem;text-decoration:none}}.p-navy{{background:{NAVY};color:#fff}}.p-out{{border:1px solid #c9d3dd;color:{NAVY};background:#fff}}.p-green{{background:{LIME};color:{NAVY}}}
.hero{{position:relative;min-height:640px;display:flex;align-items:center;overflow:hidden;background:#eef3ee}}
.hero .bg{{position:absolute;right:-4%;top:50%;transform:translateY(-50%) rotate(-8deg)}}.hero .bg .phone{{width:340px}}
.hero:before{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#fff 30%,rgba(255,255,255,.6) 55%,transparent 75%);z-index:1}}
.hero .wrap{{position:relative;z-index:2}}.ey{{display:flex;align-items:center;gap:.7rem;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:{GREEN};font-weight:700}}.ey:before{{content:"";width:28px;height:2px;background:{GREEN}}}
.hero h1{{font-size:clamp(2.6rem,5vw,4rem);line-height:1.05;margin:1rem 0;font-weight:700;max-width:36rem}}.hero h1 span{{color:{GREEN}}}.hero p{{max-width:30rem;color:#405265;line-height:1.6}}
.btns{{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1.6rem}}
.qa{{padding:4rem 0}}.qa .wrap{{max-width:760px}}.qa h2{{font-size:1.8rem;margin:0 0 1rem}}.qa p{{color:#405265;line-height:1.7}}
.trust{{text-align:center;padding:3rem 0}}.trust .ey{{justify-content:center}}.trust .ey:before{{display:none}}.trust p{{color:#5a6b7c;max-width:28rem;margin:.8rem auto 2rem}}
.lgrid{{display:grid;grid-template-columns:repeat(6,1fr);gap:2rem;align-items:center}}.lgrid .lg img{{max-height:52px;margin:auto;object-fit:contain;filter:grayscale(1) contrast(1.1);opacity:.75}}
.simple .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center;padding:5rem 0}}.simple h2{{font-size:2.8rem;margin:.6rem 0 1rem}}
.step{{display:grid;grid-template-columns:34px 1fr;gap:1rem;margin:1.4rem 0}}.step i{{width:30px;height:30px;border-radius:50%;background:{NAVY};color:#fff;display:grid;place-items:center;font-style:normal;font-size:.8rem;font-weight:700}}.step h3{{margin:0 0 .3rem;font-size:1.05rem}}.step p{{margin:0;color:#5a6b7c;font-size:.9rem}}
.glass{{border-radius:22px;background:radial-gradient(circle at 30% 30%,rgba(158,242,48,.25),transparent 60%),#f6faf6;box-shadow:0 30px 60px rgba(12,31,51,.08);padding:2rem;display:grid;place-items:center;min-height:420px}}.glass img{{height:380px;width:auto}}
.net{{background:radial-gradient(ellipse at 70% 0%,#173a5c,{NAVY} 60%);color:#fff;text-align:center;padding:5rem 0}}.net .ey{{justify-content:center;color:{LIME}}}.net .ey:before{{display:none}}.net h2{{font-size:2.6rem;margin:.8rem 0}}.net small{{color:#9fb2c4}}
.ngrid{{display:grid;grid-template-columns:repeat(4,1fr);margin:3rem 0}}.ngrid div{{border-right:1px solid rgba(255,255,255,.12);padding:1rem}}.ngrid div:last-child{{border:0}}.ngrid b{{display:block;font-size:3rem;color:{LIME};font-weight:500}}.ngrid span{{font-size:.75rem;letter-spacing:.15em;text-transform:uppercase;color:#9fb2c4}}
.sol{{padding:5rem 0}}.sol .head{{text-align:center;margin-bottom:3rem}}.sol .ey{{justify-content:center}}.sol .ey:before{{display:none}}.sol h2{{font-size:2.4rem;margin:.6rem 0}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center;margin-bottom:4rem}}.row.rev .im{{order:2}}
.row .im{{border-radius:20px;background:linear-gradient(160deg,#eaf7e0,#d9efe2);height:380px;display:grid;place-items:center;position:relative;overflow:hidden}}.row .im img{{height:340px;width:auto}}.row .im em{{position:absolute;left:1rem;bottom:1rem;background:#fff;border-radius:20px;padding:.3rem .8rem;font-size:.75rem;font-style:normal}}
.row h3{{font-size:1.8rem;margin:0 0 .8rem}}.row p{{color:#5a6b7c}}.row ul{{list-style:none;padding:0;margin:1rem 0 1.6rem}}.row li{{padding:.4rem 0 .4rem 1.8rem;position:relative;font-size:.92rem}}.row li:before{{content:"✓";position:absolute;left:0;width:20px;height:20px;border-radius:50%;background:#e4f8d2;color:{GREEN};font-size:.7rem;display:grid;place-items:center}}
footer{{background:{NAVY};color:#9fb2c4;padding:3rem 0;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav{{display:none}}.simple .wrap,.row{{grid-template-columns:1fr}}.row.rev .im{{order:0}}.ngrid,.lgrid{{grid-template-columns:1fr 1fr}}.hero .bg{{opacity:.35}}}}
"""
    rows = [("For venues", "Free stations for pubs, restaurants, hotels and cafés. Guests stay longer and your venue earns a share of every rental.", ["Free installation and maintenance", "Revenue share on every rental", "Kept stocked by Jolt", "Card pre-authorisation on every rental"], "countertop-12"),
            ("For events", "Floor-standing stations for nightclubs, gigs and festivals, built for busy rooms.", ["Up to 48 power banks per station", "Tap-to-pay", "Return to any Jolt station", "Lightning, USB-C and Micro-USB cables"], "tower-48"),
            ("For public spaces", "Stations for hospitals, stadiums and transport hubs.", ["Secure Locker with closed compartments", "Large-screen Media Kiosk", "Installed and looked after by Jolt"], "secure-locker-24")]
    rws = "".join(f'<div class="row{" rev" if i % 2 else ""}"><div class="im"><img src="{st_img(s, sm=False)}" alt=""><em>{t}</em></div><div><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul><a class="pill p-navy" href="{FORM}">Request for your venue</a></div></div>' for i, (t, d, L, s) in enumerate(rows))
    body = f"""
<header class="nav"><div class="wrap"><img src="{LOGO_B}" alt="Jolt"><nav><a href="/">Home</a><a href="/stations/">Stations</a><a href="/areas/">Areas</a><a href="#faq">FAQ</a></nav><a class="pill p-navy" href="{FORM}">Request for your venue</a></div></header>
<section class="hero"><div class="bg">{PHONE}</div><div class="wrap"><span class="ey">Ireland &amp; the UK's power bank network</span><h1>Powering Ireland's<br><span>best venues</span></h1><p>Jolt is a power bank rental network for pubs, bars, restaurants, hotels and other venues. We install a free station, your guests tap a card to borrow a charger and stay longer, and your venue earns a share of every rental.</p><div class="btns"><a class="pill p-navy" href="{FORM}">Request for your venue</a><a class="pill p-out" href="#how">See how it works</a></div></div></section>
<section class="qa" id="faq"><div class="wrap"><h2>How much does a Jolt station cost a venue?</h2><p>Nothing. The station, power banks, installation and maintenance are free. You provide a small space and a standard power socket, and Jolt shares the rental income with your venue.</p></div></section>
<section class="trust"><div class="wrap"><span class="ey">Trusted by leading venues</span><p>4,000+ venues across Ireland and the UK have used Jolt to keep their guests connected.</p><div class="lgrid">{logos_html()}</div></div></section>
<section class="simple" id="how"><div class="wrap"><div><span class="ey">Tap, charge &amp; return</span><h2>It's that simple</h2>{"".join(f'<div class="step"><i>{i + 1}</i><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(STEPS))}<a class="pill p-navy" href="{FORM}">Request for your venue</a></div><div class="glass"><img src="{st_img('countertop-8-white', 'angle', False)}" alt="Jolt Countertop 8"></div></div></section>
<section class="net"><div class="wrap"><span class="ey">Our network</span><h2>A growing network across<br>Ireland and the UK</h2><div class="ngrid">{"".join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in FACTS)}</div><a class="pill p-green" href="{FORM}">Request for your venue</a></div></section>
<section class="sol"><div class="wrap"><div class="head"><span class="ey">Solutions</span><h2>Charging stations for<br>different environments</h2></div>{rws}</div></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Power bank rental for venues across Ireland and the UK</span></div></footer>"""
    return page("clean-navy", "Clean navy", ["plus-jakarta-sans"], css, body)


# ---------------------------------------------------------------- 4. Rounded & playful (Naki layout)
def ex_pill_play(S):
    css = f"""
body{{font-family:Montserrat,sans-serif;color:#1c2230;background:#fff;overflow-x:hidden}}
.nav{{position:sticky;top:14px;z-index:50;margin:14px auto 0;width:min(900px,92vw);background:rgba(255,255,255,.9);backdrop-filter:blur(12px);border-radius:60px;box-shadow:0 10px 30px rgba(0,0,0,.08);display:flex;align-items:center;gap:1.6rem;padding:.7rem 1.4rem}}
.nav img{{height:22px}}.nav nav{{margin-left:auto;display:flex;gap:1.4rem;font-size:.85rem;font-weight:600}}.nav nav a{{text-decoration:none}}.nav .biz{{color:{GREEN};font-weight:800;text-decoration:none;font-size:.85rem}}
.hero{{display:grid;grid-template-columns:1fr 1fr;align-items:center;gap:3rem;padding:4rem 0 3rem}}
.blob{{height:380px;border-radius:0 220px 220px 0;background:linear-gradient(135deg,{GREEN},{LIME});display:flex;align-items:center;justify-content:flex-end;padding-right:3rem;overflow:hidden}}.blob img{{height:330px;width:auto;border-radius:20px;background:#fff;padding:8px}}
.hero h1{{font-size:clamp(2.6rem,5vw,4.4rem);line-height:1;margin:0 0 1.2rem;font-weight:800}}.hero p{{max-width:28rem;color:#4b5363;font-size:.95rem;line-height:1.6}}
.qq{{display:flex;gap:1rem;align-items:center;margin-top:1.4rem}}.qq .em{{font-size:2.6rem}}.qq h3{{margin:0;font-size:1.1rem;font-weight:800}}
.marq{{overflow:hidden;padding:.6rem 0}}.track{{display:flex;gap:1rem;width:max-content;animation:mv 40s linear infinite}}.marq.r .track{{animation-direction:reverse}}
.pillimg{{flex:none;width:340px;height:170px;border-radius:120px;overflow:hidden;background:linear-gradient(135deg,#eaf9da,#d4f0dc);display:grid;place-items:center}}.pillimg img{{height:150px;width:auto}}.pillimg img[src*=stations]{{mix-blend-mode:multiply}}.pillimg.map img{{width:100%;height:100%;object-fit:cover}}
@keyframes mv{{to{{transform:translateX(-50%)}}}}
.smart{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center;padding:5rem 0}}.smart img{{height:200px;width:auto}}.smart h2{{font-size:3rem;margin:1rem 0;font-weight:800;line-height:1}}.smart p{{color:#4b5363;max-width:24rem}}
.chips{{display:flex;flex-direction:column;gap:.7rem;align-items:flex-start}}.chip{{border:1px solid #e3e7ee;border-radius:40px;padding:.6rem 1rem;font-size:.85rem;font-weight:600;color:{GREEN};background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.04)}}
.dark{{background:#1c2230;color:#fff;padding:5rem 0}}.dark small{{letter-spacing:.2em;text-transform:uppercase;font-size:.75rem;color:#9aa3b5}}.dark h2{{font-size:clamp(3rem,8vw,6.4rem);line-height:1;margin:1rem 0 0;font-weight:800;background:linear-gradient(90deg,{LIME},{GREEN});-webkit-background-clip:text;background-clip:text;color:transparent}}
.steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem;margin-top:3rem}}.steps div{{background:#262d3d;border-radius:28px;padding:1.6rem}}.steps b{{font-size:1.4rem;color:{LIME}}}.steps p{{color:#c7cdd8;font-size:.9rem}}
.full{{height:440px;background:#0e1219 url(/assets/app/map-dublin-area.webp) center/cover;position:relative}}.full:after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#1c2230,transparent 30%,transparent 70%,#fff)}}
.app{{display:grid;grid-template-columns:1fr 1.3fr;gap:3rem;align-items:center;padding:4rem 0 6rem}}.app small{{font-size:.75rem;color:#7a8394;letter-spacing:.1em;text-transform:uppercase}}.app h2{{font-size:2.6rem;font-weight:800;margin:.6rem 0 1rem;line-height:1.05}}.app p{{color:#4b5363}}
.app a.more{{color:{GREEN};font-weight:700;text-decoration:none}}.screens{{display:flex;gap:1rem;justify-content:center}}.scr{{width:180px;aspect-ratio:9/19;border-radius:28px;border:7px solid #1c2230;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,.15)}}.scr img{{width:100%;height:100%;object-fit:cover}}.scr:nth-child(2){{transform:translateY(-20px)}}
footer{{background:#1c2230;color:#9aa3b5;padding:3rem 0;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}footer img{{height:22px}}
@media(max-width:860px){{.nav nav{{display:none}}.hero,.smart,.app{{grid-template-columns:1fr}}.steps{{grid-template-columns:1fr}}.blob{{height:260px}}.blob img{{height:220px}}.screens .scr:nth-child(3){{display:none}}}}
"""
    tiles = ([(st_img(x["slug"]), "") for x in S] + [("/assets/app/map-dublin.webp", "map"), ("/assets/app/map-london.webp", "map"), ("/assets/app/map-cork.webp", "map")])
    def marq(items, rev=False):
        t = "".join(f'<div class="pillimg {c}"><img src="{s}" alt="" loading="lazy"></div>' for s, c in items)
        return f'<div class="marq{" r" if rev else ""}"><div class="track">{t}{t}</div></div>'
    body = f"""
<header class="nav"><img src="{LOGO_B}" alt="Jolt"><nav><a href="#how">How it works</a><a href="/areas/">Locations</a><a href="/stations/">Stations</a></nav><a class="biz" href="{FORM}">For venues</a></header>
<div class="hero"><div class="blob"><img class="nb" src="{st_img('countertop-12', 'front', False)}" alt="Jolt Countertop 12"></div><div style="padding-right:4vw"><h1>Stop running out.<br>Start sharing.</h1><p>Jolt is a power bank sharing network. Rent a power bank from one of thousands of Jolt stations across Ireland and the UK, charge your phone and return it to any station.</p><div class="qq"><span class="em">🔋</span><div><h3>Phone on 5%?</h3><p style="margin:.2rem 0 0">Open the Jolt app and find the nearest station.</p></div></div></div></div>
{marq(tiles[:6])}{marq(tiles[4:], True)}
<div class="wrap smart"><div><img src="{st_img('countertop-8-black', 'front', False)}" alt=""><h2>Charge<br>smarter.</h2><p>One power bank shared by many people, instead of chargers bought and forgotten in a drawer.</p></div><div class="chips"><span class="chip">🔋 Rent as you need</span><span class="chip">⚡ Charge on the go</span><span class="chip">📍 Return to any station</span><span class="chip">🔌 Three cables built in</span><span class="chip">🕐 Available 24/7</span></div></div>
<section class="dark" id="how"><div class="wrap"><small>How it works</small><h2>Relax.<br>We've got you<br>covered.</h2><div class="steps">{"".join(f'<div><b>{i + 1}. {t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(STEPS))}</div></div></section>
<div class="full"></div>
<div class="wrap app"><div><small>Rent with the Jolt app</small><h2>Find a power bank in seconds.</h2><p>The Jolt app shows every station near you on a live map. Tap your card at the station and you're charging.</p><a class="more" data-app href="#">Find out where Jolt is →</a></div><div class="screens"><div class="scr"><img src="/assets/app/map-dublin-hero.webp" alt=""></div><div class="scr"><img src="/assets/app/map-london-area.webp" alt=""></div><div class="scr"><img src="/assets/app/map-galway.webp" alt=""></div></div></div>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><a href="{FORM}" style="color:{LIME};text-decoration:none;font-weight:700">Get a free station for your venue →</a></div></footer>"""
    return page("pill-play", "Rounded & playful", ["montserrat"], css, body)


# ---------------------------------------------------------------- 5. Fresh & friendly (ChargerGoGo layout)
def ex_fresh_green(S):
    css = f"""
body{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#1f2a24;background:#fff}}
.ann{{background:#f1fbe6;text-align:center;font-size:.85rem;padding:.55rem 1rem}}.ann b{{background:{GREEN};color:#fff;border-radius:20px;padding:.1rem .6rem;font-size:.7rem;margin-right:.5rem}}
.nav{{position:sticky;top:0;z-index:50;background:#fff;box-shadow:0 1px 0 #eef2ee}}.nav .wrap{{display:flex;align-items:center;gap:2rem;height:72px}}.nav img{{height:26px}}.nav nav{{display:flex;gap:1.6rem;font-size:.9rem;margin-left:1rem}}.nav nav a{{text-decoration:none}}.nav nav a:first-child{{color:{GREEN};font-weight:600}}
.nav .cta{{margin-left:auto;background:{GREEN};color:#fff;border-radius:8px;padding:.7rem 1.1rem;font-weight:600;text-decoration:none;font-size:.9rem}}
.btn{{display:inline-block;border-radius:8px;padding:.85rem 1.3rem;font-weight:700;font-size:.9rem;text-decoration:none}}.bg{{background:{GREEN};color:#fff}}.bo{{background:#fff;color:#1f2a24;border:1px solid #d6e2d8}}
.hero{{background:linear-gradient(180deg,#fff 0%,#f0fbe4 100%);padding:4rem 0 5rem}}.hero .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}}
.hero h1{{font-size:clamp(2.4rem,4.6vw,3.6rem);line-height:1.1;margin:0 0 1rem}}.hero p{{color:#5b6b61;margin:0 0 1.6rem}}.hero .im{{border-radius:24px;background:linear-gradient(135deg,#dff5c8,#c4ecd2);height:420px;display:grid;place-items:center;overflow:hidden}}.hero .im img{{height:390px;width:auto}}
.trust{{text-align:center;padding:2.4rem 0}}.trust small{{color:#6b7a70}}.lrow{{display:flex;gap:2.4rem;justify-content:center;flex-wrap:wrap;margin-top:1.2rem}}.lrow .lg img{{height:50px;width:auto;object-fit:contain}}
.news{{padding:3rem 0 5rem;background:#f7f9f7}}.news .wrap{{display:grid;grid-template-columns:1.1fr .9fr;gap:3rem;align-items:center}}.tag{{background:{GREEN};color:#fff;border-radius:20px;padding:.15rem .6rem;font-size:.7rem;font-weight:700}}
.news h2{{font-size:2rem;margin:.8rem 0}}.news p{{color:#5b6b61}}.boxes{{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;margin:1.4rem 0}}.boxes div{{background:#fff;border:1px solid #e3ebe5;border-radius:10px;padding:1rem}}.boxes b{{display:block;font-size:1.4rem;color:{GREEN}}}.boxes span{{font-size:.75rem;color:#6b7a70}}
.news .im{{border-radius:16px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,.08)}}
.join{{background:linear-gradient(180deg,#fff,#eefbe4 60%,#bfe89c);padding:5rem 0;text-align:center}}.join h2{{font-size:2.2rem;margin:0}}.join>.wrap>p{{color:#6b7a70}}
.c4{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:2.4rem;text-align:left}}.c{{background:#fff;border-radius:16px;padding:1rem;box-shadow:0 10px 30px rgba(0,60,20,.08)}}.c .ci{{border-radius:12px;background:#f2f8ef;height:170px;display:flex;align-items:center;justify-content:center}}.c .ci img{{height:150px;width:auto}}
.c h3{{font-size:1.05rem;margin:.9rem 0 .4rem}}.c p{{font-size:.85rem;color:#5b6b61;min-height:3.4rem}}.c .btn{{display:block;text-align:center}}.c .lm{{display:block;text-align:center;font-size:.8rem;color:{GREEN};margin-top:.6rem;text-decoration:none;font-weight:600}}
.what{{padding:5rem 0}}.what .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}}.what .im{{border-radius:20px;background:url(/assets/app/map-dublin.webp) center/cover;min-height:380px}}.what h2{{font-size:2.6rem;margin:0 0 1rem}}.what p{{color:#5b6b61;line-height:1.7}}
.pres{{text-align:center;padding:4rem 0}}.pres h2{{font-size:2.2rem;margin:0}}.pres p{{color:#6b7a70}}.map{{margin:2rem auto;max-width:760px;border-radius:16px;overflow:hidden;box-shadow:0 20px 40px rgba(0,0,0,.08)}}.map img{{width:100%}}
.nums{{display:flex;justify-content:center;gap:3rem;margin:2rem 0}}.nums b{{display:block;font-size:2.4rem;color:{GREEN}}}.nums span{{color:#6b7a70;font-size:.85rem}}
.uses{{padding:4rem 0 6rem;text-align:center}}.uses h2{{font-size:2rem;max-width:40rem;margin:0 auto}}.u3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:2rem}}.u{{border:1px solid #e3ebe5;border-radius:14px;padding:1.6rem}}.u .ic{{font-size:2rem}}.u h3{{margin:.6rem 0 .4rem}}.u p{{font-size:.85rem;color:#5b6b61}}
footer{{background:#13261a;color:#b6c7bb;padding:3rem 0;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav{{display:none}}.hero .wrap,.news .wrap,.what .wrap{{grid-template-columns:1fr}}.c4,.u3{{grid-template-columns:1fr}}.nums{{gap:1.4rem;flex-wrap:wrap}}}}
"""
    c4 = [("Get a free station", "A free Jolt station for your venue, installed and maintained by us.", "Get a station", "countertop-8-white"),
          ("Events & nightlife", "High-capacity stations for clubs, gigs and festivals.", "Talk to us", "tower-48"),
          ("Public spaces", "Stations for hospitals, stadiums and transport hubs.", "Talk to us", "media-kiosk-48"),
          ("Charge my phone", "Find the nearest Jolt station in the app and rent a power bank.", "Find a station", "slim-kiosk-24")]
    cards = "".join(f'<div class="c"><div class="ci"><img src="{st_img(s)}" alt=""></div><h3>{t}</h3><p>{d}</p><a class="btn bg" {"data-app" if b == "Find a station" else ""} href="{FORM}">{b}</a><a class="lm" href="/stations/{s}/">Learn more</a></div>' for t, d, b, s in c4)
    uses = [("🍺", "Pubs & bars", "Guests stay for another round instead of leaving to charge."), ("🏥", "Hospitals", "Patients and visitors can stay in touch while they wait."), ("🏨", "Hotels", "A free station at reception, the lobby or the bar.")]
    body = f"""
<div class="ann"><b>New</b>4,000+ venues across Ireland and the UK have used Jolt</div>
<header class="nav"><div class="wrap"><img src="{LOGO_B}" alt="Jolt"><nav><a href="/">Home</a><a href="/stations/">Products</a><a href="/areas/">Areas</a><a href="#how">How it works</a></nav><a class="cta" href="{FORM}">Get a free station</a></div></header>
<section class="hero"><div class="wrap"><div><h1>Charge your phone<br>on the go</h1><p>Stay powered up, wherever the night takes you.</p><a class="btn bg" href="{FORM}">Get a free station</a> <a class="btn bo" data-app href="#">Find a power bank</a></div><div class="im"><img src="{st_img('countertop-12', 'angle', False)}" alt=""></div></div></section>
<section class="trust"><div class="wrap"><small>Trusted by venues across Ireland &amp; the UK</small><div class="lrow">{"".join(f'<div class="lg"><img src="/assets/venues/{n}.webp" alt=""></div>' for n in VENUE_LOGOS[:7])}</div></div></section>
<section class="news"><div class="wrap"><div><span class="tag">FREE</span><h2>A free station for your venue</h2><p>The station, power banks, installation and maintenance are free, and your venue earns a share of every rental.</p><div class="boxes"><div><b>€0</b><span>cost to install</span></div><div><b>7</b><span>station models</span></div><div><b>24/7</b><span>rent and return</span></div></div><a class="btn bg" href="/stations/">See the stations</a></div><div class="im"><img src="/assets/app/map-dublin-hero.webp" alt=""></div></div></section>
<section class="join"><div class="wrap"><h2>Join the Jolt network</h2><p>There are several ways to work with Jolt.</p><div class="c4">{cards}</div></div></section>
<section class="what" id="how"><div class="wrap"><div class="im"></div><div><h2>What is Jolt?</h2><p>Jolt is a power bank rental network for venues in Ireland and the UK. Guests tap a card or phone on the station, take a power bank with Lightning, USB-C and Micro-USB cables built in, and return it to any Jolt station.</p><a class="btn bg" href="/stations/">Check our products</a></div></div></section>
<section class="pres"><div class="wrap"><h2>Our presence</h2><p>Jolt stations across Dublin and beyond.</p><div class="map"><img src="/assets/app/map-dublin-area.webp" alt="Map of Jolt stations around Dublin"></div><div class="nums"><div><b>4,000+</b><span>venues have used Jolt</span></div><div><b>2</b><span>countries</span></div><div><b>7</b><span>station models</span></div></div><a class="btn bo" href="{FORM}">Get a free station</a> <a class="btn bg" data-app href="#">Find a power bank</a></div></section>
<section class="uses"><div class="wrap"><h2>Phone charging stations for every kind of venue</h2><div class="u3">{"".join(f'<div class="u"><div class="ic">{i}</div><h3>{t}</h3><p>{d}</p><a class="btn bg" href="{FORM}">Learn more</a></div>' for i, t, d in uses)}</div></div></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Ireland &amp; the UK</span></div></footer>"""
    return page("fresh-green", "Fresh & friendly", [], css, body)


# ---------------------------------------------------------------- 6. Night-out energy (Chimpy layout)
def ex_night_out(S):
    css = f"""
body{{font-family:Inter,sans-serif;color:#111;background:#fff}}
.nav{{position:sticky;top:12px;z-index:50;display:flex;justify-content:center;gap:.6rem;align-items:center;margin-top:12px}}
.nav .logo{{background:#111;border-radius:50px;padding:.55rem .9rem;display:flex}}.nav .logo img{{height:22px}}
.nav nav{{background:rgba(240,240,240,.92);backdrop-filter:blur(10px);border-radius:12px;padding:.4rem;display:flex;gap:.2rem;align-items:center}}.nav nav a{{padding:.5rem .8rem;font-size:.85rem;font-weight:600;text-decoration:none;border-radius:8px}}.nav nav a.b2b{{background:#111;color:{LIME}}}
.hero{{position:relative;margin-top:-60px;min-height:640px;display:grid;place-items:center;text-align:center;color:#fff;background:#0b0f0b url(/assets/app/map-dublin-area.webp) center/cover;overflow:hidden}}
.hero:before{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,.35),rgba(0,0,0,.8))}}
.hero>div{{position:relative}}.hero h1{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:800;text-transform:uppercase;font-size:clamp(3rem,8vw,6.4rem);line-height:.9;margin:0 0 1.4rem}}.hero h1 span{{color:{LIME}}}
.bt{{display:inline-flex;align-items:center;gap:.5rem;border-radius:40px;padding:.85rem 1.4rem;font-weight:700;font-size:.85rem;text-decoration:none}}.bt-g{{background:{LIME};color:#111}}.bt-k{{background:#111;color:#fff;border:1px solid #333}}
.promo{{width:min(1180px,92vw);margin:2rem auto;border-radius:22px;overflow:hidden;background:linear-gradient(110deg,#111 40%,{GREEN});color:#fff;display:grid;grid-template-columns:1fr 1fr;align-items:center;min-height:300px}}
.promo div{{padding:2.4rem}}.promo h2{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:800;font-size:3.4rem;line-height:.95;margin:0 0 1.2rem;text-transform:uppercase}}.promo img{{height:260px;width:auto;margin:20px auto;border-radius:18px}}
.empty{{width:min(1000px,92vw);margin:5rem auto;display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}}.empty h2{{font-size:2rem;margin:0 0 1rem;font-weight:800}}.empty p{{color:#555}}.empty .m{{border-radius:20px;overflow:hidden}}
.partners{{display:flex;gap:2.4rem;justify-content:center;flex-wrap:wrap;padding:1rem 0 4rem}}.partners .lg img{{height:44px;width:auto;object-fit:contain}}
.offer{{width:min(1180px,92vw);margin:0 auto 4rem;display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:center}}.offer .im{{border-radius:20px;background:#f2f2f2;height:380px;display:flex;align-items:center;justify-content:center}}.offer .im img{{height:340px;width:auto}}.offer h2{{font-size:2rem;font-weight:800;margin:0 0 1rem}}.offer p{{color:#555}}.offer small{{display:block;margin-top:1rem;color:#888}}
.event{{width:min(1180px,92vw);margin:0 auto 4rem;border-radius:22px;overflow:hidden;position:relative;color:#fff;background:#111;min-height:320px;display:grid;grid-template-columns:1.2fr .8fr;align-items:center}}
.event div{{padding:2.4rem;position:relative;z-index:1}}.event h2{{font-family:'Barlow Condensed',sans-serif;font-style:italic;font-weight:800;font-size:3rem;line-height:.95;margin:0 0 1rem;text-transform:uppercase}}.event h2 span{{color:{LIME}}}.event p{{color:#ccc;max-width:26rem}}.event img{{height:280px;width:auto;margin:20px auto;border-radius:18px}}
footer{{background:#111;color:#bbb;padding:3rem 0}}footer .wrap{{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;font-size:.85rem}}footer h4{{color:{LIME};font-family:'Barlow Condensed',sans-serif;font-style:italic;font-size:1.4rem;margin:0 0 .6rem;text-transform:uppercase}}footer a{{display:block;color:#bbb;text-decoration:none;margin:.3rem 0}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav a:not(.b2b){{display:none}}.promo,.empty,.offer,.event,footer .wrap{{grid-template-columns:1fr}}}}
"""
    body = f"""
<header class="nav"><a class="logo" href="#"><img src="{LOGO_W}" alt="Jolt"></a><nav><a href="#how">How to rent</a><a href="/areas/">Locations</a><a href="/stations/">Stations</a><a class="b2b" href="{FORM}">For venues</a></nav></header>
<section class="hero"><div><h1>Jolt, the power bank<br><span>for your night out</span></h1><a class="bt bt-g" href="#how">How it works</a> <a class="bt bt-k" href="{FORM}">For venues</a></div></section>
<div class="promo"><div><h2>Jolt is now in<br>4,000+ venues</h2><a class="bt bt-g" data-app href="#">Find one near you →</a></div><img class="nb" src="{st_img('countertop-8-black', 'angle', False)}" alt=""></div>
<div class="empty" id="how"><div><h2>Empty battery?<br>Rent a Jolt!</h2><p>Find Jolt power banks at thousands of venues across Ireland and the UK. Rent, charge and return, wherever you are.</p><a class="bt bt-g" data-app href="#">Find the nearest station</a></div><div class="m"><img src="/assets/app/map-dublin.webp" alt="Jolt stations in Dublin"></div></div>
<div class="partners">{"".join(f'<div class="lg"><img src="/assets/venues/{n}.webp" alt=""></div>' for n in VENUE_LOGOS[:8])}</div>
<div class="offer"><div class="im"><img src="{st_img('countertop-12', 'angle', False)}" alt=""></div><div><h2>Want to offer Jolt power banks?</h2><p>A free Jolt station gives your guests a reason to stay longer, and your venue a share of every rental. We install it, stock it and look after it.</p><a class="bt bt-k" href="{FORM}">Get a free station</a><small>Not sure which station fits? <a href="/stations/">See all seven</a>.</small></div></div>
<div class="event"><div><h2>Running a gig<br>or <span>festival?</span></h2><p>High-capacity Jolt stations keep a full room charged all night.</p><a class="bt bt-g" href="{FORM}">Talk to us →</a></div><img class="nb" src="{st_img('tower-48', 'angle', False)}" alt=""></div>
<footer><div class="wrap"><div><h4>Service</h4><a href="#how">How to rent</a><a href="/areas/">Locations</a><a href="/stations/">Stations</a></div><div><h4>Venues</h4><a href="{FORM}">Get a free station</a><a href="/customers/">Customers</a></div><div><img src="{LOGO_W}" alt="Jolt"><p>Ireland &amp; the UK</p></div></div></footer>"""
    return page("night-out", "Night-out energy", ["barlow-condensed"], css, body)


# ---------------------------------------------------------------- 7. Dark cinematic (ChargeSPOT layout)
def ex_city_lights(S):
    css = f"""
body{{font-family:Poppins,sans-serif;color:#fff;background:#07090a}}
.nav{{position:absolute;top:auto;left:0;right:0;z-index:50}}.nav .wrap{{display:flex;align-items:center;height:76px;gap:2rem}}.nav img{{height:26px}}.nav nav{{margin-left:auto;display:flex;gap:1.6rem;font-size:.85rem}}.nav nav a{{text-decoration:none;color:#e5e5e5}}
.nav .pt{{border:1px solid {LIME};color:{LIME};border-radius:30px;padding:.5rem 1rem;font-size:.85rem;text-decoration:none}}
.hero{{position:relative;min-height:760px;background:#07090a;overflow:hidden}}
.hero .bg{{position:absolute;inset:0;background:url(/assets/app/map-dublin-area.webp) center/cover;filter:grayscale(1) brightness(.35) contrast(1.4)}}
.hero .trails{{position:absolute;inset:0;background:repeating-linear-gradient(115deg,transparent 0 38px,rgba(158,242,48,.07) 40px 41px),radial-gradient(ellipse at 30% 110%,rgba(158,242,48,.35),transparent 50%)}}
.hero .box{{position:absolute;right:6vw;top:140px;width:min(400px,86vw)}}.hero .box u{{text-decoration-color:{LIME};text-underline-offset:6px;font-size:1.05rem}}.hero .box p{{color:#ddd}}.hero .box b{{display:block;font-size:1.05rem}}
.bt{{display:inline-block;border-radius:30px;padding:.75rem 1.3rem;font-size:.85rem;font-weight:600;text-decoration:none;margin:.3rem .3rem 0 0}}.bt-l{{background:{LIME};color:#07090a}}.bt-o{{border:1px solid #fff;color:#fff}}
.hero h1{{position:absolute;left:4vw;bottom:40px;margin:0;font-size:clamp(3.4rem,9vw,8rem);line-height:.95;font-weight:600}}
.how{{background:#fff;color:#07090a;padding:6rem 0}}.how .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:center}}.lab{{font-size:.75rem;letter-spacing:.2em;color:{GREEN};font-weight:600}}.how h2{{font-size:3rem;margin:.4rem 0 1rem}}
.how ol{{padding:0;list-style:none;counter-reset:s}}.how li{{counter-increment:s;padding:1rem 0 1rem 3.2rem;position:relative;border-bottom:1px solid #eee;font-weight:600}}.how li:before{{content:counter(s);position:absolute;left:0;top:.8rem;width:2.2rem;height:2.2rem;border-radius:50%;background:#07090a;color:{LIME};display:grid;place-items:center}}
.how .im{{border-radius:24px;background:#f2f5ef;display:flex;align-items:center;justify-content:center;height:460px}}.how .im img{{height:420px;width:auto}}
.scale{{padding:6rem 0}}.scale .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:4rem}}.scale h2{{font-size:2.8rem;margin:.4rem 0 1rem}}.scale p{{color:#bbb}}.big{{display:grid;gap:1.4rem}}.big b{{font-size:3.2rem;color:{LIME};font-weight:600;display:block;line-height:1}}.big span{{color:#999;font-size:.85rem}}
.partners{{padding:3rem 0;border-top:1px solid #1b1f1d;border-bottom:1px solid #1b1f1d}}.partners .lab{{display:block;text-align:center;margin-bottom:1.6rem}}.pl{{display:flex;gap:1rem;overflow:hidden}}.pl .lg{{flex:none;background:#fff;border-radius:12px;width:130px;height:70px;display:grid;place-items:center;padding:8px}}.pl .lg img{{max-height:50px;object-fit:contain}}
.venues{{padding:6rem 0}}.venues .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start}}.venues h2{{font-size:2.8rem;margin:.4rem 0 1rem}}.venues p{{color:#bbb}}.vl{{display:grid;grid-template-columns:1fr 1fr;gap:.7rem}}.vl div{{border:1px solid #232825;border-radius:14px;padding:1.2rem;font-weight:600}}.vl div:before{{content:"●";color:{LIME};margin-right:.6rem}}
.one{{background:linear-gradient(180deg,#07090a,#0d1a10);padding:6rem 0;text-align:center}}.one h2{{font-size:3rem;margin:0}}.one p{{color:#bbb}}.tabs3{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:2.4rem}}.tabs3 div{{border-radius:20px;background:#121614;padding:2rem;text-align:left;border:1px solid #1e2420}}.tabs3 h3{{margin:0 0 .5rem;color:{LIME}}}.tabs3 p{{margin:0;font-size:.9rem}}
.grid10{{padding:6rem 0}}.grid10 h2{{font-size:2.4rem;margin:.4rem 0 2rem}}.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem}}.g div{{background:#101412;border-radius:14px;padding:1.4rem;font-weight:600}}
.app{{background:{LIME};color:#07090a;padding:4rem 0}}.app .wrap{{display:flex;justify-content:space-between;align-items:center;gap:2rem;flex-wrap:wrap}}.app h2{{font-size:2.4rem;margin:0}}.app .bt{{background:#07090a;color:#fff}}
footer{{padding:4rem 0;color:#999;font-size:.85rem}}footer .wrap{{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;align-items:center}}footer img{{height:24px}}
@media(max-width:860px){{.nav nav{{display:none}}.how .wrap,.scale .wrap,.venues .wrap{{grid-template-columns:1fr}}.tabs3,.g{{grid-template-columns:1fr}}.hero .box{{left:4vw;right:auto;top:110px}}}}
"""
    vt = ["Bars, clubs & nightlife", "Restaurants & cafés", "Festivals & events", "Stadiums & sport", "Shopping centres & retail", "Universities & campuses", "Hotels", "Gyms & leisure", "Hospitals"]
    body = f"""
<header class="nav"><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><nav><a href="#how">How it works</a><a href="/stations/">Stations</a><a href="/areas/">Locations</a><a href="/customers/">Customers</a></nav><a class="pt" href="{FORM}">For venues</a></div></header>
<section class="hero"><div class="bg"></div><div class="trails"></div><div class="box"><u>Phone charging stations for venues &amp; on-the-go charging</u><p>Stay powered, wherever you are. Rent a portable power bank and return it to any Jolt station.</p><b>4,000+ venues have used Jolt.</b><b>Ireland &amp; the UK.</b><b>Open 24/7.</b><br><a class="bt bt-l" data-app href="#">Find a power bank</a><a class="bt bt-o" href="{FORM}">Get a free station</a></div><h1>Stay charged.<br>Stay out.</h1></section>
<section class="how" id="how"><div class="wrap"><div><span class="lab">HOW IT WORKS</span><h2>Tap. Grab. Return.</h2><p>Charge your phone while you're out, then return the power bank to any Jolt station.</p><ol><li>Tap to pay with your phone or card</li><li>Take a power bank and charge on the go</li><li>Return it to any Jolt station</li></ol><a class="bt bt-l" data-app href="#" style="color:#07090a">Download the app</a></div><div class="im"><img src="{st_img('media-kiosk-48', 'angle', False)}" alt=""></div></div></section>
<section class="scale"><div class="wrap"><div><span class="lab">SCALE</span><h2>Where people go, Jolt is already there.</h2><p>From late nights to hospital waiting rooms, Jolt sits inside the places people spend time across Ireland and the UK.</p></div><div class="big"><div><b>4,000+</b><span>venues have used Jolt</span></div><div><b>7</b><span>station models, countertop to floor-standing</span></div><div><b>6000mAh</b><span>power banks with 3 cables built in</span></div></div></div></section>
<section class="partners"><span class="lab">OUR VENUE PARTNERS</span><div class="pl">{logos_html()}</div></section>
<section class="venues"><div class="wrap"><div><span class="lab">FOR VENUES</span><h2>Turn foot traffic into revenue</h2><p>A free Jolt station gives your customers convenience and gives your venue a share of every rental.</p><a class="bt bt-l" href="{FORM}">Order your free station</a></div><div class="vl"><div>Revenue share</div><div>Free installation</div><div>Guests stay longer</div><div>Nothing to manage</div><div>Kept stocked by Jolt</div><div>No lost stock</div></div></div></section>
<section class="one"><div class="wrap"><h2>Never get caught on 1%</h2><p>You don't think about it until you need it.</p><div class="tabs3"><div><h3>On a night out</h3><p>Grab a power bank at the bar and keep going.</p></div><div><h3>In hospital</h3><p>Stay in touch while you wait.</p></div><div><h3>At an event</h3><p>Big crowds, big stations.</p></div></div></div></section>
<section class="grid10"><div class="wrap"><span class="lab">WHERE YOU'LL FIND JOLT</span><h2>Stations for every venue</h2><div class="g">{"".join(f"<div>{v}</div>" for v in vt)}</div></div></section>
<section class="app"><div class="wrap"><h2>Ready to stay charged anywhere?</h2><div><a class="bt" href="https://apps.apple.com/ie/app/joltireland/id6471393616" target="_blank" rel="noopener">App Store</a><a class="bt" href="https://play.google.com/store/apps/details?id=com.joltireland.charge" target="_blank" rel="noopener">Google Play</a></div></div></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Keeping Ireland &amp; the UK connected</span></div></footer>"""
    return page("city-lights", "Dark cinematic", ["poppins"], css, body)


# ---------------------------------------------------------------- 8. Black & neon (voozaa layout)
def ex_neon_dark(S):
    css = f"""
body{{font-family:Afacad,sans-serif;color:#fff;background:#0a0a0a;font-size:1.05rem}}
.nav{{position:sticky;top:0;z-index:50;background:rgba(10,10,10,.92);backdrop-filter:blur(10px)}}.nav .wrap{{display:flex;align-items:center;height:64px;gap:2rem}}.nav img{{height:22px}}.nav nav{{display:flex;gap:1.4rem;font-size:.9rem;color:#ccc;margin-left:1rem}}.nav nav a{{text-decoration:none}}
.nav .cta{{margin-left:auto;background:{LIME};color:#0a0a0a;border-radius:8px;padding:.55rem 1rem;font-weight:700;font-size:.9rem;text-decoration:none}}
.c{{text-align:center}}.hl{{color:{LIME}}}
.hero{{padding:5rem 0 4rem}}.hero h1{{font-size:clamp(2.4rem,5vw,4rem);line-height:1.1;margin:0 auto 1rem;max-width:52rem;font-weight:700}}.hero p{{color:#bbb;max-width:36rem;margin:0 auto 2.4rem}}
.vid{{max-width:860px;margin:0 auto;border-radius:16px;overflow:hidden;background:#111;aspect-ratio:16/9;display:grid;grid-template-columns:1fr 1fr;align-items:center}}.vid img{{height:88%;width:auto;margin:auto;border-radius:12px}}.vid .m{{height:100%;background:url(/assets/app/map-dublin-hero.webp) center/cover}}
.btn{{display:inline-block;background:{LIME};color:#0a0a0a;border-radius:8px;padding:.85rem 1.4rem;font-weight:700;font-size:.85rem;letter-spacing:.06em;text-transform:uppercase;text-decoration:none;margin-top:2rem}}
.sec{{padding:5rem 0;border-top:1px solid #161616}}.sec h2{{font-size:2.4rem;margin:0 0 2.4rem;font-weight:700}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}}.card{{background:#141414;border:1px solid #232323;border-radius:14px;padding:1.8rem;text-align:left}}.card.on{{border-color:{LIME};background:#151a0c}}.card h3{{margin:0 0 1rem;font-size:1rem;color:{LIME}}}
.card ul{{list-style:none;padding:0;margin:0}}.card li{{padding:.45rem 0 .45rem 1.8rem;position:relative}}.card li:before{{content:"✓";position:absolute;left:0;width:20px;height:20px;border:1.5px solid {LIME};border-radius:50%;color:{LIME};font-size:.7rem;display:grid;place-items:center}}.card.no li:before{{content:"×";border-color:#666;color:#888}}
.card .foot{{margin-top:1rem;color:{LIME};font-weight:700}}
.tiles{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}}.tile{{background:#141414;border:1px solid #232323;border-radius:12px;padding:1.4rem;text-align:left;display:flex;gap:.9rem;align-items:center}}.tile i{{flex:none;width:34px;height:34px;border-radius:50%;border:2px solid {LIME};display:grid;place-items:center;font-style:normal;color:{LIME}}}
.box{{max-width:860px;margin:2.4rem auto 0;border:1px solid {LIME};border-radius:14px;padding:1.6rem;color:#ccc}}.box b{{color:{LIME};display:block;margin-top:.6rem}}
.icons{{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem}}.icons div{{background:#141414;border:1px solid #232323;border-radius:12px;padding:1.4rem 1rem;font-size:.9rem;color:#ccc}}.icons span{{display:block;font-size:1.6rem;color:{LIME};margin-bottom:.6rem}}
.st{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}.st a{{background:#141414;border:1px solid #232323;border-radius:14px;padding:1rem;text-decoration:none;text-align:left}}.st .im{{background:#fff;border-radius:10px;height:180px;display:flex;align-items:center;justify-content:center}}.st img{{height:165px;width:auto}}.st h3{{margin:.8rem 0 .2rem;font-size:1.05rem}}.st small{{color:{LIME}}}
footer{{padding:3rem 0;color:#888;font-size:.9rem;border-top:1px solid #161616}}footer .wrap{{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap}}footer img{{height:22px}}
@media(max-width:860px){{.nav nav{{display:none}}.two,.tiles,.icons,.st{{grid-template-columns:1fr 1fr}}.vid{{grid-template-columns:1fr}}.vid .m{{display:none}}}}
"""
    stations = "".join(f'<a href="/stations/{x["slug"]}/"><div class="im"><img src="{st_img(x["slug"])}" alt=""></div><h3>{x["name"]}{" · " + x["finish"] if x["slug"].startswith("countertop-8") else ""}</h3><small>{cap(x)}</small></a>' for x in S)
    body = f"""
<header class="nav"><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><nav><a href="/stations/">Stations</a><a href="/areas/">Locations</a><a href="/customers/">Customers</a><a href="#how">How it works</a></nav><a class="cta" data-app href="#">Download the app</a></div></header>
<section class="hero c"><div class="wrap"><h1>Add a free charging station to your venue and earn from <span class="hl">every rental</span></h1><p>No cost, no staff time, no stock to manage. Jolt installs it, keeps it stocked and shares the income with you.</p><div class="vid"><img class="nb" src="{st_img('countertop-12', 'front', False)}" alt="Jolt Countertop 12"><div class="m"></div></div><a class="btn" href="{FORM}">Get a free station</a></div></section>
<section class="sec c" id="how"><div class="wrap"><h2>How does the <span class="hl">system work</span></h2><div class="two"><div class="card"><h3>For your guests:</h3><ul><li>Tap a card or phone on the station</li><li>Charge their phone on the go</li><li>Return the power bank to any Jolt station</li></ul></div><div class="card on"><h3>For your venue:</h3><ul><li>Free station and installation</li><li>A share of every rental</li><li>No staff time needed</li><li>No stock to manage</li><li>No cost for unreturned banks</li></ul><div class="foot">Jolt does the work for you.</div></div></div></div></section>
<section class="sec c"><div class="wrap"><h2>Is Jolt <span class="hl">right</span> for your venue?</h2><div class="two"><div class="card on"><h3>Jolt is ideal if you…</h3><ul><li>want a new revenue stream with no setup cost</li><li>want guests to stay longer</li><li>run a pub, hotel, club, gym or hospital</li><li>have a small space and a power socket</li></ul></div><div class="card no"><h3>Jolt may not suit you if you…</h3><ul><li>have no space near a power socket</li><li>are outside Ireland and the UK (join the EU priority list instead)</li></ul></div></div></div></section>
<section class="sec c"><div class="wrap"><h2>Why <span class="hl">now</span>?</h2><div class="tiles"><div class="tile"><i>1</i>Phones run flat on every night out</div><div class="tile"><i>2</i>4,000+ venues already use Jolt</div><div class="tile"><i>3</i>Your guests already have the app nearby</div></div><div class="box">Every rental at your station earns your venue a share of the income.<b>And it costs you nothing to start.</b></div></div></section>
<section class="sec c"><div class="wrap"><h2>What makes Jolt <span class="hl">different</span>?</h2><div class="icons"><div><span>⌂</span>Ireland &amp; UK network</div><div><span>⚡</span>6000mAh power banks</div><div><span>⇄</span>Return to any station</div><div><span>◎</span>3 cables built in</div><div><span>✓</span>Free install &amp; maintenance</div></div></div></section>
<section class="sec c"><div class="wrap"><h2>Pick your <span class="hl">station</span></h2><div class="st">{stations}</div><a class="btn" href="{FORM}">Get a free station</a></div></section>
<footer><div class="wrap"><img src="{LOGO_W}" alt="Jolt"><span>Ireland &amp; the UK</span></div></footer>"""
    return page("neon-dark", "Black & neon", ["afacad"], css, body)


BUILDERS = {"blue-wave": ex_blue_wave, "bold-colour": ex_bold_colour, "clean-navy": ex_clean_navy, "pill-play": ex_pill_play,
            "fresh-green": ex_fresh_green, "night-out": ex_night_out, "city-lights": ex_city_lights, "neon-dark": ex_neon_dark}


def build(write, stations, ios, android):
    for slug, _, _ in EXAMPLES:
        write(f"examples/{slug}/index.html", BUILDERS[slug](stations).replace("{IOS}", ios).replace("{AND}", android))
    links = "".join(f'<a href="/examples/{s}/"><b>{html.escape(l)}</b><span>Layout based on {r}</span></a>' for s, l, r in EXAMPLES)
    write("examples/index.html", page("", "All examples", [], """body{font-family:Inter,sans-serif;background:#060806;color:#fff}.wrap{padding:4rem 0}h1{font-size:2.4rem}
.l{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}.l a{display:block;border:1px solid #1f261f;border-radius:14px;padding:1.4rem;text-decoration:none;background:#0c100c}.l a:hover{border-color:#9ef230}.l b{display:block;font-size:1.1rem}.l span{color:#8a948a;font-size:.85rem}""",
                                     f'<div class="wrap"><img src="{LOGO_W}" alt="Jolt" style="height:30px"><h1>Website examples</h1><div class="l">{links}</div></div>'))


def nav_dropdown():
    """The 'Examples' dropdown for the main site's top bar."""
    items = "".join(f'<a href="/examples/{s}/">{html.escape(l)}</a>' for s, l, _ in EXAMPLES)
    return f'<details class="exdd"><summary>Examples</summary><div class="exdd-menu">{items}<a href="/examples/" class="all">See all examples</a></div></details>'


def mobile_links():
    return '<span class="mm-label">Website examples</span>' + "".join(f'<a class="mm-ex" href="/examples/{s}/">{html.escape(l)}</a>' for s, l, _ in EXAMPLES)
