import { shopPage } from './shop/shop_api.mjs';

export async function initGamePage(gameId) {
  const app = document.getElementById('game-app');

  console.log('=== DEBUG initGamePage ===');
  console.log('Received gameId:', gameId, 'type:', typeof gameId);

  if (!gameId) {
    app.innerHTML = '<p>Game not found</p>';
    return;
  }

  try {
    let games = await shopPage(1, 1000);
    console.log('Total games fetched:', games.length);

    const game = games.find(g => g.appid == gameId); 
    console.log('Found game:', game);

    if (!game) {
      app.innerHTML = '<p>Game not found</p>';
      return;
    }

    renderGamePage(game);

  } catch (error) {
    console.error('Error loading games:', error);
    app.innerHTML = '<p>Error loading game</p>';
  }
}

export function renderGamePage(game) {
  const app = document.getElementById('game-app');

  const imageUrl = (game.photos_url && game.photos_url.length > 0)
    ? game.photos_url[0]
    : game.image_url || 'https://via.placeholder.com/400x200';

  app.innerHTML = `
    <div class="game-detail-page">
      <div class="game-header">
        <button id="back-to-shop" class="back-btn">← Back to Shop</button>
        <img src="${imageUrl}" alt="${game.name}" class="game-detail-cover">
        <div class="game-info">
          <h1>${game.name}</h1>
          <p class="price">$${game.price}</p>
          <button class="cart-btn">Add to Cart</button>
          <button class="buy-btn">Buy Now</button>
        </div>
      </div>

      <div class="game-description">
        <h2>Description</h2>
        <p>${game.description || "No description available"}</p>
      </div>

      <div class="game-reviews">
        <h2>Reviews</h2>
        <div id="reviews-list">
          <p>No reviews yet...</p>
        </div>
        <form id="add-review">
          <textarea placeholder="Leave your review..." required></textarea>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  `;

  // Back button handler
  document.getElementById('back-to-shop').addEventListener('click', () => {
    if (window.initializeShop) {
      window.initializeShop();
    } else {
      window.location.reload();
    }
  });

  // Review form handler
  const form = document.getElementById('add-review');
  form.onsubmit = (e) => {
    e.preventDefault();
    const textarea = form.querySelector('textarea');
    const text = textarea.value.trim();
    if (text) {
      const reviewEl = document.createElement('div');
      reviewEl.classList.add('review');
      reviewEl.innerHTML = `<strong>Player:</strong> ${text}`;

      const noReviewsMsg = document.getElementById('reviews-list').querySelector('p');
      if (noReviewsMsg && noReviewsMsg.textContent === 'No reviews yet...') {
        noReviewsMsg.remove();
      }

      document.getElementById('reviews-list').appendChild(reviewEl);
      textarea.value = '';
    }
  };
}
