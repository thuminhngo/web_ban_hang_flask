from flask import Flask, jsonify, render_template, request
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from routes.signup import signup_bp
from routes.login import login_bp
from routes.products import products_bp  
from routes.service import service_bp

from routes.admin import admin_bp
from models import db, User  

app = Flask(__name__, static_folder='static')

app.secret_key = '123'

app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(products_bp)
app.register_blueprint(service_bp)

app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return render_template("home.html")

#Cấu hình database
password = urllib.parse.quote_plus("Thu2004@@")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{password}@localhost/qlcuahang'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("config")

# Khởi tạo SQLAlchemys
db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
