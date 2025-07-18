import {
  login,
  logout,
  registerUser,
  getCurrentUser,
  getLibrary,
  getAllUsers,
  banUser,
  updateUserRole
} from "./api.mjs";

function clearApp() {
  document.getElementById("app").innerHTML = "";
}

function renderLoginForm() {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="auth-container">
      <h2>Login</h2>
      <form id="login-form" class="auth-form">
        <input type="text" name="username" placeholder="Username" required />
        <input type="password" name="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p class="auth-switch">No account? <a href="#" id="go-register">Register here</a></p>
    </div>
  `;

  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;
    const result = await login(username, password);
    const user = await getCurrentUser();
    if (user.role === "administrator") {
      renderAdminPanel(user);
    } else {
      renderShop(user);
    }
  });

  document.getElementById("go-register").addEventListener("click", renderRegisterForm);
}

function renderRegisterForm() {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="auth-container">
      <h2>Register</h2>
      <div class="auth-form">
        <input type="text" id="register-username" placeholder="Username" />
        <input type="password" id="register-password" placeholder="Password" />
        <button id="register-btn">Register</button>
      </div>
      <p class="auth-switch">Already have an account? <a href="#" id="go-login">Login</a></p>
    </div>
  `;

  document.getElementById("register-btn").addEventListener("click", async () => {
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    if (!username || !password) {
      alert("Please fill in both fields");
      return;
    }
    await registerUser(username, password);
    alert("Registration successful");
    renderLoginForm();
  });

  document.getElementById("go-login").addEventListener("click", renderLoginForm);
}

function renderShop(user) {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="shop-container">
      <h2>Welcome, ${user.username}!</h2>
      <div class="shop-actions">
        <button id="library-btn" class="action-btn">My Library</button>
        <button id="logout-btn" class="logout-btn">Logout</button>
      </div>
    </div>
  `;

  document.getElementById("library-btn").addEventListener("click", async () => {
    const library = await getLibrary();
    displayLibrary(library);
  });

  document.getElementById("logout-btn").addEventListener("click", async () => {
    await logout();
    renderLoginForm();
  });
}

function displayLibrary(library) {
  clearApp();
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="library-container">
      <h2>My Library</h2>
      <div id="games-list" class="games-grid"></div>
      <button id="back-btn" class="action-btn">Back to Shop</button>
    </div>
  `;

  const gamesList = document.getElementById("games-list");
  library.forEach(game => {
    gamesList.innerHTML += `
      <div class="game-card">
        <h3>${game.title}</h3>
        <p>Price: $${game.price}</p>
      </div>
    `;
  });

  document.getElementById("back-btn").addEventListener("click", async () => {
    const user = await getCurrentUser();
    renderShop(user);
  });
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

    const roleBtn = userDiv.querySelector(`#change-role-${u.id}`);
    const roleSelect = userDiv.querySelector(`#role-${u.id}`);
    const toggleBtn = userDiv.querySelector(`#toggle-block-${u.id}`);

    roleBtn.addEventListener("click", async () => {
      const newRole = roleSelect.value;
      try {
        await updateUserRole(u.id, newRole);
        alert(`Role updated to ${newRole}`);
        renderAdminPanel(user);
      } catch (err) {
        alert("Error updating role: " + err.message);
        console.error(err);
      }
    });

    toggleBtn.addEventListener("click", async () => {
      try {
        await banUser(u.id);
        renderAdminPanel(user);
      } catch (err) {
        alert("Error updating status: " + err.message);
        console.error(err);
      }
    });
  });
  console.log("Users:", users);
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
      renderShop(user);
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