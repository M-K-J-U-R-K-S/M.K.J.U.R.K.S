import {
  api, requireLogin, renderNavbar, el,
  showError, showSuccess, clearMessage, withBusy
} from './common.js?v=account-1';

const PAGE_SIZE = 20;

if (requireLogin()) {
  renderNavbar('my-reviews.html');
  start();
}

function stars(rating) {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

function formatDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? ''
    : date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
}

function start() {
  const list = document.getElementById('reviews');
  const count = document.getElementById('review-count');
  const empty = document.getElementById('empty');
  const loadMore = document.getElementById('load-more');
  let loaded = 0; // reviews currently on the page
  let total = 0;  // reviews you have in all

  function refreshSummary() {
    count.textContent = total ? `${total} review${total === 1 ? '' : 's'}` : '';
    empty.hidden = total > 0;
    loadMore.hidden = loaded >= total;
  }

  function reviewCard(review) {
    const deleteButton = el('button', {
      class: 'btn btn-danger btn-small', type: 'button', text: 'Delete',
      'aria-label': `Delete your review of ${review.gym_name}`,
      onclick: () => removeReview(review, deleteButton, card)
    });
    const card = el('article', { class: 'card' },
      el('h3', {}, el('a', { href: `gym-detail.html?id=${encodeURIComponent(review.gym_id)}`, text: review.gym_name })),
      el('div', { class: 'row', style: 'justify-content: space-between; align-items: center;' },
        el('span', { class: 'stars', role: 'img', 'aria-label': `${review.rating} out of 5 stars`, text: stars(review.rating) }),
        el('span', { class: 'muted small', text: formatDate(review.created_at) })),
      review.review_text && el('p', { text: review.review_text, style: 'white-space: pre-wrap; margin-top: 0.5rem;' }),
      review.busy_hour_info && el('p', { class: 'muted small', text: `Busy: ${review.busy_hour_info}` }),
      review.photo_url && el('img', {
        class: 'review-photo', src: review.photo_url,
        alt: `Photo you shared in your review of ${review.gym_name}`, loading: 'lazy'
      }),
      el('div', { style: 'margin-top: 0.5rem;' }, deleteButton));
    return card;
  }

  async function loadReviews(reset) {
    if (reset) {
      loaded = 0;
      list.replaceChildren();
    }
    const data = await api.myReviews({ limit: PAGE_SIZE, offset: loaded });
    data.reviews.forEach(review => list.append(reviewCard(review)));
    loaded += data.reviews.length;
    total = data.total;
    refreshSummary();
  }

  async function removeReview(review, button, card) {
    if (!window.confirm(`Delete your review of ${review.gym_name}? This cannot be undone.`)) return;
    clearMessage();
    await withBusy(button, async () => {
      try {
        await api.deleteReview(review.id);
        card.remove();
        loaded -= 1;
        total -= 1;
        refreshSummary();
        showSuccess('Review deleted.');
      } catch (error) {
        showError(error.message);
        if (error.status === 404) loadReviews(true).catch(() => {}); // already gone: refresh the list
      }
    });
  }

  loadMore.addEventListener('click', () => {
    withBusy(loadMore, async () => {
      try { await loadReviews(false); } catch (error) { showError(error.message); }
    });
  });

  loadReviews(true).catch(error => showError(error.message));
}