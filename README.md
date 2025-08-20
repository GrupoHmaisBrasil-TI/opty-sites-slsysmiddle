# sadalla-db-sfmc
Integração de agendamentos do banco de dados do cliente para o Marketing Cloud

## Integração
- Requisitar dados para a rota de agendamentos (d+2)
- Realizar as tratativas para o Marketing Cloud identificar esses dados de forma correta (Data, telefone, locale, etc)
- Enviar os dados para o servidor SFTP da BU: 534017328

## Automação (Salesforce Marketing Cloud)
- Identificar novo arquivo no servidor
    - Taxonomia nome: `appointments_sadalla_YYYY-mm-dd.csv`
- Importar os dados para a base correta
    - Automação: Automation Studio / [AT] Integração Agendamentos
    - Data Extension: Integrações / tb_agendamentos

## Requerimentos: 
- ### Definição das variáveis de ambiente 

    DB_HOST = ""
    > Host Banco de dados
    DB_NAME = ""
    > Nome do Banco de dados
    DB_USER = ""
    > Usuário Banco de dados
    DB_PASSWORD = ""
    > Senha Banco de dados
    SFTP_HOST = ""
    > Host SFTP Sadalla
    SFTP_USER = ""
    > Usuário SFTP Sadalla
    SFTP_PASSWORD = ""
    > Senha SFTP Sadalla

- ### Instalação dos pacotes necessários
    - Os pacotes e versões utilizadas encontram-se em requirements.txt
    - Para instalar direto do arquivo, utilizar o comando `python -m pip install -r requirements.txt`

- ### Versão do python 
    - `>= 3.12` (versão utilizada para desenvolvimento)

- ### Alternativas 
    - Dockerfile: testado em ambiente local, caso seja necessário, o arquivo do container encontra-se na pasta raiz do projeto
