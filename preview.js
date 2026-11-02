'use strict';

// Intentionally offline. No fetch, analytics, cookies, storage, or signup endpoint.
const form = document.querySelector('#signup-form');
const submit = document.querySelector('#preview-submit');
const status = document.querySelector('#form-status');
form.addEventListener('submit', event => event.preventDefault());
const previewSignup = () => {
  if (!form.reportValidity()) return;
  status.textContent = 'Preview complete. Nothing was sent or saved, and you have not joined a list. Signups will open when the site is ready.';
  form.reset();
  status.focus();
};
submit.disabled = false;
submit.addEventListener('click', previewSignup);
form.addEventListener('keydown', event => {
  if (event.key === 'Enter' && event.target.matches('input:not([type="checkbox"])')) {
    event.preventDefault();
    previewSignup();
  }
});
form.addEventListener('input', () => { status.textContent = ''; });

const motion = document.querySelector('#motion-control');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let paused = false;
const updateMotionControl = () => {
  motion.hidden = reducedMotion.matches;
  motion.setAttribute('aria-pressed', String(paused));
  motion.innerHTML = paused ? '<span aria-hidden="true">▷</span> Resume light' : '<span aria-hidden="true">Ⅱ</span> Pause light';
  document.body.classList.toggle('motion-paused', paused);
};
motion.addEventListener('click', () => { paused = !paused; updateMotionControl(); });
reducedMotion.addEventListener('change', updateMotionControl);
updateMotionControl();
const updateVisibility = () => document.body.classList.toggle('page-hidden', document.hidden);
document.addEventListener('visibilitychange', updateVisibility);
updateVisibility();
if ('IntersectionObserver' in window) {
  const visibility = new IntersectionObserver(entries => {
    for (const entry of entries) entry.target.classList.toggle('out-of-view', !entry.isIntersecting);
  }, { threshold: 0 });
  document.querySelectorAll('.light-field').forEach(field => visibility.observe(field));
}
const respond = document.querySelector('#respond-button');
const study = document.querySelector('#light-study');
const fieldState = document.querySelector('#field-state');
respond.hidden = false;
let responseTimer;
respond.addEventListener('click', () => {
  clearTimeout(responseTimer);
  study.classList.add('engaged');
  fieldState.textContent = 'A moment of warmth';
  responseTimer = setTimeout(() => {
    study.classList.remove('engaged');
    fieldState.textContent = 'Resting study';
  }, 6500);
});
