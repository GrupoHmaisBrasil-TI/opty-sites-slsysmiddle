import asyncio
from typing import Any
from urllib.parse import urlparse
from aiohttp import ClientSession, TCPConnector
from json import dumps
from core.settings import CREDENTIALS 

class SessionManager:
    def __init__(self, *, delay: bool, conn_limit: int = 500, timeout: int = 5):
        """
        delay       -> Se True, inicializa manualmente com .init()
        conn_limit  -> Máx. conexões simultâneas por host
        timeout     -> Timeout padrão (segundos) para requisições
        """
        self.loaded = False
        self.conn_limit = conn_limit
        self.timeout = timeout
        self.clients: dict[str, ClientSession] = {}
        if not delay:
            self.init()

    def init(self):
        if self.loaded:
            return
        self.get_client("http://default")
        self.loaded = True
        print(f"[SessionManager] iniciado com limite={self.conn_limit} e timeout={self.timeout}s")

    def get_client(self, url: str) -> ClientSession:
        name = urlparse(url).netloc
        client = self.clients.get(name)
        if client is None or client.closed:  # <- se fechou, cria nova
            connector = TCPConnector(limit=self.conn_limit)
            client = ClientSession(connector=connector)
            self.clients[name] = client
        return client

    async def request(self, method: str, url: str, *, headers: dict = None, **kwargs) -> Any:
        kwargs.setdefault("timeout", self.timeout)
        async with self.get_client(url).request(method, url, headers=headers, **kwargs) as response:
            try:
                data = await response.json(encoding="utf8")
            except Exception as error:
                print({"status": response.status, "text": await response.text()})
                print(f'[ERROR] : {error}')
                data = await response.text()
            return data

    async def get(self, url: str, *, params: dict[str, Any] = None, **kwargs) -> Any:
        return await self.request("GET", url, params=params,**kwargs)
    
    async def put(self, url: str, *, params: dict[str, Any] = None, headers: dict = None, data=None, **kwargs) -> Any:
        return await self.request("PUT", url, params=params, headers=headers, data=data, **kwargs)

    async def post(self, url: str, *, json: dict[str, Any] = {}, data: dict[str, Any] = {}, **kwargs) -> Any:
        if json:
            return await self.request("POST", url, json=json, **kwargs)
        else:
            return await self.request("POST", url, data=data, **kwargs)

    async def finish(self):
        await asyncio.gather(*[session.close() for session in self.clients.values()])
        print("[SessionManager] conexões HTTP encerradas")


# Instância global com limite ajustado
session_manager = SessionManager(delay=True, conn_limit=500, timeout=5)

# Limite de requisições simultâneas para evitar sobrecarga
semaphore = asyncio.Semaphore(200)


async def send_status_sysmidle(client: SessionManager, data: dict) -> dict:
    async with semaphore:  # controla concorrência
        try:

            status_agendamento = data['chonse_data'][0]['status_consulta']
            id_exame = data['data'][data['chonse_data'][1]['opcao_consulta']]

            # Tratamento para id_exame em lote
            # Valor esperado: id_exame = 123,456,789
            if ',' in id_exame:
                list_id_exame = []
                for value in id_exame.split(','):
                    list_id_exame.append(int(value))
                payload = dumps(list_id_exame)
            else:                
                payload = dumps([id_exame])

            data_response = await client.put(
                url=f"{CREDENTIALS.get('ENDPOINT_HML')}{status_agendamento}", 
                headers = {
                    'Content-Type': 'application/json',
                    "apiKey": f"{CREDENTIALS.get('APIKEY')}"
                },
                data=payload
            )
            return data_response

        except Exception as e:
            return {"status": "error", "message": str(e)}


async def execute_request(data_recive: dict):
    session_manager.init()
    list_data = [{
        'data': data_recive['inArguments'][0], 
        'chonse_data': data_recive['metadata']['options_metadata']
    }]

    # Executa em paralelo respeitando o limite do semaphore
    response = await asyncio.gather(*[send_status_sysmidle(session_manager, data) for data in list_data])
    
    return response

