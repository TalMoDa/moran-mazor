/* ============================================================
   מורן זילכה מזור — סקריפט האתר
   אין שרת ואין API: הטופס מרכיב הודעת וואטסאפ / דוא"ל בצד הלקוח.
   ============================================================ */
(function () {
  'use strict';

  /* ---- פרטי יצירת קשר (מקור אמת יחיד לטופס) ----
     לעדכון: שנו כאן וגם בקישורים שב-HTML (ראו CONTENT.md). */
  var CONTACT = {
    whatsapp: '972500000000',            // מספר בפורמט בינלאומי, בלי + ובלי מקפים
    email: 'office@zilka-mazor.co.il'
  };

  var root = document.documentElement;
  var body = document.body;

  /* ---------- 1. כותרת דביקה ---------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- 2. תפריט מובייל ---------- */
  var burger = document.querySelector('.burger');
  var panel = document.querySelector('.nav-panel');
  if (burger && panel) {
    var setMenu = function (open) {
      body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', String(open));
      panel.setAttribute('aria-hidden', String(!open));
      body.style.overflow = open ? 'hidden' : '';
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
    setMenu(false);
  }

  /* ---------- 3. חשיפה בגלילה ---------- */
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
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    revealables.forEach(function (el, i) {
      // השהיה מדורגת בתוך אותה קבוצה
      if (!el.style.getPropertyValue('--d')) {
        var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : i;
        el.style.setProperty('--d', Math.min(sibs, 5) * 90 + 'ms');
      }
      io.observe(el);
    });
  }

  /* ---------- 4. אנימציית פתיחה של ההירו ---------- */
  var hero = document.querySelector('.hero');
  if (hero) requestAnimationFrame(function () { hero.classList.add('is-in'); });

  /* ---------- 5. סימון הסעיף הפעיל בתפריט ---------- */
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
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- 6. שנה נוכחית ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- 7. טופס יצירת קשר — ללא שרת ---------- */
  var form = document.querySelector('#contact-form');
  if (form) {
    var status = form.querySelector('.form__status');

    var compose = function (d) {
      var lines = [
        'שלום מורן, הגעתי דרך האתר.',
        '',
        'שם: ' + d.name,
        'טלפון: ' + d.phone,
        d.email ? 'דוא"ל: ' + d.email : '',
        'נושא: ' + d.topic,
        '',
        d.message
      ];
      return lines.filter(function (l) { return l !== ''; }).join('\n');
    };

    var submitVia = function (channel) {
      if (!form.reportValidity()) return;
      // שימו לב: form.name מחזיר את שם הטופס ולא את השדה — לכן ניגשים דרך elements
      var val = function (n) {
        var el = form.elements[n];
        return el && el.value ? el.value.trim() : '';
      };
      var data = {
        name: val('name'),
        phone: val('phone'),
        email: val('email'),
        topic: val('topic'),
        message: val('message')
      };
      var text = compose(data);
      var url;
      if (channel === 'email') {
        url = 'mailto:' + CONTACT.email +
              '?subject=' + encodeURIComponent('פנייה מהאתר — ' + data.topic) +
              '&body=' + encodeURIComponent(text);
      } else {
        url = 'https://wa.me/' + CONTACT.whatsapp + '?text=' + encodeURIComponent(text);
      }
      window.open(url, channel === 'email' ? '_self' : '_blank', 'noopener');
      if (status) {
        status.textContent = channel === 'email'
          ? 'נפתחה תוכנת הדוא"ל שלך עם פרטי הפנייה — נותר רק לשלוח.'
          : 'נפתח וואטסאפ עם פרטי הפנייה — נותר רק ללחוץ שליחה.';
      }
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submitVia('whatsapp');
    });

    var mailBtn = form.querySelector('[data-send="email"]');
    if (mailBtn) {
      mailBtn.addEventListener('click', function (e) {
        e.preventDefault();
        submitVia('email');
      });
    }
  }


  /* ---------- 9. תפריט נגישות ---------- */
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

  /* ---------- 8. גלילה רכה עם כיבוד prefers-reduced-motion ---------- */
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    root.style.scrollBehavior = 'auto';
  }
})();
