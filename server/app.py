from domain.config.logging_config import logger
from fastapi import FastAPI, Request
from rest import stock, strategy, account
from fastapi.responses import JSONResponse
from domain.exception import InvestAppException
from scheduler import token_refresh_scheduler

app = FastAPI(lifespan=token_refresh_scheduler.lifespan)

app.include_router(strategy.router)
app.include_router(account.router)
app.include_router(stock.router)


@app.exception_handler(InvestAppException)
async def handle(request: Request, exc: InvestAppException):
    logger.error(exc)
    return JSONResponse(status_code=exc.error_code, content=exc.message)


@app.exception_handler(AssertionError)
async def handle(request: Request, exc: AssertionError):
    logger.error(exc)
    return JSONResponse(status_code=400, content=str(exc))


def create_app():
    return app
