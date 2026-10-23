(() => {
  'use strict';
  const WA_NUMBER = '50256029990';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // sticky header turns solid after the hero starts scrolling
  const header = document.querySelector('.header');
  const onScroll = () => header.classList.toggle('solid', scrollY > 24);
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // mobile menu
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
  };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.addEventListener('click', (e) => e.target.closest('a') && setMenu(false));
  addEventListener('keydown', (e) => e.key === 'Escape' && setMenu(false));

  // staggered reveal on scroll
  document.querySelectorAll('.cards, .why, .stats-grid, .repair-list, .steps, .phones').forEach((group) => {
    [...group.children].forEach((el, i) => el.style.setProperty('--d', `${i * 0.08}s`));
  });
  const revealEls = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach((el) => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      }),
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' },
    );
    revealEls.forEach((el) => io.observe(el));
  }

  // count-up numbers
  const counters = document.querySelectorAll('[data-count]');
  const run = (el) => {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduce) { el.textContent = target + suffix; return; }
    const start = performance.now();
    const dur = 1400;
    const tick = (t) => {
      const p = Math.min((t - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries) => entries.forEach((e) => {
      if (e.isIntersecting) { run(e.target); co.unobserve(e.target); }
    }), { threshold: 0.6 });
    counters.forEach((c) => co.observe(c));
  } else counters.forEach(run);

  // hero product follows the pointer a little (desktop only)
  const art = document.querySelector('.hero-art');
  const product = document.getElementById('heroProduct');
  if (art && product && !reduce && matchMedia('(hover: hover)').matches) {
    document.querySelector('.hero').addEventListener('pointermove', (e) => {
      const r = art.getBoundingClientRect();
      const x = (e.clientX - (r.left + r.width / 2)) / r.width;
      const y = (e.clientY - (r.top + r.height / 2)) / r.height;
      product.style.transform = `rotate(${-12 + x * 8}deg) translate(${x * 18}px, ${y * 14}px)`;
    });
  }

  // repair request -> prefilled WhatsApp message
  const form = document.getElementById('quoteForm');
  const err = document.getElementById('quoteErr');
  form && form.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const nombre = String(f.get('nombre') || '').trim();
    err.hidden = !!nombre;
    if (!nombre) return form.elements.nombre.focus();
    const detalle = String(f.get('detalle') || '').trim();
    const text = `Hola petXpert, soy ${nombre}. Necesito reparar mi equipo: ${f.get('equipo')}.` + (detalle ? ` Detalle: ${detalle}` : '');
    window.open(`https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
