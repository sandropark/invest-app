from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from src.domain.account import account_service


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app):
    account_service.refresh_kis_token()
    scheduler.add_job(account_service.refresh_kis_token, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()
