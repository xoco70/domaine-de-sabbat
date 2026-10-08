// Domaine de Sabbat — interactions légères (menu mobile, formulaire de contact)
(function () {
  'use strict';

  // Menu mobile
  var toggle = document.getElementById('menu-toggle');
  var menu = document.getElementById('mobile-menu');
  if (toggle && menu) {
    var setOpen = function (open) {
      toggle.setAttribute('aria-expanded', String(open));
      menu.hidden = !open;
      document.body.classList.toggle('overflow-hidden', open);
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !menu.hidden) { setOpen(false); toggle.focus(); }
    });
    window.matchMedia('(min-width: 1024px)').addEventListener('change', function (e) {
      if (e.matches) setOpen(false);
    });
  }

  // Ombre de l'en-tête au défilement
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('shadow-lg', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Formulaire de contact : site statique, on compose un e-mail pré-rempli
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var t = (form.dataset.labels || 'Message du site|Nom|Adresse|E-mail|Téléphone').split('|');
      var subject = t[0] + ' — ' + d.get('nom');
      var body = [
        t[1] + ' : ' + d.get('nom'),
        t[2] + ' : ' + (d.get('adresse') || '—'),
        t[3] + ' : ' + d.get('email'),
        t[4] + ' : ' + d.get('telephone'),
        '',
        d.get('message'),
      ].join('\n');
      window.location.href = 'mailto:' + form.dataset.to +
        '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      var note = document.getElementById('contact-note');
      if (note) note.hidden = false;
    });
  }

  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
