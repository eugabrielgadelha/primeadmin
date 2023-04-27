class FuncionariosDAO:
    def __init__(self, con):
        self.con = con

    def inserir(self, funcionarios):

        try:
            sql = "INSERT INTO funcionarios(nome, salario, dt_nascimento, telefone, senha) VALUES (%s, %s, %s, %s, %s)"
            cursor = self.con.cursor()
            cursor.execute(sql, (
                funcionarios.nome, funcionarios.salario, funcionarios.dt_nascimento, funcionarios.telefone,
                funcionarios.senha))

            self.con.commit()
            codigo = cursor.lastrowid
            return codigo

        except:
            return 0

    def autenticar(self, nome, senha):
        try:
            sql = "SELECT * FROM Funcionarios WHERE nome=%s AND senha=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (nome, senha))

            funcionarios = cursor.fetchone()  # lastrowid, fetchone, fetchall

            return funcionarios
        except:
            return None
