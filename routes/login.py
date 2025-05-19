from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from models import db, User

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        mat_khau = request.form.get("password")

        if not email or not mat_khau:
            flash("Vui lòng điền đầy đủ thông tin", "error")
            return redirect(url_for("home", modal="login"))

        user = User.query.filter_by(email=email).first()
        if not user or user.mat_khau != mat_khau:
            flash("Sai email hoặc mật khẩu", "error")
            return redirect(url_for("home", modal="login"))

        session['user'] = {
            "id": user.ma_nguoi_dung,
            "name": user.ho_ten,
            "email": user.email,
            "phone": user.so_dien_thoai,
        }
        flash("Đăng nhập thành công", "success")
        return redirect(url_for("home"))

    return redirect(url_for("home", modal="login"))

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Đăng xuất thành công", "success")
    return redirect(url_for("home"))