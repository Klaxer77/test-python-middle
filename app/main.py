from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import time
import asyncio
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from redis import asyncio as aioredis
from app.utils.redis import redis_helper
from app.config import settings
from app.database import Base, engine
from app.logger import logger
from app.item.router import router as item_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await redis_helper.connect()
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await redis_helper.close()


app = FastAPI(
    lifespan=lifespan,
    title="ToDoList",
    root_path="/api",
    version="0.1.0"
)

app.include_router(item_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    log_data = {
        "process_time": round(process_time, 4),
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers)
        }
    logger.info("Request information", extra=log_data)
    return response
