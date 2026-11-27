// Teaser timeline. seek(t, variant) draws the frame at time t (seconds) from scratch.
// variant: 'teaser' (ends on «عرفتوها؟», 15.5 s) or 'reveal' (stamp «دقاش · توزر», 17 s).
(function () {
  const T = window.TEASER;
  const $ = id => document.getElementById(id);
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, p) => a + (b - a) * p;
  const P = (t, a, b) => clamp((t - a) / (b - a));
  const eo = p => 1 - Math.pow(1 - p, 3);
  const eio = p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
  const eback = p => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); };
  const show = (el, on) => { el.style.display = on ? '' : 'none'; };

  const stars = [...document.querySelectorAll('.tw')].map(e => [e, +e.dataset.p, +e.dataset.s]);
  const refl = [...document.querySelectorAll('.rf')].map(e => [e, +e.dataset.p]);
  const waves = [...document.querySelectorAll('.wave')].map(e => [e, +e.dataset.P, +e.dataset.v]);
  const trail = $('trailPath'), mask = $('trailMaskPath');
  const TL = trail.getTotalLength();
  const look = []; for (let i = 0; i <= 800; i++) { const l = TL * i / 800; look.push([l, trail.getPointAtLength(l).y]); }
  const lenAtY = y => { let best = 0; for (const [l, yy] of look) { if (yy <= y) best = l; else break; } return best; };
  const [PX, PY] = T.pin;

  // torn top edge on the logbook page
  (() => { const pts = ['0% 100%', '100% 100%']; let x = 100; let k = 0;
    while (x > 0) { pts.push(`${x.toFixed(2)}% ${(k % 2 ? 4 : 10) + (k * 7 % 5)}px`); x -= 1.6 + (k * 13 % 7) * .25; k++; }
    pts.push('0% 8px'); document.querySelector('.paper').style.clipPath = `polygon(${pts.join(',')})`; })();

  const BASE = [[-26, 10, -5.5], [28, -14, 4.2], [-14, 18, -2.6], [20, -8, 3.4]];
  const PUSH = [[10, -6, .8], [-12, 8, -.9], [8, 6, .6], [0, 0, 0]];
  const CT = i => 4.75 + 1.6 * i;          // clue i lands at CT(i)+0.42

  window.DURATION = { teaser: 15.5, reveal: 17.0 };

  window.seek = function (t, variant) {
    const R = variant === 'reveal';
    const DUR = R ? 17.0 : 15.5;
    const loopBack = t >= DUR - 0.6;           // the last half second fades back into frame 0
    const ht = loopBack ? 0 : t;              // hook time
    const wt = loopBack ? t - DUR : t;        // ambient time (stars, waves); runs on into the next loop

    // ---------------- world (S1-S2)
    const camY = loopBack ? 0 : (t < 2.05 ? 0 : eio(P(t, 2.05, 4.55)) * T.camEnd);
    const z = loopBack ? 1 : 1 + 1.7 * eio(P(t, 4.4, 4.82));
    $('world').style.transform = `translate(0px,${-camY}px) translate(${PX}px,${PY}px) scale(${z}) translate(${-PX}px,${-PY}px)`;
    const worldOn = loopBack || t < 4.85;
    show($('cam'), worldOn);
    if (worldOn) {
      // shake on the «لوين؟» slam
      const sp = P(ht, .74, .95);
      const sh = (ht > .74 && ht < .95) ? 16 * (1 - sp) : 0;
      $('cam').style.transform = `translate(${sh * Math.sin(ht * 97)}px,${sh * Math.cos(ht * 83)}px)`;
      for (const [e, p, s] of stars) e.setAttribute('opacity', (.35 + .65 * (.5 + .5 * Math.sin(wt * s + p))).toFixed(3));
      for (const [e, p] of refl) e.setAttribute('opacity', (.12 + .5 * (.5 + .5 * Math.sin(wt * 3.1 + p * 2))).toFixed(3));
      for (const [e, Pd, v] of waves) { const off = (((wt * v) % Pd) + Pd) % Pd; e.setAttribute('transform', `translate(${(off - Pd).toFixed(1)} 0)`); }
      $('beam').setAttribute('transform', `rotate(${(-28 + wt * 38).toFixed(2)} 975 860)`);
      $('boat').setAttribute('transform', `translate(${360 + wt * 6} ${1430 + 6 * Math.sin(wt * 2.2)}) rotate(${2.5 * Math.sin(wt * 2.2 + .8)})`);
      $('lampGlow').setAttribute('opacity', (.75 + .25 * Math.sin(wt * 6)).toFixed(3));
      $('foam').setAttribute('transform', `translate(${((wt * 34) % 140).toFixed(1)} 0)`);
      // hook text
      $('hk1').style.transform = `scale(${lerp(.94, 1, eo(P(ht, 0, .45)))})`;
      const p2 = P(ht, .5, .76);
      $('hk2').style.opacity = P(ht, .5, .57);
      $('hk2').style.transform = `scale(${lerp(2.3, 1, eback(p2))})`;
      $('hk3').style.opacity = P(ht, 1.1, 1.45);
      $('hk3').style.transform = `translateY(${lerp(34, 0, eo(P(ht, 1.1, 1.5)))}px)`;
      // trail draws as the camera travels
      let len = 0;
      if (!loopBack && t > 2.3) len = Math.min(TL, lenAtY(camY + 1150 + 80 * P(t, 4.15, 4.45)));
      mask.setAttribute('stroke-dasharray', `${len.toFixed(1)} ${TL.toFixed(1)}`);
      const hp = trail.getPointAtLength(Math.max(1, len));
      const headOn = len > 2 && len < TL - 4 ? 1 : 0;
      for (const id of ['head', 'headGlow']) { $(id).setAttribute('cx', hp.x.toFixed(1)); $(id).setAttribute('cy', hp.y.toFixed(1)); $(id).setAttribute('opacity', headOn); }
      // the «؟» pin drops in
      const pp = P(t, 4.12, 4.42);
      $('pin').setAttribute('opacity', loopBack ? 0 : P(t, 4.12, 4.17));
      $('pin').setAttribute('transform', `translate(${PX} ${PY + lerp(-160, 0, eback(pp))}) scale(${lerp(.6, 1, eo(pp))})`);
      const rp = ((t * 1.7) % 1);
      $('pinRing').setAttribute('r', (40 + 46 * rp).toFixed(1)); $('pinRing').setAttribute('opacity', (1 - rp).toFixed(2));
    }
    // journey overlay
    const jOut = 1 - P(t, 4.32, 4.52);
    $('scrim').style.opacity = loopBack ? 0 : P(t, 2.2, 2.6) * jOut;
    $('jr1').style.opacity = loopBack ? 0 : P(t, 2.6, 2.9) * jOut;
    $('jr1').style.transform = `translateY(${lerp(30, 0, eo(P(t, 2.6, 2.95)))}px)`;
    $('jr2').style.opacity = loopBack ? 0 : P(t, 2.95, 3.02) * jOut;
    $('jr2').style.transform = `scale(${lerp(1.8, 1, eback(P(t, 2.95, 3.22)))})`;

    // ---------------- logbook (S3-S6, and the pile in S7)
    const endStart = R ? 13.6 : 13.1;
    const bookOn = t >= 4.48 && t < endStart + 0.45 && !loopBack;
    show($('book'), bookOn);
    if (bookOn) {
      $('book').style.transform = `translateY(${lerp(1920, 0, eo(P(t, 4.48, 4.8)))}px)`;
      let landed = 0;
      for (let i = 0; i < 4; i++) {
        const c = $('card' + i), ti = CT(i);
        if (t < ti) { c.style.opacity = 0; continue; }
        const p = P(t, ti, ti + .42);
        if (t >= ti + .3) landed = i + 1;
        let [bx, by, br] = BASE[i];
        let dark = 0;
        for (let k = i + 1; k < 4; k++) { const q = eo(P(t, CT(k) + .3, CT(k) + .55)); bx += PUSH[i][0] * q; by += PUSH[i][1] * q; br += PUSH[i][2] * q; dark += .05 * q; }
        const y = lerp(-1350, by, eback(p)), x = lerp(bx + (i % 2 ? 160 : -160), bx, eo(p));
        const r = lerp(br + (i % 2 ? 26 : -26), br, eo(p)), s = lerp(1.22, 1, eo(p));
        c.style.opacity = 1;
        c.style.transform = `translate(${x}px,${y}px) rotate(${r}deg) scale(${s})`;
        c.style.filter = dark > 0 ? `brightness(${1 - dark})` : '';
        const tape = c.querySelector('.tape');
        tape.style.opacity = P(t, ti + .36, ti + .46);
        tape.style.transform = `rotate(${i % 2 ? 5 : -4}deg) scale(${lerp(1.3, 1, eo(P(t, ti + .36, ti + .5)))})`;
        $('cap' + i).style.clipPath = `inset(0 0 0 ${((1 - eo(P(t, ti + .45, ti + 1.0))) * 100).toFixed(1)}%)`;
        const num = c.querySelector('.num');
        num.style.opacity = P(t, ti + .28, ti + .34);
        num.style.transform = `scale(${lerp(2.2, 1, eback(P(t, ti + .28, ti + .5)))}) rotate(${i % 2 ? -8 : 10}deg)`;
      }
      const n = Math.max(1, landed);
      $('bkN').textContent = `تلميح ${n} / 4`;
      const lastLand = CT(n - 1) + .3;
      const cp = P(t, lastLand, lastLand + .22);
      $('bkN').parentElement.style.transform = `rotate(-4deg) scale(${t >= lastLand && cp < 1 ? lerp(1.25, 1, eo(cp)) : 1})`;

      if (!R) {
        const q = eio(P(t, 11.15, 11.65));
        $('night').style.opacity = .92 * eo(P(t, 11.15, 11.6));
        $('pileWrap').style.transform = `translateY(${lerp(0, -440, q)}px) scale(${lerp(1, .6, q)})`;
        $('bkHead').style.opacity = 1 - P(t, 11.15, 11.4);
        $('bkNote').style.opacity = 1 - P(t, 11.15, 11.4);
        $('stampWrap').style.opacity = 0;
      } else {
        // the stamp slams onto the pile, then the answer completes the hook
        const sp = P(t, 11.25, 11.48);
        $('stampWrap').style.opacity = P(t, 11.25, 11.29);
        $('stampWrap').style.transform = `rotate(-9deg) scale(${lerp(2.6, 1, sp * sp)})`;
        const q = eio(P(t, 12.3, 12.8));
        $('night').style.opacity = .92 * eo(P(t, 12.3, 12.75));
        $('pileWrap').style.transform = `translateY(${lerp(0, -440, q)}px) scale(${lerp(1, .6, q)})`;
        $('bkHead').style.opacity = 1 - P(t, 12.3, 12.55);
        $('bkNote').style.opacity = 1 - P(t, 11.1, 11.3);
        const bs = (t > 11.48 && t < 11.68) ? 12 * (1 - P(t, 11.48, 11.68)) : 0;
        $('book').style.transform += ` translate(${bs * Math.sin(t * 101)}px,${bs * Math.cos(t * 89)}px)`;
      }
    }

    // ---------------- S7
    const askOn = !R && t >= 11.4 && t < endStart + 0.45 && !loopBack;
    show($('ask'), askOn);
    if (askOn) {
      $('ask').style.opacity = 1;
      $('ask1').style.opacity = P(t, 11.45, 11.52);
      $('ask1').style.transform = `scale(${lerp(1.9, 1, eback(P(t, 11.45, 11.74)))})`;
      $('ask2').style.opacity = P(t, 11.9, 12.1);
      $('ask2').style.transform = `translateX(-50%) translateY(${lerp(40, 0, eo(P(t, 11.9, 12.2)))}px)`;
      $('arrow').style.opacity = P(t, 12.1, 12.25);
      $('arrow').style.transform = `translate(${6 * Math.sin(t * 8)}px,${12 * Math.sin(t * 8)}px)`;
    }
    const ansOn = R && t >= 12.55 && t < endStart + 0.45 && !loopBack;
    show($('ans'), ansOn);
    if (ansOn) {
      $('ans').style.opacity = 1;
      $('ans1').style.opacity = P(t, 12.6, 12.8);
      $('ans1').style.transform = `translateY(${lerp(36, 0, eo(P(t, 12.6, 12.9)))}px)`;
      $('ans2').style.opacity = P(t, 12.85, 12.92);
      $('ans2').style.transform = `scale(${lerp(1.9, 1, eback(P(t, 12.85, 13.12)))})`;
    }

    // ---------------- S8 end cards
    const end = R ? $('endR') : $('end');
    show($('end'), !R); show($('endR'), R);
    const eOp = P(t, endStart, endStart + .3) * (1 - P(t, DUR - .5, DUR - 1 / 30));
    end.style.opacity = eOp;
    if (eOp > 0) {
      const s0 = endStart + .15;
      const pop = (sel, a, from = .9) => { const e = end.querySelector(sel); if (!e) return; const p = P(t, a, a + .3);
        e.style.opacity = P(t, a, a + .12); e.style.transform = (sel === '.e-call' ? 'translateX(-50%) ' : '') + `scale(${lerp(from, 1, eback(p))})`; };
      const rise = (sel, a) => { const e = end.querySelector(sel); if (!e) return;
        e.style.opacity = P(t, a, a + .25); e.style.transform = `translateY(${lerp(30, 0, eo(P(t, a, a + .35)))}px)`; };
      pop('.logos', s0, .85);
      pop('.e-title', s0 + .1, 1.5);
      rise('.e-date', s0 + .3);
      if (!R) {
        const e = end.querySelector('.e-soon'); e.style.opacity = P(t, s0 + .45, s0 + .5);
        e.style.clipPath = `inset(0 0 0 ${((1 - eo(P(t, s0 + .45, s0 + 1.0))) * 100).toFixed(1)}%)`;
        rise('.e-who', s0 + .65); rise('.e-org', s0 + .8);
      } else {
        pop('.e-place', s0 + .45, 1.6); rise('.e-who', s0 + .65); rise('.e-price', s0 + .8); pop('.e-call', s0 + 1.0, 1.3);
      }
    }

    // ---------------- flashes, grain
    let fl = 0;
    if (ht > .72 && ht < .9) fl = .32 * (1 - P(ht, .72, .9));
    if (R && t > 11.47 && t < 11.62) fl = .28 * (1 - P(t, 11.47, 11.62));
    $('flash').style.opacity = fl;
    const f = Math.round(t * 30);
    $('grain').style.backgroundPosition = `${(f * 37) % 256}px ${(f * 91) % 256}px`;
  };
})();
