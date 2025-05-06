import logging
import traceback

from fastapi import FastAPI, Request, Response, status
from starlette_csrf import CSRFMiddleware
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.slack import send_slack_notification
from routers import auth, todos
from config.csrf import csrf_settings
from config.env import app_settings


logger = logging.getLogger("uvicorn")

app = FastAPI()


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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Exception Occurred",
        )
    return response


# https://github.com/frankie567/starlette-csrf/tree/main
if not app_settings.TEST_MODE:
    app.add_middleware(CSRFMiddleware, **csrf_settings)
# https://fastapi.tiangolo.com/ja/tutorial/cors/#corsmiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:3000",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(todos.router)


@app.get("/api/health")
def health_check():
    return {"msg": "pass"}
