import asyncio
import logging
from typing import Type

from app.utils.redis_helper import RedisHelper, redis_helper


class RedisHandler(logging.Handler):
    def __init__(self, redis_helper: Type[RedisHelper]):
        super().__init__()
        self.redis_helper = redis_helper

    def emit(self, record):
        try:
            loop = asyncio.get_running_loop()
            if self.redis_helper.redis_client is None:
                loop.create_task(self.redis_helper.connect()) 
            log_entry = self.format(record) 
            loop.create_task(self.redis_helper.log_to_redis(log_entry)) 
        except Exception:
            self.handleError(record)


redis_handler = RedisHandler(redis_helper)
