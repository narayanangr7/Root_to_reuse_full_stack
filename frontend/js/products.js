// products.js - Requires api.js

let categoryData = {}; // Will be populated dynamically

const contentTemplates = {
    "Tooth Brush": {
        title: "🪥 Karuvela Tooth Brush",
        color: "#4A7C29", // Organic Green
        description: "Natural and organic tooth brushes made from authentic Karuvela wood. Traditional oral care with medicinal properties for healthy teeth and gums."
    },
    "Firewood": {
        title: "🔥 Karuvela Firewood",
        color: "#D35400", // Warm Fire Orange
        description: "High-quality Karuvela firewood known for its excellent burning properties, long-lasting heat, and minimal smoke. Ideal for cooking and heating."
    },
    "Charcoal": {
        title: "⚫ Karuvela Charcoal",
        color: "#2C3E50", // Deep Charcoal
        description: "Premium quality Karuvela charcoal with superior burning time and heat intensity. Perfect for BBQ, grilling, and industrial applications."
    }
};

document.addEventListener('DOMContentLoaded', async () => {
    await initializeCategories();

    // Check if category is in URL, else use default
    const params = new URLSearchParams(window.location.search);
    const catId = params.get('category');

    if (catId && categoryData[catId]) {
        switchCategory(parseInt(catId), false);
    } else {
        // Find the first available category if none in URL
        const firstCatId = Object.keys(categoryData)[0];
        if (firstCatId) {
            switchCategory(parseInt(firstCatId), false);
        } else {
            loadProducts();
        }
    }
});

async function initializeCategories() {
    try {
        const categories = await api.get('/catagory/');
        const tabsContainer = document.querySelector('.tabs');
        if (tabsContainer) tabsContainer.innerHTML = ''; // Clear hardcoded tabs

        categories.forEach(cat => {
            // Map fetched category to our content templates
            // Use loose matching for names to be robust
            let template = null;
            for (let key in contentTemplates) {
                if (cat.name.toLowerCase().includes(key.toLowerCase())) {
                    template = contentTemplates[key];
                    break;
                }
            }

            // Store in categoryData with actual DB ID
            categoryData[cat.id] = template || {
                title: cat.name,
                color: "#4A7C29",
                description: cat.content || "Discovery analysis: Root to Reuse " + cat.name + " provides premium sustainable value."
            };

            // Dynamically create tab
            if (tabsContainer) {
                const btn = document.createElement('button');
                btn.className = 'tab';
                btn.innerText = cat.name;
                btn.setAttribute('data-id', cat.id); // Add data-id for reliable identification
                btn.onclick = () => switchCategory(cat.id);
                tabsContainer.appendChild(btn);
            }
        });
    } catch (error) {
        console.error('Error initializing categories:', error);
    }
}

async function loadProducts() {
    const productsContainer = document.getElementById('products-container');
    if (!productsContainer) return;

    const categoryIdFilter = productsContainer.getAttribute('data-category-id');

    try {
        productsContainer.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Loading products...</p>
            </div>
        `;

        const products = await api.get('/products/');

        let filteredProducts = products;
        if (categoryIdFilter) {
            filteredProducts = products.filter(p => p.category_id == categoryIdFilter);
        }

        renderProducts(filteredProducts);
    } catch (error) {
        productsContainer.innerHTML = '<p class="error">Failed to load products. Please try again later.</p>';
        console.error(error);
    }
}

function switchCategory(categoryId, updateUrl = true) {
    const container = document.getElementById('products-container');
    const infoCard = document.querySelector('.info-card');
    const heroTitle = document.querySelector('.hero h1');

    if (!container || !infoCard) return;

    // Update data attribute
    container.setAttribute('data-category-id', categoryId);

    // Get the category data
    const data = categoryData[categoryId];
    if (data) {
        // Set dynamic tab color identity
        document.documentElement.style.setProperty('--tab-color', data.color || '#4A7C29');

        // Update Hero Title
        if (heroTitle) {
            const cleanTitle = data.title.replace(/[\u{1F300}-\u{1F9FF}]/gu, '').trim();
            heroTitle.innerHTML = `<span class="hero-icon">🌳</span> ${cleanTitle}`;
        }

        document.title = `${data.title.replace(/[\u{1F300}-\u{1F9FF}]/gu, '').trim()} - Root to Reuse`;

        // Update info card content
        infoCard.querySelector('h2').innerText = data.title;
        infoCard.querySelector('p').innerText = data.description;
    }

    // Update active tab UI using data-id
    document.querySelectorAll('.tab').forEach(tab => {
        const tabId = tab.getAttribute('data-id');
        if (tabId == categoryId) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    // Reload products
    loadProducts();

    if (updateUrl) {
        const newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?category=' + categoryId;
        window.history.pushState({ path: newUrl }, '', newUrl);
    }
}

function renderProducts(products) {
    const productsContainer = document.getElementById('products-container');
    productsContainer.innerHTML = '';

    if (products.length === 0) {
        productsContainer.innerHTML = '<p>No products found in this category.</p>';
        return;
    }

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.classList.add('product-card');

        let detailsLink = `./product_detail.html?id=${product.id}`;
        const imageSrc = product.image || '../assets/default-product.jpg';

        productCard.innerHTML = `
            <div class="product-image">
                <img src="${imageSrc}" alt="${product.name}">
            </div>
            <div class="product-content">
                <h3 class="product-title">${product.name}</h3>
                <p class="product-description">${product.description}</p>
                <div class="product-footer">
                    <div class="price">₹${product.price}</div>
                    <div style="display: flex; gap: 10px;">
                        <a href="${detailsLink}"><button class="btn" style="background-color: #666;">Details</button></a>
                        <button onclick="addToCart(event, ${product.id})" class="btn">Add to Cart</button>
                    </div>
                </div>
            </div>
        `;
        productsContainer.appendChild(productCard);
    });
}

async function addToCart(event, productId) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
        alert('Please login first to add items to cart');
        window.location.href = './login_page.html';
        return;
    }

    try {
        await api.post('/cart/add', {
            user_id: parseInt(userId),
            product_id: productId,
            quantity: 1
        });

        const btn = event ? event.currentTarget : null;
        if (btn && btn.classList.contains('btn')) {
            const originalText = btn.innerText;
            const originalBg = btn.style.backgroundColor;
            btn.innerText = 'Added! ✓';
            btn.style.backgroundColor = '#28a745';
            btn.disabled = true;

            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.backgroundColor = originalBg;
                btn.disabled = false;
            }, 2000);
        } else {
            alert('Product added to cart!');
        }

    } catch (error) {
        console.error('Error adding to cart:', error);
        alert('Failed to add product to cart: ' + error.message);
    }
}
