from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

import infra.kis.token_refresher as token_refresher


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app):
    token_refresher.refresh_token_all()
    scheduler.add_job(token_refresher.refresh_token_all, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()
