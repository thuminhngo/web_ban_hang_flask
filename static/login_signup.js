
let loginModal = document.getElementById("loginModal");
let signupModal = document.getElementById("signupModal");

let openLogin = document.getElementById("openLogin");  
let closeLogin = document.getElementById("closeLogin");  
let closeSignup = document.getElementById("closeSignup");  
let showSignup = document.getElementById("showSignup");  


openLogin.onclick = function() {
    loginModal.style.display = "block";
}

closeLogin.onclick = function() {
    loginModal.style.display = "none";
}

closeSignup.onclick = function() {
    signupModal.style.display = "none";
}

//
showSignup.onclick = function() {
    loginModal.style.display = "none";
    signupModal.style.display = "block"; 
}


window.onclick = function(event) {
    if (event.target == loginModal || event.target == signupModal) {
        loginModal.style.display = "none";
        signupModal.style.display = "none";
    }
}

// Xử lý gửi form Đăng Nhập 
document.getElementById("loginForm").onsubmit = function(event) {
    event.preventDefault(); 
    let email = document.getElementById("email").value;
    let matKhau = document.getElementById("mat_khau").value;

    if (!email || !matKhau) {
        alert("Vui lòng điền đầy đủ email và mật khẩu!");
        return; 
    }

    
    let formData = {
        'email': email,
        'password': matKhau 
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  
            'Accept': 'application/json' 
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (data.message) {
            loginModal.style.display = "none"; 
            window.location.href = '/account';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Có lỗi xảy ra. Vui lòng thử lại.");
    });
};

// Xử lý gửi form Đăng Ký
document.getElementById("signupForm").onsubmit = function(event) {
    event.preventDefault(); 
    let tenDangNhap = document.getElementById("ten_dang_nhap").value;
    let hoTen = document.getElementById("ho_ten").value;
    let email = document.getElementById("emailSignup").value;
    let matKhau = document.getElementById("mat_khauSignup").value;
    let soDienThoai = document.getElementById("so_dien_thoai").value;
    let diaChi = document.getElementById("dia_chi").value;

    
    let formData = {
        'ten_dang_nhap': tenDangNhap,
        'ho_ten': hoTen,
        'email': email,
        'mat_khau': matKhau,
        'so_dien_thoai': soDienThoai,
        'dia_chi': diaChi
    };

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Gửi dưới dạng JSON
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        if (data.message) {
            signupModal.style.display = "none"; // Đóng Modal Đăng Ký khi đăng ký thành công
            window.location.href = '/account';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Có lỗi xảy ra. Vui lòng thử lại.");
    });
};

