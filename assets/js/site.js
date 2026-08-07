// Confetti burst on every CTA click — rewards the conversion action, not the page load.
// Rolled Canvas2D physics, no libraries. Never blocks the button's real action (no preventDefault).
(function () {
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  // Read from the palette tokens so confetti follows any future colour change.
  var rootStyle = getComputedStyle(document.documentElement);
  function token(name, fallback) {
    var v = rootStyle.getPropertyValue(name).trim();
    return v || fallback;
  }
  var COLORS = [
    token('--accent', '#e3452f'),
    token('--accent-bright', '#f0563f'),
    token('--cream', '#f4efe6'),
    token('--ink-panel-2', '#242424')
  ];
  var MAX_PARTICLES = 140;
  var GRAVITY = 0.14;
  var DECAY = 0.012;

  var canvas, ctx, particles = [], rafId = null, lastT = 0, resizeTimer = null;

  function ensureCanvas() {
    if (canvas) return;
    canvas = document.createElement('canvas');
    canvas.setAttribute('aria-hidden', 'true');
    canvas.style.cssText = 'position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:9999;';
    document.body.appendChild(canvas);
    resize();
    window.addEventListener('resize', scheduleResize);
  }

  function scheduleResize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 150);
  }

  function resize() {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function burst(x, y) {
    ensureCanvas();
    var count = 42;
    for (var i = 0; i < count && particles.length < MAX_PARTICLES; i++) {
      var angle = Math.PI + Math.random() * Math.PI; // upward-biased spread
      var speed = 3 + Math.random() * 5;
      particles.push({
        x: x, y: y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 2,
        size: 4 + Math.random() * 5,
        rot: Math.random() * Math.PI * 2,
        vr: (Math.random() - 0.5) * 0.3,
        color: COLORS[(Math.random() * COLORS.length) | 0],
        life: 1
      });
    }
    if (!rafId) rafId = requestAnimationFrame(tick);
  }

  function tick(t) {
    if (!lastT) lastT = t;
    var dt = Math.min((t - lastT) / 16.67, 2);
    lastT = t;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var alive = false;
    for (var i = particles.length - 1; i >= 0; i--) {
      var p = particles[i];
      p.vy += GRAVITY * dt;
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.rot += p.vr * dt;
      p.life -= DECAY * dt;
      if (p.life <= 0) { particles.splice(i, 1); continue; }
      alive = true;
      ctx.save();
      ctx.globalAlpha = Math.max(p.life, 0);
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.fillStyle = p.color;
      ctx.fillRect(-p.size / 2, -p.size / 3, p.size, p.size * 0.6);
      ctx.restore();
    }

    if (alive) {
      rafId = requestAnimationFrame(tick);
    } else {
      rafId = null;
      lastT = 0;
      if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
  }

  document.querySelectorAll('.btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var r = btn.getBoundingClientRect();
      burst(r.left + r.width / 2, r.top + r.height / 2);
    });
  });
})();

// Mobile nav toggle
(function () {
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('mobileNav');
  if (!toggle || !nav) return;

  function closeMenu() {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    nav.classList.remove('is-open');
  }
  function openMenu() {
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Close menu');
    nav.classList.add('is-open');
  }

  toggle.addEventListener('click', function () {
    var isOpen = toggle.getAttribute('aria-expanded') === 'true';
    if (isOpen) closeMenu(); else openMenu();
  });

  nav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  document.addEventListener('click', function (e) {
    if (!nav.contains(e.target) && !toggle.contains(e.target)) closeMenu();
  });
})();

// Back-to-top button
(function () {
  var btn = document.getElementById('backToTop');
  if (!btn) return;
  var threshold = window.innerHeight * 0.8;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function onScroll() {
    if (window.scrollY > threshold) btn.classList.add('is-visible');
    else btn.classList.remove('is-visible');
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });
})();

// Quote form -> POST /api/contact (Vercel serverless fn, sends via Resend).
// The API accepts exactly: name, email, phone, event-date, event-type, message.
// It REQUIRES name, email, phone and event-date, and silently ignores anything else,
// so "venue" is appended to message rather than sent as its own field.
(function () {
  var form = document.getElementById('quoteForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var PHONE = '647.375.0660';

  function say(msg, state) {
    if (!status) return;
    status.textContent = msg;
    status.className = 'form-status' + (state ? ' is-' + state : '');
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var button = form.querySelector('button[type="submit"]');
    var original = button.textContent;

    // Let the browser surface its own field-level messages first.
    if (!form.checkValidity()) {
      form.reportValidity();
      say('Check the highlighted fields and try again.', 'error');
      return;
    }

    var data = {};
    new FormData(form).forEach(function (value, key) { data[key] = value; });

    // Fold venue into the message body so it reaches the inbox.
    var venue = (data.venue || '').trim();
    delete data.venue;
    if (venue) {
      data.message = (data.message ? data.message.trim() + '\n\n' : '') + 'Venue / city: ' + venue;
    }

    button.disabled = true;
    button.textContent = 'Sending…';
    say('Sending…');

    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        return res.json().catch(function () {
          throw new Error('Server returned ' + res.status + ' ' + res.statusText);
        }).then(function (result) {
          if (!res.ok) throw new Error(result.error || result.details || 'Something went wrong.');
          return result;
        });
      })
      .then(function () {
        form.reset();
        say('Got it. We’ll come back with availability and a quote, usually same day.', 'ok');
      })
      .catch(function (err) {
        say(err.message + ' Please try again, or call ' + PHONE + '.', 'error');
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = original;
      });
  });
})();
