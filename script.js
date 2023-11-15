// DOM elements
const loginForm = document.getElementById("login-form");
const registerForm = document.getElementById("register-form");
const showRegisterButton = document.getElementById("show-register");
const loginButton = document.getElementById("login");
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

// Implement login functionality
loginButton.addEventListener("click", async () => {
    const studentEmail = document.getElementById("login-email").value; // Change to studentEmail
    const password = document.getElementById("login-password").value;

    try {
        const response = await fetch('http://localhost:5000/authenticate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                studentEmail: studentEmail, // Correct field name
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            // Login successful, you can redirect to the homepage or perform other actions
            localStorage.setItem('authToken', data.token);
            window.location.href = "homepage.html";
        } else {
            // Handle login failure, display an error message, etc.
            console.error('Login failed:', data.message);
        }
    } catch (error) {
        console.error('Error during login:', error);
    }
});

// Implement registration functionality
registerButton.addEventListener("click", async () => {
    const studentEmail = document.getElementById("register-email").value; // Change to studentEmail
    const username = document.getElementById("register-username").value;
    const fName = document.getElementById("register-firstname").value;
    const lName = document.getElementById("register-lastname").value;
    const password = document.getElementById("register-password").value;

    // Frontend validation
    if (!validateRegistrationInputs(studentEmail, username, fName, lName, password)) {
        // Validation failed, display an error message or take appropriate action
        console.error('Registration validation failed');
        return;
    }

    try {
        // Your registration fetch request here
        const response = await fetch('http://localhost:5000/registerStudent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                studentEmail: studentEmail,
                username: username,
                fName: fName,
                lName: lName,
                password: password,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            // Registration successful, you can redirect to the homepage or perform other actions
            localStorage.setItem('authToken', data.token);
            window.location.href = "homepage.html";
        } else {
            // Handle registration failure, display an error message, etc.
            console.error('Registration failed:', data.message);
        }
    } catch (error) {
        console.error('Error during registration:', error);
    }
});

// Function to validate registration inputs
function validateRegistrationInputs(email, username, firstName, lastName, password) {
    // Perform your validation logic here
    // For example, check if the email and username are not empty
    if (!email || !username || !firstName || !lastName || !password) {
        alert('Please fill in all fields.');
        return false;
    }

    // Additional validation logic can be added as needed

    return true;
}
