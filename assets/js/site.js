/* ============================================================
   עו״ד מורן זילכה מזור — סקריפט האתר
   אין שרת ואין API: הטופס מרכיב הודעת וואטסאפ / דוא"ל בצד הלקוח.
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;
  var body = document.body;

  /* ---------- 1. תפריט מובייל ---------- */
  var burger = document.querySelector('.burger');
  var panel = document.querySelector('.nav-panel');
  if (burger && panel) {
    var setMenu = function (open) {
      body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', String(open));
    };
    burger.addEventListener('click', function () {
      setMenu(!body.classList.contains('nav-open'));
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) setMenu(false);
    });
  }

  /* ---------- 1b. כיווץ הכותרת + מד התקדמות גלילה ---------- */
  var header = document.querySelector('.site-header');
  var progress = document.querySelector('#progress');
  if (header || progress) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY || 0;
        if (header) header.classList.toggle('is-scrolled', y > 40);
        if (progress) {
          var max = document.documentElement.scrollHeight - window.innerHeight;
          progress.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
        }
        ticking = false;
      });
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
  }

  /* ---------- 2. חשיפה בגלילה ---------- */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (!('IntersectionObserver' in window)) {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.08 });
    revealables.forEach(function (el, i) {
      if (!el.style.getPropertyValue('--d')) {
        var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : i;
        el.style.setProperty('--d', Math.min(sibs, 5) * 70 + 'ms');
      }
      io.observe(el);
    });
  }

  /* ---------- 3. סימון הסעיף הפעיל בתפריט ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.id;
        navLinks.forEach(function (a) {
          a.setAttribute('aria-current', a.getAttribute('href') === '#' + id ? 'true' : 'false');
        });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- 4. שנה נוכחית ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- 5. קרוסלת ציטוטים ---------- */
  var track = document.querySelector('#quotes');
  if (track) {
    var slides = Array.prototype.slice.call(track.querySelectorAll('.quote-slide'));
    var dotsWrap = document.querySelector('#quote-dots');
    var index = 0;
    var timer = null;

    var show = function (i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.classList.toggle('is-active', n === index); });
      if (dotsWrap) {
        dotsWrap.querySelectorAll('button').forEach(function (d, n) {
          d.setAttribute('aria-current', n === index ? 'true' : 'false');
        });
      }
    };
    var start = function () {
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      if (root.classList.contains('a11y-nomotion')) return;
      stop();
      timer = setInterval(function () { show(index + 1); }, 7000);
    };
    var stop = function () { if (timer) { clearInterval(timer); timer = null; } };

    if (dotsWrap) {
      slides.forEach(function (_, n) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'ציטוט ' + (n + 1));
        b.addEventListener('click', function () { show(n); start(); });
        dotsWrap.appendChild(b);
      });
    }
    var prev = document.querySelector('.quote-nav--prev');
    var next = document.querySelector('.quote-nav--next');
    if (prev) prev.addEventListener('click', function () { show(index - 1); start(); });
    if (next) next.addEventListener('click', function () { show(index + 1); start(); });

    var band = document.querySelector('.quote-band');
    if (band) {
      band.addEventListener('mouseenter', stop);
      band.addEventListener('mouseleave', start);
      band.addEventListener('focusin', stop);
    }
    show(0);
    start();
  }

  /* ---------- 6. חלונות תחומי עיסוק ---------- */
  var openCard = null;
  var openModal = function (id) {
    var dlg = document.getElementById(id);
    if (!dlg) return;
    if (typeof dlg.showModal === 'function') dlg.showModal();
    else dlg.setAttribute('open', '');       // נפילה אחורה בדפדפנים ישנים
  };
  document.querySelectorAll('[data-modal]').forEach(function (card) {
    var trigger = function (e) {
      if (e.type === 'keydown' && e.key !== 'Enter' && e.key !== ' ') return;
      e.preventDefault();
      openCard = card;
      openModal(card.getAttribute('data-modal'));
    };
    card.addEventListener('click', trigger);
    card.addEventListener('keydown', trigger);
  });
  document.querySelectorAll('dialog.modal').forEach(function (dlg) {
    var close = function () {
      if (typeof dlg.close === 'function') dlg.close();
      else dlg.removeAttribute('open');
      if (openCard) { openCard.focus(); openCard = null; }
    };
    dlg.querySelectorAll('.modal__close').forEach(function (b) { b.addEventListener('click', close); });
    dlg.querySelectorAll('[data-close-go]').forEach(function (a) { a.addEventListener('click', close); });
    // לחיצה על הרקע סוגרת
    dlg.addEventListener('click', function (e) {
      if (e.target === dlg) close();
    });
  });

  /* ---------- 7. תפריט נגישות ---------- */
  var a11yBtn = document.querySelector('.a11y__btn');
  var a11yPanel = document.querySelector('.a11y__panel');
  if (a11yBtn && a11yPanel) {
    var KEY = 'mzm-a11y';
    var state = { contrast: false, links: false, readable: false, nomotion: false, font: 0 };
    try { state = Object.assign(state, JSON.parse(localStorage.getItem(KEY) || '{}')); } catch (e) {}

    var apply = function () {
      root.classList.toggle('a11y-contrast', !!state.contrast);
      root.classList.toggle('a11y-links', !!state.links);
      root.classList.toggle('a11y-readable', !!state.readable);
      root.classList.toggle('a11y-nomotion', !!state.nomotion);
      root.style.fontSize = state.font ? (100 + state.font * 12.5) + '%' : '';
      a11yPanel.querySelectorAll('[data-a11y]').forEach(function (b) {
        var k = b.getAttribute('data-a11y');
        if (k in state && typeof state[k] === 'boolean') b.setAttribute('aria-pressed', String(state[k]));
      });
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
    };

    var togglePanel = function (open) {
      a11yPanel.hidden = !open;
      a11yBtn.setAttribute('aria-expanded', String(open));
    };

    a11yBtn.addEventListener('click', function () { togglePanel(a11yPanel.hidden); });
    document.addEventListener('click', function (e) {
      if (!a11yPanel.hidden && !e.target.closest('.a11y')) togglePanel(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !a11yPanel.hidden) { togglePanel(false); a11yBtn.focus(); }
    });
    a11yPanel.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-a11y]');
      if (!btn) return;
      var k = btn.getAttribute('data-a11y');
      if (k === 'font-up') state.font = Math.min(state.font + 1, 3);
      else if (k === 'font-down') state.font = Math.max(state.font - 1, -1);
      else if (k === 'reset') state = { contrast: false, links: false, readable: false, nomotion: false, font: 0 };
      else state[k] = !state[k];
      apply();
    });

    apply();
    togglePanel(false);
  }

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    root.style.scrollBehavior = 'auto';
  }
})();
