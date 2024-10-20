document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('form');
    const passwordInput = document.getElementById('password');
    
    loginForm.addEventListener('submit', function(event) {
        const username = document.getElementById('username').value;
        const password = passwordInput.value;

        // Basic validation
        if (!username || !password) {
            alert('Please fill in both fields.');
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });

    // Handle password visibility toggle
    const togglePasswordVisibility = document.getElementById('password');
    const togglePasswordVisibilityImage = document.getElementById('peekaboo');

    togglePasswordVisibilityImage.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent the anchor tag from causing any navigation
        console.log("clicked");
        // Toggle between password and text type for input
        if (togglePasswordVisibility.type === 'password') {
            togglePasswordVisibility.type = 'text';
            togglePasswordVisibilityImage.src = '/static/show.png';  // Change icon to "show" state
        } else {
            togglePasswordVisibility.type = 'password';
            togglePasswordVisibilityImage.src = '/static/hide.png';  // Change icon to "hide" state
        }
    });
});
