// CODE ROT Frame-Animator: deterministische Animation pro Zeitpunkt t (Sekunden).
// window.SHOT = {dauer, fps, bg:{typ, frames:[urls], start, loop, n}, move, figuren:[{aktion, seed, ...}], fx:[...], hud:{...}}
(function () {
  const S = window.SHOT;
  const W = 1080, H = 1920;
  // ---------- Zufall (deterministisch) ----------
  function rnd(seed) { let x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); }
  function noise1(t, seed) { // glattes 1D-Rauschen
    const i = Math.floor(t), f = t - i, u = f * f * (3 - 2 * f);
    return (rnd(i + seed * 101) * (1 - u) + rnd(i + 1 + seed * 101) * u) * 2 - 1;
  }
  const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
  const easeOut = x => 1 - Math.pow(1 - Math.min(Math.max(x, 0), 1), 3);
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

  // ---------- Kamera (2D) ----------
  function kamera(t) {
    const p = clamp(t / S.dauer, 0, 1), m = S.move || "drift";
    let z = 1, x = 0, y = 0;
    if (m === "zoom_in") z = 1 + 0.08 * ease(p);
    else if (m === "zoom_schnell") z = 1 + 0.22 * easeOut(p);
    else if (m === "zoom_out") z = 1.14 - 0.12 * ease(p);
    else if (m === "pan_r") { z = 1.14; x = (0.5 - ease(p)) * W * 0.12; }
    else if (m === "pan_l") { z = 1.14; x = (ease(p) - 0.5) * W * 0.12; }
    else if (m === "pan_hoch") { z = 1.14; y = (ease(p) - 0.5) * H * 0.12; }
    else if (m === "shake") { z = 1.07 + 0.03 * p; x = 22 * noise1(t * 9, 1) + 10 * noise1(t * 23, 2); y = 18 * noise1(t * 8, 3) + 8 * noise1(t * 21, 4); }
    else if (m === "shake_stark") { z = 1.12; const d = Math.exp(-t * 3.2); x = 70 * d * noise1(t * 14, 5) + 12 * noise1(t * 6, 6); y = 60 * d * noise1(t * 13, 7) + 10 * noise1(t * 7, 8); }
    else if (m === "statisch") z = 1.02;
    else { z = 1.03 + 0.015 * p; x = 6 * noise1(t * 0.8, 9); y = 6 * noise1(t * 0.7, 10); } // drift (3D-Shots)
    // Handkamera-Grundrauschen
    x += 2.5 * noise1(t * 1.7, 11); y += 2.5 * noise1(t * 1.5, 12);
    return { z, x, y };
  }

  // ---------- Hintergrund ----------
  const bgImg = document.getElementById("bgimg");
  async function setzeBg(t) {
    if (!S.bg || S.bg.typ !== "seq") return;
    let f = Math.round(t * S.fps) + S.bg.start;
    f = S.bg.loop ? ((f % S.bg.n) + S.bg.n) % S.bg.n : clamp(f, 0, S.bg.n - 1);
    const url = S.bg.muster.replace("####", String(f + 1).padStart(4, "0"));
    if (bgImg.getAttribute("src") !== url) { bgImg.src = url; try { await bgImg.decode(); } catch (e) {} }
  }

  // ---------- Figuren-Rigs ----------
  function setzeT(el, tf) { if (el) el.setAttribute("transform", tf); }
  function um(el, deg, sx, sy, dx, dy) { // Rotation/Skalierung um data-o + Verschiebung
    if (!el) return;
    const o = (el.getAttribute("data-o") || "0,0").split(",").map(Number);
    el.setAttribute("transform", `translate(${(dx || 0) + o[0]},${(dy || 0) + o[1]}) rotate(${deg || 0}) scale(${sx || 1},${sy || 1}) translate(${-o[0]},${-o[1]})`);
  }
  function blinzel(t, seed) { // 0 offen .. 1 zu
    let tb = 0.4 + rnd(seed) * 1.5, k = 0;
    while (tb < t + 0.2 && k < 40) {
      const d = t - tb; if (d > -0.07 && d < 0.13) return d < 0 ? 1 + d / 0.07 : 1 - d / 0.13;
      tb += 2.2 + rnd(seed + k * 7) * 2.8; k++;
    }
    return 0;
  }
  function animiereFigur(F, t) {
    const el = F.el, s = F.seed, a = F.aktion || "", ex = F.ausdruck || "neutral";
    const q = n => el.querySelector(".rig-" + n);
    // Grundbewegung: Atmen, Kopf, Blick
    const atem = Math.sin(t * (ex === "angst" || ex === "schreien" ? 7 : 2.6) + s) * (ex === "angst" ? 0.012 : 0.008);
    um(q("koerper"), 0, 1, 1 + atem, 0, 0);
    let kd = 2.2 * noise1(t * 0.6, s + 1), kx = 0, ky = -atem * 300;
    if (ex === "angst") { kx += 2.5 * noise1(t * 18, s + 2); ky += 2 * noise1(t * 17, s + 3); }
    if (ex === "schreien") { kd += 5 * Math.sin(t * 22) * Math.exp(-t * 2); ky += -8 * Math.exp(-t * 3); }
    if (a === "nicken") { const p = clamp((t - 0.15) / 0.7, 0, 1); ky += 26 * Math.sin(p * Math.PI * 2) * (p < 1 ? 1 : 0); kd += 0; }
    if (ex === "erleichtert") { kd += 4 * Math.sin(t * 1.3 + s); }
    um(q("kopf"), kd, 1, 1, kx, ky);
    const blick = ex === "seitenblick" ? 10 + 4 * noise1(t * 2, s) : 7 * noise1(t * 0.9, s + 4);
    setzeT(q("pupillen"), `translate(${blick},${4 * noise1(t * 0.7, s + 5)})`);
    const b = blinzel(t, s); const l = q("lider");
    if (l) { l.removeAttribute("transform"); l.style.transform = `scale(1,${Math.max(b, 0.0001)})`; }
    const brauY = ex === "angst" ? -4 + 3 * noise1(t * 3, s) : 2 * noise1(t * 1.2, s + 6);
    setzeT(q("brauen"), `translate(0,${brauY})`);
    const mundS = ex === "schreien" ? 1 + 0.25 * Math.abs(Math.sin(t * 14)) : 1 + 0.04 * noise1(t * 3, s + 7);
    um(q("mund"), 0, 1, mundS, 0, 0);
    const sw = q("schweiss");
    if (sw) { const p = (t * 0.6 + rnd(s)) % 1; setzeT(sw, `translate(0,${p * 70})`); sw.setAttribute("opacity", String(1 - p)); }
    // Arme / Beine
    let armL = 1.5 * noise1(t * 0.8, s + 8), armR = 1.5 * noise1(t * 0.8, s + 9), beinL = 0, beinR = 0;
    let fx = 0, fy = 0, fr = 0;
    if (a === "rennen") {
      const ph = t * 9 + s;
      beinL = 28 * Math.sin(ph); beinR = -28 * Math.sin(ph); armL = -25 * Math.sin(ph); armR = 25 * Math.sin(ph);
      fy = -18 * Math.abs(Math.sin(ph)); fx = (F.richtung || 1) * t * (F.tempo || 260); fr = 4 * (F.richtung || 1);
    }
    if (a === "kriechen") { fx = t * 90; fy = 10 * Math.abs(Math.sin(t * 5)); fr = 2 * Math.sin(t * 5); }
    if (a === "fallen") { const p = easeOut((t - (F.ab || 0.5)) / 0.5); fr = -25 * p; fy = 380 * p; fx = -60 * p; }
    if (a === "gehen") { const ph = t * 5 + s; fy = -8 * Math.abs(Math.sin(ph)); fx = (F.richtung || -1) * t * 70; }
    if (a === "pop") { const p = easeOut(t / 0.35); fy = (1 - p) * 120; }
    if (ex === "schreien" || a === "zucken") { fx += 10 * noise1(t * 25, s); }
    um(q("arm-l"), armL, 1, 1, 0, 0); um(q("arm-r"), armR, 1, 1, 0, 0);
    um(q("bein-l"), beinL, 1, 1, 0, 0); um(q("bein-r"), beinR, 1, 1, 0, 0);
    // ganze Figur
    let sc = 1;
    if (a === "pop") sc = 0.85 + 0.15 * easeOut(t / 0.35);
    F.wrap.style.transform = `translate(${fx}px,${fy}px) rotate(${fr}deg) scale(${sc})`;
    // Inserts
    if (a === "funk") {
      F.wrap.style.transform = `translate(${8 * noise1(t * 2, s)}px,${10 * noise1(t * 1.8, s + 1) + 30 * Math.exp(-t * 4)}px) rotate(${1.5 * noise1(t, s + 2)}deg)`;
      el.querySelectorAll("circle[fill='#C0392B']").forEach(c => c.setAttribute("opacity", (Math.floor(t * 4) % 2) ? "0.25" : "1"));
    }
    if (a === "klettern") {
      F.wrap.style.transform = `translate(0px,${(t * 230) % 250}px)`;
    }
    if (a === "silhouetten_weg") {
      el.querySelectorAll(".rig-silhouette").forEach((g, i) => setzeT(g, `translate(${easeOut((t - 0.1 - i * 0.12) / 0.8) * 520},${-10 * Math.abs(Math.sin(t * 9))})`));
    }
    if (a === "silhouetten") {
      el.querySelectorAll(".rig-silhouette").forEach((g, i) => setzeT(g, `translate(${14 * noise1(t * 0.9, s + i)},${5 * noise1(t * 1.3, s + i + 3)}) rotate(${2 * noise1(t * 0.7, s + i + 9)} 540 1000)`));
    }
    if (a === "tv") {
      el.querySelectorAll("feTurbulence").forEach(n => n.setAttribute("seed", String(Math.floor(t * S.fps) % 97 + 1)));
      const roll = el.querySelector(".rig-tvbild"); if (roll) setzeT(roll, `translate(0,${(t * 90) % 40 - 20})`);
    }
    if (a === "scope") {
      F.wrap.style.transform = `translate(${14 * noise1(t * 0.9, s) + 6 * Math.sin(t * 1.6)}px,${10 * Math.sin(t * 1.4 + s) + 6 * noise1(t * 1.1, s + 3)}px)`;
    }
    if (a === "trage") { F.wrap.style.transform = `translate(${-t * 80}px,${-6 * Math.abs(Math.sin(t * 6))}px)`; }
  }

  // ---------- Partikel ----------
  const cv = document.getElementById("fx"), cx = cv.getContext("2d");
  function partikel(t) {
    cx.clearRect(0, 0, W, H);
    for (const fx of (S.fx || [])) {
      const n = fx.n || 60;
      for (let i = 0; i < n; i++) {
        const r1 = rnd(i * 3.1 + fx.seed), r2 = rnd(i * 7.7 + fx.seed), r3 = rnd(i * 1.3 + fx.seed);
        if (fx.typ === "staub") {
          const x = (r1 * W + t * 25 * (r2 - 0.3) + 30 * noise1(t * 0.4, i)) % W, y = (r2 * H + t * 12 * (r3 - 0.5) + 20 * noise1(t * 0.3, i + 50)) % H;
          const a = 0.12 + 0.25 * (0.5 + 0.5 * Math.sin(t * 2 + i));
          cx.fillStyle = `rgba(220,230,255,${a * (fx.alpha || 1)})`; cx.beginPath(); cx.arc(x, y, 1.5 + r3 * 3, 0, 7); cx.fill();
        } else if (fx.typ === "glut") {
          const life = 2.5 + r3 * 2, ph = ((t + r1 * life) % life) / life;
          const x = fx.x + (r2 - 0.5) * (fx.breite || 500) + 60 * noise1(t * 0.8 + i, i) + ph * 80 * (r1 - 0.5);
          const y = fx.y - ph * (fx.hoehe || 900);
          const a = (1 - ph) * (0.6 + 0.4 * Math.sin(t * 20 + i));
          cx.fillStyle = `rgba(255,${120 + 100 * r3 | 0},40,${a})`; cx.beginPath(); cx.arc(x, y, 2 + 4 * r2 * (1 - ph), 0, 7); cx.fill();
        } else if (fx.typ === "rauch") {
          const life = 6 + r3 * 4, ph = ((t + r1 * life) % life) / life;
          const x = fx.x + (r2 - 0.5) * (fx.breite || 600) + ph * 200 * (r1 - 0.3), y = fx.y - ph * (fx.hoehe || 1200);
          const rad = 80 + ph * 260;
          const g = cx.createRadialGradient(x, y, 0, x, y, rad);
          g.addColorStop(0, `rgba(${fx.farbe || "40,40,48"},${0.22 * Math.sin(ph * Math.PI) * (fx.alpha || 1)})`); g.addColorStop(1, "rgba(0,0,0,0)");
          cx.fillStyle = g; cx.fillRect(x - rad, y - rad, rad * 2, rad * 2);
        } else if (fx.typ === "funken") {
          const per = 0.9, ph = ((t + r1 * per) % per) / per;
          const ang = -Math.PI / 2 + (r2 - 0.5) * 2.2, v = 900 + r3 * 900;
          const x = fx.x + Math.cos(ang) * v * ph * 0.6, y = fx.y + Math.sin(ang) * v * ph * 0.6 + 900 * ph * ph * 0.5;
          cx.strokeStyle = `rgba(255,220,140,${(1 - ph)})`; cx.lineWidth = 3; cx.beginPath(); cx.moveTo(x, y);
          cx.lineTo(x - Math.cos(ang) * 30, y - Math.sin(ang) * 30 + 10); cx.stroke();
        } else if (fx.typ === "flimmern") { // Scheinwerfer/Glow-Flackern
          const a = (fx.alpha || 0.15) * (0.5 + 0.5 * noise1(t * 12, fx.seed));
          const g = cx.createRadialGradient(fx.x, fx.y, 0, fx.x, fx.y, fx.r || 700);
          g.addColorStop(0, `rgba(${fx.farbe || "255,140,50"},${a})`); g.addColorStop(1, "rgba(0,0,0,0)");
          cx.fillStyle = g; cx.fillRect(0, 0, W, H); break;
        } else if (fx.typ === "feuerwerk") {
          const per = 2.2 + r3 * 1.2, start = r1 * per, ph = ((t + start) % per) / per;
          const zyk = Math.floor((t + start) / per);
          const bx = 120 + rnd(i * 5.5 + zyk * 3.3 + fx.seed) * 840, by = 220 + rnd(i * 2.1 + zyk * 1.7 + fx.seed) * 700;
          const farben = ["255,80,60", "255,220,90", "120,200,255", "255,255,255", "120,255,140"];
          const fb = farben[Math.floor(rnd(i * 9.1 + zyk) * farben.length)];
          if (ph < 0.25) { // Aufstieg
            const p = ph / 0.25; cx.fillStyle = `rgba(255,220,160,${0.9})`;
            cx.beginPath(); cx.arc(bx, H - (H - by) * p, 4, 0, 7); cx.fill();
          } else { // Explosion
            const p = (ph - 0.25) / 0.75, rad = 260 * Math.pow(p, 0.5), a = Math.max(0, 1 - p * 1.15);
            for (let k = 0; k < 28; k++) {
              const an = k / 28 * 6.283 + i, x = bx + Math.cos(an) * rad, y = by + Math.sin(an) * rad + p * p * 120;
              cx.fillStyle = `rgba(${fb},${a})`; cx.beginPath(); cx.arc(x, y, 3.5 * (1 - p) + 1, 0, 7); cx.fill();
            }
            if (p < 0.12) { const g = cx.createRadialGradient(bx, by, 0, bx, by, 500); g.addColorStop(0, `rgba(${fb},${0.35 * (1 - p / 0.12)})`); g.addColorStop(1, "rgba(0,0,0,0)"); cx.fillStyle = g; cx.fillRect(0, 0, W, H); }
          }
        } else if (fx.typ === "scanlines") {
          cx.fillStyle = "rgba(0,0,0,0.12)"; for (let yy = (t * 120) % 8; yy < H; yy += 8) cx.fillRect(0, yy, W, 3); break;
        }
      }
    }
  }

  // ---------- HUD ----------
  function hud(t) {
    const u = document.getElementById("uhr");
    if (u) { u.querySelector(".dot").style.opacity = (Math.floor(t * 2) % 2) ? 0.25 : 1;
      const p = easeOut(t / 0.25); if (S.hud && S.hud.uhr_neu) u.style.transform = `scale(${1.25 - 0.25 * p})`; }
    const neu = document.querySelector(".regeln .neu");
    if (neu) { const p = easeOut(t / 0.3); neu.style.opacity = p; neu.style.transform = `translateX(${(1 - p) * -60}px)`;
      neu.style.textShadow = `0 0 ${20 * (1 - p)}px #fff`; }
    const kopf = document.querySelector(".regeln .kopf");
    if (kopf && S.hud && S.hud.regeln_neu_box) { const p = easeOut(t / 0.3); document.querySelector(".regeln").style.transform = `translateX(-50%) scale(${0.6 + 0.4 * p})`; }
    const titel = document.querySelector(".titel");
    if (titel) { const p = easeOut((t - 0.05) / 0.35); titel.style.transform = `scale(${2.2 - 1.2 * p}) translateY(${8 * noise1(t * 20, 3) * (1 - p)}px)`; titel.style.opacity = p;
      const ut = document.querySelector(".untertitel"); if (titel.offsetHeight > 250) titel.style.top = "1060px"; ut.style.top = (titel.offsetTop + titel.offsetHeight + 30) + "px"; ut.style.opacity = easeOut((t - 0.35) / 0.4); ut.style.letterSpacing = `${10 + 12 * (1 - easeOut((t - 0.35) / 0.6))}px`; }
    document.querySelectorAll(".ringe circle").forEach((c, i) => {
      const p = ((t * 0.9 + i * 0.25) % 1); c.setAttribute("r", String(150 + p * 420)); c.setAttribute("opacity", String((1 - p) * 0.9));
    });
    const linie = document.getElementById("linie"); if (linie) linie.style.opacity = 0.75 + 0.25 * Math.sin(t * 20);
    const logo = document.querySelector(".logo"); if (logo) logo.style.textShadow = `0 0 ${20 + 25 * (0.5 + 0.5 * Math.sin(t * 9))}px rgba(255,30,30,.8)`;
  }

  // ---------- Blitze / Blenden ----------
  function blenden(t) {
    const fl = document.getElementById("blitz"); let a = 0, c = "#fff";
    if (S.blitz) { a = Math.max(a, 1 - t / 0.2); if (S.blitz === "orange") c = "#ff8a2a"; }
    if (S.ende_blitz) a = Math.max(a, (t - (S.dauer - 0.15)) / 0.15);
    if (S.blitz_kurz) a = Math.max(a, 0.55 * (1 - t / 0.08));
    fl.style.background = c; fl.style.opacity = clamp(a, 0, 1);
    const sw = document.getElementById("schwarz"); let b = 0;
    if (S.ende_schwarz) b = (t - (S.dauer - 0.5)) / 0.5;
    if (S.stille) b = Math.max(b, 0.25);
    sw.style.opacity = clamp(b, 0, 1);
    const tint = document.getElementById("tint");
    if (tint && S.tint_puls) tint.style.opacity = 0.75 + 0.25 * Math.sin(t * 10);
  }

  // ---------- Frame setzen ----------
  const FIG = [];
  document.querySelectorAll(".figwrap").forEach((w, i) => {
    const d = S.figuren[i] || {};
    FIG.push(Object.assign({}, d, { wrap: w, el: w.querySelector("svg") }));
  });
  window.setzeZeit = async function (t) {
    await setzeBg(t);
    const k = kamera(t);
    // Aggressiver Schnitt: harte Punch-ins (Sprungschnitte im Bild) und Stöße auf Schlüsselwörtern
    if (S.punches && S.punches.length) {
      let p = null; for (const q of S.punches) if (t >= q[0]) p = q;
      if (p) { k.z *= p[1]; k.x += p[2]; k.y += p[3] + 160 * (p[1] - 1); }
    }
    (S.stoesse || []).forEach((q, i) => {
      const d = (t - q[0]) / q[1]; if (d < 0 || d > 1) return; const a = 1 - d;
      k.x += 30 * a * noise1(t * 45, 40 + i); k.y += 26 * a * noise1(t * 41, 60 + i); k.z *= 1 + 0.06 * a;
    });
    document.querySelectorAll(".tiefe").forEach(l => {
      const d = parseFloat(l.dataset.tiefe || "1");
      l.style.transform = `translate(${k.x * d}px,${k.y * d}px) scale(${1 + (k.z - 1) * d})`;
    });
    FIG.forEach(F => animiereFigur(F, t));
    partikel(t); hud(t); blenden(t);
    return true;
  };
})();
