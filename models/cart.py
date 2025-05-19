from . import db

class Cart(db.Model):
    __tablename__ = "cart"
    ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey("users.ma_nguoi_dung"), primary_key=True, nullable=False)
    ma_san_pham = db.Column(db.Integer, db.ForeignKey("products.ma_san_pham"), primary_key=True, nullable=False)
    so_luong = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", backref="carts")