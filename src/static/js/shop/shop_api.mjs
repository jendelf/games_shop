const API_URL = "http://localhost:8000";

function getHeaders(auth = true) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getAccessToken();
    if (!token) throw new Error("No access token, please log in");
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse(res, defaultError = "Request failed") {
  let data = null;
  if (res.headers.get("content-type")?.includes("application/json")) {
    try {
      data = await res.json();
    } catch {
      data = null;
    }
  }

  if (!res.ok) {
    const message = data?.message || `${defaultError} (status ${res.status})`;
    throw new Error(message);
  }

  return data;
}

export async function shopPage(page = 1, perPage = 12) {
  try {
    const res = await fetch(
      `${API_URL}/api/shop/?page=${page}&page_size=${perPage}`,
      { method: "GET", headers: getHeaders(false) }
    );

    const data = await handleResponse(res, "Failed to load shop data");

    return {
      games: data?.games || [],
      total: data?.total || 0,
      page: data?.page || page,
      perPage: data?.page_size || perPage,
      totalPages:
        data?.total_pages ||
        Math.ceil((data?.total || 0) / (data?.page_size || perPage)),
    };
  } catch (error) {
    console.error("Error fetching shop data:", error.message);
    return {
      games: [],
      total: 0,
      page,
      perPage,
      totalPages: 0,
      error: error.message,
    };
  }
}

export async function addGame(gameData) {
  try {
    const res = await fetch(`${API_URL}/api/shop/add`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(gameData),
    });

    const data = await handleResponse(res, "Failed to add game");
    return data;
  } catch (err) {
    console.error("Add game failed:", err.message);
    return { error: err.message };
  }
}

export async function deleteGame(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/delete`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    const data = await handleResponse(res, "Failed to delete game");
    console.log(data?.message || "Game deleted successfully!");
    return data;
  } catch (err) {
    console.error("Delete game failed:", err.message);
    return { error: err.message };
  }
}

export async function updateGame(gameData) {
  try {
    const res = await fetch(`${API_URL}/api/shop/update`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify(gameData),
    });

    const data = await handleResponse(res, "Could not update game data");
    console.log(data?.message || "Game information updated successfully!");
    return data;
  } catch (err) {
    console.error("Update game failed:", err.message);
    return { error: err.message };
  }
}

export async function addWishlist(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/wishlist`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    const data = await handleResponse(res, "Failed to add to wishlist");
    console.log(data?.message || "Game added to wishlist!");
    return data;
  } catch (err) {
    console.error("Wishlist failed:", err.message);
    return { error: err.message };
  }
}

export async function like(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/like`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    return await handleResponse(res, "Failed to like game");
  } catch (err) {
    console.error("Like failed:", err.message);
    return { error: err.message };
  }
}

export async function gameInfo(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/game_info`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    return await handleResponse(res, "Failed to get game info");
  } catch (err) {
    console.error("Get game info failed:", err.message);
    return null;
  }
}

export async function buyGame(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/buy`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    const data = await handleResponse(res, "Error. Failed to buy a game");
    console.log(data?.message || "Game successfully purchased");
    return data;
  } catch (err) {
    console.error("Buy game failed:", err.message);
    return { error: err.message };
  }
}

export async function addCart(gameId) {
  try {
    const res = await fetch(`${API_URL}/api/shop/cart`, {
      method: "POST",
      headers: getHeaders(true),
      body: JSON.stringify({ id: gameId }),
    });

    return await handleResponse(res, "Error. Failed to add game to the cart");
  } catch (err) {
    console.error("Add to cart failed:", err.message);
    return { error: err.message };
  }
}
