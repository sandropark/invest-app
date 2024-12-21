import logging
import os


def setup_logging():
    # 환경별로 다른 로깅 레벨 설정
    log_level = (
        logging.DEBUG if os.getenv("ENVIRONMENT") == "development" else logging.INFO
    )

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    logger = logging.getLogger(__name__)

    # 파일로도 로그 저장하기 (선택사항)
    # if os.getenv("LOG_TO_FILE"):
    #     file_handler = logging.FileHandler("app.log")
    #     file_handler.setFormatter(
    #         logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    #     )
    #     logger.addHandler(file_handler)

    return logger


logger = setup_logging()
