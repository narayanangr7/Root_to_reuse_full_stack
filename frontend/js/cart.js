// cart.js - Requires api.js
document.addEventListener('DOMContentLoaded', () => {
    loadCart();
});

async function loadCart() {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
        alert('Please login to view your cart');
        window.location.href = '../index.html';
        return;
    }

    const cartItemsContainer = document.querySelector('.cart-items');
    if (!cartItemsContainer) return;

    try {
        const cartItems = await api.get(`/cart/user/${userId}`);
        renderCart(cartItems);
    } catch (error) {
        console.error('Error loading cart:', error);
        cartItemsContainer.innerHTML = '<p>Error loading cart. Please try again later.</p>';
    }
}

function renderCart(items) {
    const cartItemsContainer = document.querySelector('.cart-items');
    cartItemsContainer.innerHTML = '';

    if (items.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty.</p>';
        updateSummary(0);
        return;
    }

    let subtotal = 0;

    items.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;

        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <div class="item-image">
                <img src="${item.image || '../assets/default-product.jpg'}" alt="${item.name}">
            </div>
            <div class="item-details">
                <div>
                    <div class="item-name">${item.name}</div>
                    <div class="item-description">${item.description || ''}</div>
                </div>
                <div class="item-actions">
                    <div class="quantity-control">
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">−</button>
                        <span class="quantity">${item.quantity}</span>
                        <button class="quantity-btn" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                    </div>
                    <div class="item-price">₹${item.price}</div>
                </div>
            </div>
            <button class="remove-btn" onclick="removeItem(${item.id})">Remove</button>
        `;
        cartItemsContainer.appendChild(cartItem);
    });

    updateSummary(subtotal);
}

async function updateQuantity(cartId, newQuantity) {
    if (newQuantity < 0) return;

    try {
        await api.put(`/cart/${cartId}`, { quantity: newQuantity });
        loadCart(); // Refresh cart
    } catch (error) {
        console.error('Error updating quantity:', error);
        alert('Failed to update quantity');
    }
}

async function removeItem(cartId) {
    if (!confirm('Are you sure you want to remove this item?')) return;

    try {
        await api.delete(`/cart/${cartId}`);
        loadCart(); // Refresh cart
    } catch (error) {
        console.error('Error removing item:', error);
        alert('Failed to remove item');
    }
}

function updateSummary(subtotal) {
    const shipping = subtotal > 0 ? 15 : 0;
    const tax = subtotal * 0.1; // 10% tax
    const total = subtotal + shipping + tax;

    // Update the UI
    const summaryRows = document.querySelectorAll('.summary-row span:last-child');
    if (summaryRows.length >= 4) {
        summaryRows[0].textContent = `₹${subtotal.toFixed(2)}`;
        summaryRows[1].textContent = `₹${shipping.toFixed(2)}`;
        summaryRows[2].textContent = `₹${tax.toFixed(2)}`;
        summaryRows[3].textContent = `₹${total.toFixed(2)}`;
    }
}
