from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from core.settings import templates
from routing import operation_handler

routes = APIRouter()


@routes.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Custom Avenida"}
    )


routes.include_router(operation_handler.router, prefix="/api", tags=["Operations"])