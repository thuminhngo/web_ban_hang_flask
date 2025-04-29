const navbarLinks = document.querySelectorAll('#navbar a');

  navbarLinks.forEach(link => {
    link.addEventListener('click', function () {
      // Xóa class active ở tất cả link
      navbarLinks.forEach(item => item.classList.remove('active'));

      // Thêm class active cho link được nhấn
      this.classList.add('active');
    });
  });

