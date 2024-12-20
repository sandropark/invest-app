from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class KisAccessToken:
    token: str
    expiration: str

    def of(json: dict):
        return KisAccessToken(
            token=json["access_token"], expiration=json["access_token_token_expired"]
        )

    def to_dict(self):
        return {
            "token": self.token,
            "expiration": self.expiration,
        }

    def is_expired(self) -> bool:
        return self._get_token_expiration() < datetime.now()

    def _get_token_expiration(self) -> datetime:
        return datetime.strptime(self.expiration, "%Y-%m-%d %H:%M:%S") - timedelta(
            hours=12
        )
