(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var menu = document.getElementById('nav-menu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) { menu.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  // Contact form -> mailto with a readable body (no backend)
  var form = document.getElementById('quote-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var subject = 'Project request: ' + d.get('service') + ' — ' + d.get('name');
      var body = [
        'Name: ' + d.get('name'),
        'Email: ' + d.get('email'),
        'Service: ' + d.get('service'),
        'Budget: ' + d.get('budget'),
        '',
        d.get('message')
      ].join('\n');
      window.location.href = 'mailto:' + form.dataset.email +
        '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }

  // "Book a call" falls back to a prefilled email when no booking URL is configured
  document.querySelectorAll('[data-cta="call"]').forEach(function (a) {
    if (a.getAttribute('href') === '#contact' && form) {
      a.addEventListener('click', function () {
        var msg = document.getElementById('f-msg');
        if (msg && !msg.value) msg.value = "I'd like to book a free 20-minute call. Good times for me: ";
      });
    }
  });
})();
