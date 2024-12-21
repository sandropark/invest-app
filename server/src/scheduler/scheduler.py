from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from src.infra.account.kis import token_refresher


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app):
    token_refresher.refresh_kis_token()
    scheduler.add_job(token_refresher.refresh_kis_token, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()
