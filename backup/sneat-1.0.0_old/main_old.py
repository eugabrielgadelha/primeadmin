from flask import Flask, g, render_template, request, redirect, url_for, flash, session
import mysql.connector

from models.funcionarios import Funcionario
from models.funcionariosDAO import FuncionariosDAO

app = Flask(__name__)
app.secret_key = "senha123"

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "mydb"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        nome = request.form['nome']
        senha = request.form['senha']

        # Verificar dados
        dao = FuncionariosDAO(get_db())
        funcionarios = dao.autenticar(nome, senha)

        if funcionarios is not None:
            session['logado'] = {
                'codigo': funcionarios[0],
                'nome': funcionarios[1],
                'senha': funcionarios[6],
            }
            return redirect(url_for('Login'))
        else:
            flash("Erro ao efetuar login!", "danger")

    return render_template("auth-login-basic.html", titulo="Login")


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == "POST":
        nome = request.form['nome']
        salario = request.form['salario']
        dt_nascimento = request.form['dt_nascimento']
        telefone = request.form['telefone']
        senha = request.form['senha']

        Funcionarios = Funcionario(nome, salario, dt_nascimento, telefone, senha)

        dao = FuncionariosDAO(get_db())
        codigo = dao.inserir(Funcionarios)

        if codigo > 0:
            flash("Cadastrado com sucesso! Código %d" % codigo, "sucess")
        else:
            flash("Erro ao cadastrar!", "danger")

    vartitulo = "Cadastrar"
    return render_template("auth-register-basic.html", titulo=vartitulo)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("index.html", titulo=dashboard)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
