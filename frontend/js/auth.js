// auth.js - Requires api.js to be loaded first

async function handleLogin() {
    const usernameInput = document.getElementById('loginUsername');
    const passwordInput = document.getElementById('loginPassword');

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    // Standardize login: Allow the database to handle Nara's credentials too
    // This ensure Nara gets a real user_id and user_phone in localStorage
    if (!username || !password) {
        alert('Please fill in all fields');
        return;
    }

    try {
        // Note: Backend schema uses 'Password' with capital P for login
        const response = await api.post('/users/login', {
            id: 0, // Backend schema currently requires an ID for some reason
            username: username,
            Password: password
        });

        alert('Login Successful!');

        // Save user info
        localStorage.setItem('user_id', response.user_id);
        localStorage.setItem('username', response.username);
        localStorage.setItem('user_phone', response.phone_no);

        // Redirect based on role
        if (response.username === 'nara' || response.username === 'demoadmin') {
            window.location.href = '../admin.html';
        } else {
            window.location.href = '../index.html';
        }

    } catch (error) {
        alert('Login Failed: ' + error.message);
    }
}

async function handleSignup() {
    const username = document.getElementById('signupUsername').value.trim();
    const password = document.getElementById('signupPassword').value.trim();
    const phone = document.getElementById('signupPhone').value.trim();
    const email = document.getElementById('signupEmail').value.trim();

    if (!username || !password || !phone || !email) {
        alert('Please fill in all fields');
        return;
    }

    try {
        await api.post('/users/signup', {
            username: username,
            password: password,
            phone_no: phone.replace(/\D/g, ''), // Send as string
            email: email
        });

        alert('Account created successfully! Please login.');
        // Switch to login side
        if (typeof switchToLogin === 'function') {
            switchToLogin();
        }
    } catch (error) {
        alert('Signup Failed: ' + error.message);
    }
}
