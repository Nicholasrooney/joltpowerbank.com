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
