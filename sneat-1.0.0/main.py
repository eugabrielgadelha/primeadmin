from flask import Flask, g, render_template,\
    request, redirect, url_for, session

from datetime import datetime
import mysql.connector

from models.funcionario import Funcionario
from models.funcionarioDAO import FuncionarioDAO
from models.cliente import Cliente
from models.clienteDAO import ClienteDAO
from models.compra import Compra
from models.compraDAO import CompraDAO
from models.produto import Produto
from models.produtoDAO import ProdutoDAO
from models.compraproduto import Compraproduto
from models.compraprodutoDAO import CompraprodutoDAO
from models.comissao import Comissao
from models.comissaoDAO import ComissaoDAO
from models.ponto import Ponto
from models.pontoDAO import PontoDAO
from models.pontos import Pontos
from models.pontosDAO import PontosDAO


app = Flask(__name__, template_folder="templates")
app.secret_key = "senha123"

DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "db"

app.auth = {
    # acao: { perfil:permissao }
    'index': {0:1, 1:1},
    'logout': {0:1, 1:1},
    'cadastrar_cliente': {0:1, 1:1},
    'listar_cliente': {0:1, 1:1},
    'atualizar_cliente': {0:1, 1:1},
    'deletar_cliente': {0:1, 1:1},
    'cadastrar_produto': {0:1, 1:1},
    'listar_produto': {0:1, 1:1},
    'atualizar_produto': {0:1, 1:1},
    'deletar_produto': {0:1, 1:1},
    'cadastrar_compra': {0:1, 1:1},
    'listar_compra': {0:1, 1:1},
    'atualizar_compra': {0:1, 1:1},
    'deletar_compra': {0:1, 1:1},
    'cadastrar_comissao': {0:1, 1:1},
    'listar_comissao': {0:1, 1:1},
    'atualizar_comissao': {0:1, 1:1},
    'deletar_comissao': {0:1, 1:1},
    'listar_funcionario': {0:1, 1:1},
    'atualizar_funcionario': {0:1, 1:1},
    'deletar_funcionario': {0:1, 1:1}
}

@app.before_request
def autorizacao():
    acao = request.path[1:]
    acao = acao.split('/')
    if len(acao)>=1:
        acao = acao[0]

    acoes = app.auth.keys()
    if acao in list(acoes):
        if session.get('logado') is None:
            return redirect(url_for('login'))
        else:
            tipo = session['logado']['tipo']
            if app.auth[acao][tipo]==0:
                return redirect(url_for('index'))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = mysql.connector.connect(
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


@app.route('/index')
def index():
    dao = PontoDAO(get_db())
    ponto = dao.quantidade(session['logado']['id'])[0]
    nome = session['logado']['nome']
    func_id = session['logado']['id']
    tipo = session['logado']['tipo']
    return render_template("index.html", ponto = ponto, nome=nome, tipo=tipo, func_id=func_id)


#--------FUNCIONARIO-----------


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        nome = request.form['nome']
        senha = request.form['senha']

        # Verificar dados
        dao = FuncionarioDAO(get_db())
        usuario = dao.autenticar(nome, senha)

        if usuario is not None:
            session['logado'] = {
                'id': usuario[0],
                'nome': usuario[1],
                'tipo': usuario[6]
            }
            criar_comissao()
            return redirect(url_for('index'))
        else:
            msg = ("Erro ao efetuar login!")

    return render_template("login.html", titulo="Login")


@app.route('/logout')
def logout():
    session['logado'] = None
    session.clear()
    return redirect(url_for('index'))


@app.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    return render_template("recuperar-senha.html")


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    msg = ''
    if request.method == "POST":
        # valor = request.form['campoHTML']
        nome = request.form['nome']
        senha = request.form['senha']
        salario = request.form['salario']
        dt_nascimento = request.form['dt_nascimento']
        telefone = request.form['telefone']

        funcionario = Funcionario(nome, senha, salario, dt_nascimento, telefone, 1)

        dao = FuncionarioDAO(get_db())
        codigo = dao.inserir(funcionario)

        if codigo > 0:
            msg = ("Cadastrado com sucesso!")
        else:
            msg = ("Erro ao cadastrar!")

    vartitulo = "Cadastro"
    return render_template("cadastrar.html", titulo=vartitulo, msg=msg)


@app.route('/listar_funcionario', methods=['GET', 'POST'])
def listar_funcionario():
    dao = FuncionarioDAO(get_db())
    funcionarios = dao.listar()
    return render_template("lista-funcionario.html", funcionarios=funcionarios)



@app.route('/atualizar-funcionario-<id>', methods=['GET', 'POST'])
def atualizar_funcionario(id):
    dao = FuncionarioDAO(get_db())
    funcionario = dao.buscar(id)

    if request.method == 'POST':
        nome = request.form['nome']
        salario = request.form['salario']
        dt_nascimento = request.form['dt_nascimento']
        telefone = request.form['telefone']

        print(nome)
        print(funcionario[2])
        print(salario)
        print(dt_nascimento)
        print(telefone)
        print(funcionario[6])


        funcionario = Funcionario(nome, funcionario[2], salario, dt_nascimento, telefone, funcionario[6])
        funcionario.setId(id)
        codigo = dao.atualizar(funcionario)

        if codigo > 0:
            msg = ("Atualizado com sucesso!")
        else:
            msg = ("Erro ao atualizar!")

        return redirect(url_for('listar_funcionario'))
    funcionario_db = dao.listar(id)
    return render_template('atualizar-funcionario.html', funcionario=funcionario_db)


@app.route('/deletar_funcionario/<id>', methods=['GET', 'POST'])
def deletar_funcionario(id):
    dao = FuncionarioDAO(get_db())
    dao.excluir(id)
    return redirect(url_for('listar_funcionario'))


#--------CLIENTE-----------


@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    msg = ''
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

        cliente = Cliente(cpf, nome, rua, bairro, \
                           numero, cep, telefone, email, sexo)

        dao = ClienteDAO(get_db())
        codigo = dao.inserir(cliente)

        if codigo > 0:
            msg = ("Cadastrado com sucesso!")
        else:
            msg = ("Erro ao cadastrar!")

    vartitulo = "Cadastro de Cliente"
    return render_template("cadastro-cliente.html", titulo=vartitulo, msg=msg)


@app.route('/listar_cliente', methods=['GET', 'POST'])
def listar_cliente():
    dao = ClienteDAO(get_db())
    clientes = dao.listar()
    return render_template("lista-cliente.html", clientes=clientes)

@app.route('/deletar_cliente/<id>', methods=['GET', 'POST'])
def deletar_cliente(id):
    dao = ClienteDAO(get_db())
    dao.excluir(id)
    return redirect(url_for('listar_cliente'))


@app.route('/atualizar-cliente-<id>', methods=['GET', 'POST'])
def atualizar_cliente(id):
    dao = ClienteDAO(get_db())

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

        cliente = Cliente(cpf, nome, rua, bairro, cep, numero, telefone, email, sexo)
        cliente.setId(id)
        codigo = dao.atualizar(cliente)

        if codigo > 0:
            msg = ("Atualizado com sucesso!")
        else:
            msg = ("Erro ao atualizar!")

        return redirect(url_for('listar_cliente'))
    cliente_db = dao.listar(id)
    return render_template('atualizar-cliente.html', cliente=cliente_db)


#--------PRODUTO-----------


@app.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    msg = ''
    if request.method == 'POST':
        nome = request.form['nome']
        qt_estoque = request.form['qt_estoque']
        preco = request.form['preço']
        fabricante = request.form['fabricante']
        estado = request.form['estado']
        tempo_de_uso = request.form['tempo_de_uso']

        produto = Produto(nome, qt_estoque, preco, fabricante, estado, tempo_de_uso, 0)

        dao = ProdutoDAO(get_db())
        codigo = dao.inserir(produto)

        if codigo > 0:
            msg = ("Cadastrado com sucesso!")
        else:
            msg = ("Erro ao cadastrar!")

    vartitulo = "Cadastro de Produto"
    return render_template("cadastro-produto.html", titulo=vartitulo, msg=msg)


@app.route('/listar_produto', methods=['GET', 'POST'])
def listar_produto():
    dao = ProdutoDAO(get_db())
    produtos = dao.listar()
    verifica_quantidade()
    return render_template("lista-produto.html", produtos=produtos)


@app.route('/listar_produto-<string:opc>', methods=['GET', 'POST'])
def ordenar_produto(opc):
    dao = ProdutoDAO(get_db())
    produtos = dao.ordenar(opc)
    verifica_quantidade()
    return render_template("lista-produto.html", produtos=produtos)



@app.route('/deletar_produto/<id>', methods=['GET', 'POST'])
def deletar_produto(id):
    dao = ProdutoDAO(get_db())
    dao.excluir(id)
    return redirect(url_for('listar_produto'))



@app.route('/atualizar-produto-<id>', methods=['GET', 'POST'])
def atualizar_produto(id):
    dao = ProdutoDAO(get_db())

    if request.method == 'POST':
        nome = request.form['nome']
        qt_estoque = request.form['qt_estoque']
        preco = request.form['preco']
        fabricante = request.form['fabricante']
        estado = request.form['estado']
        tempo_de_uso = request.form['tempo_de_uso']

        produto = Produto(nome, qt_estoque, preco, fabricante, estado, tempo_de_uso, 0)
        produto.setId(id)
        codigo = dao.atualizar(produto)

        if codigo > 0:
            msg = ("Atualizado com sucesso!")
        else:
            msg = ("Erro ao atualizar!")

        return redirect(url_for('listar_produto'))
    produto_db = dao.listar(id)
    return render_template('atualizar-produto.html', produto=produto_db)


#--------COMPRA-----------


@app.route('/cadastrar_compra', methods=['GET', 'POST'])
def cadastrar_compra():
    msg = ''

    dao = ProdutoDAO(get_db())
    if request.method == 'POST':

        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']

        produto_estoque = dao.buscar(produto_id)

        if int(quantidade) > produto_estoque[2]:
            pass
        else:
            compraproduto = Compraproduto(produto_estoque[1], quantidade, produto_estoque[3], produto_estoque[4], produto_estoque[5], produto_estoque[6], produto_estoque[7])
            new = CompraprodutoDAO(get_db())
            codigo1 = new.inserir(compraproduto)

            produto_novo = Produto(produto_estoque[1], (produto_estoque[2]- int(quantidade)), produto_estoque[3], produto_estoque[4], produto_estoque[5], produto_estoque[6], produto_estoque[7])
            produto_novo.setId(produto_estoque[0])

            codigo2 = dao.inserir(produto_novo)

            if codigo1 > 0 and codigo2 > 0:
                msg = ("Cadastrado com sucesso!")
                dao.excluir(produto_estoque[0])
            else:
                msg = ("Erro ao cadastrar!")

    vartitulo = "Cadastro de Compra"
    produtos = dao.listar()
    verifica_quantidade()
    return render_template("cadastro-compra.html", titulo=vartitulo, msg=msg, produtos=produtos)


@app.route('/compra-cliente', methods=['GET', 'POST'])
def compra_cliente():
    dao = ClienteDAO(get_db())
    msg = ''
    quantidade = 0
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']

        new = CompraprodutoDAO(get_db())
        compras = new.listar()

        for item in compras:
            quantidade = quantidade + int(item[2])
            valor = quantidade * int(item[3])

        data = datetime.now().strftime('%d/%m/%Y')

        cat = ComissaoDAO(get_db())
        comissao = cat.buscar(session['logado']['id'])

        compra = Compra(data, quantidade, valor, comissao[0], cliente_id)
        sup = CompraDAO(get_db())
        codigo = sup.inserir(compra)

        now = ComissaoDAO(get_db())
        comissao = Comissao(valor, session['logado']['id'])
        now.inserir(comissao)

        if codigo > 0:
            msg = ("Cadastrado com sucesso!")

            new.excluir_tabela()
            return redirect(url_for('listar_compra'))
        else:
            msg = ("Erro ao cadastrar!")

    clientes = dao.listar()
    return render_template('compra-cliente.html', clientes=clientes, msg=msg)


@app.route('/verifica-quantidade', methods=['GET', 'POST'])
def verifica_quantidade():
    dao = ProdutoDAO(get_db())
    dao.excluir_zero()


@app.route('/listar_compra', methods=['GET', 'POST'])
def listar_compra():
    dao = CompraDAO(get_db())
    compras = dao.listar()
    return render_template("lista-compra.html", compras=compras)


#--------PONTO-----------


@app.route('/cadastrar-ponto')
def cadastrar_ponto():
    msg = ''
    dao = PontoDAO(get_db())

    hora = datetime.now().strftime('%H:%M:%S')
    data = datetime.now().strftime('%d/%m/%Y')

    ponto_entrada = Ponto(hora, data, session['logado']['nome'], session['logado']['id'])
    codigo = dao.inserir(ponto_entrada)

    if codigo > 0:
        msg = ("Cadastrado com sucesso!")
        return redirect(url_for('index'))

    else:
        msg = ("Erro ao cadastrar!")


    vartitulo = "Cadastro de Produto"

    ponto = dao.quantidade(session['logado']['id'])[0]
    return render_template("index.html", titulo=vartitulo, msg=msg, ponto=ponto)


@app.route('/finalizar-ponto', methods=['GET', 'POST'])
def finalizar_ponto():
    dao = PontoDAO(get_db())

    ponto_entrada = dao.buscar(session['logado']['nome'])

    hora = ponto_entrada[1] + ' - ' + datetime.now().strftime('%H:%M:%S')
    data = ponto_entrada[2] + ' - ' + datetime.now().strftime('%d/%m/%Y')

    ponto_saida = Ponto(hora, data, session['logado']['nome'], session['logado']['id'])
    ponto_saida.setId(ponto_entrada[0])
    codigo = dao.atualizar(ponto_saida)

    if codigo == 0:
        msg = ("Cadastrado com sucesso!")

        new = PontosDAO(get_db())
        ponto = new.inserir(ponto_saida)

        dao.excluir(ponto_entrada[0])

        return redirect(url_for('index'))
    else:
        msg = ("Erro ao cadastrar!")

    ponto = dao.quantidade(session['logado']['id'])[0]

    return render_template("index.html", ponto=ponto)


#--------COMISSAO-----------


@app.route('/listar-comissao', methods=['GET', 'POST'])
def listar_comissao():
    dao = ComissaoDAO(get_db())
    comissaos = dao.juntar(session['logado']['id'])
    return render_template("lista-comissao.html", comissaos=comissaos)


def criar_comissao():
    dao = ComissaoDAO(get_db())
    comissao = Comissao(0,session['logado']['id'])
    comissao.setId(0)
    dao.inserir(comissao)


@app.route('/comissao-mes', methods=['GET', 'POST'])
def comissao_mes():
    meses = {'Janeiro':'01', 'Fevereiro':'02', 'Março':'03', 'Abril':'04', 'Maio':'05', 'Junho':'06', 'Julho':'07', 'Agosto':'08', 'Setembro':'09', 'Outubro':'10', 'Novembro':'11', 'Dezembro':'12'}
    compras_mes = ''
    mes = 'vazio'
    lista = []
    if request.method == 'POST':
        mes = request.form['mes']

        for item in meses:
            if mes == item:
                mes_novo = meses[item]

        new = CompraDAO(get_db())
        compras = new.listar()
        for compra in compras:
            data = compra[1]
            compras_mes = new.filtrar(mes_novo, data)
            if compras_mes not in lista:
                lista.append(compras_mes)

        return render_template("comissao-mes.html", meses=meses, lista=lista)
    return render_template("comissao-mes.html", meses=meses, compras_mes=compras_mes)

#--------PONTO-----------


@app.route('/listar-ponto', methods=['GET', 'POST'])
def listar_ponto():
    dao = PontosDAO(get_db())
    pontos = dao.listar()
    return render_template("lista-ponto.html", pontos=pontos)


if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)