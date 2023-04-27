class Pontos():
    def __init__(self, hora, data, nome, funcionario_id):

        self.id = 0
        self.hora = hora
        self.data = data
        self.nome = nome
        self.funcionario_id = funcionario_id

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
