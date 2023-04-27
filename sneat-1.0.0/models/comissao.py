class Comissao():
    def __init__(self, valor, funcionario_id):

        self.id = 0
        self.valor = valor
        self.funcionario_id = funcionario_id

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
