from . import db

class Review(db.Model):
    __tablename__ = "reviews"
    ma_danh_gia = db.Column(db.Integer, primary_key=True)
    ma_nguoi_dung = db.Column(db.Integer, db.ForeignKey("users.ma_nguoi_dung"), nullable=False)
    ma_dich_vu = db.Column(db.Integer, db.ForeignKey("services.ma_dich_vu"), nullable=True)
    ma_san_pham = db.Column(db.Integer, db.ForeignKey("products.ma_san_pham"), nullable=True)
    so_sao = db.Column(db.Integer, nullable=False)
    binh_luan = db.Column(db.Text)
    ngay_danh_gia = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())