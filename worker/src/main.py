from contextlib import asynccontextmanager

from handlers.events import router
from broker.rabbit import broker

import uvicorn
from fastapi import FastAPI
from faststream.rabbit import RabbitExchange, ExchangeType

@asynccontextmanager
async def start_broker(app):
    """Start the broker with the app."""
    async with broker:
        broker.include_router(router)
        await broker.start()
        await broker.declare_exchange(RabbitExchange("exchange", type=ExchangeType.X_DELAYED_MESSAGE, durable=True))
        yield

app = FastAPI(lifespan=start_broker)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8003,
        reload=True,
    )
