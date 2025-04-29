import os

SECRET_KEY = os.environ.get("SECRET_KEY", "123")
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Thu2004@@@localhost/qlcuahang"
SQLALCHEMY_TRACK_MODIFICATIONS = False