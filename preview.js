'use strict';

// Intentionally offline. No fetch, analytics, cookies, storage, or signup endpoint.
document.querySelectorAll('[data-preview-signup]').forEach(form => {
  const submit = form.querySelector('.preview-submit');
  const status = form.querySelector('.form-status');

  submit.disabled = false;

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    status.textContent = 'Preview complete. Nothing was sent or saved, and you have not joined a list yet.';
    form.reset();
    status.focus();
  });

  form.addEventListener('input', () => {
    status.textContent = '';
  });
});

const motion = document.querySelector('#motion-control');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let paused = false;

const updateMotionControl = () => {
  if (!motion) return;
  motion.hidden = reducedMotion.matches;
  motion.setAttribute('aria-pressed', String(paused));
  motion.innerHTML = paused
    ? '<span aria-hidden="true">▷</span> Resume motion'
    : '<span aria-hidden="true">Ⅱ</span> Pause motion';
  document.body.classList.toggle('motion-paused', paused);
};

if (motion) {
  motion.addEventListener('click', () => {
    paused = !paused;
    updateMotionControl();
  });
}

if (typeof reducedMotion.addEventListener === 'function') {
  reducedMotion.addEventListener('change', updateMotionControl);
}

updateMotionControl();

const updateVisibility = () => {
  document.body.classList.toggle('page-hidden', document.hidden);
};

document.addEventListener('visibilitychange', updateVisibility);
updateVisibility();

if ('IntersectionObserver' in window) {
  const visibility = new IntersectionObserver(entries => {
    for (const entry of entries) {
      entry.target.classList.toggle('out-of-view', !entry.isIntersecting);
    }
  }, { threshold: 0 });

  document.querySelectorAll('.light-field').forEach(field => visibility.observe(field));
}
