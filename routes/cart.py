from flask import Blueprint, jsonify, render_template, session, request
from models import db, Cart, Product, Order, OrderDetail, User
from decimal import Decimal
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/cart')
def show_cart():
    logger.debug("Session user: %s", session.get('user'))
    if not session.get('user') or 'id' not in session['user']:
        logger.warning("Người dùng chưa đăng nhập hoặc session không hợp lệ")
        return jsonify({"html": "<p>Vui lòng đăng nhập để xem giỏ hàng.</p>"}), 401

    ma_nguoi_dung = session['user']['id']
    cart_items = Cart.query.filter_by(ma_nguoi_dung=ma_nguoi_dung).all()
    if not cart_items:
        logger.info("Giỏ hàng trống cho người dùng ID: %s", ma_nguoi_dung)
        return jsonify({"html": render_template("cart.html", cart_items=[], total=0)})

    total = sum(Decimal(str(item.product.gia)) * item.so_luong for item in cart_items)
    logger.debug("Tổng tiền giỏ hàng: %s", total)
    return jsonify({"html": render_template("cart.html", cart_items=cart_items, total=float(total))})

@cart_bp.route('/cart/update_quantity', methods=['POST'])
def update_quantity():
    # Kiểm tra đăng nhập
    if not session.get('user') or 'id' not in session['user']:
        logger.warning("Người dùng chưa đăng nhập hoặc session không hợp lệ")
        return jsonify({"success": False, "message": "Vui lòng đăng nhập!"}), 401

    # Kiểm tra Content-Type
    if request.content_type != 'application/json':
        logger.error("Content-Type không được hỗ trợ: %s", request.content_type)
        return jsonify({"success": False, "message": "Yêu cầu phải là JSON!"}), 415

    # Lấy dữ liệu
    data = request.get_json()
    ma_san_pham = data.get('ma_san_pham')
    action = data.get('action')
    if not ma_san_pham or not action or action not in ['increase', 'decrease']:
        logger.warning("Dữ liệu không hợp lệ: ma_san_pham=%s, action=%s", ma_san_pham, action)
        return jsonify({"success": False, "message": "Dữ liệu không hợp lệ!"}), 400

    ma_nguoi_dung = session['user']['id']
    try:
        # Tìm sản phẩm trong giỏ hàng
        cart_item = Cart.query.filter_by(ma_nguoi_dung=ma_nguoi_dung, ma_san_pham=ma_san_pham).first()
        if not cart_item:
            logger.warning("Sản phẩm không có trong giỏ hàng: %s", ma_san_pham)
            return jsonify({"success": False, "message": "Sản phẩm không có trong giỏ hàng!"}), 404

        # Kiểm tra sản phẩm
        product = Product.query.get(ma_san_pham)
        if not product:
            logger.error("Sản phẩm không tồn tại: %s", ma_san_pham)
            return jsonify({"success": False, "message": "Sản phẩm không tồn tại!"}), 400

        if hasattr(product, 'trang_thai') and product.trang_thai != 'active':
            logger.warning("Sản phẩm %s không còn hoạt động", product.ten_san_pham)
            return jsonify({"success": False, "message": f"Sản phẩm {product.ten_san_pham} không còn hoạt động!"}), 400

        # Xử lý tăng/giảm số lượng
        new_quantity = cart_item.so_luong
        if action == 'increase':
            if product.so_luong_ton < cart_item.so_luong + 1:
                logger.warning("Sản phẩm %s không đủ tồn kho: yêu cầu %s, còn %s",
                             product.ten_san_pham, cart_item.so_luong + 1, product.so_luong_ton)
                return jsonify({"success": False, "message": f"Sản phẩm {product.ten_san_pham} không đủ tồn kho!"}), 400
            new_quantity += 1
        elif action == 'decrease':
            new_quantity -= 1
            if new_quantity < 1:
                # Nếu số lượng nhỏ hơn 1, xóa sản phẩm
                db.session.delete(cart_item)
                db.session.commit()
                logger.info("Đã xóa sản phẩm %s khỏi giỏ hàng do số lượng về 0", ma_san_pham)
                return jsonify({"success": True, "message": "Sản phẩm đã được xóa khỏi giỏ hàng!"})

        # Cập nhật số lượng
        cart_item.so_luong = new_quantity
        db.session.commit()
        logger.info("Đã cập nhật số lượng sản phẩm %s: %s", ma_san_pham, new_quantity)
        return jsonify({"success": True, "message": "Cập nhật số lượng thành công!"})

    except Exception as e:
        db.session.rollback()
        logger.error("Lỗi khi cập nhật số lượng: %s", str(e))
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"}), 500

@cart_bp.route("/checkout", methods=["POST"])
def checkout():
    logger.debug("Nhận yêu cầu POST /checkout, Content-Type: %s", request.content_type)
    if not session.get('user') or 'id' not in session['user']:
        logger.warning("Người dùng chưa đăng nhập hoặc session không hợp lệ")
        return jsonify({"success": False, "message": "Vui lòng đăng nhập để thanh toán!"}), 401

    # Xử lý cả JSON và form-data
    if request.content_type == 'application/json':
        data = request.get_json()
        if not data:
            logger.error("Không nhận được dữ liệu JSON")
            return jsonify({"success": False, "message": "Dữ liệu JSON không hợp lệ!"}), 400
        address = data.get("address", "").strip()
        phone = data.get("phone", "").strip()
    elif request.content_type == 'application/x-www-form-urlencoded':
        logger.debug("Xử lý dữ liệu form-urlencoded")
        address = request.form.get("address", "").strip()
        phone = request.form.get("phone", "").strip()
    else:
        logger.error("Content-Type không được hỗ trợ: %s", request.content_type)
        return jsonify({"success": False, "message": "Content-Type không được hỗ trợ!"}), 415

    logger.debug("Dữ liệu nhận được: address=%s, phone=%s", address, phone)

    if not address or not phone:
        logger.warning("Thiếu địa chỉ hoặc số điện thoại")
        return jsonify({"success": False, "message": "Vui lòng nhập đầy đủ địa chỉ và số điện thoại!"}), 400

    if not phone.isdigit() or len(phone) not in [10, 11]:
        logger.warning("Số điện thoại không hợp lệ: %s", phone)
        return jsonify({"success": False, "message": "Số điện thoại phải có 10 hoặc 11 số!"}), 400

    user_id = session['user']['id']
    user = User.query.get(user_id)
    if not user:
        logger.error("Không tìm thấy người dùng với ID: %s", user_id)
        return jsonify({"success": False, "message": "Người dùng không tồn tại!"}), 400

    cart_items = Cart.query.filter_by(ma_nguoi_dung=user_id).all()
    if not cart_items:
        logger.warning("Giỏ hàng trống cho người dùng ID: %s", user_id)
        return jsonify({"success": False, "message": "Giỏ hàng của bạn đang trống!"}), 400

    try:
        logger.debug("Kiểm tra sản phẩm và tồn kho")
        for item in cart_items:
            product = Product.query.get(item.ma_san_pham)
            if not product:
                logger.error("Sản phẩm không tồn tại: %s", item.ma_san_pham)
                return jsonify({
                    "success": False,
                    "message": f"Sản phẩm ID {item.ma_san_pham} không tồn tại!"
                }), 400
            if hasattr(product, 'trang_thai') and product.trang_thai != 'active':
                logger.warning("Sản phẩm %s không còn hoạt động", product.ten_san_pham)
                return jsonify({
                    "success": False,
                    "message": f"Sản phẩm {product.ten_san_pham} không còn hoạt động!"
                }), 400
            if product.so_luong_ton < item.so_luong:
                logger.warning("Sản phẩm %s không đủ tồn kho: yêu cầu %s, còn %s",
                             product.ten_san_pham, item.so_luong, product.so_luong_ton)
                return jsonify({
                    "success": False,
                    "message": f"Sản phẩm {product.ten_san_pham} không đủ tồn kho!"
                }), 400
            if not isinstance(product.gia, (int, float, Decimal)) or product.gia < 0:
                logger.error("Giá sản phẩm không hợp lệ: %s", product.gia)
                return jsonify({
                    "success": False,
                    "message": f"Giá sản phẩm {product.ten_san_pham} không hợp lệ!"
                }), 400

        total = sum(Decimal(str(item.product.gia)) * item.so_luong for item in cart_items)
        logger.debug("Tổng tiền đơn hàng: %s", total)

        logger.debug("Tạo đơn hàng mới")
        new_order = Order(
            ma_nguoi_dung=user_id,
            tong_tien=total,
            dia_chi_nhan_hang=address,
            so_dien_thoai=phone,
            trang_thai="Chờ xử lý"
        )
        db.session.add(new_order)
        db.session.flush()
        logger.debug("Đã tạo đơn hàng với ID: %s", new_order.ma_don_hang)

        logger.debug("Tạo chi tiết đơn hàng và cập nhật tồn kho")
        for item in cart_items:
            product = Product.query.get(item.ma_san_pham)
            order_detail = OrderDetail(
                ma_don_hang=new_order.ma_don_hang,
                ma_san_pham=item.ma_san_pham,
                so_luong=item.so_luong,
                gia=Decimal(str(item.product.gia))
            )
            db.session.add(order_detail)
            product.so_luong_ton -= item.so_luong
            logger.debug("Cập nhật tồn kho sản phẩm %s: còn %s", product.ten_san_pham, product.so_luong_ton)

        logger.debug("Xóa giỏ hàng của người dùng ID: %s", user_id)
        deleted_rows = Cart.query.filter_by(ma_nguoi_dung=user_id).delete()
        logger.debug("Đã xóa %s bản ghi trong giỏ hàng", deleted_rows)

        # Kiểm tra xem giỏ hàng đã được xóa hoàn toàn chưa
        remaining_items = Cart.query.filter_by(ma_nguoi_dung=user_id).count()
        if remaining_items > 0:
            logger.error("Giỏ hàng vẫn còn %s bản ghi sau khi xóa", remaining_items)
            raise Exception("Không thể xóa hoàn toàn giỏ hàng")

        logger.debug("Commit thay đổi vào cơ sở dữ liệu")
        db.session.commit()
        logger.info("Đơn hàng được tạo thành công: ID %s, giỏ hàng đã được xóa", new_order.ma_don_hang)

        return jsonify({
            "success": True,
            "message": "Đơn hàng đã được tạo thành công và giỏ hàng đã được xóa!",
            "order_id": new_order.ma_don_hang
        })

    except Exception as e:
        db.session.rollback()
        logger.error("Lỗi khi xử lý checkout: %s, chi tiết: %s", str(e), e.__traceback__)
        return jsonify({"success": False, "message": f"Lỗi khi tạo đơn hàng: {str(e)}"}), 500

@cart_bp.route('/cart/delete', methods=['POST'])
def delete_cart_item():
    # Kiểm tra đăng nhập
    if not session.get('user') or 'id' not in session['user']:
        return jsonify({"success": False, "message": "Vui lòng đăng nhập!"}), 401

    # Kiểm tra Content-Type
    if request.content_type != 'application/json':
        return jsonify({"success": False, "message": "Yêu cầu phải là JSON!"}), 415

    # Lấy dữ liệu
    data = request.get_json()
    ma_san_pham = data.get('ma_san_pham')
    if not ma_san_pham:
        return jsonify({"success": False, "message": "Thiếu mã sản phẩm!"}), 400

    # Lấy ID người dùng
    ma_nguoi_dung = session['user']['id']

    try:
        # Tìm và xóa sản phẩm trong giỏ hàng
        cart_item = Cart.query.filter_by(ma_nguoi_dung=ma_nguoi_dung, ma_san_pham=ma_san_pham).first()
        if not cart_item:
            return jsonify({"success": False, "message": "Sản phẩm không có trong giỏ hàng!"}), 404

        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"success": True, "message": "Đã xóa sản phẩm khỏi giỏ hàng!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Lỗi: {str(e)}"}), 500