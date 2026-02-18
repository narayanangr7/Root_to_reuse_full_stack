// nav.js - Dynamic navigation logic
document.addEventListener('DOMContentLoaded', () => {
    updateNav();
    setupMobileMenu();
});

function setupMobileMenu() {
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links');

    if (toggleBtn && navLinks) {
        toggleBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            toggleBtn.textContent = navLinks.classList.contains('active') ? '✕' : '☰';
        });
    }
}

function updateNav() {
    const authBtn = document.getElementById('nav-auth-btn');
    if (!authBtn) return;

    const username = localStorage.getItem('username');

    if (username) {
        // User is logged in
        if (username === 'nara' || username === 'demoadmin') {
            authBtn.textContent = 'Admin Dashboard';
            authBtn.href = window.location.pathname.includes('/pages/') ? '../admin.html' : './admin.html';
        } else {
            authBtn.textContent = 'My Profile';
            authBtn.href = window.location.pathname.includes('/pages/') ? './profile.html' : './pages/profile.html';
        }

        // Optional: Add styling to indicate active session
        authBtn.style.background = '#27ae60';
        authBtn.style.color = 'white';
    } else {
        // User is logged out
        authBtn.textContent = 'Login';
        authBtn.href = window.location.pathname.includes('/pages/') ? './login_page.html' : './pages/login_page.html';
    }
}
