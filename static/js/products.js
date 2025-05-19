document.addEventListener("DOMContentLoaded", () => {
    const productsLink = document.getElementById("products");
    const productsContent = document.getElementById("products_content");

    // Hàm hiển thị section cụ thể và ẩn các section khác
    function showSection(sectionId, contentElement, content) {
        const sections = ["products_content", "account_section", "cart_content"];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) {
                section.style.display = id === sectionId ? "block" : "none";
            }
        });
        if (contentElement && content) {
            contentElement.innerHTML = content;
        }
    }

    if (productsLink) {
        productsLink.addEventListener("click", function (e) {
            e.preventDefault();
            fetch("/products")
                .then(response => response.json())
                .then(data => {
                    showSection("products_content", productsContent, data.html);
                    // Gắn sự kiện cho các nút "Thêm vào giỏ" sau khi nội dung được tải
                    attachAddToCartEvents();
                })
                .catch(error => {
                    console.error("Lỗi khi tải danh sách sản phẩm:", error);
                });
        });
    }

    // Hàm gắn sự kiện cho các nút "Thêm vào giỏ"
    function attachAddToCartEvents() {
        const addToCartButtons = document.querySelectorAll(".add-to-cart");
        addToCartButtons.forEach(button => {
            button.addEventListener("click", function () {
                const productId = this.getAttribute("data-product-id");
                addToCart(productId);
            });
        });
    }

    // Hàm gửi yêu cầu thêm sản phẩm vào giỏ hàng
    function addToCart(productId) {
        fetch("/add_to_cart", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1 // Mặc định thêm 1 sản phẩm
            })
        })
            .then(response => {
                if (!response.ok) throw new Error("Yêu cầu thêm sản phẩm thất bại: " + response.status);
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert("Sản phẩm đã được thêm vào giỏ hàng!");
                    
                } else {
                    alert(data.message || "Lỗi khi thêm sản phẩm vào giỏ hàng.");
                }
            })
            .catch(error => {
                console.error("Lỗi khi thêm vào giỏ hàng:", error);
                alert("Không thể thêm sản phẩm vào giỏ hàng. Vui lòng thử lại.");
            });
    }
});