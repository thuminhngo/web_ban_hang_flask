let cart = [];

// Hàm thêm sản phẩm vào giỏ hàng
function addToCart(product) {
    const productIndex = cart.findIndex(item => item.id === product.id);
    
    if (productIndex > -1) {
        // Nếu sản phẩm đã có trong giỏ, tăng số lượng
        cart[productIndex].quantity += 1;
    } else {
        // Nếu sản phẩm chưa có trong giỏ, thêm vào giỏ
        cart.push({...product, quantity: 1});
    }
    
    updateCartDisplay();
}

// Hàm hiển thị giỏ hàng
function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cart_items');
    const totalPriceElement = document.getElementById('total_price');
    
    cartItemsContainer.innerHTML = '';  // Làm sạch giỏ hàng trước khi cập nhật
    let totalPrice = 0;
    
    cart.forEach(item => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        
        cartItem.innerHTML = `
            <img src="${item.hinh_anh ? item.hinh_anh : 'static/default.png'}" alt="${item.ten_san_pham}">
            <h3>${item.ten_san_pham}</h3>
            <p>Giá: ${item.gia}đ</p>
            <p>Số lượng: 
                <button onclick="updateQuantity(${item.id}, 'decrease')">-</button>
                <span>${item.quantity}</span>
                <button onclick="updateQuantity(${item.id}, 'increase')">+</button>
            </p>
            <button onclick="removeFromCart(${item.id})">Xóa</button>
        `;
        
        cartItemsContainer.appendChild(cartItem);
        totalPrice += item.gia * item.quantity;
    });
    
    totalPriceElement.innerText = `${totalPrice.toLocaleString()}đ`;
}

// Hàm thay đổi số lượng sản phẩm trong giỏ
function updateQuantity(productId, action) {
    const productIndex = cart.findIndex(item => item.id === productId);
    
    if (productIndex > -1) {
        if (action === 'increase') {
            cart[productIndex].quantity += 1;
        } else if (action === 'decrease' && cart[productIndex].quantity > 1) {
            cart[productIndex].quantity -= 1;
        }
    }
    
    updateCartDisplay();
}

// Hàm xóa sản phẩm khỏi giỏ
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartDisplay();
}

// Hàm thanh toán
function checkout() {
    if (cart.length === 0) {
        alert("Giỏ hàng của bạn đang trống.");
        return;
    }
    
    alert("Thanh toán thành công!");
    cart = [];  // Xóa giỏ hàng sau khi thanh toán
    updateCartDisplay();
}

// Hàm mở giỏ hàng
document.getElementById('viewCart').addEventListener('click', function() {
    document.getElementById('cart_section').style.display = 'block';
});
