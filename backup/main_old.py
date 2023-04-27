from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db'
mysql = MySQL(app)

engine = create_engine('mysql://root:@localhost/db')
connection = engine.connect()
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    rua = Column(String, nullable=False)
    bairro = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    telefone = Column(String)
    email = Column(String)
    sexo = Column(String)


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    qt_estoque = Column(Integer, nullable=False)
    preco = Column(Integer, nullable=False)
    fabricante = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    tempo_de_uso = Column(String)
    compra_id = Column(Integer, ForeignKey('compra.id'))


class ProdutoCompra(Base):
    __tablename__ = "produtocompra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    fabricante = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    tempo_de_uso = Column(String)


class Compra(Base):
    __tablename__ = "compra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor = Column(Integer, nullable=False)
    comissao_id = Column(Integer, ForeignKey('comissao.id'))
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    produto = relationship('Produto', backref='Compra', lazy=True)


class Funcionario(Base):
    __tablename__ = "funcionario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    salario = Column(String, nullable=False)
    dt_nascimento = Column(String, nullable=False)
    telefone = Column(String)


class Ponto(Base):
    __tablename__ = "ponto"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hora = Column(String, nullable=False)
    data = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))

class Comissao(Base):
    __tablename__ = "comissao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Integer, nullable=False)
    funcionario_id = Column(Integer, ForeignKey('funcionario.id'))


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':

        nome = request.form['nome']
        senha = request.form['senha']
        salario = request.form['salario']
        dt_nascimento = request.form['dt_nascimento']
        telefone = request.form['telefone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM funcionario WHERE nome = %s', (nome,))
        account = cursor.fetchone()

        if account:
            return redirect(url_for('login'))
        else:
            data = Funcionario(nome = nome, senha = senha, salario = salario, dt_nascimento = dt_nascimento, telefone = telefone)
            session.add(data)
            session.commit()
            return redirect(url_for('login'))

    return render_template('cadastrar.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM funcionario WHERE nome = %s AND senha = %s', (nome, senha,))
        account = cursor.fetchone()

        if account:
            return redirect(url_for('index'))
        else:
            pass

    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    return render_template("recuperar-senha.html")


@app.route('/configuracoes-usuario', methods=['GET', 'POST'])
def account_settings():
    return render_template("configuracoes-usuario.html")



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))



@app.route('/cadastrar-cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        rua = request.form['rua']
        bairro = request.form['bairro']
        cep = request.form['cep']
        numero = request.form['numero']
        telefone = request.form['telefone']
        email = request.form['email']
        sexo = request.form['sexo']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cliente WHERE cpf = %s', (cpf,))
        account = cursor.fetchone()

        if account:
            pass
        else:
            data = Cliente(cpf = cpf, nome = nome, rua = rua, bairro = bairro, \
                           numero = numero, cep = cep, telefone = telefone, email = email, sexo = sexo)
            session.add(data)
            session.commit()

    return render_template('cadastro-cliente.html')



@app.route('/listar-cliente', methods=['GET', 'POST'])
def listar_cliente():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cliente')
    clientes = cursor.fetchall()
    return render_template('lista-cliente.html', clientes=clientes)



@app.route('/atualizar-cliente/<int:id>', methods=['GET', 'POST'])
def atualizar_cliente(id):
    cliente = session.query(Cliente).filter(Cliente.id == id).one()

    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        rua = request.form['rua']
        bairro = request.form['bairro']
        cep = request.form['cep']
        numero = request.form['numero']
        telefone = request.form['telefone']
        email = request.form['email']
        sexo = request.form['sexo']

        cliente.cpf = cpf
        cliente.nome = nome
        cliente.rua = rua
        cliente.bairro = bairro
        cliente.cep = cep
        cliente.numero = numero
        cliente.telefone = telefone
        cliente.email = email
        cliente.sexo = sexo

        session.commit()
        return redirect(url_for('listar_cliente'))

    return render_template('atualizar-cliente.html', cliente=cliente)


@app.route('/deletar_cliente/<id>', methods=['GET', 'POST'])
def deletar_cliente(id):
    session.query(Cliente).filter(Cliente.id == id).delete()
    session.commit()
    return redirect(url_for('listar_cliente'))


@app.route('/cadastrar-produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':

        nome = request.form['nome']
        qt_estoque = request.form['qt_estoque']
        preco = request.form['preço']
        fabricante = request.form['fabricante']
        estado = request.form['estado']
        tempo_de_uso = request.form['tempo_de_uso']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM produto WHERE nome = %s', (nome,))
        account = cursor.fetchone()

        if account:
            pass
        else:
            data = Produto(nome = nome, qt_estoque = qt_estoque, preco = preco, \
                           fabricante = fabricante, estado = estado, tempo_de_uso = tempo_de_uso, compra_id = 1)
            session.add(data)
            session.commit()

    return render_template('cadastro-produto.html')


@app.route('/listar-produto', methods=['GET', 'POST'])
def listar_produto():
    if request.method == 'POST':
        opc = request.form['opc']

        if opc == 'nome-asc':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM produto ORDER BY nome ASC')
            produtos = cursor.fetchall()
        elif opc == 'nome-des':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM produto ORDER BY nome DESC')
            produtos = cursor.fetchall()
        elif opc == 'fab-asc':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM produto ORDER BY fabricante ASC')
            produtos = cursor.fetchall()
        elif opc == 'fab-des':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM produto ORDER BY fabricante DESC')
            produtos = cursor.fetchall()
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM produto')
            produtos = cursor.fetchall()

    return render_template('lista-produto.html', produtos=produtos, opc=opc)


@app.route('/listar-produto-compra', methods=['GET', 'POST'])
def listar_produto_compra():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM produtocompra')
    produtos = cursor.fetchall()
    return render_template('lista-produto-compra.html', produtos=produtos)


@app.route('/atualizar-produto/<int:id>', methods=['GET', 'POST'])
def atualizar_produto(id):
    produto = session.query(Produto).filter(Produto.id == id).one()

    if request.method == 'POST':
        nome = request.form['nome']
        qt_estoque = request.form['qt_estoque']
        preco = request.form['preco']
        fabricante = request.form['fabricante']
        estado = request.form['estado']
        tempo_de_uso = request.form['tempo_de_uso']

        produto.nome = nome
        produto.qt_estoque = qt_estoque
        produto.preco = preco
        produto.fabricante = fabricante
        produto.estado = estado
        produto.tempo_de_uso = tempo_de_uso

        session.commit()
        return redirect(url_for('listar_produto'))

    return render_template('atualizar-produto.html', produto=produto)


@app.route('/deletar_produto/<id>', methods=['GET', 'POST'])
def deletar_produto(id):
    session.query(Produto).filter(Produto.id == id).delete()
    session.commit()
    return redirect(url_for('listar_produto'))


@app.route('/cadastrar-compra', methods=['GET', 'POST'])
def cadastrar_compra():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM produto')
    produtos_ = cursor.fetchall()
    msg = ''
    if request.method == 'POST':
        produto_ = request.form['produto_']
        quantidade = request.form['quantidade']

        account = session.query(Produto.qt_estoque).filter(Produto.id == produto_).one()

        produto = session.query(Produto).filter(Produto.id == produto_).one()

        if int(quantidade) > int(account[0]):
            msg = 'Quantidade maior que o estoque!'
        else:
            msg = 'Produto adicionado!'
            data = ProdutoCompra(nome = produto.nome, preco = produto.preco, fabricante = produto.fabricante, estado = produto.estado, tempo_de_uso = produto.tempo_de_uso)
            session.add(data)
            session.commit()

            session.query(Produto). \
                filter(Produto.id == produto_). \
                update({'qt_estoque': Produto.qt_estoque - quantidade})
            session.commit()

            verifica_quantidade()


    return render_template('cadastro-compra.html', produtos=produtos_, msg=msg)


def verifica_quantidade():
    session.query(Produto).filter(Produto.qt_estoque == 0).delete()
    session.commit()

@app.route('/compra-cliente', methods=['GET', 'POST'])
def compra_cliente():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cliente')
    clientes = cursor.fetchall()
    msg = ''
    if request.method == 'POST':
        cliente_ = request.form['cliente_']
        cliente = session.query(Cliente).filter(Cliente.id == cliente_).one()
        valor = session.query(ProdutoCompra, func.sum(ProdutoCompra.preco)).one()
        quantidade = session.query(ProdutoCompra).count()

        data_ = Compra(data=str(datetime.date.today()), quantidade=quantidade, valor=int(valor[1]), comissao_id=1,
                       cliente_id=cliente.id)
        session.add(data_)
        session.commit()

        session.query(ProdutoCompra).delete()
        session.commit()

        return redirect(url_for('index'))

    return render_template('compra-cliente.html', clientes=clientes)

@app.route('/deletar_produto-compra/<id>', methods=['GET', 'POST'])
def deletar_produto_compra(id):
    session.query(ProdutoCompra).filter(ProdutoCompra.id == id).delete()
    session.commit()
    return redirect(url_for('listar_produto_compra'))



@app.route('/listar-compra', methods=['GET', 'POST'])
def listar_compra():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM compra')
    compras = cursor.fetchall()
    return render_template('lista-compra.html', compras=compras)


@app.route('/atualizar-compra', methods=['GET', 'POST'])
def atualizar_compra():
    return render_template('atualizar-compra.html')



@app.route('/deletar_compra/<id>', methods=['GET', 'POST'])
def deletar_compra(id):
    session.query(Compra).filter(Compra.id == id).delete()
    session.commit()
    return redirect(url_for('listar_compra'))



@app.route('/listar-funcionario', methods=['GET', 'POST'])
def listar_funcionario():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM funcionario')
    funcionarios = cursor.fetchall()
    return render_template('lista-funcionario.html', funcionarios=funcionarios)


@app.route('/atualizar-funcionario', methods=['GET', 'POST'])
def atualizar_funcionario():


    return render_template('atualizar-funcionario.html')


@app.route('/deletar_funcionario/<id>', methods=['GET', 'POST'])
def deletar_funcionario(id):
    session.query(Funcionario).filter(Funcionario.id == id).delete()
    session.commit()
    return redirect(url_for('listar_funcionario'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

session.close()