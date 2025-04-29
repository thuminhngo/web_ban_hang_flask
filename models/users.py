from . import db

class User(db.Model):
    
    __tablename__ = "users"
    ma_nguoi_dung = db.Column(db.Integer, primary_key=True)
    ten_dang_nhap = db.Column(db.String(50), nullable=False, unique=True)
    mat_khau = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    ho_ten = db.Column(db.String(100), nullable=False)
    so_dien_thoai = db.Column(db.String(15))
    dia_chi = db.Column(db.String(255))
    ngay_tao = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    orders = db.relationship("Order", backref="user", lazy=True)

