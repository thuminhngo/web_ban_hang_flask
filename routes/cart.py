from flask import Blueprint, jsonify, render_template, request, session
from flask_login import current_user
from models import db, Product,Cart

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/get_cart')
def get_cart():
    ma_nguoi_dung = current_user.ma_nguoi_dung
    danh_sach_gio_hang = Cart.query.filter_by(ma_nguoi_dung=ma_nguoi_dung).all()

    result = []
    for item in danh_sach_gio_hang:
        san_pham = Product.query.get(item.ma_san_pham)
        result.append({
            'ma_san_pham': san_pham.ma_san_pham,
            'ten_san_pham': san_pham.ten_san_pham,
            'gia': float(san_pham.gia),
            'hinh_anh': san_pham.hinh_anh,
            'so_luong': item.so_luong
        })

    return jsonify(result)
