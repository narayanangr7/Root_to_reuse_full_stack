// admin.js - Requires api.js
document.addEventListener('DOMContentLoaded', () => {
    // Check if logged in as admin
    const username = localStorage.getItem('username');
    if (username !== 'nara' && username !== 'demoadmin') {
        alert('Admin access only!');
        window.location.href = './pages/login_page.html';
        return;
    }

    // Sidebar Navigation Logic
    setupNavigation();

    // Initial Load
    loadStats();
    loadVolunteers();
    loadCampRequests();
    loadProductsTable();
    loadCategoryOptions();

    // Form Submissions
    setupProductForm();
    setupCategoryForm();
});

function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.admin-page');
    const pageTitle = document.getElementById('page-title');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const sectionName = item.getAttribute('data-section');

            // Update Active Nav Item
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Show Corresponding Section
            sections.forEach(sec => sec.classList.remove('active'));
            const target = document.getElementById(`section-${sectionName}`);
            if (target) target.classList.add('active');

            // Update Header Title
            pageTitle.textContent = item.textContent;
        });
    });
}

async function loadStats() {
    try {
        const [products, categories, volunteers, camps] = await Promise.all([
            api.get('/products'),
            api.get('/catagory'),
            api.get('/volunteers'),
            api.get('/camp/requests')
        ]);

        document.getElementById('total-products').textContent = products.length;
        document.getElementById('total-categories').textContent = categories.length;
        document.getElementById('total-volunteers').textContent = volunteers.length;
        document.getElementById('total-camps').textContent = camps.length;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadVolunteers() {
    const container = document.getElementById('volunteers-container');
    if (!container) return;

    try {
        const volunteers = await api.get('/volunteers');
        console.log("Fetched volunteers:", volunteers);

        if (!Array.isArray(volunteers)) {
            console.error("Expected array but got:", volunteers);
            container.innerHTML = '<p>Error: Invalid data format received from server.</p>';
            return;
        }

        container.innerHTML = volunteers.length ? '' : '<p>No volunteer requests found.</p>';

        volunteers.forEach(v => {
            const card = document.createElement('div');
            card.classList.add('volunteer-card');

            const statusColor = v.status === 'Approved' ? '#27ae60' : '#f39c12';

            card.innerHTML = `
                <div class="volunteer-header">
                    <div class="volunteer-name">${v.full_name}</div>
                    <span style="background: ${statusColor}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">${v.status}</span>
                </div>
                <div class="volunteer-info"><strong>User:</strong> ${v.username} (Ref: ${v.user_phone})</div>
                <div class="volunteer-info"><strong>Email:</strong> ${v.email}</div>
                <div class="volunteer-info"><strong>Phone:</strong> ${v.phone_no}</div>
                <div class="volunteer-info"><strong>Skills:</strong> ${v.skills || 'N/A'}</div>
                <div class="volunteer-info"><strong>Location:</strong> ${v.location}</div>
                <div class="volunteer-info"><strong>Age:</strong> ${v.age}</div>
                
                <div class="volunteer-actions" style="margin-top:15px; display: flex; gap: 10px;">
                    ${v.status !== 'Approved' ?
                    `<button class="btn btn-success" onclick="approveVolunteer(${v.id})" style="flex:1">Approve</button>` :
                    ''
                }
                    <button class="btn btn-danger" onclick="deleteVolunteer(${v.id})" style="flex:1">${v.status === 'Approved' ? 'Remove' : 'Reject'}</button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading volunteers:', error);
    }
}

async function loadCampRequests() {
    const container = document.getElementById('camps-requests-container');
    if (!container) return;

    try {
        const camps = await api.get('/camp/requests');
        container.innerHTML = camps.length ? '' : '<p>No camp requests found.</p>';

        camps.forEach(c => {
            const card = document.createElement('div');
            card.classList.add('volunteer-card');

            const statusColor = c.status === 'Approved' ? '#27ae60' : '#f39c12';

            card.innerHTML = `
                <div class="volunteer-header">
                    <div class="volunteer-name">${c.event_name}</div>
                    <span style="background: ${statusColor}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px;">${c.status}</span>
                </div>
                <div class="volunteer-info"><strong>Proposed By:</strong> ${c.volunteer_name || c.full_name}</div>
                <div class="volunteer-info"><strong>Event Date:</strong> ${c.event_date || 'N/A'}</div>
                <div class="volunteer-info"><strong>Location:</strong> ${c.address}</div>
                <div class="volunteer-info"><strong>Hours:</strong> ${c.hours}h</div>
                <div class="volunteer-info"><strong>Contact:</strong> ${c.phone} | ${c.email}</div>
                <div class="volunteer-info" style="margin-top:5px; border-top: 1px dashed #ccc; padding-top:5px;">
                    <strong>Message:</strong> ${c.message || 'No message'}
                </div>
                
                <div class="volunteer-info" style="margin-top:10px; padding: 10px; background: #f0f7f0; border-radius: 4px;">
                    <strong>Joined Volunteers (${c.participants.length}):</strong>
                    <ul style="margin-top:5px; font-size: 13px; list-style: inside;">
                        ${c.participants.length > 0
                    ? c.participants.map(p => `<li>${p.volunteer_name} (${p.phone_no})</li>`).join('')
                    : '<li>No one joined yet</li>'}
                    </ul>
                </div>
                
                <div class="volunteer-actions" style="margin-top:15px; display: flex; gap: 10px;">
                    ${c.status !== 'Approved' ?
                    `<button class="btn btn-success" onclick="approveCamp(${c.id})" style="flex:1">Approve Camp</button>` :
                    ''
                }
                    <button class="btn btn-danger" onclick="deleteCamp(${c.id})" style="flex:1">${c.status === 'Approved' ? 'Remove' : 'Reject'}</button>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading camp requests:', error);
    }
}

async function approveVolunteer(id) {
    try {
        await api.post(`/volunteers/${id}/approve`);
        alert('Volunteer approved successfully!');
        loadVolunteers();
        loadStats();
    } catch (error) {
        alert('Approval failed: ' + error.message);
    }
}

async function approveCamp(id) {
    try {
        await api.post(`/camp/approve/${id}`);
        alert('Camp approved and published!');
        loadCampRequests();
        loadStats();
    } catch (error) {
        alert('Camp approval failed: ' + error.message);
    }
}

async function deleteCamp(id) {
    if (!confirm('Delete this camp request?')) return;
    try {
        await api.delete(`/camp/delete/${id}`);
        loadCampRequests();
        loadStats();
    } catch (error) {
        alert('Delete failed');
    }
}

async function loadProductsTable() {
    const tbody = document.querySelector('#products-table tbody');
    if (!tbody) return;

    try {
        const products = await api.get('/products');
        tbody.innerHTML = products.length ? '' : '<tr><td colspan="6">No products found.</td></tr>';

        products.forEach(p => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>₹${p.price}</td>
                <td>${p.product_type}</td>
                <td>${p.material}</td>
                <td>
                    <div class="action-buttons">
                        <button class="btn btn-danger" onclick="deleteProduct(${p.id})">Delete</button>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function loadCategoryOptions() {
    const select = document.getElementById('product-category-select');
    if (!select) return;

    try {
        const categories = await api.get('/catagory');
        select.innerHTML = '<option value="">Select Category</option>';
        categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function setupProductForm() {
    const form = document.getElementById('product-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const inputs = form.querySelectorAll('input, select, textarea');
        const data = {
            name: inputs[0].value,
            category_id: parseInt(inputs[1].value),
            price: parseInt(inputs[2].value),
            product_type: inputs[3].value,
            description: inputs[4].value,
            material: inputs[5].value,
            length: inputs[6].value,
            weight: inputs[7].value,
            shelf_life: inputs[8].value,
            usage: inputs[9].value,
            image: inputs[10].value
        };

        try {
            await api.post('/products/create_product', data);
            alert('Product added successfully!');
            form.reset();
            loadProductsTable();
            loadStats();
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

function setupCategoryForm() {
    const form = document.getElementById('category-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const inputs = form.querySelectorAll('input, textarea');
        const data = {
            name: inputs[0].value,
            content: inputs[2].value
        };

        try {
            await api.post('/catagory', data);
            alert('Category added successfully!');
            form.reset();
            loadCategoryOptions();
            loadStats();
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function deleteProduct(id) {
    if (!confirm('Delete this product?')) return;
    try {
        await api.delete(`/products/${id}`);
        loadProductsTable();
        loadStats();
    } catch (error) {
        alert('Delete failed');
    }
}

async function deleteVolunteer(id) {
    if (!confirm('Delete this request?')) return;
    try {
        await api.delete(`/volunteers/${id}`);
        loadVolunteers();
        loadStats();
    } catch (error) {
        alert('Delete failed');
    }
}
