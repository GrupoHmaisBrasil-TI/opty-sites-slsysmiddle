from core.api import get_application
from uvicorn import run
from routing import router

app = get_application(router.routes)


if __name__ == "__main__":
    # Run local
    run("server:app", host="127.0.0.1", port=8000, reload=True)
    # Run Uvcicorn + Local Tunnel
    '''
    CMD 1: uvicorn server:app --host 0.0.0.0 --port 8000 --reload
    CMD 2: lt --port 8000 --subdomain meuapp
    '''
    