// camps.js - Requires api.js
document.addEventListener('DOMContentLoaded', () => {
    loadCamps();
    setupCampForm();
});

async function loadCamps() {
    const campsContainer = document.getElementById('camps-container');
    if (!campsContainer) return;

    try {
        const camps = await api.get('/camp/all');
        renderCamps(camps);
    } catch (error) {
        campsContainer.innerHTML = '<p class="error">Failed to load events. Please try again later.</p>';
        console.error(error);
    }
}

function renderCamps(camps) {
    const campsContainer = document.getElementById('camps-container');
    campsContainer.innerHTML = '';

    if (camps.length === 0) {
        campsContainer.innerHTML = '<p>No upcoming camps.</p>';
        return;
    }

    camps.forEach(camp => {
        const campCard = document.createElement('div');
        campCard.classList.add('camp-card');

        campCard.innerHTML = `
            <div class="camp-details">
                <h3>${camp.event_name || 'Volunteer Camp'}</h3>
                <p><strong>Date:</strong> ${camp.event_date || 'TBD'}</p>
                <p><strong>Location:</strong> ${camp.address}</p>
                <p><strong>Duration:</strong> ${camp.hours} hours</p>
                <p><strong>Organizer:</strong> ${camp.volunteer_name || camp.full_name}</p>
                <p>${camp.message || 'Join us to remove Karuvela trees.'}</p>
                <button class="join-btn" onclick="joinEvent(${camp.id})">Join Event</button>
            </div>
        `;
        campsContainer.appendChild(campCard);
    });
}

async function joinEvent(campId) {
    const username = localStorage.getItem('username');
    if (!username) {
        alert('Please login first to join the event.');
        window.location.href = './login_page.html';
        return;
    }

    try {
        const response = await api.post(`/camp/join/${campId}?username=${username}`);
        alert(response.message || 'Joined successfully!');
    } catch (error) {
        alert('Joining failed: ' + error.message);
    }
}

function setupCampForm() {
    const form = document.querySelector('.contact-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 1. Verify Authentication
        const username = localStorage.getItem('username');
        if (!username) {
            alert('Please login first to connect with a camp.');
            window.location.href = './login_page.html';
            return;
        }

        try {
            // 2. Verify Volunteer Status
            const volunteer = await api.get(`/volunteers/user/${username}`);

            if (volunteer.status !== 'Approved') {
                alert('Only Approved Volunteers can propose or connect to a new camp. Please wait for admin approval of your volunteer status.');
                return;
            }

            // 3. Prepare Data
            const data = {
                event_name: document.getElementById('Event').value,
                full_name: document.getElementById('name').value,
                volunteer_id: volunteer.id,
                email: document.getElementById('email').value,
                phone: document.getElementById('Phone_no').value,
                address: document.getElementById('address').value,
                hours: parseInt(document.getElementById('time').value) || 0,
                event_date: document.getElementById('date').value,
                message: document.getElementById('message').value
            };

            // 4. Submit Proposal
            await api.post('/camp/create', data);

            alert('Your camp proposal has been submitted! It will appear on the page once approved by the admin.');
            form.reset();

        } catch (error) {
            if (error.message.includes('404')) {
                alert('You are not registered as a volunteer. Please register in the Volunteer Section first.');
            } else {
                alert('Failed to submit proposal: ' + error.message);
            }
        }
    });
}
