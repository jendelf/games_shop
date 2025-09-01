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

async function registerUser(email, password) {
  const username = email.split("@")[0];

  const res = await fetch(`${API_URL}/api/auth/register`, {
    method: "POST",
    headers: getHeaders(false),
    body: JSON.stringify({ username, email, password }),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || "Registration failed");
  }

  return res.json();
}

async function login(username, password) {
  const res = await fetch(`${API_URL}/api/auth/token`, {
    method: "POST",
    body: new URLSearchParams({ username, password }),
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || "Login failed");
  }

  const data = await res.json();
  localStorage.setItem("access_token", data.access_token);
  if (data.refresh_token) {
    localStorage.setItem("refresh_token", data.refresh_token);
  }
  return data;
}

async function refreshToken() {
    const refresh_token = localStorage.getItem("refresh_token");
    if (!refresh_token) throw new Error("No refresh token");

    const res = await fetch(`${API_URL}/api/auth/refresh`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${refresh_token}` }
    });

    if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to refresh token");
    }

    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    if (data.refresh_token) {
        localStorage.setItem("refresh_token", data.refresh_token);
    }
    return data;
}

async function logout() {
    const refresh_token = localStorage.getItem("refresh_token");
    try {
        if (refresh_token) {
            await fetch(`${API_URL}/api/auth/logout`, {
                method: "POST",
                headers: { "Authorization": `Bearer ${refresh_token}` }
            });
        }
    } finally {
        localStorage.clear();
    }
}

async function getCurrentUser() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  const res = await fetch(`${API_URL}/api/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!res.ok) return null;
  return res.json();
}

async function getLibrary() {
    const res = await fetch(`${API_URL}/api/auth/me/library`, {
        headers: getHeaders()
    });

    if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to load library");
    }

    return res.json();
}

//-----------------------------------------------------------------------------------------Admin functionality

async function getAllUsers() {
    const res = await fetch(`${API_URL}/api/auth/admin/users`, {
        headers: getHeaders()
    });

    if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to load users");
    }

    return res.json();
}

async function banUser(userId) {
    const res = await fetch(`${API_URL}/api/auth/admin/ban?user_id=${userId}`, {
        method: "POST",
        headers: getHeaders()
    });

    if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to ban user");
    }

    return res.json();
}

async function updateUserRole(userId, role) {
  if (!Number.isInteger(Number(userId))) {
    throw new Error("Invalid user ID");
  }

  const res = await fetch(`${API_URL}/api/auth/admin/set-role?user_id=${userId}&role=${role}`, {
    method: "POST",
    headers: getHeaders()
  });
  
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to update role");
  }
  
  return res.json();
}

export {
    registerUser, login, logout, refreshToken,
    getCurrentUser, getLibrary, getAllUsers,
    banUser, updateUserRole
};
