from fastapi import FastAPI
from rest import quote, strategy, account


def create_app():
    app = FastAPI()

    app.include_router(strategy.router)
    app.include_router(account.router)
    app.include_router(quote.router)

    return app
