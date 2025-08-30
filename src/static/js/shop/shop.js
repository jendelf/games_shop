import { 
  shopPage, 
  like, 
  addWishlist, 
  addCart, 
  buyGame, 
  fetchGameData 
} from './shop_api.mjs';

let currentPage = 1;
const perPage = 12;

async function renderGamePage(gameId) {
  console.log('=== renderGamePage ===');
  console.log('Game ID:', gameId);
  
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="game-page">
      <h2>Loading game...</h2>
    </div>
  `;
  
  try {
    const game = await fetchGameData(gameId);

    app.innerHTML = `
      <div class="game-detail-page">
        <button onclick="window.initializeShop(1)">← Back to Shop</button>
        <h1 class="game-detail-title">${game.name || 'Unknown Game'}</h1>
        <div class="game-detail-header">
          <img src="${game.image_url || 'https://placehold.co/400x200?text=No+Image'}" 
              alt="${game.name}" class="game-detail-cover">
          <div class="game-detail-info">
            <p class="game-detail-description"><strong>Description:</strong> ${game.detailed_description || 'No description'}</p>
            <p><strong>Price:</strong> $${game.price || 0}</p>
            <p><strong>App ID:</strong> ${game.appid || gameId}</p>
            <div class="game-detail-buttons">
              <button class="detail-like-btn" onclick="like(${game.appid || gameId})">Like</button>
              <button class="detail-wishlist-btn" onclick="addWishlist(${game.appid || gameId})">Wishlist</button>
              <button class="detail-cart-btn" onclick="addCart(${game.appid || gameId})">Add to Cart</button>
              <button class="detail-buy-btn" onclick="buyGame(${game.appid || gameId})">Buy</button>
            </div>
          </div>
        </div>
      </div>
    `;
    
  } catch (error) {
    console.error('Error loading game:', error);
    app.innerHTML = `
      <div class="game-page">
        <button onclick="window.initializeShop(1)">← Back to Shop</button>
        <h2>Error loading game</h2>
        <p>${error.message}</p>
      </div>
    `;
  }
}

export async function initializeShop(page = 1) {
  try {
    clearApp();

    const app = document.getElementById("app");
    app.innerHTML = `
      <div class="shop-container">
        <h2>GAMES SHOP</h2>
        <div id="games-container" class="games-container"></div>
        <div id="pagination" class="pagination"></div>
      </div>
    `;

    currentPage = page;

    const response = await shopPage(page, perPage);
    console.log('API Response:', response);

    displayGames(response.games);
    renderPagination(response.total, response.page, response.totalPages);
    
  } catch (error) {
    console.error("Shop error:", error);
    const app = document.getElementById("app");
    app.innerHTML = `
      <div class="shop-container">
        <h2>GAMES SHOP</h2>
        <p>Failed to get games.</p>
      </div>
    `;
  }
}

function clearApp() {
  document.getElementById("app").innerHTML = "";
}

function displayGames(games) {
  const gamesContainer = document.getElementById("games-container");

  if (!games || !games.length) {
    gamesContainer.innerHTML = `<p>No games are available</p>`;
    return;
  }

  games.forEach((game) => {
    const gameCard = renderGameCard(game);
    gamesContainer.appendChild(gameCard);
  });
}

function renderGameCard(game) {
  const card = document.createElement("div");
  card.className = "game-card";

  const imageUrl = game.photos_url && game.photos_url.length > 0
    ? game.photos_url[0]
    : game.image_url || "https://placehold.co/300x200?text=No+Image";

  card.innerHTML = `
    <img src="${imageUrl}" alt="${game.name}" class="game-image" />
    <h3>${game.name}</h3>
    <p>Price: $${game.price}</p>
    <p>${game.description || "No description"}</p>
    <div>
      <button class="like-btn">Like</button>
      <button class="wishlist-btn">Wishlist</button>
      <button class="cart-btn">Add to Cart</button>
      <button class="buy-btn">Buy</button>
    </div>
  `;

  card.querySelector(".like-btn").onclick = (e) => {
    e.stopPropagation();
    like(game.id);
  };
  card.querySelector(".wishlist-btn").onclick = (e) => {
    e.stopPropagation();
    addWishlist(game.id);
  };
  card.querySelector(".cart-btn").onclick = (e) => {
    e.stopPropagation();
    addCart(game.id);
  };
  card.querySelector(".buy-btn").onclick = (e) => {
    e.stopPropagation();
    buyGame(game.id);
  };

  card.addEventListener("click", (e) => {
    e.preventDefault();
    console.log('game.appid:', game.appid, 'type:', typeof game.appid);
    renderGamePage(game.appid);
  });

  return card;
}

function renderPagination(total, currentPage, totalPages) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const prevBtn = document.createElement("button");
  prevBtn.textContent = "⬅ Prev";
  prevBtn.disabled = currentPage === 1;
  prevBtn.onclick = () => initializeShop(currentPage - 1);

  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next ➡";
  nextBtn.disabled = currentPage >= totalPages;
  nextBtn.onclick = () => initializeShop(currentPage + 1);

  const info = document.createElement("span");
  info.textContent = `Page ${currentPage} of ${totalPages} (${total} total games)`;

  pagination.appendChild(prevBtn);
  pagination.appendChild(info);
  pagination.appendChild(nextBtn);
}

window.initializeShop = initializeShop;
window.renderGamePage = renderGamePage;
