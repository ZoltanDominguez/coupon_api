import logging

from coupon_api.initialization.config import config

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s", level=config.main.log_level
)


def get_logger(name: str):
    return logging.getLogger(name)
