from turtle import pos
from rede_social_ks import app, database, bcrypt
from rede_social_ks.models import Usuario, Post
import secrets
from flask_login import current_user
from PIL import Image
import os

from rede_social_ks.forms import (
    FormEditarPerfil,
    FormCriarConta, 
    FormLogin,
    FormCriarPost
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
    request,
    abort
)





@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())

    return render_template('home.html', posts=posts)


@app.route('/contato')
def contato():

    return render_template('contato.html')


@app.route('/usuarios')
@login_required # Esse decorator deixa apenas usuarios logados ter acesso a essas URL
def usuarios():
    lista_usuarios = Usuario.query.all()

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


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)

    #Mudando Nome do Arquivo
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (200, 200)

    #Reduzindo o tamanho da imagem para poupar o banco de dados
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)

    #Salvando a imagem reduzida
    imagem_reduzida.save(caminho_completo)

    return nome_arquivo


def atualizar_linguagem_programacao(form):
    #Salvando check-box de linguagem de programação
    lista = []
    for campo in form:
        if 'dev_' in campo.name:
            if campo.data:
                lista.append(campo.label.text)
    return ';'.join(lista)



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


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(
            titulo=form.titulo.data,
            corpo=form.corpo.data,
            autor=current_user
        )
        database.session.add(post)
        database.session.commit()
        flash('Post criado com SUCESSO!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('post.html', form=form)


@app.route('/perfil/editar',  methods=['POST', 'GET'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.linguagem_programacao = atualizar_linguagem_programacao(form)
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


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso!', 'alert-success')

            return redirect(url_for('home'))
    else:
        form = None


    return render_template('pagina_post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
