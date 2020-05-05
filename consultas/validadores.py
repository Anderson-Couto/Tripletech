import csv
import datetime
from consultas.conexão_database import retorna_consulta


BANCO_DADOS_INTEGRADO = retorna_consulta('select PA.PessoaId, PA.AgendamentoId, PE.Nome, AG.DataInicio, AG.DataFim from dbo.PessoaAgendamento PA inner join dbo.Agendamento AG on AG.ID = PA.AgendamentoId inner join dbo.Pessoa PE on PE.Id = PA.PessoaId')
BANCO_DADOS_PESSOA = retorna_consulta('select * from dbo.Pessoa')
BANCO_DADOS_AGENDAMENTO = retorna_consulta('select * from dbo.Agendamento')

def importar_csv(documento):
    leitor = csv.reader(documento)
    dicionario = {}
    n = 0
    for linha in leitor:
        dicionario[n] = linha
        n += 1
    return dicionario


def transformar(separador, dicionario):
    informacao = f'{separador}'.join(dicionario)
    return informacao


def verificador_disponibilidade_por_pessoa(ident_pessoa, data_i, data_f):

    validador = True

    data_i = datetime.datetime.strptime(data_i, "%Y-%m-%d %H:%M:%S")
    data_f = datetime.datetime.strptime(data_f, "%Y-%m-%d %H:%M:%S")
    if data_f < data_i:
        validador = False

    for objeto in BANCO_DADOS_INTEGRADO:
        if str(ident_pessoa) == str(objeto[0]):
            caso_a = data_i > objeto[3] and data_i < objeto[4]
            caso_b = data_f > objeto[3] and data_f < objeto[4]
            caso_c = data_i == objeto[3]
            caso_d = data_f == objeto[4]
            caso_e = data_i < objeto[3] and data_f > objeto[4]
            caso_f = caso_c and caso_d
            if caso_a or caso_b or caso_c or caso_d or caso_e or caso_f:
                validador = False

    return validador


def id_eh_registrado(id, banco_dados):
    validador = True

    ids_registrados = []
    for objeto in banco_dados:
        ids_registrados.append(objeto[0])

    if id not in ids_registrados:
        validador = False

    return validador


def buscar_pessoas_no_evento(agendamento_id):
    lista_ids = []
    for objeto in BANCO_DADOS_INTEGRADO:
        if str(agendamento_id) == str(objeto[1]):
            lista_ids.append(objeto[0])

    return lista_ids


