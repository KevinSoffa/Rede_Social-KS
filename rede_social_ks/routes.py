import email
from rede_social_ks.forms import FormCriarConta, FormLogin
from rede_social_ks.models import Usuario, Post
from rede_social_ks import app, database, bcrypt
from flask_login import login_user


from flask import (
    render_template, 
    redirect, 
    url_for,
    flash,
    request
)


lista_usuarios = ['Kevin', 'Fernanda']



@app.route('/')
def home():

    return render_template('home.html')


@app.route('/contato')
def contato():

    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():

    return render_template(
        'usuarios.html', 
        lista_usuarios=lista_usuarios
    )


# Criação de Conta e Login
@app.route('/login_criacao', methods=['GET', 'POST'])
def login_criacao():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    #Login do Usuário
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com SUCESSO no E-mail: {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
             flash(f'Falha no Login. E-mail ou Senha Incorretos: {form_login.email.data}', 'alert-danger')

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:

        # criptografando senha
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)

        # criando conta
        usuario = Usuario(
            username=form_criar_conta.username.data, 
            email=form_criar_conta.email.data, 
            senha=senha_cript
        )
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com SUCESSO! {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template(
        'login_criar.html',
        form_login=form_login,
        form_criar_conta=form_criar_conta
    )
