import { createApi } from '../api.js?v=merged-5';

const TOKEN_KEY = 'pump_check_access_token';
const LOGIN_PAGE = 'login.html';

// One API client for every page. Change baseUrl when the backend is deployed.
export const api = createApi({
    baseUrl: ['127.0.0.1', 'localhost'].includes(window.location.hostname)
    ? 'http://127.0.0.1:8000'
    : 'https://pump-check-api.onrender.com',
  onUnauthorized: () => { window.location.href = LOGIN_PAGE; }
});

export function isLoggedIn() {
  return Boolean(sessionStorage.getItem(TOKEN_KEY));
}

// Call at the top of every page that needs a logged-in user
export function requireLogin() {
  if (!isLoggedIn()) {
    window.location.href = LOGIN_PAGE;
    return false;
  }
  return true;
}

/**
 * Build an HTML element safely. Text is always inserted as plain text,
 * never as HTML, so user-written reviews cannot inject code (XSS).
 * Example: el('p', { class: 'muted' }, 'Hello')
 */
export function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [name, value] of Object.entries(attrs)) {
    if (value === undefined || value === null || value === false) continue;
    if (name === 'class') node.className = value;
    else if (name === 'text') node.textContent = value;
    else if (name.startsWith('on')) node.addEventListener(name.slice(2).toLowerCase(), value);
    else node.setAttribute(name, value === true ? '' : value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined || child === false) continue;
    node.append(child);
  }
  return node;
}

function showMessage(type, text) {
  const box = document.getElementById('message');
  if (!box) return;
  box.className = `alert alert-${type}`;
  box.setAttribute('role', type === 'error' ? 'alert' : 'status');
  box.textContent = text;
  box.hidden = false;
  box.scrollIntoView({ block: 'nearest' });
}

export const showError = text => showMessage('error', text);
export const showSuccess = text => showMessage('success', text);

export function clearMessage() {
  const box = document.getElementById('message');
  if (box) { box.hidden = true; box.textContent = ''; }
}

// Disable a button while a request runs, so users cannot double-submit
export async function withBusy(button, task) {
  button.disabled = true;
  try {
    return await task();
  } finally {
    button.disabled = false;
  }
}

export function starText(rating) {
  if (rating === null || rating === undefined) return 'No reviews yet';
  const value = Number(rating);
  const filled = Math.round(value);
  return `${'★'.repeat(filled)}${'☆'.repeat(5 - filled)} ${value.toFixed(1)}`;
}

// Today as YYYY-MM-DD in the user's own time zone
export function todayISO() {
  const d = new Date();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${month}-${day}`;
}

const LINKS = [
  ['index.html', 'Home'],
  ['gyms.html', 'Gyms'],
  ['workouts.html', 'Workouts'],
  ['plans.html', 'My Plans'],
  ['calories.html', 'Calories'],
  ['community.html', 'Community'],
  ['account.html', 'Account']
];

/**
 * Fill <header id="navbar"> with the site navigation.
 * Pass the current page's file name, e.g. renderNavbar('gyms.html').
 */
export function renderNavbar(current) {
  document.querySelector('.skip-link')?.remove();
  document.body.prepend(
    el('a', { class: 'skip-link', href: '#main', text: 'Skip to main content' })
  );

  const nav = el('nav', { 'aria-label': 'Main' },
    LINKS.map(([href, label]) =>
      el('a', { href, text: label, 'aria-current': href === current ? 'page' : null })));

  const userLabel = el('span', { class: 'small' });
  const logout = el('button', {
    class: 'btn btn-secondary btn-small',
    type: 'button',
    text: 'Log out',
    onclick: async () => {
      try { await api.logout(); } catch { /* token is cleared either way */ }
      window.location.href = LOGIN_PAGE;
    }
  });

  const header = document.getElementById('navbar');
  header.className = 'navbar';
  header.replaceChildren(el('div', { class: 'container' },
        el('a', { class: 'brand', href: 'index.html', 'aria-label': 'Pump Check home' },
      el('img', { src: 'assets/logo-wordmark.png', alt: 'Pump Check' })),
    nav, userLabel, logout));

  // Footer with the legal links, added once per page
    // Footer: legal links and health disclaimer, kept at the bottom of every page
  if (!document.getElementById('site-footer')) {
    document.body.append(
      el('footer', { id: 'site-footer', class: 'legal-footer' },
        el('div', { class: 'container small muted' },
          el('p', {
            text: 'Workout plans, logs, recommendations, and calorie information are for general information only and are not medical, fitness, or nutrition advice. Talk to a qualified professional before starting a new exercise program, and stop if something hurts.'
          }),
          el('p', {},
            el('a', { href: 'privacy.html', text: 'Privacy Policy', 'data-legal': 'Privacy Policy' }), ' · ',
            el('a', { href: 'terms.html', text: 'Terms of Use', 'data-legal': 'Terms of Use' }),
            ' · Pump Check is a student demo project.'))));
  }

  // Show the username; a failure here is not worth an error message
  api.me().then(user => { userLabel.textContent = user.username; }).catch(() => {});
}
// ---- Pop-up for the Privacy Policy and Terms of Use ----
let legalDialog = null;
let legalFrame = null;
let legalHeading = null;

function openLegal(href, title) {
  if (!legalDialog) {
    legalHeading = el('h2', { id: 'legal-dialog-title', style: 'margin: 0; font-size: 1.1rem;' });
    legalFrame = el('iframe', {
      title: 'Legal document',
      style: 'flex: 1; width: 100%; border: 0; background: #0b0f17;'
    });
    legalDialog = el('dialog', {
      'aria-labelledby': 'legal-dialog-title',
      style: 'width: min(760px, calc(100% - 2rem)); height: min(80vh, 720px); padding: 0; overflow: hidden;'
    },
      el('div', { style: 'display: flex; flex-direction: column; height: 100%;' },
        el('div', {
          style: 'display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border);'
        },
          legalHeading,
          el('button', {
            class: 'btn btn-secondary btn-small', type: 'button', text: 'Close',
            onclick: () => legalDialog.close()
          })),
        legalFrame));
    // Clicking the dark area outside the window closes it
    legalDialog.addEventListener('click', event => {
      if (event.target === legalDialog) legalDialog.close();
    });
    legalDialog.addEventListener('close', () => legalFrame.removeAttribute('src'));
    document.body.append(legalDialog);
  }
  legalHeading.textContent = title;
  legalFrame.setAttribute('src', href);
  legalDialog.showModal();
}

// Any link with a data-legal attribute opens in the pop-up instead of a new page
document.addEventListener('click', event => {
  const link = event.target.closest && event.target.closest('a[data-legal]');
  if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey) return;
  event.preventDefault();
  openLegal(link.getAttribute('href'), link.dataset.legal);
});