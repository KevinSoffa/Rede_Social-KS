from rede_social_ks import app, database, bcrypt
from rede_social_ks.models import Usuario, Post
from flask_login import current_user

from rede_social_ks.forms import (
    FormEditarPerfil,
    FormCriarConta, 
    FormLogin,
)

from flask_login import (
    login_user, 
    logout_user,
    current_user,
    login_required
)

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
@login_required # Esse decorator deixa apenas usuarios logados ter acesso a essas URL
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
            
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            
            else:
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


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout Feito com SUCESSO!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for(
        'static', 
        filename=f'fotos_perfil/{current_user.foto_perfil}') 
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('post.html')


@app.route('/perfil/editar',  methods=['POST', 'GET'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        database.session.commit()
        flash('Alterações salvas com SUCESSO!', 'alert-success')
        return redirect(url_for('perfil'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    _foto_perfil = url_for(
        'static', 
        filename=f'fotos_perfil/{current_user.foto_perfil}') 

    return render_template(
        'editar_perfil.html', 
        foto_perfil=_foto_perfil,
        form=form
    )

