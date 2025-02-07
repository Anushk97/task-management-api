import json
from typing import Optional
import redis.asyncio as redis
from fastapi import Depends
from .models import TaskResponse

class RedisCache:
    def __init__(self):
        self.redis_client = None

    async def init_redis(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        try:
            await self.redis_client.ping()
        except redis.ConnectionError:
            self.redis_client = None

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()

    async def get_task(self, task_id: int) -> Optional[dict]:
        if not self.redis_client:
            return None
        
        try:
            data = await self.redis_client.get(f"task:{task_id}")
            if data:
                return json.loads(data)
        except Exception:
            return None
        return None

    async def set_task(self, task_id: int, task: TaskResponse):
        if not self.redis_client:
            return
        
        try:
            task_data = task.model_dump()
            await self.redis_client.set(
                f"task:{task_id}",
                json.dumps(task_data),
                ex=3600  # Cache for 1 hour
            )
        except Exception:
            pass

    async def invalidate_task(self, task_id: int):
        if not self.redis_client:
            return
        
        try:
            await self.redis_client.delete(f"task:{task_id}")
        except Exception:
            pass

cache = RedisCache()
