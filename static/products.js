document.getElementById('products').addEventListener('click', function(event) {
    event.preventDefault();

    fetch('/products')
        .then(response => response.text())
        .then(data => {
            document.getElementById('products_content').innerHTML = data;
        })
        .catch(error => console.error('Lỗi tải sản phẩm:', error));
});
