import logging
import traceback

from fastapi import FastAPI, Request, Response, status
from routers import auth, todos
from utils.slack import send_slack_notification

logger = logging.getLogger("uvicorn")

app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = request.url.path

    try:
        response = await call_next(request)
    except Exception:
        response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f"Request: {method} {url} {response.status_code} ip: {client_ip}")
        send_slack_notification(traceback.format_exc())
    finally:
        return response


@app.get("/api/health")
def health_check():
    return {"msg": "pass"}
