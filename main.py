from flask import Flask, render_template


app = Flask(__name__)


lista_usuarios = ['Kevin', 'Fernanda', 'Leo']

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuario():

    return render_template(
        'usuarios.html', 
        lista_usuarios=lista_usuarios
    )



if __name__=='__main__':
    app.run(debug=True)



# Fim aula 06