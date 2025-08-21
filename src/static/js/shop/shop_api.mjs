const API_URL = "http://localhost:8000"; 


function getHeaders(auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth) {
        const token = getAccessToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

export async function shopPage() {
  try {
    const res = await fetch(`${API_URL}/api/shop/`, {
      method: "GET",
      headers: getHeaders(false),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return await res.json();
  } catch (error) {
    console.error('Error fetching shop data:', error);
    // Можно вернуть данные по умолчанию или пробросить ошибку дальше
    return { 
      items: [], 
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
