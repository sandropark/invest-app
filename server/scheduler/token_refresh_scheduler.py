from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from infra.kis.token_refresh import refresh_token_all


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app):
    scheduler.add_job(refresh_token_all, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()
