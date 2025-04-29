from . import db
class Product(db.Model):
    __tablename__ = "products"
    ma_san_pham = db.Column(db.Integer, primary_key=True)
    ten_san_pham = db.Column(db.String(100), nullable=False)
    mo_ta = db.Column(db.Text)
    gia = db.Column(db.Numeric(10, 2), nullable=False)
    so_luong_ton = db.Column(db.Integer, nullable=False)
    hinh_anh = db.Column(db.String(255)) 
