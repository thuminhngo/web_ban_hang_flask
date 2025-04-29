from flask import Blueprint, jsonify, render_template, request, session
from flask_login import current_user
from models import db, Product,Cart

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/products')
def show_products():
    danh_sach_sp = Product.query.all()
    return render_template("products.html", danh_sach=danh_sach_sp)

@products_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    ma_san_pham = request.json.get('ma_san_pham')
    ma_nguoi_dung = current_user.ma_nguoi_dung

    # Kiểm tra sản phẩm có tồn tại không
    san_pham = Product.query.get(ma_san_pham)
    if not san_pham:
        return jsonify({'message': 'Sản phẩm không tồn tại.'}), 404

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    gio_hang_item = Cart.query.filter_by(ma_nguoi_dung=ma_nguoi_dung, ma_san_pham=ma_san_pham).first()

    if gio_hang_item:
        gio_hang_item.so_luong += 1
    else:
        gio_hang_item = Cart(ma_nguoi_dung=ma_nguoi_dung, ma_san_pham=ma_san_pham, so_luong=1)
        db.session.add(gio_hang_item)

    db.session.commit()
    return jsonify({'message': 'Đã thêm vào giỏ hàng'})

@products_bp.route('/get_cart')
def get_cart():
    cart = session.get('cart', [])
    return jsonify(cart)
