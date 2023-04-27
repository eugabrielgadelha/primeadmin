class CompraDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, compra):
        try:
            sql = "INSERT INTO Compra(data, quantidade, valor, comissao_id, cliente_id) VALUES (%s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (compra.data, compra.quantidade, compra.valor,
                                 compra.comissao_id, compra.cliente_id,))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0


    def buscar(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Compra WHERE id=%s"
            cursor.execute(sql, (id,))
            compra = cursor.fetchone()
            return compra
        except:
            return 0

    def listar(self, id=None):
        try:
            cursor = self.con.cursor()
            if id != None:
                # pegar somente uma compra
                sql = "SELECT * FROM Compra WHERE id=%s"
                cursor.execute(sql, (id,))
                compra = cursor.fetchone()
                return compra
            else:
                # pegar todas as compras
                sql = "SELECT * FROM Compra WHERE id>0"
                cursor.execute(sql)
                compras = cursor.fetchall()
                return compras
        except:
            return None

    def filtrar(self, mes, data):
        try:
            data_nova = data[:3]+mes+data[5:]
            cursor = self.con.cursor()
            sql = "SELECT * FROM Compra WHERE data=%s"
            cursor.execute(sql, (data_nova,))
            compra = cursor.fetchall()
            return compra
        except:
            return None

    def atualizar(self, compra):
        try:
            sql = "UPDATE Compra " \
                  "SET data=%s, quantidade=%s, " \
                  "valor=%s, comissao_id=%s, cliente_id=%s " \
                  "WHERE id=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (compra.data, compra.quantidade,
                                 compra.valor, compra.comissao_id, compra.cliente_id, compra.id))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0


    def atualizar_pelo_valor(self, compra):
        try:
            sql = "UPDATE Compra " \
                  "SET valor=%s, cliente_id=%s " \
                  "WHERE id=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (compra.valor, compra.cliente_id, compra.id))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0

















