from . import db

class Order(db.Model):
    __tablename__ = "orders"
    ma_don_hang = db.Column(db.Integer, primary_key=True)
    ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey("users.ma_nguoi_dung"), nullable=False)
    ngay_dat_hang = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    tong_tien = db.Column(db.Numeric(10, 2), nullable=False)
    trang_thai = db.Column(db.Enum('Chờ xử lý','Đang giao','Đã giao','Đã hủy'), nullable=False)
    dia_chi_nhan_hang = db.Column(db.String(255), nullable=False)
    so_dien_thoai = db.Column(db.String(20), nullable=False)

    order_details = db.relationship("OrderDetail", backref="order", lazy=True)