import { shopPage } from './shop_api.mjs';

export async function initializeShop() {
  try {
    clearApp();

    const app = document.getElementById("app");
    app.innerHTML = `
      <div class="shop-container">
        <h2>GAMES SHOP</h2>
        <div id="games-container" class="games-container"></div>
      </div>
    `;

    let games = await shopPage();

    games.sort((a, b) => (b.positive_ratings ?? 0) - (a.positive_ratings ?? 0));

    displayGames(games);
  } catch (error) {
    console.error("Shop error:", error);
  }
}

function clearApp() {
  document.getElementById("app").innerHTML = "";
}

function displayGames(games) {
  const gamesContainer = document.getElementById("games-container");

  if (!games.length) {
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
         : game.image_url || "https://via.placeholder.com/300x200/667eea/white?text=No+Image";

    card.innerHTML = `
        <img src="${imageUrl}" alt="${game.name}" class="game-image" onerror="this.src='https://via.placeholder.com/300x200/667eea/white?text=No+Image'" />
        <h3>${game.name}</h3>
        <p>Price: $${game.price}</p>
        <p>${game.description || "Описание отсутствует"}</p>
        <div>
            <button class="like-btn">Like</button>
            <button class="wishlist-btn">Wishlist</button>
            <button class="cart-btn">Add to Cart</button>
            <button class="buy-btn">Buy</button>
            <button class="delete-btn">Delete</button>
        </div>
    `;

    card.querySelector(".like-btn").onclick = () => like(game.id);
    card.querySelector(".wishlist-btn").onclick = () => addWishlist(game.id);
    card.querySelector(".cart-btn").onclick = () => addCart(game.id);
    card.querySelector(".buy-btn").onclick = () => buyGame(game.id);
    card.querySelector(".delete-btn").onclick = async () => {
        await deleteGame(game.id);
        card.remove();
    };

    return card;
}
