from flask import Blueprint, jsonify, redirect, request, render_template, session, url_for
from models import db, User

account_bp = Blueprint('account', __name__)

@account_bp.route("/account", methods=["GET"])
def account():
    # Kiểm tra xem người dùng có đăng nhập không
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
    
    # Lấy thông tin người dùng từ cơ sở dữ liệu
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "Người dùng không tồn tại"}), 404
    
    
    # Trả về trang HTML với thông tin người dùng
    return render_template('account.html', user=user)


@account_bp.route("/update_account", methods=["POST"])
def update_account():
    # Kiểm tra người dùng đã đăng nhập chưa
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # Nếu chưa đăng nhập thì chuyển tới trang đăng nhập
    
    # Lấy thông tin người dùng từ session
    user = User.query.get(session['user_id'])  # Lấy người dùng theo ID từ session
    if not user:
        return "Người dùng không tồn tại", 404

    # Cập nhật các thông tin người dùng từ form
    user.ho_ten = request.form.get("ho_ten")
    user.email = request.form.get("email")
    user.so_dien_thoai = request.form.get("so_dien_thoai")
    user.dia_chi = request.form.get("dia_chi")
    
    # Lưu thay đổi vào cơ sở dữ liệu
    db.session.commit()

    # Chuyển hướng về trang tài khoản và hiển thị thông báo thành công
    return redirect(url_for('account.account', message="Cập nhật thành công!"))
