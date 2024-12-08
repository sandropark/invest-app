class InvestAppException(Exception):
    def __init__(self, message: str, error_code: int, *args):
        self.error_code = error_code
        self.message = message.format(*args)
