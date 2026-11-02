'use strict';

// Same approved message behavior, with a bounded email-only signup POST.
(() => {
  const body = document.body;
  const moments = [...document.querySelectorAll('.moment')];
  const controls = document.querySelector('.message-controls');
  const dots = [...controls.querySelectorAll('button')];
  const motion = document.querySelector('#motion-control');
  const form = document.querySelector('#signup-form');
  const email = document.querySelector('#email');
  const submit = document.querySelector('#signup-submit');
  const status = form.querySelector('.form-status');
  const config = window.IOLEIA_SIGNUP;
  const ready = config && typeof config.endpoint === 'string' &&
    /^https:\/\/[a-z0-9]+\.execute-api\.ca-central-1\.amazonaws\.com\/early-access$/.test(config.endpoint) &&
    config.consentVersion === 'ioleia-early-access-v3-2026-11-02';
  let submitting = false;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0;
  let explicitlyPaused = false;
  let interactionPaused = false;
  let focusPaused = false;
  let timer;
  let animations = [];
  let timerStarted = 0;
  let remaining = Number(moments[0].dataset.dwell);
  const blocked = () => reduced.matches || document.hidden || explicitlyPaused || interactionPaused || focusPaused;

  function markCurrent() {
    moments.forEach((moment, index) => {
      moment.classList.toggle('is-current', index === current);
      moment.setAttribute('aria-hidden', String(index !== current));
      moment.inert = index !== current;
      dots[index].setAttribute('aria-pressed', String(index === current));
    });
  }
  function cancelTimer() {
    if (timer !== undefined) {
      clearTimeout(timer);
      remaining = Math.max(0, remaining - (performance.now() - timerStarted));
      timer = undefined;
    }
  }
  function schedule() {
    if (blocked() || timer !== undefined || animations.length) return;
    timerStarted = performance.now();
    timer = setTimeout(() => {
      timer = undefined;
      show((current + 1) % moments.length, true);
    }, remaining);
  }
  function syncMotion() {
    const paused = blocked();
    body.classList.toggle('motion-paused', paused);
    motion.hidden = reduced.matches;
    motion.setAttribute('aria-pressed', String(paused));
    motion.textContent = paused ? 'Resume motion' : 'Pause motion';
    if (paused) {
      cancelTimer();
      animations.forEach(animation => animation.pause());
    } else {
      animations.forEach(animation => animation.play());
      schedule();
    }
  }
  function show(next, animate) {
    cancelTimer();
    const old = moments[current];
    animations.forEach(animation => animation.cancel());
    animations = [];
    current = next;
    markCurrent();
    remaining = Number(moments[current].dataset.dwell);
    if (animate && !reduced.matches && old !== moments[current]) {
      // Opacity only. The shared grid reserves the tallest message's height.
      const options = {duration: 1200, easing: 'ease-in-out'};
      const pair = [old.animate([{opacity: 1}, {opacity: 0}], options), moments[current].animate([{opacity: 0}, {opacity: 1}], options)];
      animations = pair;
      Promise.all(pair.map(animation => animation.finished)).then(() => {
        if (animations !== pair) return;
        animations = [];
        schedule();
      }).catch(() => {}); // A manual selection or preference change cancels a fade.
    }
    syncMotion();
  }
  motion.addEventListener('click', () => {
    if (blocked()) {
      explicitlyPaused = false;
      interactionPaused = false;
    } else {
      explicitlyPaused = true;
    }
    syncMotion();
  });
  dots.forEach((dot, index) => dot.addEventListener('click', () => {
    explicitlyPaused = true;
    // Direct access is deliberately static and remains available with reduced motion.
    show(index, false);
  }));
  form.addEventListener('focusin', () => {focusPaused = true; syncMotion();});
  form.addEventListener('focusout', () => {
    // Merely inspecting an empty form resumes with a fresh full reading interval.
    // Typing or submission stays paused until an explicit Resume motion click.
    queueMicrotask(() => {
      focusPaused = form.contains(document.activeElement);
      if (!focusPaused && !interactionPaused) remaining = Number(moments[current].dataset.dwell);
      syncMotion();
    });
  });
  form.addEventListener('input', () => {
    interactionPaused = true;
    status.textContent = '';
    syncMotion();
  });
  form.addEventListener('invalid', () => {interactionPaused = true; syncMotion();}, true);
  form.addEventListener('submit', async event => {
    event.preventDefault();
    interactionPaused = true;
    syncMotion();
    if (!ready || submitting || !form.reportValidity()) return;
    submitting = true;
    email.disabled = true;
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    status.textContent = 'Joining…';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch(config.endpoint, {
        method: 'POST', mode: 'cors', credentials: 'omit', cache: 'no-store',
        referrerPolicy: 'no-referrer', redirect: 'error', signal: controller.signal,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({email: email.value, consent_version: config.consentVersion})
      });
      if (!response.ok) throw new Error('Signup unavailable');
      const result = await response.json();
      if (result.message !== 'Thanks. Your early-access request has been received.') throw new Error('Unexpected response');
      status.textContent = result.message;
      form.reset();
    } catch (_) {
      status.textContent = 'We couldn’t save that just now. Please try again.';
    } finally {
      clearTimeout(timeout);
      submitting = false;
      email.disabled = false;
      submit.disabled = false;
      form.removeAttribute('aria-busy');
      status.focus();
    }
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches) show(0, false);
    syncMotion();
  });
  document.addEventListener('visibilitychange', syncMotion);
  // Clear a temporary field value if the browser restores this page from history.
  window.addEventListener('pageshow', event => {if (event.persisted) form.reset();});
  markCurrent();
  body.classList.add('enhanced');
  controls.hidden = false;
  email.disabled = !ready;
  submit.disabled = !ready;
  syncMotion();
})();
