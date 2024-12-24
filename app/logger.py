import asyncio
import logging
from datetime import datetime
from typing import Type
from app.utils.redis import RedisHelper, redis_helper
from pythonjsonlogger import json
from app.config import settings


logger = logging.getLogger()

logHandler = logging.FileHandler("./app/logs/logs.json")


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
            
class RedisHandler(logging.Handler):
    def __init__(self, redis_helper: Type[RedisHelper]):
        super().__init__()
        self.redis_helper = redis_helper
        self.loop = asyncio.get_event_loop()

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.loop.create_task(self.redis_helper.log_to_redis(log_entry))
        except Exception as e:
            self.handleError(record)


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LVL)

redis_handler = RedisHandler(redis_helper)
redis_handler.setFormatter(formatter)
logger.addHandler(redis_handler)
