from forms import FormCriarConta, FormLogin

from flask import (
    Flask, 
    render_template,
    url_for
)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa563b763628c512d458658cb390c583'


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


@app.route('/login_criacao')
def login_criacao():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    return render_template(
        'login_criar.html',
        form_login=form_login,
        form_criar_conta=form_criar_conta
    )



if __name__=='__main__':
    app.run(debug=True)

# ir para aula 11