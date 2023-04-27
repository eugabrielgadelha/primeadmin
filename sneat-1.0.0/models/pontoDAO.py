class PontoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, ponto):
        try:
            sql = "INSERT INTO ponto(hora, data, nome, funcionario_id) VALUES (%s, %s, %s, %s)"
            cursor = self.con.cursor()
            cursor.execute(sql, (ponto.hora, ponto.data, ponto.nome,
                                 ponto.funcionario_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def atualizar(self, ponto):
        try:
            sql = "UPDATE Ponto SET hora=%s, data=%s, nome=%s WHERE funcionario_id=%s"
            cursor = self.con.cursor()
            cursor.execute(sql, (ponto.hora, ponto.data, ponto.nome,
                                 ponto.funcionario_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def buscar(self, nome):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Ponto WHERE nome=%s"
            cursor.execute(sql, (nome,))
            ponto = cursor.fetchone()
            return ponto
        except:
            return 0


    def quantidade(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT COUNT(id) FROM ponto WHERE funcionario_id=%s"
            cursor.execute(sql, (id,))
            produto = cursor.fetchone()
            return produto
        except:
            return 0


    def excluir(self, id):
        try:
            sql = "DELETE FROM Ponto WHERE id = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0














