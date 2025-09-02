# Agendamento Sysmiddle Atividade Customizada

O objetivo é criar uma atividade customizada em uma jornada capaz de confirmar ou cancelar um agendamento de uma consulta ou exame em tempo de execução de uma jornada no Marketiing Cloud

## 🏗️ Arquitetura da Aplicação

### Componentes Principais

3. **🖥️ Frontend** (`public/`)
   - Interface responsiva com componentes [Salesforce](https://developer.salesforce.com/docs/component-library/overview/components)
   - Gerenciamento de status de consultas e exames (confirmar ou cancelar)
   - Renderização de campos da Data Extenion selecionada

2. **⚙️ Backend** (`src/`)
   - API REST desenvolvida com FastAPI
   - Requisições para os endpoints de confirmação e cancelamento Sysmiddle

## 🚀 Como Executar

### Pré-requisitos
- Domínio configurado na aplicação
- Gerar nos pacotes do Marketing Cloud e Definir applicationExtensionKey em config.json

### 1. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto backend (src/):

```env
Credenciais Sysmiddle
ENDPOINT_HML = ENDPOINT_HML
ENDPOINT_PRD = ENDPOINT_PRD
APIKEY = APIKEY
```

### 2. Executar local

```bash
# Executar servidor local para validação simples do layout frontend
cd src
py server.py

```

### 2.1. Executar local (ex: localtunnel NodeJS)

```bash
# Executar em um CMD paralelo (simultaneo)
lt --port 8000 --subdomain my-app-v2

# Incluir a url gerada no lugar de exemple em config.json, como o exemplo abaixo
https://exemple/api/execute -> https://my-app-v2.loca.lt/api/execute
https://exemple/api/save -> https://my-app-v2.loca.lt/api/save 
https://exemple/api/publish -> https://my-app-v2.loca.lt/api/publish
https://exemple/api/stop -> https://my-app-v2.loca.lt/api/stop
https://exemple/api/validate -> https://my-app-v2.loca.lt/api/validate

# Executar em outro CMD um servidor temporario com uvicorn
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
## 📦 Estrutura de Arquivos

```
opty-custom-activity-agendamento-sysmiddle/
├── public/           # Frontend
│   ├── assets/          # Images
│   ├── fonts/               # Fontes
│   ├── js/          
        ├── customActivity.js  # Script de manipulação de dados e comunicação com o Marketing Cloud
        ├── postmonger.js           # Obrigatório para aplicações customizadas
        └── require.js  # Load do carregamento do layout
│   ├── styles/               # Styles
        ├── salesforce-lightning-design-system.min.css   # Obrigatório para aplicações customizadas
│   ├── config.json               # Configuração de Endpoint Marketing Cloud
│   ├── index.html      # Página principal
├── src/ # Backend
│   ├── controllers/             # Endpoints da API
        ├── operations_controller.py   # Controllers de recebimento de dados da jornada
│   ├── core/            # Variaveis Constantes
        ├── settings.py   # Pegar dados .env
│   ├── routing/            # View
        ├── operation_handler.py   # Pegar dados .env
        ├── router.py   # View home page e rederização do public/html
│   ├── .env          # Variaveis de Ambiente
│   ├── server.py          # Instacia servidor
│   ├── services.py         # Funções auxiliares
├── Dockerfile
├── requirements.txt # Bibliotecas

```

## 🔧 Funcionalidades

### Aplicação Frontend
- ✅ Interface intuitiva e responsiva padrão Salesforce
- ✅ Decisão de ação (confirmar ou cancelar)
- ✅ Captação de dados essenciais para o funcionamento da atividade customizada

### API Backend
- ✅ Captação de dados individuais de forma async
- ✅ Requisições com base nas escolhas feitas pelo frontend


## 🛡️ Segurança

- **Rate Limiting** para prevenir abuso da API
- **Variáveis de ambiente** para dados sensíveis
- **Validação de acesso** com credencial direta com o Marketing Cloud

## 🧪 Desenvolvimento

Siga o passo a passo para garantir um bom funcionamento da aplicação

- 1º: Substitua "exemple" pelo dominio da sua aplicação
- 2°: Crie um installed package no Marketing Cloud, sendo:
    - Novo
    - Nome e descriação
    - Adicionar Componente > Journey Builder Activity
    - Name, Descrição, Categoria e Endpoint URL (Raiz da aplicação que será redenrizado o html)
- 3º: Dê acesso somente aos usuários e unidades de negócios necessários em "Access" na configuração do pacote
- 4º: Preencha "applicationExtensionKey" em config.json com a chave unica gerado pela configuração do pacote

## 📞 Suporte

Para suporte técnico ou dúvidas:
- email: backend@leoo.com.br
- email: vivaldo.martins@leoo.com.br

---

**Agendamento Sysmiddle Atividade Customizada** - Aproveite dessa aplicação para gerar uma integrção completa entre dois sistemas que antes não era possível! 🚀
