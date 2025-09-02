from controllers import Controller
from core.settings import logger
from fastapi.responses import JSONResponse
from services import execute_request


class OperationsController(Controller):
    def include_routes(self):
        self.router.post("/execute", name="receive data")(self.receive_data)
        self.router.post("/save", response_model=None, name="save")(self.save)
        self.router.post("/validate", response_model=None, name="validate")(
            self.validate
        )
        self.router.post("/publish", response_model=None, name="publish")(self.publish)
        self.router.post("/stop", response_model=None, name="stop")(self.stop)

    def _log_handler(self, operation_name: str):
        logger.info(f"Received operation: {operation_name}")

    def save(self):
        self._log_handler("save")

    def validate(self):
        self._log_handler("validate")

    def publish(self):
        self._log_handler("publish")

    def stop(self):
        self._log_handler("stop")

    @staticmethod
    def log_data(phone: str, journey: str):
        logger.info(f"Received data from {phone} in journey {journey}")

    async def receive_data(self, data:dict):  
        response = await execute_request(data)

        try:
            status = str(response[0].get('status'))

            if status == '304 Not Modified' or status == '400':
                return JSONResponse(content={'status': 'ERROR', 'message': "Erro ao processar a requisição"}, status_code=400)
            return JSONResponse(content={'status': 'SUCCESS', 'message': "Sucesso"},status_code=200)
        except:
            return JSONResponse(content={'status': 'SUCCESS', 'message': "Sucesso"},status_code=200)

        