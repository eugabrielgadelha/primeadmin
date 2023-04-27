class ComissaoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, comissao):
        try:
            sql = "INSERT INTO Comissao(valor, funcionario_id) VALUES (%s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (comissao.valor, comissao.funcionario_id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def buscar(self, funcionario_id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Comissao WHERE funcionario_id=%s"
            cursor.execute(sql, (funcionario_id,))
            compra = cursor.fetchone()
            return compra
        except:
            return 0



    def atualizar(self, comissao):
        try:
            sql = "UPDATE Comissao SET valor=%s, funcionario_id=%s WHERE id=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (comissao.valor, comissao.funcionario_id, comissao.id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def somar_valor(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT SUM(valor) FROM Compra WHERE comissao_id=%s"
            cursor.execute(sql, (id,))
            produto = cursor.fetchone()
            return produto
        except:
            return 0

    def listar(self, id=None):
        try:
            cursor = self.con.cursor()
            if id != None:
                # pegar somente um funcionario
                sql = "SELECT * FROM Comissao WHERE id=%s"
                cursor.execute(sql, (id,))
                funcionario = cursor.fetchone()
                return funcionario
            else:
                # pegar todas os funcionarios
                sql = "SELECT * FROM Comissao"
                cursor.execute(sql)
                funcionarios = cursor.fetchall()
                return funcionarios
        except:
            return None


    def mes(self, id=None):
        try:
            cursor = self.con.cursor()
            # pegar todas os funcionarios
            sql = "SELECT * FROM Comissao"
            cursor.execute(sql)
            funcionarios = cursor.fetchall()
            return funcionarios
        except:
            return None

    def juntar(self, funcionario_id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT id, SUM(valor), funcionario_id FROM Comissao WHERE funcionario_id=%s GROUP BY funcionario_id"
            cursor.execute(sql, (funcionario_id,))
            ponto = cursor.fetchall()
            return ponto
        except:
            return 0