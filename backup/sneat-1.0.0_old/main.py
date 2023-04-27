from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "nome" and "senha" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nome' in request.form and 'senha' in request.form:
        # Create variables for easy access
        nome = request.form['nome']
        senha = request.form['senha']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM funcionarios WHERE nome = %s AND senha = %s', (nome, senha,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in funcionarios table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['logado'] = True
            session['codigo'] = account['codigo']
            session['nome'] = account['nome']
            # Redirect to home page
            return redirect(url_for('index'))
        else:
            # Account doesnt exist or nome/senha incorrect
            msg = 'Incorrect nome/senha!'
    # Show the login form with message (if any)
    return render_template('auth-login-basic.html', msg=msg)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    return render_template("auth-forgot-password-basic.html")

@app.route('/account-settings', methods=['GET', 'POST'])
def account_settings():
    return render_template("pages-account-settings-account.html")

@app.route('/logout')
def logout():
    session.pop('logado', None)
    session.pop('codigo', None)
    session.pop('nome', None)
    return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    # Output message if something goes wrong...
    msg = ''
    # Check if "nome", "senha" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'nome' in request.form and 'salario' in request.form and 'dt_nascimento' in request.form and 'telefone' in request.form and 'senha' in request.form:
        # Create variables for easy access
        nome = request.form['nome']
        salario = request.form['salario']
        dt_nascimento = request.form['dt_nascimento']
        telefone = request.form['telefone']
        senha = request.form['senha']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM funcionarios WHERE nome = %s', (nome,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into funcionarios table
            cursor.execute('INSERT INTO funcionarios VALUES (0, %s, %s, %s, %s, %s, 1)', (nome, salario, dt_nascimento, telefone, senha,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    
    # Show registration form with message (if any)
    return render_template('auth-register-basic.html', msg=msg)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)