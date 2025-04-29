document.getElementById('service').addEventListener('click', function(event) {
    event.preventDefault();

    fetch('/service')  // Gọi route Flask trả về products.html
        .then(response => response.text())
        .then(data => {
            document.getElementById('products_content').innerHTML = data;
        })
        .catch(error => console.error('Lỗi tải sản phẩm:', error));
});
