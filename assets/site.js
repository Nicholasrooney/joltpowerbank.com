/* Lead form handler.
   Set FORM_ENDPOINT to a form backend (e.g. https://formspree.io/f/xxxx) to receive leads by email.
   Until it's set, submissions open WhatsApp with the details pre-filled so no lead is lost. */
const FORM_ENDPOINT = "";
const WHATSAPP = "353870365888";

/* ---------- Setup card: market -> venues -> weekly customers -> contact ----------
   Every lead is tagged with market (IE / UK / EU / INTL) and lead_status:
     IE, UK -> "active"       (sales lead for that market)
     EU     -> "eu_priority"  (priority onboarding list for EU expansion)
     INTL   -> "waitlist"                                                     */
(function () {
  const card = document.getElementById("setup-card");
  if (!card) return;
  const $ = s => card.querySelector(s);
  const slider = $("#setup-slider"), bars = card.querySelectorAll(".setup-meter i");
  const marketPills = card.querySelectorAll("#setup-market .setup-pill"), sitePills = card.querySelectorAll("#setup-sites .setup-pill");
  const country = $("#setup-country"), submit = $("#setup-submit");
  const STOPS = [50, 100, 250, 500, 1000, 2500, 5000];
  const MARKET = {
    IE:   { status: "active",      cur: "€", button: "Get my free station",
            reassure: "We'll call you within one working day · free install · no spam",
            done: ["Got it. Thanks.", "Someone from Jolt Ireland will be in touch within one working day."] },
    UK:   { status: "active",      cur: "£", button: "Get my free station",
            reassure: "We'll call you within one working day · free install · no spam",
            done: ["Got it. Thanks.", "Someone from the Jolt UK team will be in touch within one working day."] },
    EU:   { status: "eu_priority", cur: "€", button: "Join the EU priority list",
            reassure: "No cost · no commitment · we'll only contact you about onboarding",
            done: ["Thank you so much.", "We'll be expanding into the EU shortly. When we do, you're on the priority list for onboarding."] },
    INTL: { status: "waitlist",    cur: "",  button: "Join the waitlist",
            reassure: "No cost · no commitment · we'll only contact you when we launch near you",
            done: ["Great, you're on the waitlist.", "We'll reach out as soon as it's time for us to service your area."] },
  };
  let market = card.dataset.preset || "", sites = "1";
  if (!market) {                                   // main page: best guess from the browser language, visitor can change it
    const l = (navigator.language || "").toLowerCase();
    market = l === "en-gb" ? "UK" : l === "en-ie" || l === "ga" ? "IE" : "IE";
  }

  const valueAt = pos => {
    const seg = Math.min(5, Math.floor(pos / 100)), t = (pos - seg * 100) / 100;
    const v = STOPS[seg] * Math.pow(STOPS[seg + 1] / STOPS[seg], t);
    return v < 100 ? Math.round(v / 10) * 10 : v < 1000 ? Math.round(v / 50) * 50 : Math.round(v / 250) * 250;
  };
  const fmt = v => (v >= 5000 ? "5,000+" : v.toLocaleString("en-IE"));
  // weekly customers per venue -> station from the range (slugs match /stations/<slug>/)
  const station = v => v < 250  ? ["Countertop 8",  "8 power banks · sits beside the till", "countertop-8-black"]
                    : v < 1000 ? ["Countertop 12", "12 power banks on a small countertop footprint", "countertop-12"]
                    : v < 3000 ? ["Slim Kiosk 24", "24 power banks · floor-standing with tap-to-pay", "slim-kiosk-24"]
                    :            ["Tower 48",      "48 power banks for the busiest venues", "tower-48"];
  const NAMES = { "countertop-8-white": "Countertop 8 (white)", "countertop-8-black": "Countertop 8 (black)", "countertop-12": "Countertop 12",
                  "slim-kiosk-24": "Slim Kiosk 24", "secure-locker-24": "Secure Locker 24", "media-kiosk-48": "Media Kiosk 48", "tower-48": "Tower 48" };
  const wanted = new URLSearchParams(location.search).get("station");
  if (wanted && NAMES[wanted]) {
    $("#setup-h-station").value = NAMES[wanted];
    const chip = $("#setup-interest"); chip.hidden = false;
    chip.innerHTML = `Station you're interested in: <b>${NAMES[wanted]}</b> <button type="button" aria-label="Remove">×</button>`;
    chip.querySelector("button").onclick = () => { chip.hidden = true; $("#setup-h-station").value = ""; };
  }

  function select(pills, el) {
    pills.forEach(x => { x.classList.remove("is-active"); x.setAttribute("aria-checked", "false"); });
    el.classList.add("is-active"); el.setAttribute("aria-checked", "true");
  }

  function update() {
    const M = MARKET[market], pos = +slider.value, v = valueAt(pos), multi = sites !== "1";
    slider.style.setProperty("--p", (pos / 6) + "%");
    $("#setup-count").textContent = fmt(v);
    $("#setup-q3").textContent = multi ? "How many customers a week, per venue?" : "How many customers a week?";
    $("#setup-per").textContent = multi ? " per venue" : "";
    const [st, desc, slug] = station(v);
    let name, inc;
    if (sites === "1") { name = st; inc = desc + " · installed free · you earn a revenue share"; }
    else if (sites === "2") { name = "2 × " + st; inc = "A station in each venue · installed free · revenue share on both"; }
    else if (sites === "3-10") { name = st + " in every venue"; inc = "We plan placement across all your sites · installed free · revenue share on each"; }
    else { name = "Group rollout"; inc = "A rollout plan for your whole group, venue by venue · installed free · revenue share across the group"; }

    const result = $("#setup-result");
    result.classList.toggle("is-list", market === "EU" || market === "INTL");
    if (market === "EU") {
      $("#setup-label").textContent = "EU priority list";
      $("#setup-name").textContent = "We're expanding into the EU shortly";
      $("#setup-price").innerHTML = "Register now for <strong>priority onboarding</strong>";
      $("#setup-inc").textContent = "When we launch in your country you'll be first in line for a " + name.toLowerCase() + ".";
      $("#setup-q4").textContent = "Where should we reach you?";
    } else if (market === "INTL") {
      $("#setup-label").textContent = "Waitlist";
      $("#setup-name").textContent = "Not in your area yet";
      $("#setup-price").innerHTML = "Join the <strong>waitlist</strong>";
      $("#setup-inc").textContent = "We'll reach out as soon as we can service your area.";
      $("#setup-q4").textContent = "Where should we reach you?";
    } else {
      $("#setup-label").textContent = "Recommended setup";
      $("#setup-name").textContent = name;
      $("#setup-price").innerHTML = `Cost to you: <strong>${M.cur}0</strong>`;
      $("#setup-inc").textContent = inc;
      $("#setup-q4").textContent = "Where should we send your setup?";
    }
    const link = $("#setup-link"); link.href = `/stations/${slug}/`; link.hidden = market === "EU" || market === "INTL";
    const needCountry = market === "EU" || market === "INTL";
    country.hidden = !needCountry; country.required = needCountry;
    submit.textContent = M.button;
    $("#setup-reassure").textContent = M.reassure;
    const lit = Math.max(1, Math.round((pos / 600) * bars.length));
    bars.forEach((b, i) => b.classList.toggle("on", i < lit));
    $("#setup-h-market").value = market; $("#setup-h-status").value = M.status;
    $("#setup-h-venues").value = sites; $("#setup-h-customers").value = v >= 5000 ? "5000+" : v; $("#setup-h-rec").value = name;
  }

  marketPills.forEach(p => {
    if (p.dataset.market === market) select(marketPills, p);
    p.addEventListener("click", () => { select(marketPills, p); market = p.dataset.market; update(); });
  });
  sitePills.forEach(p => p.addEventListener("click", () => { select(sitePills, p); sites = p.dataset.sites; update(); }));
  slider.addEventListener("input", update);
  update();

  const form = $("#setup-form"), msg = form.querySelector(".form-msg");
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (form._gotcha.value) return;
    let ok = true;
    form.querySelectorAll("[required]").forEach(f => {
      const v = f.value.trim();
      const bad = !v || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(v)) || (f.type === "tel" && v.replace(/\D/g, "").length < 7);
      f.classList.toggle("invalid", bad); if (bad) ok = false;
    });
    if (!ok) { msg.textContent = "Please fill in every field so we can reach you."; msg.className = "form-msg err"; return; }
    msg.textContent = "";
    const data = Object.fromEntries(new FormData(form)); delete data._gotcha;
    if (!country.required) delete data.country;
    data.page = location.pathname;
    if (window.gtag) gtag("event", "generate_lead", { form_id: "setup-hero", market: data.market, lead_status: data.lead_status, venues: data.venues });
    submit.disabled = true; submit.textContent = "Sending…";
    let sent = false;
    if (FORM_ENDPOINT) {
      try {
        const r = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
        sent = r.ok;
      } catch (_) {}
    }
    if (!sent) {
      const tag = { active: `${data.market} LEAD`, eu_priority: "EU PRIORITY LIST", waitlist: "INTERNATIONAL WAITLIST" }[data.lead_status];
      const text = `[${tag}]\nBusiness: ${data.business}\nName: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone}` +
        (data.country ? `\nCountry: ${data.country}` : "") +
        (data.station_interest ? `\nInterested in: ${data.station_interest}` : "") + `\nVenues: ${data.venues}\nCustomers/week: ${data.weekly_customers}\nRecommended: ${data.recommended}`;
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, "_blank");
    }
    const [h, p] = MARKET[market].done;
    $(".setup-capture").innerHTML = `<div class="setup-success"><b>${h}</b><p class="muted">${p}</p></div>`;
  });
})();

/* ---------- Station page gallery ---------- */
(function () {
  const main = document.getElementById("st-main");
  if (!main) return;
  const thumbs = document.querySelectorAll(".st-thumb");
  thumbs.forEach(t => t.addEventListener("click", () => {
    thumbs.forEach(x => x.classList.remove("is-active")); t.classList.add("is-active");
    main.src = t.dataset.src; main.alt = t.dataset.alt;
  }));
})();

/* ---------- Brand showcase: 5 preview designs (pick one, then delete the others + the switcher) ---------- */
(function () {
  const dataEl = document.getElementById("venue-data");
  if (!dataEl) return;
  const V = JSON.parse(dataEl.textContent);
  const withLogo = V.filter(v => v.logo), noLogo = V.filter(v => !v.logo);
  // interleave: roughly 1 name tile per logo tile so every venue appears, logos lead
  const MIX = []; { let i = 0, j = 0; while (i < withLogo.length || j < noLogo.length) { if (i < withLogo.length) MIX.push(withLogo[i++]); if (j < noLogo.length) MIX.push(noLogo[j++]); if (j < noLogo.length && i >= withLogo.length) MIX.push(noLogo[j++]); } }
  const SHORT = { "Hospitals & healthcare": "Hospital", "Hotels": "Hotel", "Nightclubs & late bars": "Late bar", "Pubs & bars": "Pub", "Restaurants & cafés": "Café & dining", "Retail, transport & campus": "Retail & transport", "Venues, sport & attractions": "Venue" };
  const esc = s => s.replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const tile = (v, cls = "") => v.logo
    ? `<div class="bt bt-logo ${cls}" title="${esc(v.name)}"><img src="/assets/venues/${v.logo}" alt="${esc(v.name)}" loading="lazy" decoding="async"></div>`
    : `<div class="bt bt-name ${cls}"><span>${esc(v.name)}</span><i>${SHORT[v.category] || ""}</i></div>`;
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const makeDesigns = stage => ({
    /* 1. Drum: the runway's flow, curved over a big cylinder. Rows come over the crest and roll down toward you.
          Same 4 columns, tile size and surface speed as the runway; rows are refilled while they're out of sight. */
    1() {
      const FACES = 20, PER = 4, STEP = 360 / FACES;
      const W = stage.clientWidth, H = stage.clientHeight;
      const DW = W * 1.16, colW = (DW - 3 * 10) / 4, faceH = colW * 5 / 9 + 10, PUSH = 170;   // wider drum, pushed back for depth           // tile 9:5 + 10px gap, like the runway
      const r = faceH / (2 * Math.tan(Math.PI / FACES));
      stage.innerHTML = `<div class="drum-wrap"><div class="drum" style="height:${faceH}px;width:${DW}px;left:${(W - DW) / 2}px;top:${H - faceH * 1.05}px"></div></div>`;
      const drum = stage.querySelector(".drum");
      let next = 0; const take = () => { const out = []; for (let k = 0; k < PER; k++) out.push(MIX[next++ % MIX.length]); return out; };
      const faces = [];
      for (let i = 0; i < FACES; i++) {
        const f = document.createElement("div"); f.className = "drum-face";
        f.style.transform = `rotateX(${i * STEP}deg) translateZ(${r}px)`; f.innerHTML = take().map(v => tile(v)).join("");
        drum.appendChild(f); faces.push({ el: f, base: i * STEP, back: false });
      }
      const degPerMs = (50 / r) * (180 / Math.PI) / 1000;                      // 50px/s along the surface = runway speed
      let angle = 0, last = performance.now(), raf;
      const loop = t => {
        const dt = Math.min(50, t - last); last = t; if (!reduce) angle -= dt * degPerMs;
        drum.style.transform = `translateZ(${-r - PUSH}px) rotateX(${angle}deg)`;
        faces.forEach(f => {
          const a = ((f.base + angle) % 360 + 360) % 360;
          const isBack = a > 110 && a < 250;
          if (isBack && !f.back) f.el.innerHTML = take().map(v => tile(v)).join("");
          f.back = isBack;
        });
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      return () => cancelAnimationFrame(raf);
    },

    /* 2. Flip wall: a grid of tiles; one flips to a new venue every ~0.7s */
    2() {
      const COLS = 4, ROWS = 5, N = COLS * ROWS; let next = 0;
      const pick = () => MIX[next++ % MIX.length];
      stage.innerHTML = `<div class="flipwall" style="--cols:${COLS}">${Array.from({ length: N }, () => `<div class="fw-cell"><div class="fw-card"><div class="fw-face">${tile(pick())}</div><div class="fw-face fw-back"></div></div></div>`).join("")}</div>`;
      const cells = [...stage.querySelectorAll(".fw-card")]; let lastIdx = -1;
      const id = setInterval(() => {
        if (reduce) return;
        let i; do { i = Math.floor(Math.random() * N); } while (i === lastIdx); lastIdx = i;
        const c = cells[i], flipped = c.classList.contains("flipped");
        c.querySelector(flipped ? ".fw-face:not(.fw-back)" : ".fw-back").innerHTML = tile(pick());
        c.classList.toggle("flipped");
      }, 700);
      return () => clearInterval(id);
    },

    /* 3. Runway: columns of venues streaming toward you on a tilted plane */
    3() {
      const COLS = 4, per = Math.ceil(MIX.length / COLS);
      const cols = Array.from({ length: COLS }, (_, c) => MIX.slice(c * per, (c + 1) * per));
      stage.innerHTML = `<div class="runway"><div class="runway-plane">${cols.map((list, c) => {
        const h = list.map(v => tile(v)).join("");
        return `<div class="rw-col"><div class="rw-track" style="animation-duration:${90 + c * 12}s;animation-delay:-${c * 9}s">${h}${h}</div></div>`;
      }).join("")}</div></div>`;
      return () => {};
    },

    /* 4. Categories: counts per category; auto-cycles, click to pick */
    4() {
      const cats = [...new Set(V.map(v => v.category))].sort((a, b) => V.filter(v => v.category === b).length - V.filter(v => v.category === a).length);
      const groups = [["All venues", MIX], ...cats.map(c => [c, V.filter(v => v.category === c).sort((a, b) => (b.logo ? 1 : 0) - (a.logo ? 1 : 0))])];
      stage.innerHTML = `<div class="cats"><div class="cat-chips">${groups.map(([c, l], i) => `<button type="button" class="cat-chip" data-i="${i}">${c} <b>${l.length}</b><i></i></button>`).join("")}</div><div class="cat-grid"></div></div>`;
      const grid = stage.querySelector(".cat-grid"), chips = [...stage.querySelectorAll(".cat-chip")];
      let cur = 0, page = 0, timer, auto = true;
      const SHOW = 12;   // 4 x 3
      const render = () => {
        const list = groups[cur][1], start = (page * SHOW) % Math.max(1, list.length);
        const items = list.length <= SHOW ? list : Array.from({ length: SHOW }, (_, k) => list[(start + k) % list.length]);
        grid.innerHTML = items.map((v, k) => tile(v, "cat-in").replace('class="bt', `style="animation-delay:${k * 40}ms" class="bt`)).join("");
        chips.forEach((c, i) => c.classList.toggle("is-active", i === cur));
      };
      const go = i => { cur = i; page = 0; render(); };
      chips.forEach((c, i) => c.addEventListener("click", () => { auto = false; clearInterval(timer); go(i); }));
      render();
      timer = setInterval(() => {
        if (!auto || reduce) return;
        const list = groups[cur][1];
        if (list.length > SHOW && page < 2) { page++; render(); } else go((cur + 1) % groups.length);
      }, 3500);
      return () => clearInterval(timer);
    },

    /* 5. Orbit: venues on tilted elliptical orbits around a Jolt station (front = bigger + brighter) */
    5() {
      const W = stage.clientWidth, H = stage.clientHeight, cx = W / 2, cy = H / 2;
      const rings = [{ n: 6, rx: W * 0.25, ry: H * 0.13, sp: 0.00016 }, { n: 9, rx: W * 0.36, ry: H * 0.24, sp: -0.00011 }, { n: 12, rx: W * 0.46, ry: H * 0.38, sp: 0.00008 }];
      let next = 0; const pool = [...withLogo, ...noLogo];
      const pick = () => pool[next++ % pool.length];
      stage.innerHTML = `<div class="orbit"><div class="orbit-core"><img src="/assets/stations/countertop-12-angle-sm.webp" alt="Jolt station"></div></div>`;
      const orbit = stage.querySelector(".orbit"), items = [];
      rings.forEach((g, ri) => {
        const ring = document.createElement("div"); ring.className = "orbit-path";
        ring.style.cssText = `width:${g.rx * 2}px;height:${g.ry * 2}px;left:${cx - g.rx}px;top:${cy - g.ry}px`; orbit.appendChild(ring);
        for (let k = 0; k < g.n; k++) {
          const el = document.createElement("div"); el.className = "orbit-up"; el.innerHTML = tile(pick());
          orbit.appendChild(el); items.push({ el, g, a: (Math.PI * 2 / g.n) * k + ri * 0.4 });
        }
      });
      let last = performance.now(), raf;
      const loop = t => {
        const dt = Math.min(50, t - last); last = t;
        items.forEach(it => {
          if (!reduce) it.a += it.g.sp * dt;
          const sn = Math.sin(it.a), depth = (sn + 1) / 2;                       // 0 = back (top), 1 = front (bottom)
          const x = cx + Math.cos(it.a) * it.g.rx, y = cy + sn * it.g.ry, sc = 0.62 + depth * 0.5;
          it.el.style.transform = `translate(${x - 40}px, ${y - 22}px) scale(${sc})`;
          it.el.style.zIndex = sn > 0 ? 3 + Math.round(depth * 10) : 1;
          it.el.style.opacity = 0.35 + depth * 0.65;
        });
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      const id = setInterval(() => {
        if (reduce) return;
        const back = items.filter(i => Math.sin(i.a) < -0.3); if (!back.length) return;   // swap only tiles at the back
        const it = back[Math.floor(Math.random() * back.length)]; it.el.innerHTML = tile(pick());
      }, 600);
      return () => { cancelAnimationFrame(raf); clearInterval(id); };
    },
  });

  /* each .brands block gets its own stage; animations only run while the block is on screen */
  function Showcase(root) {
    const stage = root.querySelector(".brand-stage"), designs = makeDesigns(stage);
    let cleanup = () => {}, current = null, visible = false;
    const run = () => { cleanup(); cleanup = designs[current]() || (() => {}); };
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting && !visible) { visible = true; run(); }
      else if (!e.isIntersecting && visible) { visible = false; cleanup(); cleanup = () => {}; }
    }), { rootMargin: "100px" });
    io.observe(root);
    return {
      stage,
      set(d) { current = designs[d] ? String(d) : "1"; root.dataset.design = current; if (visible) run(); },
    };
  }

  // fixed-design blocks (customers page)
  document.querySelectorAll(".brands[data-fixed]").forEach(r => Showcase(r).set(r.dataset.design));

  // home page block + top-bar switcher
  const homeRoot = document.getElementById("brands");
  if (!homeRoot) return;
  const home = Showcase(homeRoot), stage = home.stage;
  function show(d) {
    d = ["1","2","3","4","5"].includes(String(d)) ? String(d) : "1";
    home.set(d);
    document.querySelectorAll("#design-switch button").forEach(b => b.classList.toggle("is-active", b.dataset.d === d));
    try { localStorage.setItem("jolt-design", d); } catch (_) {}
  }
  let start = new URLSearchParams(location.search).get("design");
  if (!start) { try { start = localStorage.getItem("jolt-design"); } catch (_) {} }
  show(start || "1");
  document.querySelectorAll("#design-switch button").forEach(b => b.addEventListener("click", () => {
    show(b.dataset.d);
    const r = stage.getBoundingClientRect();                       // bring the showcase into view if it's off screen
    if (r.top < 120 || r.bottom > innerHeight) stage.scrollIntoView({ behavior: "smooth", block: "center" });
    const u = new URL(location.href); u.searchParams.set("design", b.dataset.d); history.replaceState(null, "", u);
  }));
})();
