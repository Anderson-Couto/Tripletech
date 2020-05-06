from django.shortcuts import render, redirect
from io import TextIOWrapper
from django.contrib import messages
from consultas.forms import ConsultasForms
from consultas.conexão_database import retorna_consulta, BANCO_DADOS_AGENDAMENTO, BANCO_DADOS_PESSOA
from consultas.validadores import verificador_disponibilidade_por_pessoa, importar_csv, transformar, id_eh_registrado,\
    buscar_pessoas_no_evento, vdpp_dois
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    # Método para renderizar a página inicial do sistema
    form = ConsultasForms()
    agenda = retorna_consulta('SELECT * FROM dbo.Agendamento')
    paginator = Paginator(agenda, 25)
    page = request.GET.get('page')
    agendamentos_por_pagina = paginator.get_page(page)
    dados = {
        'agenda': agendamentos_por_pagina,
        'form': form,
    }
    return render(request, 'index.html', dados)


def revisao_consulta(request):
    # metodo para renderizar a página de consultas a partir do forms da página inicial. Esse método também
    # é capaz de renderizar a si mesmo, fazendo novas consultas como se estivesse no index.
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
    else:
        return redirect('index')


def agendar(request):
    # método para a validação do documento csv e análise de conflitos com o banco de dados para realização de
    # novos agendamentos. Renderiza a si mesmo, quando um agendamento novo é válido, com as querys sql para serem
    # usadas no banco de dados
    try:
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
                    messages.error(request, f'Usuario {id_pessoa} não encontrado(a)')
                    return render(request, 'agendar.html')
                else:
                    if verificador_disponibilidade_por_pessoa(id_pessoa, data_inicio, data_fim) is False:
                        messages.error(request, f'O Usuario {id_pessoa} está indisponível neste horário')
                        return render(request, 'agendar.html')

            id_novo_agendamento = retorna_consulta("select MAX(ID)+1 from dbo.Agendamento")
            id_novo_agendamento = transformar('', str(id_novo_agendamento[0][0]))

            informacoes = [ids_pessoas, data_inicio, data_fim, id_novo_agendamento]
            contexto = {
                'informacoes': informacoes
            }

            messages.success(request, 'O agendamento solicitado não possui conflitos!!')
            return render(request, 'agendar.html', contexto)

            # messages.success(request, 'Agendamento realizado com sucesso!!')
            # return redirect('index')
        else:
            return render(request, 'agendar.html')
    except:
        messages.error(request, 'O arquivo .csv fornecido não é compátível com a funcionalidade Agendamento. Verifique a presença de erros.')
        return render(request, 'agendar.html')


def atualizar(request):
    # método para a validação do documento csv e análise de conflitos com o banco de dados para realização de
    # atualização de agendamentos já existentes. Renderiza a si mesmo, quando uma atualização é válida, com as querys
    # sql para serem usadas no banco de dados.
    try:
        if request.method == 'POST':
            atualizar_agendamento = TextIOWrapper(request.FILES['atualizar_agendamento'].file)
            dados = importar_csv(atualizar_agendamento)
            id_evento = transformar('', dados[0][0])
            data_inicio_nova = transformar('', dados[1][0])
            data_fim_nova = transformar('', dados[1][1])

            if id_eh_registrado(int(id_evento), banco_dados=BANCO_DADOS_AGENDAMENTO):
                membros_evento = buscar_pessoas_no_evento(id_evento)
                for id_pessoa in membros_evento:
                    if vdpp_dois(id_pessoa, data_inicio_nova, data_fim_nova, int(id_evento)) is False:
                        messages.error(request, f'O Usuario {id_pessoa} está indisponível neste horário')
                        return render(request, 'atualizar.html')

                informacoes = [id_evento, data_inicio_nova, data_fim_nova]
                contexto = {
                    'informacoes': informacoes
                }

                messages.success(request, f'Não há conflitos para a atualização do evento {id_evento}!!')
                return render(request, 'atualizar.html', contexto)

                # messages.success(request, f'Evento {id_evento} atualizado com sucesso!!')
                # return redirect('index')
            else:
                messages.error(request, f'Evento {id_evento} não encontrado')
                return render(request, 'atualizar.html')
        else:
            return render(request, 'atualizar.html')
    except:
        messages.error(request, 'O arquivo .csv fornecido não é compátível com a funcionalidade Atualizar. Verifique a presença de erros.')
        return render(request, 'atualizar.html')

