class ProdutoDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, produto):
        try:
            sql = "INSERT INTO Produto(nome, qt_estoque, " \
                  "preco, fabricante, estado, tempo_de_uso, compra_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (produto.nome, produto.qt_estoque, produto.preco,
                                 produto.fabricante, produto.estado, produto.tempo_de_uso,
                                 produto.compra_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def buscar(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Produto WHERE id=%s"
            cursor.execute(sql, (id,))
            produto = cursor.fetchone()
            return produto
        except:
            return 0


    def somar_valor(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT SUM(preco) FROM Produto WHERE compra_id=%s"
            cursor.execute(sql, (id,))
            produto = cursor.fetchone()
            return produto
        except:
            return 0


    def listar(self, id=None):
        try:
            cursor = self.con.cursor()
            if id != None:
                # pegar somente uma produto
                sql = "SELECT * FROM Produto WHERE id=%s"
                cursor.execute(sql, (id,))
                produto = cursor.fetchone()
                return produto
            else:
                # pegar todas as produtos
                sql = "SELECT * FROM Produto"
                cursor.execute(sql)
                produtos = cursor.fetchall()
                return produtos
        except:
            return None

    def atualizar(self, produto):
        try:
            sql = "UPDATE Produto SET nome=%s, qt_estoque=%s, preco=%s, fabricante=%s, estado=%s, tempo_de_uso=%s, compra_id=%s WHERE id=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (produto.nome, produto.qt_estoque, produto.preco,
                                 produto.fabricante, produto.estado, produto.tempo_de_uso, produto.compra_id,
                                 produto.id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def excluir(self, id):
        try:
            sql = "DELETE FROM Produto WHERE id = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0

    def excluir_zero(self):
        try:
            sql = "DELETE FROM Produto WHERE qt_estoque = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (0,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0

    def ordenar(self, opc):
        if opc == 'nome_asc':
            cursor = self.con.cursor()
            sql = "SELECT * FROM Produto ORDER BY nome ASC"
            cursor.execute(sql)
            ponto = cursor.fetchall()
            return ponto

        elif opc == 'nome_desc':
            cursor = self.con.cursor()
            sql = "SELECT * FROM Produto ORDER BY nome DESC"
            cursor.execute(sql)
            ponto = cursor.fetchall()
            return ponto

        elif opc == 'fab_asc':
            cursor = self.con.cursor()
            sql = "SELECT * FROM Produto ORDER BY fabricante ASC"
            cursor.execute(sql)
            ponto = cursor.fetchall()
            return ponto

        elif opc == 'fab_desc':
            cursor = self.con.cursor()
            sql = "SELECT * FROM Produto ORDER BY fabricante DESC"
            cursor.execute(sql)
            ponto = cursor.fetchall()
            return ponto












