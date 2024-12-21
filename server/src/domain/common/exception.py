from sqlalchemy import Enum


class ExeptionType(Enum):
    ENTITY_NOT_FOUND = ["엔티티가 없습니다. id: {}", 400]
    INVALID_ACCOUNT_TYPE = ["지원하지 않는 계좌 종류입니다. type: {}", 400]
    FAILED_TO_CREATE_TOKEN = ["토큰 생성 실패. {}", 500]
    FAILED_TO_GET_BALANCE = ["잔고 조회 실패. {}", 500]
    FAILED_TO_GET_CURRENT_PRICE = ["현재가 조회 실패. {}", 500]


class InvestAppException(Exception):
    def __init__(self, exception_type: ExeptionType, *args):
        self.error_code = exception_type[1]
        self.message = exception_type[0].format(*args)
