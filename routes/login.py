from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for
from models import db, User

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.json.get("email")
        mat_khau = request.json.get("password")

        # Kiểm tra thông tin đầu vào
        if not email or not mat_khau:
            return jsonify({"message": "Thiếu thông tin bắt buộc"}), 400

        # Tìm người dùng trong cơ sở dữ liệu
        user = User.query.filter_by(email=email).first()

        # Kiểm tra mật khẩu
        if not user or user.mat_khau != mat_khau:
            return jsonify({"message": "Sai email hoặc mật khẩu"}), 401

        # Đăng nhập thành công - lưu thông tin người dùng vào session
        session['user_id'] = user.ma_nguoi_dung  # Lưu ID người dùng vào session

        return jsonify({"message": "Đăng nhập thành công"}), 200

   
