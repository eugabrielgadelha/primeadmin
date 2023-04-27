class Compra():
    def __init__(self, data, quantidade, valor,
                 comissao_id, cliente_id):
        self.id = 0
        self.data = data
        self.quantidade = quantidade
        self.valor = valor
        self.comissao_id = comissao_id
        self.cliente_id = cliente_id

    def getData(self):
        return self.data

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

