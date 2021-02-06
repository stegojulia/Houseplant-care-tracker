from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://julia:julia123@localhost/houseplants"

db = SQLAlchemy(app)

from application import routes
