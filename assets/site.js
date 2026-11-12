/* ---------- Tracking: our own cookie-free counter (track.php) for every visitor, plus Google (only if cookies accepted) ---------- */
(function () {
  const q = new URLSearchParams(location.search);
  const base = {
    p: location.pathname, ref: document.referrer || "",
    us: q.get("utm_source") || "", um: q.get("utm_medium") || "", uc: q.get("utm_campaign") || "",
    clid: q.get("gclid") ? "gclid" : q.get("fbclid") ? "fbclid" : "",
    tz: (Intl.DateTimeFormat().resolvedOptions().timeZone || "")
  };
  window.track = function (e, l, d, gaParams) {
    try {
      const fd = new FormData();
      Object.entries(Object.assign({}, base, { e, l: l || "", d: d || "" })).forEach(([k, v]) => fd.append(k, v));
      if (!(navigator.sendBeacon && navigator.sendBeacon("/track.php", fd))) fetch("/track.php", { method: "POST", body: fd, keepalive: true }).catch(() => {});
    } catch (_) {}
    if (window.gtag && e !== "page_view") gtag("event", e, Object.assign({ event_label: l || "", detail: d || "" }, gaParams || {}));
  };
  track("page_view", document.title.slice(0, 100));

  // every click on a link or button
  document.addEventListener("click", ev => {
    const el = ev.target.closest("a, button, [role=radio]"); if (!el) return;
    const label = (el.dataset.track || el.getAttribute("aria-label") || el.innerText || el.title || "").replace(/\s+/g, " ").trim().slice(0, 80);
    const href = el.getAttribute("href") || "";
    const where = el.closest("header") ? "nav" : el.closest("footer") ? "footer" : el.closest("#setup-card") ? "form" : el.closest(".hero") ? "hero" : (el.closest("section[id]") || {}).id || "page";
    track("click", label, (href ? href.replace(/^https?:\/\/[^/]+/, "") : "button") + " @" + where);
    if (el.classList.contains("app-link")) {
      const ua = navigator.userAgent, plat = /Android/i.test(ua) ? "android" : /iPhone|iPad|iPod/i.test(ua) ? "ios" : "desktop";
      track("app_click", plat, (el.classList.contains("btn-find") ? "find-button" : el.classList.contains("hero-map") ? "hero-map" : el.classList.contains("area-map") ? "area-map" : where));
    }
    if (/wa\.me|whatsapp/i.test(href)) track("whatsapp_click", label, where);
  }, true);

  // scroll depth + engaged time
  const marks = [25, 50, 75, 100], hit = {};
  addEventListener("scroll", () => {
    const h = document.documentElement, pct = (h.scrollTop + innerHeight) / h.scrollHeight * 100;
    marks.forEach(m => { if (pct >= m - 1 && !hit[m]) { hit[m] = 1; track("scroll", m + "%"); } });
  }, { passive: true });
  let shown = 0, t0 = Date.now(), sent = false;
  const tick = setInterval(() => {
    if (document.visibilityState === "visible") shown += 1;
    if (shown >= 30 && !sent) { sent = true; track("engaged", "30s"); clearInterval(tick); }
  }, 1000);

  // the quote form: seen, each step, each contact field filled
  addEventListener("DOMContentLoaded", () => {
    const card = document.getElementById("setup-card"); if (!card) return;
    new IntersectionObserver((es, o) => es.forEach(x => { if (x.isIntersecting) { track("form_view", location.pathname); o.disconnect(); } }), { threshold: .35 }).observe(card);
    card.addEventListener("click", ev => {
      const m = ev.target.closest("#setup-market .setup-pill"); if (m) track("form_step", "1 · market", m.dataset.market);
      const v = ev.target.closest("#setup-sites .setup-pill"); if (v) track("form_step", "2 · venues", v.dataset.sites);
    });
    const sl = card.querySelector("#setup-slider"); if (sl) sl.addEventListener("change", () => track("form_step", "3 · customers", card.querySelector("#setup-count").textContent));
    let started = false;
    card.querySelectorAll(".setup-form__input").forEach(f => {
      f.addEventListener("focus", () => { if (!started) { started = true; track("form_step", "4 · contact started", f.name); } });
      f.addEventListener("change", () => { if (f.value.trim()) track("form_step", "4 · filled " + f.name, ""); });
    });
  });
})();

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
    if (!ok) { msg.textContent = "Please fill in every field so we can reach you."; msg.className = "form-msg err"; if (window.track) track("form_error", [...form.querySelectorAll(".invalid")].map(f => f.name).join(","), market); return; }
    msg.textContent = "";
    const data = Object.fromEntries(new FormData(form)); delete data._gotcha;
    if (!country.required) delete data.country;
    data.page = location.pathname;
    if (window.track) track("lead", data.market + " · " + data.lead_status, "venues " + data.venues + " · " + data.weekly_customers + "/wk · " + data.recommended + (data.station_interest ? " · wants " + data.station_interest : ""), { market: data.market, lead_status: data.lead_status, venues: data.venues });
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
  // "Reduce motion" (e.g. Windows "Show animations" off) slows the showcase down instead of freezing it
  const pair = v => `<div class="bt-pair">${tile(v)}<div class="bt-info"><b>${esc(v.name)}</b><span>${esc(v.location || SHORT[v.category] || "")}</span></div></div>`;
  const reduce = false, SPEED = matchMedia("(prefers-reduced-motion: reduce)").matches ? 0.6 : 1;
  const makeDesigns = stage => ({
    /* 2. Drum: the runway's flow, curved over a big cylinder. Rows come over the crest and roll down toward you.
          Same 4 columns, tile size and surface speed as the runway; rows are refilled while they're out of sight. */
    2() {
      const FACES = 20, PER = 2, STEP = 360 / FACES;   // each row: 2 pairs of [logo | name + location]
      const W = stage.clientWidth, H = stage.clientHeight;
      const DW = W * 1.16, colW = (DW - 3 * 10) / 4, faceH = colW * 5 / 9 + 10, PUSH = 170;   // wider drum, pushed back for depth           // tile 9:5 + 10px gap, like the runway
      const r = faceH / (2 * Math.tan(Math.PI / FACES));
      stage.innerHTML = `<div class="drum-wrap"><div class="drum" style="height:${faceH}px;width:${DW}px;left:${(W - DW) / 2}px;top:${H - faceH * 1.05}px"></div></div>`;
      const drum = stage.querySelector(".drum");
      let next = 0; const take = () => { const out = []; for (let k = 0; k < PER; k++) out.push(withLogo[next++ % withLogo.length]); return out; };   // logo venues only
      const faces = [];
      for (let i = 0; i < FACES; i++) {
        const f = document.createElement("div"); f.className = "drum-face";
        f.style.transform = `rotateX(${i * STEP}deg) translateZ(${r}px)`; f.innerHTML = take().map(pair).join("");
        drum.appendChild(f); faces.push({ el: f, base: i * STEP, back: false });
      }
      const degPerMs = (50 / r) * (180 / Math.PI) / 1000;                      // 50px/s along the surface = runway speed
      let angle = 0, last = performance.now(), raf;
      const loop = t => {
        const dt = Math.min(50, t - last); last = t; angle -= dt * degPerMs * SPEED;
        drum.style.transform = `translateZ(${-r - PUSH}px) rotateX(${angle}deg)`;
        faces.forEach(f => {
          const a = ((f.base + angle) % 360 + 360) % 360;
          const isBack = a > 110 && a < 250;
          if (isBack && !f.back) f.el.innerHTML = take().map(pair).join("");
          f.back = isBack;
        });
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      return () => cancelAnimationFrame(raf);
    },

    /* 4. Flip wall: a grid of tiles; one flips to a new venue every ~0.7s */
    4() {
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

    /* 5. Runway: columns of venues streaming toward you on a tilted plane */
    5() {
      const COLS = 4, per = Math.ceil(MIX.length / COLS);
      const cols = Array.from({ length: COLS }, (_, c) => MIX.slice(c * per, (c + 1) * per));
      stage.innerHTML = `<div class="runway"><div class="runway-plane">${cols.map((list, c) => {
        const h = list.map(v => tile(v)).join("");
        return `<div class="rw-col"><div class="rw-track" style="animation-duration:${90 + c * 12}s;animation-delay:-${c * 9}s">${h}${h}</div></div>`;
      }).join("")}</div></div>`;
      return () => {};
    },

    /* 3. Categories: counts per category; auto-cycles, click to pick */
    3() {
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

    /* 1. Orbit: logo venues only, fixed (no swapping). Best-known venues are the biggest tiles, on the outer ring,
          which passes closest to the viewer. The inner ring is wide enough to clear the station. */
    1() {
      const W = stage.clientWidth, H = stage.clientHeight, cx = W / 2, cy = H * 0.47;
      const by = Object.fromEntries(withLogo.map(v => [v.name, v]));
      const TOP = ["RDS", "Tesco", "O'Donoghue's", "St Vincent's University Hospital", "Cork University Hospital", "St James's Hospital",
                   "Beaumont Hospital", "Connolly Hospital", "The National Maternity Hospital", "Children's Health Ireland at Crumlin",
                   "Wexford General Hospital", "Portiuncula University Hospital", "Jameson Distillery Bow St", "Whelan's"];
      const MID = ["Clayton Hotel Ballsbridge", "Dicey's Garden", "Pawn Shop", "The George", "The Workman's Club", "Slattery's",
                   "Café en Seine", "The Harbour Bar", "Temple Bar Hotel Dublin", "Alfie's", "Harcourt Hotel", "Gleeson's Fresh Foods"];
      const used = new Set([...TOP, ...MID]);
      const REST = withLogo.filter(v => !used.has(v.name)).map(v => v.name).slice(0, 10);
      const pick = list => list.map(n => by[n]).filter(Boolean);
      const small = W < 600;
      const rings = [   // inner -> outer; sizes in px
        { list: pick(REST), rx: W * 0.33, ry: H * 0.22, sp: 0.00012, size: small ? 54 : 66 },
        { list: pick(MID),  rx: W * 0.41, ry: H * 0.32, sp: -0.00009, size: small ? 64 : 80 },
        { list: pick(TOP),  rx: W * 0.47, ry: H * 0.43, sp: 0.00007, size: small ? 76 : 98 },
      ];
      rings.forEach(g => { g.rx = Math.min(g.rx, W / 2 - g.size * 0.62); });     // keep every tile inside the frame
      stage.innerHTML = `<div class="orbit"><div class="orbit-core" style="top:${cy}px"><img src="/assets/stations/countertop-12-cutout.webp" alt="Jolt Countertop 12 station"></div></div>`;
      const orbit = stage.querySelector(".orbit"), items = [];
      rings.forEach((g, ri) => {
        const ring = document.createElement("div"); ring.className = "orbit-path";
        ring.style.cssText = `width:${g.rx * 2}px;height:${g.ry * 2}px;left:${cx - g.rx}px;top:${cy - g.ry}px`; orbit.appendChild(ring);
        g.list.forEach((v, k) => {
          const el = document.createElement("div"); el.className = "orbit-up"; el.style.width = g.size + "px"; el.innerHTML = tile(v);
          orbit.appendChild(el); items.push({ el, g, a: (Math.PI * 2 / g.list.length) * k + ri * 0.5 });
        });
      });
      let last = performance.now(), raf;
      const loop = t => {
        const dt = Math.min(50, t - last); last = t;
        items.forEach(it => {
          it.a += it.g.sp * dt * SPEED;
          const sn = Math.sin(it.a), depth = (sn + 1) / 2;                       // 0 = back (top), 1 = front (bottom)
          const x = cx + Math.cos(it.a) * it.g.rx, y = cy + sn * it.g.ry, sc = 0.7 + depth * 0.45;
          it.el.style.transform = `translate(${x - it.g.size / 2}px, ${y - it.g.size * 0.28}px) scale(${sc})`;
          it.el.style.zIndex = sn > 0.15 ? 3 + Math.round(depth * 10) : 1;      // front half passes in front of the station
          it.el.style.opacity = 0.45 + depth * 0.55;
        });
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
      return () => cancelAnimationFrame(raf);
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
    io.observe(stage);   // observe the stage (the root may be display:contents on phones)
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
  show("1");   // Orbit only for now (other designs kept in code; switcher removed)
  document.querySelectorAll("#design-switch button").forEach(b => b.addEventListener("click", () => {
    show(b.dataset.d); if (window.track) track("design_switch", b.textContent.trim());
    const r = stage.getBoundingClientRect();                       // bring the showcase into view if it's off screen
    if (r.top < 120 || r.bottom > innerHeight) stage.scrollIntoView({ behavior: "smooth", block: "center" });
    const u = new URL(location.href); u.searchParams.set("design", b.dataset.d); history.replaceState(null, "", u);
  }));
})();

/* ---------- Hero map: pinned under the word "BANK", right-aligned to the end of the first headline line (desktop + phone) ---------- */
(function () {
  const top = document.querySelector(".hero-top"), map = top && top.querySelector(".hero-map"), h1 = top && top.querySelector("h1");
  if (!map || !h1) return;
  function place() {
    if (innerWidth <= 900) { map.removeAttribute("style"); map.classList.remove("is-small"); top.style.minHeight = ""; return; }   // phone: map sits lower down in normal flow (CSS)
    const r = document.createRange(); r.selectNodeContents(h1);
    const lines = [...r.getClientRects()].filter(x => x.width > 2);
    const lead = top.querySelector(".lead");
    if (lines.length < 2) { map.style.display = "none"; top.style.minHeight = ""; if (lead) lead.style.maxWidth = ""; return; }
    map.style.display = "block";
    const box = top.getBoundingClientRect(), l1 = lines[0], l2 = lines[lines.length - 1];
    const small = innerWidth < 700;
    const width = Math.max(small ? 110 : 170, Math.min(250, l1.right - l2.right - (small ? 14 : 28)));   // fits between "STATIONS." and the end of "BANK"
    const height = width * 536 / 640, offset = l2.top - box.top + (small ? 4 : 6);
    map.style.width = width + "px";
    map.style.right = Math.max(0, box.right - l1.right) + "px";
    map.style.top = offset + "px";
    map.classList.toggle("is-small", width < 180);
    const mapLeft = l1.right - width;                                         // subtext wraps before the map
    if (lead) lead.style.maxWidth = Math.max(small ? 150 : 240, mapLeft - box.left - (small ? 12 : 24)) + "px";
    top.style.minHeight = (offset + height + 12) + "px";
  }
  place(); addEventListener("resize", place);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
})();

/* ---------- App links: iPhone -> App Store, Android -> Google Play, desktop -> choose a store ---------- */
(function () {
  const A = window.JOLT_APP; if (!A) return;
  const ua = navigator.userAgent || "";
  const isIOS = /iPhone|iPad|iPod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  const isAndroid = /Android/i.test(ua);
  const modal = document.getElementById("app-modal");
  const close = () => { if (modal) modal.hidden = true; };
  if (modal) {
    modal.addEventListener("click", e => { if (e.target === modal || e.target.closest(".app-modal-x")) close(); });
    addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  }
  document.querySelectorAll(".app-link").forEach(a => {
    a.href = isAndroid ? A.android : A.ios;
    a.addEventListener("click", e => {
      
      if (isIOS || isAndroid || !modal) return;          // phones go straight to their store (it shows "Open" if the app is installed)
      e.preventDefault(); modal.hidden = false;
    });
  });
})();

/* ---------- Cookie consent (Consent Mode v2) ---------- */
(function () {
  const bar = document.getElementById("cookie-bar"); if (!bar) return;
  let saved = null; try { saved = localStorage.getItem("jolt-consent"); } catch (_) {}
  if (!saved) bar.hidden = false;
  document.querySelectorAll(".cookie-settings").forEach(l => l.addEventListener("click", e => { e.preventDefault(); bar.hidden = false; }));
  bar.querySelectorAll("[data-consent]").forEach(b => b.addEventListener("click", () => {
    const v = b.dataset.consent;
    try { localStorage.setItem("jolt-consent", v); } catch (_) {}
    if (window.gtag) gtag("consent", "update", { analytics_storage: v, ad_storage: v, ad_user_data: v, ad_personalization: v });
    (window.dataLayer = window.dataLayer || []).push({ event: "consent_" + v });
    bar.hidden = true;
  }));
})();

/* ---------- Mirror key events as plain dataLayer events so GTM triggers can use them ---------- */
(function () {
  const orig = window.gtag; if (!orig) return;
  window.gtag = function (type, name, params) {
    orig.apply(this, arguments);
    if (type === "event") (window.dataLayer = window.dataLayer || []).push(Object.assign({ event: name }, params || {}));
  };
})();

/* ---------- Phone menu (three lines) ---------- */
(function () {
  const b = document.getElementById("burger"), m = document.getElementById("mobile-menu");
  if (!b || !m) return;
  const set = open => { m.hidden = !open; b.setAttribute("aria-expanded", open); b.setAttribute("aria-label", open ? "Close menu" : "Open menu"); };
  b.addEventListener("click", () => { const o = m.hidden; set(o); if (o && window.track) track("click", "menu-open"); });
  m.addEventListener("click", e => { if (e.target.closest("a")) set(false); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") set(false); });
})();

/* ---------- Fit "Power Bank Stations" on one line ---------- */
(function () {
  const h = document.querySelector(".hero-h1"); if (!h) return;
  function fit() {
    h.style.fontSize = ""; const max = parseFloat(getComputedStyle(h).fontSize), w = h.parentElement.clientWidth;
    if (h.scrollWidth > w) h.style.fontSize = Math.floor(max * w / h.scrollWidth * 0.99) + "px";
  }
  fit(); addEventListener("resize", fit); if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();
