import uvicorn
from app import create_app
from fastapi import Request
from fastapi.responses import JSONResponse

from domain.exception import InvestAppException


app = create_app()


@app.exception_handler(InvestAppException)
async def handle(request: Request, exc: InvestAppException):
    return JSONResponse(status_code=exc.error_code, content=exc.message)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
