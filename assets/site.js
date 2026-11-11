/* Lead form handler.
   Set FORM_ENDPOINT to a form backend (e.g. https://formspree.io/f/xxxx) to receive leads by email.
   Until it's set, submissions open WhatsApp with the details pre-filled so no lead is lost. */
const FORM_ENDPOINT = "";
const WHATSAPP = "353870365888";

/* ---------- Full enquiry form ---------- */
document.querySelectorAll(".lead-form").forEach(form => {
  const msg = form.querySelector(".form-msg");
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (form._gotcha && form._gotcha.value) return;
    let ok = true;
    form.querySelectorAll("[required]").forEach(f => {
      const bad = !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.toggle("invalid", bad); if (bad) ok = false;
    });
    if (!ok) { msg.textContent = "Please fill in the highlighted fields."; msg.className = "form-msg err"; return; }
    const data = Object.fromEntries(new FormData(form));
    delete data._gotcha;
    data.page = location.pathname;
    if (window.gtag) gtag("event", "generate_lead", { region: data.region, venue_type: data.venue_type });
    const btn = form.querySelector("button"); btn.disabled = true; btn.textContent = "Sending…";
    if (FORM_ENDPOINT) {
      try {
        const res = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
        if (!res.ok) throw new Error(res.status);
        location.href = "/thank-you/"; return;
      } catch (err) { msg.textContent = "Something went wrong. Please WhatsApp us instead."; msg.className = "form-msg err"; btn.disabled = false; btn.textContent = "Request my free station"; return; }
    }
    const text = `New venue enquiry (${data.region})\nVenue: ${data.venue}\nName: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone}\nType: ${data.venue_type}\nLocation: ${data.location}\nWeekly customers: ${data.footfall || "-"}`;
    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, "_blank");
    location.href = "/thank-you/";
  });
});

/* ---------- Setup card: venues + weekly customers -> recommended setup -> one-field capture ---------- */
(function () {
  const card = document.getElementById("setup-card");
  if (!card) return;
  const slider = card.querySelector("#setup-slider");
  const countEl = card.querySelector("#setup-count");
  const perEl = card.querySelector("#setup-per");
  const q2 = card.querySelector("#setup-q2");
  const nameEl = card.querySelector("#setup-name");
  const incEl = card.querySelector("#setup-inc");
  const bars = card.querySelectorAll(".setup-meter i");
  const pills = card.querySelectorAll(".setup-pill");
  const hV = card.querySelector("#setup-h-venues"), hC = card.querySelector("#setup-h-customers"), hR = card.querySelector("#setup-h-rec");
  const STOPS = [50, 100, 250, 500, 1000, 2500, 5000];   // notch values, evenly spaced on the slider
  let sites = "1";

  const valueAt = pos => {                                  // pos 0..600 -> customers (log between notches)
    const seg = Math.min(5, Math.floor(pos / 100)), t = (pos - seg * 100) / 100;
    const v = STOPS[seg] * Math.pow(STOPS[seg + 1] / STOPS[seg], t);
    return v < 100 ? Math.round(v / 10) * 10 : v < 1000 ? Math.round(v / 50) * 50 : Math.round(v / 250) * 250;
  };
  const fmt = v => (v >= 5000 ? "5,000+" : v.toLocaleString("en-IE"));

  function station(v) {
    if (v < 250) return ["Compact station", "Small countertop unit that sits beside the till"];
    if (v < 1500) return ["Standard station", "Countertop station sized for a steady flow of customers"];
    return ["High-capacity station", "More power banks on hand for busy bars, hotels and venues"];
  }

  function update() {
    const pos = +slider.value, v = valueAt(pos);
    slider.style.setProperty("--p", (pos / 6) + "%");
    countEl.textContent = fmt(v);
    const multi = sites !== "1";
    q2.textContent = multi ? "How many customers a week, per venue?" : "How many customers a week?";
    perEl.textContent = multi ? " per venue" : "";
    const [st, desc] = station(v);
    let name, inc;
    if (sites === "1") { name = st; inc = desc + " · installed free · you earn a revenue share"; }
    else if (sites === "2") { name = "2 × " + st; inc = "A station in each venue · installed free · revenue share on both"; }
    else if (sites === "3-10") { name = st + " in every venue"; inc = "We plan placement across all your sites · installed free · revenue share on each"; }
    else { name = "Group rollout"; inc = "A rollout plan for your whole group, venue by venue · installed free · revenue share across the group"; }
    nameEl.textContent = name; incEl.textContent = inc;
    const lit = Math.max(1, Math.round((pos / 600) * bars.length));
    bars.forEach((b, i) => b.classList.toggle("on", i < lit));
    hV.value = sites; hC.value = v >= 5000 ? "5000+" : v; hR.value = name;
  }

  pills.forEach(p => p.addEventListener("click", () => {
    pills.forEach(x => { x.classList.remove("is-active"); x.setAttribute("aria-checked", "false"); });
    p.classList.add("is-active"); p.setAttribute("aria-checked", "true");
    sites = p.dataset.sites; update();
  }));
  slider.addEventListener("input", update);
  update();

  const form = card.querySelector("#setup-form"), msg = form.querySelector(".form-msg");
  form.addEventListener("submit", async e => {
    e.preventDefault();
    if (form._gotcha.value) return;
    let ok = true;
    form.querySelectorAll("[required]").forEach(f => {
      const v = f.value.trim();
      const bad = !v || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(v)) || (f.type === "tel" && v.replace(/\D/g, "").length < 7);
      f.classList.toggle("invalid", bad); if (bad) ok = false;
    });
    if (!ok) { msg.textContent = "Please fill in all four fields so we can reach you."; msg.className = "form-msg err"; return; }
    msg.textContent = "";
    const data = Object.fromEntries(new FormData(form)); delete data._gotcha; data.page = location.pathname;
    if (window.gtag) gtag("event", "generate_lead", { form_id: "setup-hero", region: data.region, venues: data.venues });
    const btn = form.querySelector("button"); btn.disabled = true; btn.textContent = "Sending…";
    let sent = false;
    if (FORM_ENDPOINT) {
      try {
        const r = await fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) });
        sent = r.ok;
      } catch (_) {}
    }
    if (!sent) {
      const text = `New venue enquiry (${data.region})\nBusiness: ${data.business}\nName: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone}\nVenues: ${data.venues}\nCustomers/week: ${data.weekly_customers}\nRecommended: ${data.recommended}`;
      window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`, "_blank");
    }
    card.querySelector(".setup-capture").innerHTML = '<div class="setup-success"><b>Got it. Thanks.</b><p class="muted">Someone from Jolt will be in touch within one working day.</p></div>';
  });
})();
