from datetime import datetime as dt
from main import database


class Usuario(database.Model):
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
#