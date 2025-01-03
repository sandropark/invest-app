from contextlib import asynccontextmanager
from src.containers import Container
from apscheduler.schedulers.background import BackgroundScheduler

from src.account.adapter.out.kis import token_refresher


scheduler = BackgroundScheduler()

container = Container.get_instance()
strategy_service = container.strategy_service()


def rebalance_all():
    strategy_service.rebalance_all()


@asynccontextmanager
async def lifespan(app):
    token_refresher.refresh_kis_token()
    scheduler.add_job(token_refresher.refresh_kis_token, "interval", hours=12)
    scheduler.add_job(rebalance_all, "interval", hours=1)

    scheduler.start()
    yield
    scheduler.shutdown()
