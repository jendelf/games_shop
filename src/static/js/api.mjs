const API_URL = "http://localhost:8000"; 

function getAccessToken() {
    return localStorage.getItem("access_token");
}

function getHeaders(auth = true) {
    const headers = { "Content-Type": "application/json" };
    if (auth) {
        const token = getAccessToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}

async function registerUser(username, password) {
    const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: getHeaders(false),
        body: JSON.stringify({ username, password })
    });
    return res.json();
}

async function login(username, password) {
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    const res = await fetch(`${API_URL}/api/auth/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body
    });

    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
    }
    return data;
}

async function refreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    const res = await fetch(`${API_URL}/api/auth/refresh`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${refresh_token}` }
    });
    const data = await res.json();
    if (res.ok) {
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);
    }
    return data;
}

async function logout() {
    const refresh_token = localStorage.getItem("refresh_token");
    await fetch(`${API_URL}/api/auth/logout`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${refresh_token}` }
    });
    localStorage.clear();
}

async function getCurrentUser() {
    const res = await fetch(`${API_URL}/api/auth/me`, {
        headers: getHeaders()
    });
    return res.json();
}

async function getLibrary() {
    const res = await fetch(`${API_URL}/api/auth/me/library`, {
        headers: getHeaders()
    });
    return res.json();
}


//-----------------------------------------------------------------------------------------Admin functionality
async function getAllUsers() {
    const res = await fetch(`${API_URL}/api/auth/admin/users`, {
        headers: getHeaders()
    });
    return res.json();
}

async function banUser(userId) {
    return await fetch(`${API_URL}/api/auth/admin/ban?user_id=${userId}`, {
        method: "POST",
        headers: getHeaders()
    });
}

async function updateUserRole(userId, role) {

  if (typeof userId === 'undefined' || isNaN(parseInt(userId))) {
    throw new Error('Invalid user ID');
  }

  const res = await fetch(`${API_URL}/api/auth/admin/set-role?user_id=${userId}&role=${role}`, {
    method: "POST",
    headers: getHeaders()
  });
  
  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Failed to update role');
  }
  
  return res.json();
}

export {
    registerUser, login, logout, refreshToken,
    getCurrentUser, getLibrary, getAllUsers,
    banUser, updateUserRole
};
