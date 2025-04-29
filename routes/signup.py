

from flask import Blueprint, request, jsonify
from models import db
from models.users import User
from werkzeug.security import generate_password_hash

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST'])
def add_user():
    try:
        data = request.json  # Nhận dữ liệu từ Ajax
        ten_dang_nhap = data.get('ten_dang_nhap')
        ho_ten = data.get('ho_ten')
        email = data.get('email')
        mat_khau = data.get('mat_khau')
        so_dien_thoai = data.get('so_dien_thoai')
        dia_chi = data.get('dia_chi')

        # Kiểm tra dữ liệu hợp lệ
        if not (ten_dang_nhap and ho_ten and email and mat_khau):
            return jsonify({"success": False, "message": "Vui lòng điền đầy đủ thông tin"})

        # Kiểm tra email đã tồn tại chưa
        def get_user_by_email(email):
            return User.query.filter_by(email=email).first()

        # Kiểm tra xem email đã được đăng ký chưa
        existing_user = get_user_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "Email đã tồn tại!"})

        # Mã hóa mật khẩu
        #hashed_password = generate_password_hash(mat_khau)

        # Lưu vào database
        def save_user(ten_dang_nhap, ho_ten, email, mat_khau, so_dien_thoai, dia_chi):
            try:
                new_user = User(
                    ten_dang_nhap=ten_dang_nhap,
                    ho_ten=ho_ten,
                    email=email,
                    mat_khau=mat_khau,
                    so_dien_thoai=so_dien_thoai,
                    dia_chi=dia_chi
                )
                db.session.add(new_user)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                print("Lỗi khi lưu user:", e)
                return False

        # Gọi hàm lưu người dùng
        if save_user(ten_dang_nhap, ho_ten, email, mat_khau, so_dien_thoai, dia_chi):
            return jsonify({"success": True, "message": "Đăng ký thành công!"})
        else:
            return jsonify({"success": False, "message": "Có lỗi xảy ra khi đăng ký."})

    except Exception as e:
        print("Lỗi:", e)
        return jsonify({"success": False, "message": "Có lỗi xảy ra trong quá trình xử lý."})

