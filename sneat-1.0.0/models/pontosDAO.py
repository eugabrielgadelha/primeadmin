class PontosDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, ponto):
        try:
            sql = "INSERT INTO pontos(hora, data, nome, funcionario_id) VALUES (%s, %s, %s, %s)"
            cursor = self.con.cursor()
            cursor.execute(sql, (ponto.hora, ponto.data, ponto.nome,
                                 ponto.funcionario_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def listar(self, id=None):
        try:
            cursor = self.con.cursor()
            if id != None:
                # pegar somente um funcionario
                sql = "SELECT * FROM Pontos WHERE id=%s"
                cursor.execute(sql, (id,))
                funcionario = cursor.fetchone()
                return funcionario
            else:
                # pegar todas os funcionarios
                sql = "SELECT * FROM Pontos"
                cursor.execute(sql)
                pontos = cursor.fetchall()
                return pontos
        except:
            return None


    def atualizar(self, ponto):
        try:
            sql = "UPDATE Pontos SET hora=%s, data=%s, rua=%s, nome=%s WHERE funcionario_id=%s"
            cursor = self.con.cursor()
            cursor.execute(sql, (ponto.hora, ponto.data, ponto.nome,
                                 ponto.funcionario_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def buscar(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Pontos WHERE id=%s"
            cursor.execute(sql, (id,))
            ponto = cursor.fetchone()
            return ponto
        except:
            return 0


    def quantidade(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT COUNT(id) FROM pontos WHERE funcionario_id=%s"
            cursor.execute(sql, (id,))
            produto = cursor.fetchone()
            return produto
        except:
            return 0














