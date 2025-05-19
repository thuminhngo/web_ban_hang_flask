from flask import Blueprint, jsonify, render_template, session, request
from models import db, User, Order, OrderDetail, Product

account_bp = Blueprint('account', __name__)

@account_bp.route("/account", methods=["GET"])
def account():
    if not session.get('user'):
        return jsonify({"html": "<p>Bạn chưa đăng nhập.</p>"})
    
    user_id = session['user'].get('id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"html": "<p>Không tìm thấy thông tin người dùng.</p>"})
    
    # Lấy danh sách đơn hàng của người dùng
    orders = Order.query.filter_by(ma_nguoi_dung=user_id).order_by(Order.ngay_dat_hang.desc()).all()
    
    # Truyền user và orders vào template
    return jsonify({"html": render_template("account.html", user=user, orders=orders)})

@account_bp.route("/update_account", methods=["POST"])
def update_account():
    if not session.get('user'):
        print("Lỗi: Người dùng chưa đăng nhập")
        return jsonify({"success": False, "message": "Bạn chưa đăng nhập."}), 401
    
    user_id = session['user'].get('id')
    user = User.query.get(user_id)
    
    if not user:
        print("Lỗi: Không tìm thấy người dùng với ID:", user_id)
        return jsonify({"success": False, "message": "Không tìm thấy thông tin người dùng."}), 404
    
    try:
        data = request.get_json()
        print("Dữ liệu nhận được:", data)
        
        if not data:
            print("Lỗi: Không nhận được dữ liệu JSON")
            return jsonify({"success": False, "message": "Dữ liệu không hợp lệ."}), 400
        
        user.ho_ten = data.get('ho_ten', user.ho_ten)
        user.email = data.get('email', user.email)
        user.so_dien_thoai = data.get('so_dien_thoai', user.so_dien_thoai)
        
        db.session.commit()
        print("Cập nhật thành công cho người dùng:", user_id)
        return jsonify({"success": True, "message": "Cập nhật thông tin thành công!"})
    except Exception as e:
        db.session.rollback()
        print("Lỗi khi cập nhật:", str(e))
        return jsonify({"success": False, "message": f"Lỗi khi cập nhật: {str(e)}"}), 500