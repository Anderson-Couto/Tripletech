from django.shortcuts import render, redirect
from io import TextIOWrapper
from django.contrib import messages
from consultas.forms import ConsultasForms
from consultas.conexão_database import retorna_consulta, BANCO_DADOS_AGENDAMENTO, BANCO_DADOS_PESSOA
from consultas.validadores import verificador_disponibilidade_por_pessoa, importar_csv, transformar, id_eh_registrado,\
    buscar_pessoas_no_evento


def index(request):
    form = ConsultasForms()
    agenda = retorna_consulta('SELECT * FROM dbo.Agendamento')
    dados = {
        'agenda': agenda,
        'form': form,
    }
    return render(request, 'index.html', dados)


def revisao_consulta(request):
    if request.method == 'POST':
        form = ConsultasForms(request.POST)

        if form.is_valid():
            consulta_dia_inicial = form.cleaned_data['dia_inicial']
            consulta_dia_final = form.cleaned_data['dia_final']

            if consulta_dia_inicial > consulta_dia_final:
                messages.error(request, 'Data final da pesquisa não pode ser maior que a inicial')
                return redirect('index')

            agenda = retorna_consulta('SELECT * FROM dbo.Agendamento ORDER BY DataInicio')

            lista_agendamentos = []
            for agendamento in agenda:

                caso_a = consulta_dia_inicial <= agendamento[2].date() and consulta_dia_final >= agendamento[3].date()
                caso_b = consulta_dia_final == agendamento[2].date()
                caso_c = consulta_dia_inicial == agendamento[3].date()
                caso_d = consulta_dia_inicial == agendamento[2].date()
                caso_e = consulta_dia_final == agendamento[3].date()
                caso_f = agendamento[2].date() <= consulta_dia_inicial and agendamento[3].date() >= consulta_dia_final
                caso_g = consulta_dia_inicial <= agendamento[2].date() <= consulta_dia_final
                caso_h = consulta_dia_inicial <= agendamento[3].date() <= consulta_dia_final

                if caso_a or caso_b or caso_c or caso_d or caso_e or caso_f or caso_g or caso_h:
                    lista_agendamentos.append(agendamento)

            dados = {
                'agenda': lista_agendamentos,
                'form': form,
            }
            return render(request, 'minha_consulta.html', dados)

        agenda = retorna_consulta('SELECT * FROM dbo.Agendamento ORDER BY DataInicio')
        dados = {
            'agenda': agenda,
            'form': form,
        }
        return render(request, 'minha_consulta.html', dados)


def agendar(request):
    if request.method == 'POST':
        adicionar_agendamento = TextIOWrapper(request.FILES['adicionar_agendamento'].file)
        dados = importar_csv(adicionar_agendamento)
        numero_pessoas = transformar('', dados[0][0])
        ids_pessoas = dados[1]
        data_inicio = transformar('', dados[2][0])
        data_fim = transformar('', dados[2][1])

        if str(len(dados[1])) != numero_pessoas:
            messages.error(request, 'Numero de pessoas incompatível')
            return render(request, 'agendar.html')

        for id_pessoa in ids_pessoas:
            if id_eh_registrado(int(id_pessoa), banco_dados=BANCO_DADOS_PESSOA) is False:
                messages.error(request, 'Um ou mais IDs não encontrados')
                return render(request, 'agendar.html')
            else:
                if verificador_disponibilidade_por_pessoa(id_pessoa, data_inicio, data_fim) is False:
                    messages.error(request, 'Horário Ocupado')
                    return render(request, 'agendar.html')

        messages.success(request, 'Agendamento realizado com sucesso!!')
        return redirect('index')
    else:
        return render(request, 'agendar.html')


def atualizar(request):
    if request.method == 'POST':
        atualizar_agendamento = TextIOWrapper(request.FILES['atualizar_agendamento'].file)
        dados = importar_csv(atualizar_agendamento)
        id_evento = transformar('', dados[0][0])
        data_inicio_nova = transformar('', dados[1][0])
        data_fim_nova = transformar('', dados[1][1])

        if id_eh_registrado(int(id_evento), banco_dados=BANCO_DADOS_AGENDAMENTO) is True:
            membros_evento = buscar_pessoas_no_evento(id_evento)
            for id_pessoa in membros_evento:
                if verificador_disponibilidade_por_pessoa(id_pessoa, data_inicio_nova, data_fim_nova) is False:
                    messages.error(request, 'Horário Ocupado')
                    return render(request, 'atualizar.html')

            messages.success(request, 'Agendamento atualizado com sucesso!!')
            return redirect('index')
        else:
            messages.error(request, 'ID de Agendamento não encontrado')
            return render(request, 'atualizar.html')
    else:
        return render(request, 'atualizar.html')


