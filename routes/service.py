from flask import Blueprint, render_template

service_bp = Blueprint('service_bp', __name__)

@service_bp.route('/service')
def show_products():
    return render_template('service.html')
