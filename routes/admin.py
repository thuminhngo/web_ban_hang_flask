from flask import Blueprint, jsonify, redirect, request, render_template, session, url_for
from models import db, Product

admin_bp = Blueprint('admin_bp', __name__)
@admin_bp.route('/admin', methods=["GET", "POST"])
def admin():
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

        # Chuyển hướng để tránh submit lại khi reload
        return redirect("/admin")

    # Truy vấn tất cả sản phẩm
    danh_sach = Product.query.all()
    return render_template("admin.html", danh_sach=danh_sach)

@admin_bp.route("/sua_san_pham/<int:ma_sp>")
def sua_san_pham(ma_sp):
    san_pham = Product.query.get_or_404(ma_sp)
    danh_sach = Product.query.all()
    return render_template("admin.html", danh_sach=danh_sach, san_pham=san_pham)

@admin_bp.route("/cap_nhat_san_pham/<int:ma_sp>", methods=["POST"])
def cap_nhat_san_pham(ma_sp):
    sp = Product.query.get_or_404(ma_sp)
    sp.ten_san_pham = request.form["ten"]
    sp.mo_ta = request.form.get("mo_ta")
    sp.gia = request.form["gia"]
    sp.so_luong_ton = request.form["so_luong"]
    sp.hinh_anh = request.form["hinh_anh"]

    db.session.commit()
    return redirect("/admin")


