console.log("Bắt đầu tải cart.js");

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded");

    const cartLink = document.getElementById("lg-bag");
    const cartContent = document.getElementById("cart_content");

    if (!cartLink) {
        console.error("Không tìm thấy phần tử #lg-bag");
    }
    if (!cartContent) {
        console.error("Không tìm thấy phần tử #cart_content");
    }

    function showSection(sectionId, contentElement, content) {
        console.log(`Hiển thị section: ${sectionId}`);
        const sections = ["products_content", "service_content", "account_content", "cart_content"];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) {
                section.style.display = id === sectionId ? "block" : "none";
            } else {
                console.warn(`Không tìm thấy section #${id}`);
            }
        });
        if (contentElement && content) {
            contentElement.innerHTML = content;
            attachDeleteButtons();
            attachQuantityButtons(); // Gắn sự kiện cho các nút tăng/giảm số lượng
        }
    }

    if (cartLink) {
        cartLink.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Nhấp vào liên kết giỏ hàng");
            fetch("/cart", { credentials: 'include' })
                .then(response => {
                    console.log("Phản hồi từ /cart:", response.status);
                    if (!response.ok) {
                        throw new Error(`Lỗi khi tải giỏ hàng: ${response.status} ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Dữ liệu giỏ hàng:", data);
                    showSection("cart_content", cartContent, data.html);
                })
                .catch(error => {
                    console.error("Lỗi khi tải giỏ hàng:", error);
                    cartContent.innerHTML = "<p>Không thể tải giỏ hàng. Vui lòng đăng nhập hoặc thử lại.</p>";
                });
        });
    }

    // Hàm gắn sự kiện cho các nút xóa
    function attachDeleteButtons() {
        const deleteButtons = document.querySelectorAll('.delete-item');
        if (deleteButtons.length === 0) {
            console.log("Không tìm thấy nút xóa nào");
        }
        deleteButtons.forEach(button => {
            button.addEventListener('click', function () {
                const productId = this.getAttribute('data-product-id');
                console.log(`Yêu cầu xóa sản phẩm ID: ${productId}`);

                // Hiển thị xác nhận trước khi xóa
                if (!confirm("Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?")) {
                    console.log("Người dùng hủy xóa sản phẩm ID:", productId);
                    return;
                }

                // Gửi yêu cầu xóa tới server
                fetch('/cart/delete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({ ma_san_pham: productId })
                })
                    .then(response => {
                        console.log("Phản hồi từ /cart/delete:", response.status);
                        if (!response.ok) {
                            return response.json().then(data => {
                                throw new Error(data.message || `Lỗi khi xóa sản phẩm: ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Phản hồi xóa:", data);
                        if (data.success) {
                            alert(data.message || "Sản phẩm đã được xóa khỏi giỏ hàng!");
                            // Tải lại giỏ hàng
                            fetch("/cart", { credentials: 'include' })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error(`Lỗi khi tải giỏ hàng: ${response.status}`);
                                    }
                                    return response.json();
                                })
                                .then(data => {
                                    showSection("cart_content", cartContent, data.html);
                                })
                                .catch(error => {
                                    console.error("Lỗi khi tải lại giỏ hàng:", error);
                                    cartContent.innerHTML = "<p>Không thể tải giỏ hàng. Vui lòng thử lại.</p>";
                                });
                        } else {
                            alert(`Lỗi: ${data.message || "Không thể xóa sản phẩm"}`);
                        }
                    })
                    .catch(error => {
                        console.error("Lỗi khi xóa sản phẩm:", error);
                        alert(`Có lỗi xảy ra: ${error.message}`);
                    });
            });
        });
    }

    // Hàm gắn sự kiện cho các nút tăng/giảm số lượng
    function attachQuantityButtons() {
        const quantityButtons = document.querySelectorAll('.quantity-btn');
        if (quantityButtons.length === 0) {
            console.log("Không tìm thấy nút tăng/giảm số lượng nào");
        }
        quantityButtons.forEach(button => {
            button.addEventListener('click', function () {
                const productId = this.getAttribute('data-product-id');
                const action = this.classList.contains('increase') ? 'increase' : 'decrease';
                console.log(`Yêu cầu ${action} số lượng sản phẩm ID: ${productId}`);

                const input = document.querySelector(`.quantity-input[data-product-id="${productId}"]`);
                if (!input) {
                    console.error("Không tìm thấy input số lượng cho sản phẩm ID:", productId);
                    return;
                }

                // Gửi yêu cầu cập nhật số lượng tới server
                fetch('/cart/update_quantity', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify({ ma_san_pham: productId, action: action })
                })
                    .then(response => {
                        console.log("Phản hồi từ /cart/update_quantity:", response.status);
                        if (!response.ok) {
                            return response.json().then(data => {
                                throw new Error(data.message || `Lỗi khi cập nhật số lượng: ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Phản hồi cập nhật số lượng:", data);
                        if (data.success) {
                            // Tải lại giỏ hàng
                            fetch("/cart", { credentials: 'include' })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error(`Lỗi khi tải giỏ hàng: ${response.status}`);
                                    }
                                    return response.json();
                                })
                                .then(data => {
                                    showSection("cart_content", cartContent, data.html);
                                })
                                .catch(error => {
                                    console.error("Lỗi khi tải lại giỏ hàng:", error);
                                    cartContent.innerHTML = "<p>Không thể tải giỏ hàng. Vui lòng thử lại.</p>";
                                });
                        } else {
                            alert(`Lỗi: ${data.message || "Không thể cập nhật số lượng"}`);
                        }
                    })
                    .catch(error => {
                        console.error("Lỗi khi cập nhật số lượng:", error);
                        alert(`Có lỗi xảy ra: ${error.message}`);
                    });
            });
        });
    }

    // Gắn sự kiện submit cho checkoutForm
    function attachCheckoutFormListener() {
        const checkoutForm = document.getElementById('checkoutForm');
        if (checkoutForm) {
            console.log("Đã tìm thấy checkoutForm, gắn sự kiện submit");
            checkoutForm.addEventListener('submit', function (e) {
                e.preventDefault();
                console.log("Form thanh toán được submit");

                const address = document.getElementById('address')?.value.trim();
                const phone = document.getElementById('phone')?.value.trim();

                console.log("Dữ liệu form:", { address, phone });

                if (!address || !phone) {
                    console.warn("Thiếu địa chỉ hoặc số điện thoại");
                    alert("Vui lòng nhập đầy đủ địa chỉ và số điện thoại!");
                    return;
                }

                const phoneRegex = /^\d{10,11}$/;
                if (!phoneRegex.test(phone)) {
                    console.warn("Số điện thoại không hợp lệ:", phone);
                    alert("Số điện thoại không hợp lệ! Vui lòng nhập 10-11 số.");
                    return;
                }

                const data = { address, phone };
                console.log("Dữ liệu gửi tới /checkout:", data);

                const submitButton = checkoutForm.querySelector('button[type="submit"]');
                submitButton.disabled = true;
                submitButton.textContent = "Đang xử lý...";

                fetch('/checkout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    body: JSON.stringify(data)
                })
                    .then(response => {
                        console.log("Phản hồi từ /checkout:", response.status);
                        if (!response.ok) {
                            return response.json().then(data => {
                                throw new Error(data.message || `Yêu cầu thất bại với mã: ${response.status}`);
                            });
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log("Dữ liệu phản hồi từ /checkout:", data);
                        submitButton.disabled = false;
                        submitButton.textContent = "Xác nhận thanh toán";
                        if (data.success) {
                            alert(`Đơn hàng đã được tạo thành công! Mã đơn hàng: ${data.order_id || 'N/A'}. Giỏ hàng của bạn đã được xóa.`);
                            closeCheckoutModal();
                            // Tải lại giỏ hàng
                            fetch("/cart", { credentials: 'include' })
                                .then(response => response.json())
                                .then(data => showSection("cart_content", cartContent, data.html))
                                .catch(error => {
                                    console.error("Lỗi khi tải lại giỏ hàng:", error);
                                    cartContent.innerHTML = "<p>Không thể tải giỏ hàng. Vui lòng thử lại.</p>";
                                });
                        } else {
                            alert(`Lỗi: ${data.message || 'Không rõ nguyên nhân'}`);
                            closeCheckoutModal();
                        }
                    })
                    .catch(error => {
                        console.error('Lỗi khi gửi yêu cầu checkout:', error);
                        submitButton.disabled = false;
                        submitButton.textContent = "Xác nhận thanh toán";
                        alert(`Có lỗi xảy ra: ${error.message}`);
                        closeCheckoutModal();
                    });
            });
        } else {
            console.error("Không tìm thấy checkoutForm");
        }
    }

    // Gắn sự kiện khi modal mở
    window.openCheckoutModal = function () {
        console.log("Mở modal thanh toán");
        const modal = document.getElementById('checkoutModal');
        if (modal) {
            modal.style.display = 'block';
            console.log("Modal đã hiển thị");
            // Reset form và gắn sự kiện
            const checkoutForm = document.getElementById('checkoutForm');
            if (checkoutForm) {
                checkoutForm.reset();
                attachCheckoutFormListener();
            } else {
                console.error("Không tìm thấy checkoutForm khi mở modal");
                alert("Lỗi: Không thể mở form thanh toán!");
            }
        } else {
            console.error("Không tìm thấy checkoutModal");
            alert("Lỗi: Không thể mở form thanh toán!");
        }
    };

    window.closeCheckoutModal = function () {
        console.log("Đóng modal thanh toán");
        const modal = document.getElementById('checkoutModal');
        if (modal) {
            modal.style.display = 'none';
            const checkoutForm = document.getElementById('checkoutForm');
            if (checkoutForm) {
                checkoutForm.reset();
            }
        } else {
            console.error("Không tìm thấy checkoutModal");
        }
    };

    // Gọi các hàm gắn sự kiện khi trang tải
    attachDeleteButtons();
    attachQuantityButtons();
});

console.log("Hoàn tất tải cart.js");