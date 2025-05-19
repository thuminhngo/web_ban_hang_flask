from flask import Blueprint, jsonify, redirect, request, render_template, session, url_for
from models import db, Product, Order

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/admin', methods=["GET", "POST"])
def admin():
    # Lấy tham số tab từ query string, mặc định là 'products'
    active_tab = request.args.get('tab', 'products')

    if request.method == "POST":
        # Lấy dữ liệu từ form
        ten = request.form["ten"]
        mo_ta = request.form.get("mo_ta")
        gia = request.form["gia"]
        so_luong = request.form["so_luong"]
        hinh_anh = request.form["hinh_anh"]

        # Tạo sản phẩm mới
        sp_moi = Product(
            ten_san_pham=ten,
            mo_ta=mo_ta,
            gia=gia,
            so_luong_ton=so_luong,
            hinh_anh=hinh_anh
        )

        # Lưu vào database
        db.session.add(sp_moi)
        db.session.commit()

        # Chuyển hướng về tab sản phẩm
        return redirect(url_for('admin_bp.admin', tab='products'))

    # Truy vấn dữ liệu
    danh_sach = Product.query.all()
    danh_sach_don_hang = Order.query.order_by(Order.ngay_dat_hang.desc()).all()
    return render_template("admin.html", danh_sach=danh_sach, danh_sach_don_hang=danh_sach_don_hang, active_tab=active_tab)

@admin_bp.route("/sua_san_pham/<int:ma_sp>")
def sua_san_pham(ma_sp):
    san_pham = Product.query.get_or_404(ma_sp)
    active_tab = 'products'  # Khi sửa sản phẩm, luôn hiển thị tab sản phẩm
    danh_sach = Product.query.all()
    danh_sach_don_hang = Order.query.order_by(Order.ngay_dat_hang.desc()).all()
    return render_template("admin.html", danh_sach=danh_sach, danh_sach_don_hang=danh_sach_don_hang, san_pham=san_pham, active_tab=active_tab)

@admin_bp.route("/cap_nhat_san_pham/<int:ma_sp>", methods=["POST"])
def cap_nhat_san_pham(ma_sp):
    sp = Product.query.get_or_404(ma_sp)
    sp.ten_san_pham = request.form["ten"]
    sp.mo_ta = request.form.get("mo_ta")
    sp.gia = request.form["gia"]
    sp.so_luong_ton = request.form["so_luong"]
    sp.hinh_anh = request.form["hinh_anh"]

    db.session.commit()
    return redirect(url_for('admin_bp.admin', tab='products'))

@admin_bp.route("/xac_nhan_don_hang/<int:ma_don_hang>", methods=["POST"])
def xac_nhan_don_hang(ma_don_hang):
    order = Order.query.get_or_404(ma_don_hang)
    if order.trang_thai == 'Chờ xử lý':
        order.trang_thai = 'Đang giao'
        db.session.commit()
    return redirect(url_for('admin_bp.admin', tab='orders'))