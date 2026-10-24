/** J.O.I. site behavior — progressive enhancement. Content and navigation work without JS. */
(() => {
  'use strict';
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const menuButton = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-menu');
  let open = false;

  function setMenu(next, restoreFocus = false) {
    if (!menu || !menuButton) return;
    open = Boolean(next);
    document.body.classList.toggle('menu-open', open);
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    menu.inert = !open;
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.querySelector('.menu-word').textContent = open ? 'Close' : 'Menu';
    if (open) {
      const first = menu.querySelector('a');
      if (first) first.focus({ preventScroll: true });
    } else if (restoreFocus) {
      menuButton.focus({ preventScroll: true });
    }
  }
  if (menu && menuButton) {
    menuButton.addEventListener('click', () => setMenu(!open, open));
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', (event) => {
      if (!open) return;
      if (event.key === 'Escape') { setMenu(false, true); return; }
      if (event.key !== 'Tab') return;
      const focusable = [menuButton, ...menu.querySelectorAll('a')];
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
  }

  // Scroll indicator uses transform rather than layout-sensitive width changes.
  const progress = document.querySelector('.reading-progress');
  let scrollQueued = false;
  function updateScroll() {
    scrollQueued = false;
    if (!progress) return;
    const scrollMax = document.documentElement.scrollHeight - window.innerHeight;
    const amount = scrollMax > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollMax)) : 0;
    progress.style.right = '0';
    progress.style.transform = `scaleX(${amount.toFixed(4)})`;
  }
  window.addEventListener('scroll', () => {
    if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateScroll); }
  }, { passive: true });
  window.addEventListener('resize', updateScroll, { passive: true });
  updateScroll();

  // Keep the direct contact option usable when a visitor has no email app configured.
  document.querySelectorAll('[data-copy-email]').forEach(button => {
    const status = document.getElementById(button.getAttribute('aria-describedby'));
    const email = button.getAttribute('data-copy-email');
    function fallbackCopy() {
      const field = document.createElement('textarea');
      field.value = email;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.opacity = '0';
      document.body.appendChild(field);
      field.select();
      let copied = false;
      try { copied = document.execCommand('copy'); } catch (_) {}
      field.remove();
      return copied;
    }
    button.addEventListener('click', async () => {
      let copied = false;
      if (navigator.clipboard && window.isSecureContext) {
        try { await navigator.clipboard.writeText(email); copied = true; } catch (_) {}
      }
      if (!copied) copied = fallbackCopy();
      if (status) status.textContent = copied
        ? 'Email address copied to clipboard.'
        : `Copy failed. Select and copy ${email}.`;
    });
  });

  // Native IntersectionObserver: every element is visible until this enhancement is initialized.
  if (!reduced.matches && 'IntersectionObserver' in window) {
    document.documentElement.classList.add('js-motion');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -24px 0px' });
    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
  }

  // This is NOT a backend form. It explicitly composes an email for the visitor to send.
  const contact = document.getElementById('contact-form');
  if (contact) {
    contact.addEventListener('submit', event => {
      event.preventDefault();
      if (!contact.reportValidity()) return;
      const values = new FormData(contact);
      const read = key => String(values.get(key) ?? '').trim();
      const subject = `[J.O.I. enquiry] ${read('subject')} — ${read('name')}`;
      const body = [
        `Name: ${read('name')}`,
        `Email: ${read('email')}`,
        `Organisation: ${read('organisation') || 'N/A'}`,
        `Project type: ${read('subject')}`,
        '', read('message')
      ].join('\n');
      const mailto = 'mailto:ODUKOYAJOEL@ZOHOMAIL.COM?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      document.getElementById('form-status').textContent = 'Opening your email app. Please send the draft there; this page has not submitted your message.';
      window.location.href = mailto;
    });
  }

})();
