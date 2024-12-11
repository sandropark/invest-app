from contextlib import asynccontextmanager
import pprint
from apscheduler.schedulers.background import BackgroundScheduler

from infra.kis.token_refresh import refresh_token_all


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app):
    pprint.pprint("토큰 갱신 스케줄러 시작")
    scheduler.add_job(refresh_token_all, "interval", hours=12)
    scheduler.start()
    yield
    scheduler.shutdown()
