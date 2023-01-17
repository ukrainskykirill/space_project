from redis import asyncio as aioredis
import redis
from space.settings import REDIS_PORT, REDIS_HOST

async_redis = aioredis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

sync_redis = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


