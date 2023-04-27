class Cliente():
    def __init__(self, cpf, nome, rua,
                 bairro, numero, cep, telefone, email, sexo):
        self.id = 0
        self.cpf = cpf
        self.nome = nome
        self.rua = rua
        self.bairro = bairro
        self.numero = numero
        self.cep = cep
        self.telefone = telefone
        self.email = email
        self.sexo = sexo

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id
