from fastapi import FastAPI
from rest import stock, strategy, account


def create_app():
    app = FastAPI()

    app.include_router(strategy.router)
    app.include_router(account.router)
    app.include_router(stock.router)

    return app
