from . import db

class Service(db.Model):
    __tablename__ = "services"
    ma_dich_vu = db.Column(db.Integer, primary_key=True)
    ten_dich_vu = db.Column(db.String(100), nullable=False)
    mo_ta = db.Column(db.Text)
    gia = db.Column(db.Numeric(10, 2), nullable=False)
    thoi_gian = db.Column(db.Integer)