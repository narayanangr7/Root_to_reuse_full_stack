// product_detail.js - Handles dynamic product detail rendering and cart functionality

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const productId = params.get('id');

    if (!productId) {
        showError('Product not found.');
        return;
    }

    try {
        const product = await api.get(`/products/${productId}`);
        if (!product) {
            showError('Product not found.');
            return;
        }
        renderProductDetail(product);
    } catch (error) {
        console.error('Error loading product:', error);
        showError('Error loading product details. Please try again later.');
    }
});

function showError(message) {
    const container = document.getElementById('product-detail-container');
    if (container) {
        container.innerHTML = `<div class="error-message"><p>${message}</p><a href="./bresh.html" class="back-button">Back to Catalog</a></div>`;
    }
}

function renderProductDetail(product) {
    const container = document.getElementById('product-detail-container');
    if (!container) return;

    // Update page title
    document.title = `${product.name} - Root to Reuse`;

    // Dynamic rendering of the product card
    container.innerHTML = `
        <div class="product-card">
            <div class="product-content">
                <div class="product-image">
                    <img src="${product.image || '../assets/default-product.jpg'}" alt="${product.name}" />
                </div>

                <div class="product-info">
                    <h1>${product.name}</h1>
                    <div class="price">₹${product.price}</div>
                    <p class="description">${product.description || 'No description available.'}</p>
                    
                    <ul class="features">
                        ${generateFeatures(product)}
                    </ul>
                </div>
            </div>

            <div class="specifications">
                <h2>Product Specifications</h2>
                <table class="spec-table">
                    <tr>
                        <td>Product Type</td>
                        <td>${product.product_type || 'Natural Product'}</td>
                    </tr>
                    <tr>
                        <td>Material</td>
                        <td>${product.material || 'Organic Material'}</td>
                    </tr>
                    <tr>
                        <td>Weight</td>
                        <td>${product.weight || 'As per size'}</td>
                    </tr>
                    <tr>
                        <td>Shelf Life</td>
                        <td>${product.shelf_life || 'N/A'}</td>
                    </tr>
                    <tr>
                        <td>Usage</td>
                        <td>${product.usage || 'Daily Use'}</td>
                    </tr>
                </table>
            </div>

            <div class="enquiry-section">
                <h3>Interested in this product?</h3>
                <div class="action-buttons">
                    <button class="enquiry-button" onclick="addToCart(event, ${product.id})">ADD TO CART</button>
                </div>
            </div>
        </div>
    `;
}

// ... original generateFeatures ...

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

        // Show a nice success message
        const btn = event ? event.currentTarget : document.querySelector('.enquiry-button');
        if (btn) {
            const originalText = btn.innerText;
            const originalBg = btn.style.backgroundColor;
            btn.innerText = 'ADDED TO CART! ✓';
            btn.style.backgroundColor = '#28a745';
            btn.disabled = true;

            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.backgroundColor = originalBg;
                btn.disabled = false;
            }, 2000);
        }

    } catch (error) {
        console.error('Error adding to cart:', error);
        alert('Failed to add product to cart: ' + error.message);
    }
}
