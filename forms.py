from flask_wtf import FlaskForm

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo
)

from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    EmailField,
    BooleanField
)


class FormCriarConta(FlaskForm):
    username = StringField(
        'Nome de Usuário',
        validators=[DataRequired()]
    )
    email = EmailField(
        'E-mail',
        validators=[DataRequired(), Email()]
    )
    senha = PasswordField(
        'Senha',
        validators=[DataRequired(), Length(6, 20)]
    )
    confirmar_senha = PasswordField(
        'Confirmação de senha',
        validators=[DataRequired(), EqualTo('senha')]
    )
    botao_submit_criarconta = SubmitField(
        'Criar Conta'
    )


class FormLogin(FlaskForm):
    email = EmailField(
        'E-mail',
        validators=[DataRequired(), Email()]
    )
    senha = PasswordField(
        'Senha',
        validators=[DataRequired(), Length(6, 20)]
    )
    lembrar_dados = BooleanField(
        'Permanecer conectado'
    )
    botao_submit_login = SubmitField(
        'Fazer Login'
    )