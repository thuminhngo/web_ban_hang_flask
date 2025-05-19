document.addEventListener("DOMContentLoaded", () => {
    const accountIcon = document.getElementById("accountIcon");
    const accountContent = document.getElementById("account_content");

    // Hàm hiển thị section cụ thể và ẩn các section khác
    function showSection(sectionId) {
        console.log("Đang hiển thị section:", sectionId);
        const sections = [
            "profile-content",
            "password-content",
            "orders-content",
            "cart_content",
            "products_content"
        ];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (section) {
                section.style.display = id === sectionId ? "block" : "none";
            } else {
                console.warn(`Không tìm thấy section: ${id}`);
            }
        });
    }

    // Xử lý click vào biểu tượng tài khoản
    if (accountIcon) {
        accountIcon.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Đã click vào accountIcon, gửi yêu cầu đến /account");
            fetch("/account")
                .then(response => {
                    console.log("Phản hồi từ /account:", response.status);
                    return response.json();
                })
                .then(data => {
                    console.log("Dữ liệu HTML nhận được:", data.html.substring(0, 100)); // In 100 ký tự đầu
                    accountContent.innerHTML = data.html;
                    showSection("profile-content");
                    attachFormListener();
                    attachMenuListeners();
                })
                .catch(error => {
                    console.error("Lỗi khi tải thông tin tài khoản:", error);
                });
        });
    } else {
        console.error("Không tìm thấy accountIcon");
    }

    // Hàm gắn event listener cho menu
    function attachMenuListeners() {
        const menuItems = document.querySelectorAll(".menu-item");
        console.log("Số menu items tìm thấy:", menuItems.length);
        menuItems.forEach(item => {
            item.addEventListener("click", function (e) {
                e.preventDefault();
                const section = this.getAttribute("data-section");
                console.log("Đã click menu item, chuyển sang section:", section);
                showSection(`${section}-content`);
            });
        });
    }

    // Hàm gắn event listener cho form
    function attachFormListener() {
        const profileForm = document.querySelector("#profile-content form");
        if (profileForm) {
            console.log("Form đã được tìm thấy, gắn sự kiện submit...");
            profileForm.addEventListener("submit", function (e) {
                e.preventDefault();
                console.log("Form submitted!");
                const formData = {
                    ho_ten: document.getElementById("fullname").value,
                    email: document.getElementById("email").value,
                    so_dien_thoai: document.getElementById("phone").value
                };
                console.log("Dữ liệu gửi đi:", formData);

                fetch("/update_account", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(formData)
                })
                    .then(response => {
                        console.log("Phản hồi từ server:", response);
                        return response.json();
                    })
                    .then(data => {
                        console.log("Dữ liệu phản hồi:", data);
                        if (data.success) {
                            alert("Cập nhật thông tin thành công!");
                        } else {
                            alert("Lỗi: " + data.message);
                        }
                    })
                    .catch(error => {
                        console.error("Lỗi khi cập nhật thông tin:", error);
                        alert("Đã xảy ra lỗi khi cập nhật thông tin.");
                    });
            });
        } else {
            console.error("Không tìm thấy form trong #profile-content");
        }
    }
});