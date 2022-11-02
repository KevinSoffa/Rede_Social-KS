from rede_social_ks import database, login_manager
from datetime import datetime as dt
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(
        database.Integer, 
        primary_key=True
    )
    username = database.Column(
        database.String,
        nullable=False,
    )
    email = database.Column(
        database.String,
        nullable=False,
        unique=True,
    )
    senha = database.Column(
        database.String,
        nullable=False
    )
    foto_perfil = database.Column(
        database.String,
        default='default.jpg',
    )
    posts = database.relationship(
       'Post',
       backref='autor',
       lazy=True
    )
    linguagem_programacao = database.Column(
        database.String,
        default='Não informado',
    )

    def contar_post(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(
        database.Integer, 
        primary_key=True
    )
    titulo = database.Column(
        database.String,
        nullable=False,
    )
    corpo = database.Column(
        database.Text,
        nullable=False,
    )
    data_criacao = database.Column(
        database.DateTime,
        nullable=False,
        default=dt.utcnow
    )
    id_usuario = database.Column(
        database.Integer,
        database.ForeignKey('usuario.id'),
        nullable=False,
    )
