// volunteer.js - Requires api.js

document.addEventListener('DOMContentLoaded', () => {
    const volunteerForm = document.getElementById('volunteer-form');
    if (volunteerForm) {
        volunteerForm.addEventListener('submit', handleVolunteerSubmit);
    }
});

async function handleVolunteerSubmit(event) {
    event.preventDefault();

    const userId = localStorage.getItem('user_id');
    const user_username = localStorage.getItem('username');
    const user_phone = localStorage.getItem('user_phone');

    if (!userId || !user_username || !user_phone) {
        alert('Please login first to register as a volunteer');
        window.location.href = './login_page.html';
        return;
    }

    const full_name = document.getElementById('vol-name').value;
    const email = document.getElementById('vol-email').value;
    const phone_no = document.getElementById('vol-phone').value;
    const skills = document.getElementById('vol-skills').value;
    const age = document.getElementById('vol-age').value;
    const location = document.getElementById('vol-location').value;

    const volunteerData = {
        full_name: full_name,
        username: user_username,
        user_phone: user_phone, // Send as string
        email: email,
        phone_no: phone_no,
        skills: skills,
        age: parseInt(age) || 0,
        location: location
    };

    console.log("Sending Payload:", JSON.stringify(volunteerData));

    try {
        const response = await api.post('/volunteers', volunteerData);
        console.log("Success:", response);
        alert('Thank you for volunteering! We will contact you soon.');
        document.getElementById('volunteer-form').reset();
    } catch (error) {
        console.error("Submission error details:", error);
        alert('Submission failed: ' + error.message);
    }
}
