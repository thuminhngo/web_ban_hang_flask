from flask import Blueprint, jsonify, render_template, request, session
from flask_login import current_user
from models import db, Product, Cart

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/products')
def show_products():
    danh_sach_sp = Product.query.all()
    return jsonify({"html": render_template("products.html", danh_sach=danh_sach_sp)})

@products_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng."}), 401

    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id or not quantity:
        return jsonify({"success": False, "message": "Thiếu thông tin sản phẩm hoặc số lượng."}), 400

    # Kiểm tra sản phẩm có tồn tại
    product = Product.query.filter_by(ma_san_pham=product_id).first()
    if not product:
        return jsonify({"success": False, "message": "Sản phẩm không tồn tại."}), 404

    # Lấy ID người dùng từ session
    user_id = session['user']['id']

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item = Cart.query.filter_by(ma_nguoi_dung=user_id, ma_san_pham=product_id).first()
    if cart_item:
        # Nếu sản phẩm đã có, tăng số lượng
        cart_item.so_luong += int(quantity)
    else:
        # Nếu chưa có, tạo mới
        cart_item = Cart(ma_nguoi_dung=user_id, ma_san_pham=product_id, so_luong=int(quantity))
        db.session.add(cart_item)

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Sản phẩm đã được thêm vào giỏ hàng."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "Lỗi khi cập nhật giỏ hàng: " + str(e)}), 500