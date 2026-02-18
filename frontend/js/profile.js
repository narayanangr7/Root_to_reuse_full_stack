// profile.js - Requires api.js
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
});

async function loadProfile() {
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');

    if (!userId || !username) {
        window.location.href = './login_page.html';
        return;
    }

    try {
        // 1. Fetch User Base Details
        const userData = await api.get(`/users/${userId}`);

        document.getElementById('display-username').textContent = userData.username;
        document.getElementById('info-username').textContent = userData.username;
        document.getElementById('info-email').textContent = userData.email;
        document.getElementById('info-phone').textContent = userData.phone_no;
        document.getElementById('info-id').textContent = `#${userData.id}`;

        // 2. Fetch Volunteer Status
        const statusContainer = document.getElementById('volunteer-status-container');
        try {
            const volunteerData = await api.get(`/volunteers/user/${username}`);

            const badge = document.createElement('div');
            badge.className = `volunteer-badge ${volunteerData.status.toLowerCase()}`;

            let statusText = '';
            if (volunteerData.status === 'Approved') {
                statusText = 'Verified Volunteer ✅';
            } else if (volunteerData.status === 'Pending') {
                statusText = 'Volunteer Request Pending ⏳';
            } else {
                statusText = `Volunteer Status: ${volunteerData.status}`;
            }

            badge.textContent = statusText;
            statusContainer.appendChild(badge);

        } catch (error) {
            // User is not registered as a volunteer
            const badge = document.createElement('div');
            badge.className = 'volunteer-badge none';
            badge.textContent = 'Not registered as a Volunteer';
            statusContainer.appendChild(badge);
        }

    } catch (error) {
        console.error('Error loading profile:', error);
        alert('Failed to load profile data.');
    }
}

function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.clear();
        window.location.href = '../index.html';
    }
}
