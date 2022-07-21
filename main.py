from forms import FormCriarConta, FormLogin
from flask_sqlalchemy import SQLAlchemy

from flask import (
    Flask, 
    render_template,
    request,
    flash,
    redirect,
    url_for,
)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa563b763628c512d458658cb390c583'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rede_social.db'

database = SQLAlchemy(app)


lista_usuarios = ['Kevin', 'Fernanda', 'Leo']

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

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com SUCESSO no E-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        flash(f'Conta criada com SUCESSO! {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template(
        'login_criar.html',
        form_login=form_login,
        form_criar_conta=form_criar_conta
    )



if __name__=='__main__':
    app.run(debug=True)

# ir para aula 11