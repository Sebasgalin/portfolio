(() => {
  'use strict';
  const WA_NUMBER = '50256029990';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasIO = 'IntersectionObserver' in window;

  // header turns solid once the page has scrolled a little (sentinel instead of a scroll listener)
  const header = document.querySelector('.header');
  if (header && hasIO) {
    const sentinel = document.createElement('div');
    sentinel.setAttribute('aria-hidden', 'true');
    sentinel.style.cssText = 'position:absolute;top:24px;left:0;width:1px;height:1px;pointer-events:none';
    document.body.prepend(sentinel);
    new IntersectionObserver(([e]) => header.classList.toggle('solid', !e.isIntersecting)).observe(sentinel);
  }

  // mobile menu
  const burger = document.getElementById('burger');
  const nav = document.getElementById('nav');
  const setMenu = (open) => {
    nav.classList.toggle('open', open);
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    if (open) header.classList.add('solid');
  };
  burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.addEventListener('click', (e) => e.target.closest('a') && setMenu(false));
  addEventListener('keydown', (e) => e.key === 'Escape' && setMenu(false));

  // reveal content as it enters the viewport, staggered inside groups
  document.querySelectorAll('.bento, .catalog, .facts, .process').forEach((group) => {
    [...group.children].forEach((el, i) => el.style.setProperty('--d', `${i * 0.08}s`));
  });
  const revealEls = document.querySelectorAll('.reveal');
  if (reduce || !hasIO) {
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

  // repair request -> prefilled WhatsApp message
  const form = document.getElementById('quoteForm');
  const err = document.getElementById('quoteErr');
  form && form.addEventListener('submit', (e) => {
    e.preventDefault();
    const f = new FormData(form);
    const nombre = String(f.get('nombre') || '').trim();
    err.hidden = !!nombre;
    form.elements.nombre.setAttribute('aria-invalid', String(!nombre));
    if (!nombre) return form.elements.nombre.focus();
    const detalle = String(f.get('detalle') || '').trim();
    const text = `Hola PetXpert, soy ${nombre}. Necesito reparar mi equipo: ${f.get('equipo')}.` + (detalle ? ` Detalle: ${detalle}` : '');
    window.open(`https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(text)}`, '_blank', 'noopener');
  });

  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
