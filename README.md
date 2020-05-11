# Tripletech Agendamentos

## Descrição do Projeto

Este projeto tem como objetivo desenvolver um sistema web que consulte, adicione e atualize agendamentos. O banco de dados do sistema está
hospedado no SQL Server e as novas informações, que passarão por diversos testes de conflito, serão fornecidas por um documento csv. 

## Começando

Para executar o projeto, será necessário ter os seguintes programas instalados:

- [Python 3.7.7: Linguagem e versão na qual o projeto foi desenvolvido](https://www.python.org/downloads/release/python-377/.html)
- [PyCharm: IDE que possui diversos recursos extremamente úteis para tarefas em Python](https://www.jetbrains.com/pt-br/pycharm/)
- [ODBC Driver 11 for SQL Server no Windows](https://docs.microsoft.com/pt-br/sql/connect/odbc/windows/release-notes-odbc-sql-server-windows?view=sql-server-ver15#previous-releases)

**Obs**: Se o seu computador já possuir o SQL Server instalado, ignorar a etapa de instalação do **ODBC Driver 11**.

## Desenvolvimento

Para iniciar o desenvolvimento do projeto, inicie o PyCharm. No canto superior direito, clique em **File** e em seguida **New project...**
Uma tela como a da **imagem 1** abaixo se abrirá.

[imagem 1](https://prnt.sc/sc6ule)

Na aba **Location**, você pode selecionar uma pasta na qual o projeto será salvo.
Em seguida, clique em **Project Interpreter: New Virtualenv enrionment** e certifique-se que as suas definições estão de acordo com a da **imagem 2**

[imagem 2](https://prnt.sc/sc6wlx)

Clique em **Create** e aguarde a compilação do ambiente virtual.

Por fim, é necessário clonar o projeto do GitHub na pasta em que o seu projeto local foi criado:

```shell
cd "pasta do projeto local"
git clone https://github.com/Anderson-Couto/Tripletech.git
```

Se os passos anteriores forem realizados com sucesso, a pasta Tripletech estatá dentro do seu projeto local.

[imagem 3](https://prnt.sc/sc779b)

## Construção

Acessando o Terminal, na aba inferior esquerda dentro do PyCharm, digite:
```shell
cd Tripletech
```
Agora vc está dentro do projeto Tripletech Agendamentos. 
Nesta etapa será necessário instalar alguns pacotes para o código conseguir rodar de forma correta.
Mas não se preocupe! Basta um comando para realizar esta tarefa.

Ainda no terminal, digite:
```shell
pip install -r requirements.txt
```
Aguarde o término das instalações.

Por fim, continuando no terminal, inicie o servidor Django para acessar o sistema com o comando:
```shell
python manage.py runserver
```
Se todos os processos ocorrerem como o esperado, a seguinte mensagem aparecerá no terminal:

[imagem 4](https://prnt.sc/sc7lrp)

O serviço web Tripletech Agendamentos estará hospedado no link http://127.0.0.1:8000/ e já poderá ser acessado!!

## Features

Este projeto possui três funcionalidades básicas:


**1. Consultar** 

Nesta aba, estão dispostos os Agendamentos, ordenado pelo seus IDs e agrupados a cada 25 por página. 

Também há um formulário, no qual o usuário poderá selecionar uma data inicial e final de uma pesquisa. O output recebido serão todos os agendamentos que ocorrem no intervalo da data pesquisada

**2. Agendar**

O usuário fornecerá ao sistema um documento csv no qual a primeira linha contém o número de membros no evento;na segunda, o id de cada membro; e na terceira, os dias e horas em que o evento começa e termina. Será responsabilidade do sistema validar os dados recebidos. 

Em casos de erro ou conflitos*, será encaminhada uma mensagem de erro ao usuário. Se estiver tudo certo, será renderizada uma query sql para a inserção dos novos dados

*Foi considerado "conflito" uma solicitação de agendamento na qual um ou mais membros do evento já estão agendados em outro evento para aquele intervalo de tempo. Ou seja, diversos agendamentos podem ser realizados para uma mesma data e hora, desde que os membros envolvidos estejam disponíveis.

**3. Atualizar**

O usuário fornecerá ao sistema um documento csv no qual a primeira linha contém um ID de agendamento; e na segunda, os novos dias e horas em que o evento começa e termina. Será responsabilidade do sistema validar os dados recebidos. 

Em casos de erro ou conflitos*, será encaminhada uma mensagem de erro ao usuário. Se estiver tudo certo, será renderizada uma query sql para a atualização dos novos dados

*Foi considerado "conflito" uma solicitação de atualização de agendamento na qual um ou mais membros do evento já estão agendados em outro evento para aquele intervalo de tempo(desconsiderando o evento no qual está sendo requisitada a atualização).
