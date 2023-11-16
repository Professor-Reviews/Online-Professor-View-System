// profile.js

// ...
function updateProfile() {
    // Perform any necessary update logic here

    // Redirect to the homepage
    window.location.href = "homepage.html";
}

// Function to enable form fields for editing
function enableEditing() {
    const formFields = document.querySelectorAll('.profile-form input[readonly]');
    formFields.forEach(field => field.removeAttribute('readonly'));
}

// Function to fetch and display user profile data
async function fetchUserProfile() {
    try {
        const response = await fetch('http://localhost:5000/api/getUserProfile', {
            method: 'GET',
            // Do not include the Authorization header
        });

        if (response.ok) {
            const data = await response.json();
            console.log('User profile data:', data);  // Log the data
            updateProfileUI(data);
        } else {
            console.error('Failed to fetch user profile:', response.status);
        }
    } catch (error) {
        console.error('Error during fetchUserProfile:', error);
    }
}

// Function to update the profile UI with user data
function updateProfileUI(userData) {
    // Update HTML elements with user data
    document.getElementById('username').value = userData.username;
    document.getElementById('studentEmail').value = userData.studentEmail;
    document.getElementById('fName').value = userData.fName;
    document.getElementById('lName').value = userData.lName;
    // Update other profile elements as needed
}


// Function to submit updated profile data to the server
async function submitUpdateProfile(updatedProfileData) {
    try {
        const response = await fetch('http://localhost:5000/api/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify(updatedProfileData),
        });

        if (response.ok) {
            // Profile update successful, you can provide feedback or redirect to another page
            console.log('Profile updated successfully');
            fetchUserProfile(); // Fetch updated profile after successful update
        } else {
            // Handle error, e.g., show an error message
            console.error('Failed to update profile');
        }
    } catch (error) {
        console.error('Error during profile update:', error);
    }
}

// Add an event listener to call fetchUserProfile when the DOM is loaded
document.addEventListener('DOMContentLoaded', fetchUserProfile);
