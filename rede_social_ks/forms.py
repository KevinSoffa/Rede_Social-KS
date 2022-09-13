from rede_social_ks.models import Usuario
from flask_wtf import FlaskForm

from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError
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

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("""ERRO! E-mail já CADASTRADO! 
                                    Cadastra-se com outro e-mail 
                                    ou faça Login para começar.
                                """)


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
