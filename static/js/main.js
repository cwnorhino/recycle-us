document.addEventListener('DOMContentLoaded', function () {
    const signupForm = document.getElementById('signup-form');
    const loginForm = document.getElementById('login-form');
    const showLogin = document.getElementById('show-login');
    const showSignup = document.getElementById('show-signup');

    // Toggle between signup and login forms
    showLogin.addEventListener('click', function (e) {
        e.preventDefault();
        signupForm.style.display = 'none';
        loginForm.style.display = 'block';
        showLogin.parentElement.style.display = 'none';
        showSignup.parentElement.style.display = 'block';
    });

    showSignup.addEventListener('click', function (e) {
        e.preventDefault();
        loginForm.style.display = 'none';
        signupForm.style.display = 'block';
        showSignup.parentElement.style.display = 'none';
        showLogin.parentElement.style.display = 'block';
    });

    // Handle signup form submission
    signupForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var email = document.getElementById('signup-email').value;
        var password = document.getElementById('signup-password').value;
        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password }),
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Signup successful!');
                    // Redirect to home page or dashboard
                    window.location.href = '/';
                } else {
                    alert('Signup failed: ' + (data.message || 'Please try again.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
    });

    // Handle login form submission
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        var email = document.getElementById('login-email').value;
        var password = document.getElementById('login-password').value;
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email, password: password }),
            credentials: 'include'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Login successful!');
                    window.location.href = '/profile';  // Redirect to profile page
                } else {
                    alert('Login failed: ' + (data.message || 'Please check your credentials and try again.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            });
    });
});