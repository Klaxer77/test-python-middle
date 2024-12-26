import logging
from datetime import datetime

from pythonjsonlogger import json

from app.config import settings
from app.utils.redis_handler import redis_handler

logger = logging.getLogger()

logHandler = logging.FileHandler("./logs/logs.json")


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now().isoformat()
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

if not settings.MODE == "TEST":
    
    # Логгируем и в file и в redis
    
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    redis_handler.setFormatter(formatter)
    logger.addHandler(redis_handler)

    logger.setLevel(settings.LOG_LVL)
