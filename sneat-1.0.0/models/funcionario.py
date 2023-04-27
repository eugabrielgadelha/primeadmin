class Funcionario():
    def __init__(self, nome, senha,
                 salario, dt_nascimento, telefone, tipo):
        self.id = 0
        self.nome = nome
        self.senha = senha
        self.salario = salario
        self.dt_nascimento = dt_nascimento
        self.telefone = telefone
        self.tipo = tipo

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
