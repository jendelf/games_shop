import {
  login,
  logout,
  registerUser,
  getCurrentUser,
  getAllUsers,
  banUser,
  updateUserRole
} from "./auth_api.mjs";

const { initializeShop } = await import("/js/shop/shop.js");
const API_URL = "http://localhost:8000"

function clearApp() {
  document.getElementById("app").innerHTML = "";
}

function renderLoginForm() {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="auth-container">
      <div class="auth-box">
        <h2>Login</h2>
        <form id="login-form" class="auth-form">
          <input type="text" name="username" placeholder="Username" required />
          <input type="password" name="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
        <div class="auth-switch">Don't have an account? 
          <a href="#" id="go-register">Register here</a>
        </div>
      </div>
    </div>
  `;

  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
      await login(username, password);
      const user = await getCurrentUser();

      if (user.role === "administrator") {
        renderAdminPanel(user);
      } else {
        renderShop();
      }
    } catch (err) {
      alert("Login failed: " + err.message);
      console.error(err);
    }
  });

  document.getElementById("go-register").addEventListener("click", (e) => {
    e.preventDefault();
    renderRegisterForm();
  });
}

function renderRegisterForm() {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="auth-container">
      <div class="auth-box">
        <h2>Register</h2>
        <form id="register-form" class="auth-form">
          <input type="text" name="username" placeholder="Username" required />
          <input type="password" name="password" placeholder="Password" required />
          <input type="password" name="confirmPassword" placeholder="Confirm Password" required />
          <button type="submit">Register</button>
        </form>
        <div class="auth-switch">Already have an account? 
          <a href="#" id="go-login">Login here</a>
        </div>
      </div>
    </div>
  `;

  document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    const confirmPassword = e.target.confirmPassword.value;

    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      const result = await registerUser(username, password);
      if (result) {
        alert("Registration successful! Please log in.");
        renderLoginForm();
      }
    } catch (err) {
      alert("Registration failed: " + err.message);
      console.error(err);
    }
  });

  document.getElementById("go-login").addEventListener("click", (e) => {
    e.preventDefault();
    renderLoginForm();
  });
}

async function renderShop() {
  await initializeShop();
}

async function renderAdminPanel(user) {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="admin-container">
      <h2>Admin Panel</h2>
      <p>Welcome, ${user.username}</p>
      <div id="user-list" class="user-list"></div>
      <button id="logout-btn" class="logout-btn">Logout</button>
    </div>
  `;

  document.getElementById("logout-btn").addEventListener("click", async () => {
    await logout();
    renderLoginForm();
  });

  const users = await getAllUsers();
  const userListDiv = document.getElementById("user-list");
  userListDiv.innerHTML = "<h3>User Management</h3>";

  users.forEach((u) => {
    const userDiv = document.createElement("div");
    userDiv.className = "user-card";
    userDiv.innerHTML = `
      <div class="user-info">
        <p><strong>${u.username}</strong></p>
        <p>Role: ${u.role}</p>
        <p>Status: ${u.disabled ? "Banned" : "Active"}</p>
      </div>
      <div class="user-controls">
        <select id="role-${u.id}">
          <option value="customer" ${u.role === "customer" ? "selected" : ""}>Customer</option>
          <option value="seller" ${u.role === "seller" ? "selected" : ""}>Seller</option>
          <option value="administrator" ${u.role === "administrator" ? "selected" : ""}>Admin</option>
        </select>
        <button id="change-role-${u.id}" class="action-btn">Update Role</button>
        <button id="toggle-block-${u.id}" class="${u.disabled ? "unblock-btn" : "block-btn"}">
          ${u.disabled ? "Unblock" : "Block"}
        </button>
      </div>
    `;
    userListDiv.appendChild(userDiv);

    userDiv.querySelector(`#change-role-${u.id}`).addEventListener("click", async () => {
      const newRole = userDiv.querySelector(`#role-${u.id}`).value;
      try {
        await updateUserRole(u.id, newRole);
        alert(`Role updated to ${newRole}`);
        renderAdminPanel(user);
      } catch (err) {
        alert("Error updating role: " + err.message);
      }
    });

    userDiv.querySelector(`#toggle-block-${u.id}`).addEventListener("click", async () => {
      try {
        await banUser(u.id);
        renderAdminPanel(user);
      } catch (err) {
        alert("Error updating status: " + err.message);
      }
    });
  });
}

async function tryAutoLogin() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    renderLoginForm();
    return;
  }

  try {
    const user = await getCurrentUser();
    if (user.role === "administrator") {
      renderAdminPanel(user);
    } else {
      renderShop();
    }
  } catch (error) {
    console.error("Auto-login error:", error);
    await logout();
    renderLoginForm();
  }
}

document.getElementById("app").innerHTML = `
  <div class="loading-container">
    <div class="loading-spinner"></div>
    <p>Loading...</p>
  </div>
`;

tryAutoLogin();
