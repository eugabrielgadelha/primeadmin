class FuncionarioDAO():
    def __init__(self, con):
        self.con = con

    # CRUD - Create, Retrieve, Update, Delete
    def inserir(self, funcionario):
        try:
            sql = "INSERT INTO funcionario(nome, senha, " \
                  "salario, dt_nascimento, telefone, tipo) VALUES (%s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (funcionario.nome, funcionario.senha, funcionario.salario,
                                 funcionario.dt_nascimento, funcionario.telefone, funcionario.tipo,))
            self.con.commit()

            codigo = cursor.lastrowid
            return codigo
        except:
            return 0

    def autenticar(self, nome, senha):
        try:
            sql = "SELECT * FROM Funcionario WHERE nome=%s AND senha=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (nome, senha))

            usuario = cursor.fetchone()  # lastrowid, fetchone, fetchall
            return usuario
        except:
            return None

    def listar(self, id=None):
        try:
            cursor = self.con.cursor()
            if id != None:
                # pegar somente um funcionario
                sql = "SELECT * FROM Funcionario WHERE id=%s"
                cursor.execute(sql, (id,))
                funcionario = cursor.fetchone()
                return funcionario
            else:
                # pegar todas os funcionarios
                sql = "SELECT * FROM Funcionario"
                cursor.execute(sql)
                funcionarios = cursor.fetchall()
                return funcionarios
        except:
            return None

    def atualizar(self, funcionario):
        try:
            sql = "UPDATE Funcionario SET nome=%s, salario=%s, dt_nascimento=%s, telefone=%s WHERE id=%s"

            cursor = self.con.cursor()
            cursor.execute(sql, (funcionario.nome, funcionario.salario, funcionario.dt_nascimento,
                                 funcionario.telefone, funcionario.id))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0

    def buscar(self, id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Funcionario WHERE id=%s"
            cursor.execute(sql, (id,))
            funcionario = cursor.fetchone()
            return funcionario
        except:
            return 0

    def excluir(self, id):
        try:
            sql = "DELETE FROM Funcionario WHERE id = %s"
            cursor = self.con.cursor()
            cursor.execute(sql, (id,))
            self.con.commit()
            return cursor.rowcount
        except:
            return 0













