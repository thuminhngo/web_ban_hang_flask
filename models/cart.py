from . import db
class Cart(db.Model):
    __tablename__ = "cart"
    ma_gio_hang = db.Column(db.Integer, primary_key=True)
    ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey("users.ma_nguoi_dung"), nullable=False)
    ma_san_pham = db.Column(db.Integer, db.ForeignKey("products.ma_san_pham"), nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)