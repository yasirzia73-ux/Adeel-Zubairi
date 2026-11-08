/* ================= Money Map REEL ENGINE v2 (9:16, 720x1280 CSS px) ================= */
const W = 720, H = 1280;
const C = { navy: '#0B1020', gold: '#FACC15', gold2: '#EAB308', green: '#22C55E', red: '#EF4444', blue: '#3B82F6', cyan: '#22D3EE', white: '#F8FAFC', grey: '#94A3B8', slate: '#1E293B', purple: '#A855F7', orange: '#F97316' };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, p) => a + (b - a) * p;
const ease = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const easeOut = x => 1 - Math.pow(1 - clamp(x), 3);
const easeBack = x => { x = clamp(x); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const money = n => '$' + Math.round(n).toLocaleString('en-US');
const rnd = (s => () => { s = (s * 16807) % 2147483647; return s / 2147483647; })(42);

/* ---------- timing (line level) ---------- */
let LINES = [], TIM = [], TOTAL = 0;
function setupTiming(lines, sync) {
  LINES = lines;
  if (sync) { TIM = sync.lines.map(l => [l.start, l.end]); TOTAL = sync.total; return; }
  let t = 0.15;
  for (const s of lines) { const w = s.split(/\s+/).length, d = Math.max(1.2, w / 2.55); TIM.push([t, t + d]); t += d + 0.3; }
  TOTAL = t + 1.5;
}
const st = i => TIM[i][0], en = i => TIM[i][1];
const at = (T, i, off = 0, d = 0.3) => clamp((T - st(i) - off) / d);
const pop = (T, t0, d = 0.4) => { const x = clamp((T - t0) / d); return x <= 0 ? 0 : easeBack(x); };
const pin = (T, i, d = 0.4) => pop(T, st(i) - 0.08, d);
function vis(T, i, j) {
  const a = st(i) - 0.12, b = j + 1 < TIM.length ? st(j + 1) - 0.1 : TOTAL + 1;
  if (T < a || T > b) return 0; return clamp(Math.min((T - a) / 0.16, (b - T) / 0.1));
}

/* ---------- persistent photo layer ---------- */
const PH = {};
function initPhotos(list, credits) {
  const L = document.getElementById('photos');
  for (const name of list) {
    const w = document.createElement('div'); w.className = 'ph'; w.style.opacity = 0;
    const img = document.createElement('img'); img.src = `assets/${name}.jpg`; w.appendChild(img);
    const vg = document.createElement('div'); vg.className = 'vig'; w.appendChild(vg);
    const cr = document.createElement('div'); cr.className = 'credit'; cr.textContent = 'Photo: ' + ((credits[name] || {}).credit || ''); w.appendChild(cr);
    L.appendChild(w); PH[name] = { w, img };
  }
  return Promise.all(Object.values(PH).map(p => p.img.decode().catch(() => {})));
}
function hidePhotos() { for (const k in PH) PH[k].w.style.opacity = 0; }
/* o: {x,y,w,h, p (0..1 progress for Ken Burns), z0,z1, x0,x1,y0,y1 (img pan in %), r radius, glow color, tilt deg, op, credit bool} */
function photo(name, o) {
  const P = PH[name]; if (!P || o.op <= 0) return;
  const s = P.w.style, p = clamp(o.p ?? 0);
  s.opacity = o.op; s.left = o.x + 'px'; s.top = o.y + 'px'; s.width = o.w + 'px'; s.height = o.h + 'px';
  s.borderRadius = (o.r ?? 28) + 'px';
  s.boxShadow = o.glow ? `0 0 0 3px ${o.glow}, 0 0 50px ${o.glow}66, 0 30px 60px rgba(0,0,0,.6)` : '0 30px 60px rgba(0,0,0,.6)';
  s.transform = `perspective(1200px) rotateY(${o.tilt ?? 0}deg) rotateX(${o.tiltX ?? 0}deg) scale(${o.s ?? 1})`;
  const z = lerp(o.z0 ?? 1.05, o.z1 ?? 1.18, p), px = lerp(o.x0 ?? 0, o.x1 ?? 0, p), py = lerp(o.y0 ?? 0, o.y1 ?? 0, p);
  P.img.style.transform = `translate(${px}%, ${py}%) scale(${z})`;
  P.img.style.filter = o.filter || 'saturate(1.1) contrast(1.05)';
  P.w.querySelector('.credit').style.display = o.credit === false ? 'none' : 'block';
}

/* ---------- SVG / HTML building blocks ---------- */
const svgText = (x, y, s, size, fill, weight = 900, anchor = 'middle', extra = '') =>
  `<text x="${x}" y="${y}" font-family="Montserrat" font-weight="${weight}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" ${extra}>${s}</text>`;
function ov(html, x, y, w, size, color = C.white, op = 1, extra = '') {
  return `<div class="ov" style="left:${x}px;top:${y}px;width:${w}px;font-size:${size}px;color:${color};opacity:${op};${extra}">${html}</div>`;
}
/* 3D extruded number/title with gradient face */
function big3d(html, y, size, from, to, depth, op = 1, s = 1, extra = '') {
  let sh = ''; for (let i = 1; i <= 8; i++) sh += `0 ${i}px 0 ${depth},`;
  sh += '0 14px 18px rgba(0,0,0,.55), 0 0 40px rgba(0,0,0,.3)';
  return `<div class="ov" style="left:0;top:${y}px;width:${W}px;font-size:${size}px;opacity:${op};transform:scale(${s});${extra}">
    <span style="position:relative;display:inline-block">
      <span style="position:absolute;left:0;top:0;width:100%;color:transparent;text-shadow:${sh}">${html}</span>
      <span style="position:relative;background:linear-gradient(180deg,${from},${to});-webkit-background-clip:text;background-clip:text;color:transparent">${html}</span>
    </span></div>`;
}
function glass(x, y, w, h, inner, op = 1, accent = 'rgba(255,255,255,.18)', extra = '') {
  return `<div class="glass" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;opacity:${op};border-color:${accent};${extra}">${inner}</div>`;
}
function chip(txt, x, y, bg, fg, size = 28, op = 1, rot = 0, s = 1) {
  return `<div class="chip" style="left:${x}px;top:${y}px;background:${bg};color:${fg};font-size:${size}px;opacity:${op};transform:translate(-50%,-50%) rotate(${rot}deg) scale(${s})">${txt}</div>`;
}
function stamp(txt, x, y, color, size, s, rot = -8) {
  if (s <= 0) return '';
  return `<div class="stamp" style="left:${x}px;top:${y}px;color:${color};border-color:${color};font-size:${size}px;opacity:${clamp(s)};transform:translate(-50%,-50%) rotate(${rot}deg) scale(${s})">${txt}</div>`;
}
function ticker(T, items, y, op = 1) {
  const s = items.map(([t, c]) => `<span style="color:${c};margin:0 28px">${t}</span>`).join('');
  const off = -(T * 120) % 900;
  return `<div class="ticker" style="top:${y}px;opacity:${op}"><div style="transform:translateX(${off}px)">${s}${s}${s}</div></div>`;
}
/* glowing line chart; pts = [[fx 0..1, fy 0..1]], drawn up to progress p */
function glowChart(pts, p, x, y, w, h, color, op = 1, fill = true) {
  const P = pts.map(([fx, fy]) => [x + fx * w, y + h - fy * h]);
  const n = Math.max(1, (P.length - 1) * clamp(p)); const k = Math.floor(n), f = n - k;
  let d = `M${P[0][0]} ${P[0][1]}`;
  for (let i = 1; i <= k; i++) d += ` L${P[i][0]} ${P[i][1]}`;
  let end = P[k];
  if (k < P.length - 1 && f > 0) { end = [lerp(P[k][0], P[k + 1][0], f), lerp(P[k][1], P[k + 1][1], f)]; d += ` L${end[0]} ${end[1]}`; }
  const area = fill ? `<path d="${d} L${end[0]} ${y + h} L${P[0][0]} ${y + h}Z" fill="url(#gradArea${color.slice(1)})" opacity="0.5"/>` : '';
  return [`<g opacity="${op}"><defs><linearGradient id="gradArea${color.slice(1)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${color}" stop-opacity="0.6"/><stop offset="1" stop-color="${color}" stop-opacity="0"/></linearGradient></defs>
    ${area}<path d="${d}" stroke="${color}" stroke-width="16" fill="none" opacity="0.25" filter="url(#blur8)" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" stroke="${color}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="${end[0]}" cy="${end[1]}" r="12" fill="${color}" filter="url(#blur4)"/><circle cx="${end[0]}" cy="${end[1]}" r="8" fill="#fff"/></g>`, end];
}
/* isometric 3D bar */
function isoBar(cx, by, w, h, col, op = 1) {
  const d = w * 0.35;
  return `<g opacity="${op}"><polygon points="${cx - w / 2},${by} ${cx + w / 2},${by} ${cx + w / 2},${by - h} ${cx - w / 2},${by - h}" fill="${col}"/>
    <polygon points="${cx + w / 2},${by} ${cx + w / 2 + d},${by - d} ${cx + w / 2 + d},${by - h - d} ${cx + w / 2},${by - h}" fill="${col}" style="filter:brightness(.65)"/>
    <polygon points="${cx - w / 2},${by - h} ${cx + w / 2},${by - h} ${cx + w / 2 + d},${by - h - d} ${cx - w / 2 + d},${by - h - d}" fill="${col}" style="filter:brightness(1.35)"/></g>`;
}
function coinSVG(x, y, r = 18, op = 1) {
  return `<g opacity="${op}"><ellipse cx="${x}" cy="${y + r * 0.18}" rx="${r}" ry="${r * 0.9}" fill="#A16207"/><circle cx="${x}" cy="${y}" r="${r}" fill="${C.gold}" stroke="#CA8A04" stroke-width="3"/>
    ${svgText(x, y + r * 0.42, '$', r * 1.15, '#854D0E')}</g>`;
}
const BTC = '#F7931A';
/* spinning 3D coin: kind 'btc' | 'xrp'; spin = angle in radians */
function cryptoCoin(kind, x, y, r, spin = 0, op = 1) {
  const sx = Math.max(0.08, Math.abs(Math.cos(spin))), back = Math.cos(spin) < 0;
  const face = kind === 'btc' ? ['#FFD08A', BTC, '#9A5A07'] : ['#E2E8F0', '#64748B', '#0F172A'];
  const id = 'cg' + kind;
  const sym = kind === 'btc' ? svgText(0, r * 0.36, '₿', r * 1.05, '#fff', 900, 'middle', 'style="paint-order:stroke" stroke="#7C3D00" stroke-width="4"')
    : svgText(0, r * 0.2, 'XRP', r * 0.56, '#fff', 900, 'middle', 'letter-spacing="1"');
  let edge = ''; for (let i = 1; i <= 7; i++) edge += `<ellipse cx="${i * (1 - sx) * 2.2 * (back ? -1 : 1)}" cy="${i * 0.6}" rx="${r}" ry="${r}" fill="${face[2]}"/>`;
  return `<g opacity="${op}" transform="translate(${x} ${y}) scale(${sx} 1)">
    <defs><radialGradient id="${id}" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="${face[0]}"/><stop offset=".55" stop-color="${face[1]}"/><stop offset="1" stop-color="${face[2]}"/></radialGradient></defs>
    <circle r="${r * 1.25}" fill="${face[1]}" opacity=".25" filter="url(#blur8)"/>${edge}
    <circle r="${r}" fill="url(#${id})"/><circle r="${r * 0.84}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="3"/>
    ${back ? '' : sym}</g>`;
}
function confettiSVG(T, t0, cx, cy, n = 60, op = 1) {
  if (T < t0) return ''; let g = ''; const r = (s => () => { s = (s * 48271) % 2147483647; return s / 2147483647; })(99);
  const k = T - t0; const cols = [C.gold, C.green, C.cyan, C.red, '#fff', C.purple];
  for (let i = 0; i < n; i++) {
    const a = r() * Math.PI * 2, sp = 250 + r() * 450, vx = Math.cos(a) * sp, vy = Math.sin(a) * sp - 350;
    const x = cx + vx * k, y = cy + vy * k + 600 * k * k, rot = (r() * 720) * k;
    g += `<rect x="${x - 6}" y="${y - 3}" width="12" height="6" fill="${cols[i % cols.length]}" transform="rotate(${rot} ${x} ${y})" opacity="${op * clamp(1.8 - k)}"/>`;
  }
  return g;
}
function followBtn(T, t0) {
  const p = pop(T, t0, 0.45); if (p <= 0) return '';
  const pulse = 1 + 0.04 * Math.sin((T - t0) * 8);
  return `<div class="follow" style="transform:translate(-50%,-50%) scale(${p * pulse})">FOLLOW <span style="font-size:.8em">+</span></div>
    <div class="cursor" style="left:${470 + Math.sin(T * 6) * 6}px;top:${640 + Math.cos(T * 6) * 4}px">➤</div>`;
}

/* ---------- background ---------- */
const PARTS = Array.from({ length: 46 }, () => [rnd() * W, rnd() * H, 2 + rnd() * 7, 10 + rnd() * 40, rnd() * 6.28]);
function background(T, theme) {
  const [c1, c2, c3] = theme;
  const gx = 30 + 20 * Math.sin(T * 0.3), gy = 30 + 15 * Math.cos(T * 0.25);
  document.getElementById('bg').style.background =
    `radial-gradient(circle at ${gx}% ${gy}%, ${c1}aa 0%, transparent 45%), radial-gradient(circle at ${100 - gx}% ${80 - gy * 0.4}%, ${c2}88 0%, transparent 50%), linear-gradient(180deg, ${c3} 0%, #05070D 100%)`;
  let g = '';
  // perspective grid floor
  const vx = 360, vy = 700;
  for (let i = -9; i <= 9; i++) g += `<line x1="${vx}" y1="${vy}" x2="${vx + i * 130}" y2="1280" stroke="${c1}" stroke-opacity="0.18" stroke-width="1.5"/>`;
  for (let k = 0; k < 9; k++) { const f = ((k + (T * 0.6) % 1) / 9); const y = vy + Math.pow(f, 2.2) * 580; g += `<line x1="0" y1="${y}" x2="720" y2="${y}" stroke="${c1}" stroke-opacity="${0.05 + 0.2 * f}" stroke-width="1.5"/>`; }
  // bokeh particles
  for (const [x, y, r, sp, ph] of PARTS) {
    const yy = (y - T * sp) % H, Y = yy < 0 ? yy + H : yy;
    g += `<circle cx="${x + Math.sin(T * 0.5 + ph) * 12}" cy="${Y}" r="${r}" fill="${c2}" opacity="${0.12 + 0.12 * Math.sin(T + ph)}"/>`;
  }
  // light sweep
  const sx = ((T * 160) % 1600) - 400;
  g += `<rect x="${sx}" y="-200" width="120" height="1700" fill="url(#sweep)" transform="rotate(18 ${sx} 640)" opacity="0.35"/>`;
  return g;
}
const DEFS = `<defs><filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
  <filter id="blur4" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>`;

/* ---------- captions: chunked, word highlight ---------- */
function captions(T) {
  let k = -1;
  for (let i = 0; i < TIM.length; i++) if (T >= st(i) - 0.05 && T <= (i + 1 < TIM.length ? st(i + 1) - 0.05 : TOTAL)) k = i;
  if (k < 0) return '';
  const words = LINES[k].split(' '), [a, b] = TIM[k], total = LINES[k].length;
  const times = []; let acc = 0;
  for (const w of words) { times.push(a + (b - a) * acc / total); acc += w.length + 1; }
  const chunks = []; let cur = [];
  words.forEach((w, i) => { cur.push(i); if (cur.length >= 5 || /[.?!,:…]$/.test(w) && cur.length >= 2) { chunks.push(cur); cur = []; } });
  if (cur.length) chunks.push(cur);
  let ci = 0; for (let c = 0; c < chunks.length; c++) if (T >= times[chunks[c][0]] - 0.05) ci = c;
  let html = '';
  for (const i of chunks[ci]) {
    if (T < times[i] - 0.03) { html += `<span class="w" style="opacity:0">${words[i]}</span>`; continue; }
    const curW = T < (times[i + 1] ?? b + 0.2);
    const s = pop(T, times[i], 0.16), num = /[$\d%]/.test(words[i]);
    html += `<span class="w${curW ? ' cur' : ''}" style="transform:scale(${s.toFixed(3)});${num && !curW ? 'color:#4ADE80' : ''}">${words[i]}</span>`;
  }
  return `<div class="cap">${html}</div>`;
}

/* ---------- frame ---------- */
let SHAKES = [], FLASHES = [];
function renderFrame(T, R) {
  hidePhotos();
  const [g, o] = R.scene(T);
  let sh = 0; for (const t0 of SHAKES) { const k = T - t0; if (k >= 0 && k < 0.45) sh = Math.max(sh, (1 - k / 0.45) * 14); }
  const sx = sh ? (Math.sin(T * 91) * sh) : 0, sy = sh ? (Math.cos(T * 77) * sh) : 0;
  document.getElementById('cam').style.transform = `translate(${sx}px,${sy}px)`;
  let fl = 0; for (const t0 of FLASHES) { const k = T - t0; if (k >= 0 && k < 0.35) fl = Math.max(fl, 0.75 * (1 - k / 0.35)); }
  document.getElementById('flash').style.opacity = fl;
  document.getElementById('svg').innerHTML = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${DEFS}${background(T, R.theme)}${g}</svg>`;
  const prog = clamp(T / TOTAL);
  document.getElementById('ov').innerHTML = o +
    `<div class="prog"><div style="width:${prog * 100}%"></div></div>` +
    `<div class="head">${R.head}</div>` + captions(T) + `<div class="disc">${R.disc}</div>`;
}
