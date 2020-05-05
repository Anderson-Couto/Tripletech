import pyodbc


def retornar_conexao_sql():
    server = "database.czeyimd7imsc.sa-east-1.rds.amazonaws.com,1521 "
    database = "Tripletech"
    username = "candidato"
    password = "c4nd1d4t0"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + password
    conexao = pyodbc.connect(string_conexao)

    return conexao.cursor()


def retorna_consulta(string):
    cursor = retornar_conexao_sql()
    cursor.execute(string)
    agendamentos = cursor.fetchall()

    return agendamentos



BANCO_DADOS_INTEGRADO = retorna_consulta('select PA.PessoaId, PA.AgendamentoId, PE.Nome, AG.DataInicio, AG.DataFim from dbo.PessoaAgendamento PA inner join dbo.Agendamento AG on AG.ID = PA.AgendamentoId inner join dbo.Pessoa PE on PE.Id = PA.PessoaId')
BANCO_DADOS_PESSOA = retorna_consulta('select * from dbo.Pessoa')
BANCO_DADOS_AGENDAMENTO = retorna_consulta('select * from dbo.Agendamento')
BANCO_DADOS_PESSOAAGENDAMENTO = retorna_consulta('select * from dbo.PessoaAgendamento')



