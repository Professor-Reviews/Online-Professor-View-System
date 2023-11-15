// Function to check if the user is already logged in
async function checkLoginStatus() {
    try {
        const response = await fetch('http://localhost:5000/api/check-login-status', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            return data.isLoggedIn;
        } else {
            console.error('Failed to check login status:', response.statusText);
            return false;
        }
    } catch (error) {
        console.error('Error during checkLoginStatus:', error);
        return false;
    }
}

// Function to handle login success
function handleLoginSuccess(token) {
    localStorage.setItem('authToken', token);
    updateUI();
}

// Function to handle logout
function handleLogout() {
    console.log('Logging out...');
    localStorage.removeItem('authToken');
    updateUI();
}

// Function to handle "Post Your Review" button click


// Add event listener for "Post Your Review" button
document.getElementById("post-review-button").addEventListener("click", handlePostReviewButtonClick);


async function fetchReviews() {
    try {
        const response = await fetch('http://localhost:5000/api/getReviews');
        const data = await response.json();

        if (response.ok) {
            // Update UI to display reviews
            displayReviews(data.reviews);
        } else {
            console.error('Failed to fetch reviews:', data.error);
        }
    } catch (error) {
        console.error('Error during fetchReviews:', error);
    }
}

function displayReviews(reviews) {
    // Update your HTML to display reviews
    const reviewsContainer = document.getElementById('all-reviews-container');
    reviewsContainer.innerHTML = '';
    reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.classList.add('review');

        reviewElement.innerHTML = `
            <div class="review-header">
                <img src="prof.jpg" alt="Professor's Image" class="professor-image">
                <div class="professor-info">
                    <p>Professor ${review.profName}</p>
                    <p>Course: ${review.className}</p>
                </div>
            </div>
            <div class="review-body">
                <p>${review.reviewDescription}</p>
            </div>
            <div class="review-footer">
                <label for="rating">Rating: ${review.rating}</label>
                <button class="review-button">Want to leave a review?</button>
            </div>
            
        `;
        reviewElement.style.Height = '280px'; // Adjust the width as needed
        reviewElement.style.padding = '10px';


        reviewsContainer.appendChild(reviewElement);
    });
}
document.getElementById("search-button").addEventListener("click", async () => {
    const searchQuery = document.getElementById("search-bar").value;
    const filterOption = document.getElementById("filter-options").value;

    try {
        const response = await fetch(`http://localhost:5000/api/searchReviews?query=${searchQuery}&filter=${filterOption}`);
        const data = await response.json();

        if (response.ok) {
            // Update UI to display search results
            displayReviews(data.reviews);
        } else {
            console.error('Failed to fetch search results:', data.error);
        }
    } catch (error) {
        console.error('Error during searchReviews:', error);
    }
});











// Function to update the UI based on login status
async function updateUI() {
    const isLoggedIn = await checkLoginStatus();
    const createReviewButton = document.getElementById("create-review-button");
    const profileButton = document.getElementById("profile-button");
    const logoutButton = document.getElementById("logout-button");
    const userStatus = document.getElementById("user-status");
    const loginButton = document.getElementById("login-button");

    // Check if the user is not logged in and it's the initial state
    if (!isLoggedIn && localStorage.getItem('authToken')) {
        console.log('Clearing invalid authToken...');
        localStorage.removeItem('authToken');
    }

    // Show/hide elements based on login status
    userStatus.style.display = isLoggedIn ? 'block' : 'none';
    loginButton.style.display = isLoggedIn ? 'none' : 'block';
    createReviewButton.style.display = isLoggedIn ? 'block' : 'none';
    profileButton.style.display = isLoggedIn ? 'block' : 'none';
    logoutButton.style.display = isLoggedIn ? 'block' : 'none';
}

document.addEventListener("DOMContentLoaded", () => {
    fetchReviews();
    document.getElementById("post-review-button").addEventListener("click", handlePostReviewButtonClick);
    const loginButton = document.getElementById("login-button");
    const logoutButton = document.getElementById("logout-button");
    const createReviewButton = document.getElementById("create-review-button");
    const profileButton = document.getElementById("profile-button");
    const wantToLeaveReviewButtons = document.querySelectorAll(".review-button");
    const postReviewButton = document.getElementById("post-review-button");

    // Function to toggle the visibility of the "Create a Review" options
    const toggleCreateReviewOptions = () => {
        const createReviewOptions = document.getElementById("create-review-options");
        createReviewOptions.style.display = createReviewOptions.style.display === "none" ? "block" : "none";
    };

    // Function to handle "Want to leave a review?" button click
    const handleWantToLeaveReviewButtonClick = () => {
        toggleCreateReviewOptions();
    };

    // Add event listeners
    profileButton.addEventListener("click", () => {
        // Redirect to the profile page
        window.location.href = "profile.html";
    });

    createReviewButton.addEventListener("click", toggleCreateReviewOptions);
    postReviewButton.addEventListener("click", toggleCreateReviewOptions);

    wantToLeaveReviewButtons.forEach(button => {
        button.addEventListener("click", handleWantToLeaveReviewButtonClick);
    });

    postReviewButton.addEventListener("click", handlePostReviewButtonClick);
    loginButton.addEventListener("click", () => {
        // Redirect to the login page (firstiteration.html)
        window.location.href = "firstiteration.html";

    });
    logoutButton.addEventListener("click", async () => {
        console.log('Logging out...');
        await fetch('http://localhost:5000/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            }
        });

        // After logging out, clear the authentication token and update the UI
        localStorage.removeItem('authToken');
        updateUI();
    });

    updateUI(); // Ensure UI is updated on page load
});
document.addEventListener('DOMContentLoaded', () => {
    fetchReviews();

    // Add event listener for "Post Your Review" button
    document.getElementById("post-review-button").addEventListener("click", handlePostReviewButtonClick);
});
document.addEventListener('DOMContentLoaded', async () => {
    const isLoggedIn = await checkLoginStatus();
    if (isLoggedIn) {
        // Update UI for logged-in user
        updateUI();
    }
});

async function handlePostReviewButtonClick() {
    const professorName = document.getElementById("professor-name").value;
    const className = document.getElementById("class-Name").value; // Adjusted to match the frontend
    const ratingInput = document.getElementById("rating");
    const rating = parseFloat(ratingInput.value).toFixed(1);

    const reviewDescription = document.getElementById("review-description").value; // Adjusted to match the frontend

    const response = await fetch('http://localhost:5000/addReview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('authToken')}`
        },
        body: JSON.stringify({
            profName: professorName, // Adjusted to match the backend
            className: className, // Adjusted to match the backend
            rating: rating,
            reviewDescription: reviewDescription // Adjusted to match the backend
        })
    });

    if (response.ok) {
        // Handle successful review submission, e.g., update UI or show a success message

        console.log('Review submitted successfully');

        // After submitting a review, fetch and display all reviews
        fetchReviews();
    } else {
        // Handle error, e.g., show an error message
        console.error('Failed to submit review');
    }
}

