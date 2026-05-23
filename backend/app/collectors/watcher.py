from __future__ import annotations

import json

from redis.asyncio import Redis


class EventStreamPublisher:
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    async def publish(self, cluster_id: str, event: dict) -> str:
        stream = f"cluster:{cluster_id}:events"
        return await self.redis.xadd(stream, {"payload": json.dumps(event)})


class EventStreamConsumer:
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    async def read(self, cluster_id: str, last_id: str = "$", block_ms: int = 5000) -> list[tuple[str, dict]]:
        stream = f"cluster:{cluster_id}:events"
        rows = await self.redis.xread({stream: last_id}, block=block_ms, count=100)
        events: list[tuple[str, dict]] = []
        for _, entries in rows:
            for event_id, payload in entries:
                events.append((event_id, json.loads(payload[b"payload"])))
        return events
