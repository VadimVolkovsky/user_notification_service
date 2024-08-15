import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.notifications import router as notification_router, rabbit_router
from core.config import settings
from core.logger import LOGGING


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=rabbit_router.lifespan_context,
)

app.include_router(notification_router, prefix="/api/v1")
app.include_router(rabbit_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
