const API_URL = "http://localhost:8000"; 


function getHeaders(auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth) {
        const token = getAccessToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

export async function shopPage(page = 1, perPage = 12) {
  try {
    const res = await fetch(`${API_URL}/api/shop/?page=${page}&page_size=${perPage}`, {
      method: "GET",
      headers: getHeaders(false),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    
    return {
      games: data.games || [],
      total: data.total || 0,
      page: data.page || page,
      perPage: data.page_size || perPage,
      totalPages: data.total_pages || Math.ceil((data.total || 0) / perPage)
    };
    
  } catch (error) {
    console.error('Error fetching shop data:', error);
    return { 
      games: [], 
      total: 0,
      page: page,
      perPage: perPage,
      totalPages: 0,
      error: 'Failed to load shop data' 
    };
  }
}

export async function addGame(gameData) {
    try{
        const res = await fetch (`${API_URL}/api/shop/add`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getHeaders(true)
            },
            body: JSON.stringify(gameData)
        });
        const data = await res.json();
        if (!res.ok)
            throw new Error(data.message|| "Failed to add game")
        console.log(data.message|| "Game created successfully!");
    }
    catch (err){
        console.error(err.message)
    }
}

export async function deleteGame(id){
    try{
        const res = await fetch (`${API_URL}/api/shop/delete`,
            {
                method: "POST",
                headers: {
                 "Content-Type": "application/json",
                ...getHeaders(true)
                },
            body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error(data.message || "Failed to delete game")
        console.log(data.message || "Game deleted successfully!")
    }
    catch (err){
        console.log(err.message)
    }
}

export async function updateGame(gameData){
    try{
        const res = await fetch(`${API_URL}/api/shop/update`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify(gameData)
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error(data.message||"Could not update game data")
        console.log(data.message || "Game information updated successfully!")
    }
    catch (err){
        console.log(err.message)
    }
}

export async function addWishlist(id){
    try{
        const res = await fetch(`${API_URL}/api/shop/wishlist`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error (data.message || "Failed to add to wishlist")
        console.log(data.message || "Game added to wishlist!")
        
    }
    catch (err){
        console.log(err.message)
    }
}

export async function like(id){
    try {
        const res = await fetch (`${API_URL}/api/shop/like`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error (data.message || "Failed to do this action")
    }
    catch (err){
        console.log(err.message)
    }
}

export async function gameInfo(id){
    try {
        const res = await fetch (`${API_URL}/api/shop/game_info`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error (data.message || "Failed to get game info")
    }
    catch (err){
        console.log(err.message)
    }
}

export async function buyGame(id){
    try {
        const res = await fetch (`${API_URL}/api/shop/buy`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error (data.message || "Error. Failed to buy a game")
        console.log(data.message || "Game successfully purchased") 
    }
    catch (err) {
        console.log(err.message)
    }
}

export async function addCart(id){
    try {
        const res = await fetch(`${API_URL}/api/shop/cart`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    ...getHeaders(true)
                },
                body: JSON.stringify({id})
            }
        );
        const data = await res.json();
        if (!res.ok)
            throw new Error (data.message || "Error. Failed to add game to the cart")
    }
    catch (err) {
        console.log(err.message)
    }
}

export async function getGameById(gameId) {
  const response = await fetch(`${API_URL}/games/${gameId}`);
  if (!response.ok) {
    throw new Error('Game not found');
  }
  return await response.json();
}

export async function fetchGameData(gameId) {
  try {
    const response = await fetch(`${API_URL}/api/shop/game_info`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ id: gameId })
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch game data');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Fetch game error:', error);
    return {
      name: `Game ${gameId}`,
      price: 0,
      description: "Game information not available",
      appid: gameId
    };
  }
}