from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa563b763628c512d458658cb390c583'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rede_social.db'

database = SQLAlchemy(app)

#Criptografia da senha de usuário
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from rede_social_ks import routes