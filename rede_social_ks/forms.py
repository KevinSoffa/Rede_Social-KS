from flask_wtf.file import FileField, FileAllowed
from rede_social_ks.models import Usuario
from flask_login import current_user
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
    BooleanField,
    TextAreaField
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


class FormEditarPerfil(FlaskForm):
    username = StringField(
        'Nome de Usuário',
        validators=[DataRequired()]
    )
    email = EmailField(
        'E-mail',
        validators=[DataRequired(), Email()]
    )
    foto_perfil = FileField(
        'Atualizar foto de perfil',
        validators=[FileAllowed(['jpg', 'png'])]
    )
    dev_python = BooleanField(
        'Python'
    )
    dev_java_script = BooleanField(
        'JavaScript'
    )
    dev_php = BooleanField(
        'PHP'
    )
    dev_java = BooleanField(
        'Java'
    )
    dev_back_end = BooleanField(
        'Back-End'
    )
    dev_front_end = BooleanField(
        'Front-End'
    )
    botao_submit_editar_perfil = SubmitField(
        'Salvar Alterações'
    )

    def validate_email(self, email): # Validando se e-mail já está cadastrado
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("""ERRO! E-mail já CADASTRADO! 
                                        Tente com outro e-mail válido.
                                    """)


class FormCriarPost(FlaskForm):
    titulo = StringField(
        'Título do Post', 
        validators=[DataRequired(), 
        Length(2, 140)]
    )
    corpo = TextAreaField(
        'Escreva seu Post aqui...', 
        validators=[DataRequired()]
    )
    botao_submit = SubmitField(
        'Publicar'
    )