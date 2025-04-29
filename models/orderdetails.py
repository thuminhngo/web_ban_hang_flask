from . import db

class OrderDetail(db.Model):
    __tablename__ = "orderdetails"
    ma_chi_tiet = db.Column(db.Integer, primary_key=True)
    ma_don_hang = db.Column(db.Integer, db.ForeignKey("orders.ma_don_hang"), nullable=False)
    ma_san_pham = db.Column(db.Integer, db.ForeignKey("products.ma_san_pham"), nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    gia = db.Column(db.Numeric(10, 2), nullable=False)
