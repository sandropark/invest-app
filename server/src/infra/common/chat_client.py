import datetime as dt
from pytz import timezone
import requests
import yaml

with open("config/hantu-stock-config.yml", encoding="UTF-8") as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

now = dt.datetime.now(timezone("Asia/Seoul"))


def send_message(msg):
    message = {"text": f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {str(msg)}"}
    requests.post(
        _cfg["noti-url"], json=message, headers={"Content-Type": "application/json"}
    )
