class Funcionario:
    def __init__(self, nome, salario, dt_nascimento, telefone, senha):
        self.nome = nome
        self.salario = salario
        self.dt_nascimento = dt_nascimento
        self.telefone = telefone
        self.senha = senha

    def getNome(self):
        return self.nome

    def getSalario(self):
        return self.salario

