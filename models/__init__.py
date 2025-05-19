from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Import models here to register them with SQLAlchemy
from .users import User
from .products import Product
from .cart import Cart
from .reviews import Review
from .orders import Order
from .orderdetails import OrderDetail

