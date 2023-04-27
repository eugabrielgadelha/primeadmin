class Compraproduto():
    def __init__(self, nome, qt_estoque, preco, fabricante, estado, tempo_de_uso, compra_id):
        self.id = 0
        self.nome = nome
        self.qt_estoque = qt_estoque
        self.preco = preco
        self.fabricante = fabricante
        self.estado = estado
        self.tempo_de_uso = tempo_de_uso
        self.compra_id = compra_id

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def setCompraID(self, id):
        self.compra_id = id