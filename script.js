// DOM elements
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const showRegisterButton = document.getElementById("show-register");
const loginButton = document.getElementById("login-button");
const registerButton = document.getElementById("register-button");

// Initially, hide the registration form
registerForm.style.display = "none";

// Show the registration form when the "Don't have an account" link is clicked
showRegisterButton.addEventListener("click", () => {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
});

// Show the login form when the "Login" button is clicked
loginButton.addEventListener("click", () => {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
});

// Implement login and registration functionality
loginButton.addEventListener("click", () => {
    const loginEmail = document.getElementById("login-email").value;
    const loginPassword = document.getElementById("login-password").value;
    // Add your login logic here
});

registerButton.addEventListener("click", () => {
    const registerEmail = document.getElementById("register-email").value;
    const registerUsername = document.getElementById("register-username").value;
    const registerPassword = document.getElementById("register-password").value;
    // Add your registration logic here
});
