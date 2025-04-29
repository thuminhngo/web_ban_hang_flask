from flask import Flask,Blueprint, render_template, request 

views = Blueprint('user', __name__)

@views.route('/user')
def home():
    return render_template("taikhoan.html")