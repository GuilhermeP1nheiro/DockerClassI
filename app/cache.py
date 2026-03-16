import json
import os

import redis


# Cliente Redis para cache da listagem de usuários.
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=int(os.getenv("REDIS_DB", "0")),
    password=os.getenv("REDIS_PASSWORD") or None,
    decode_responses=True,
)

USUARIOS_CACHE_KEY = "usuarios:list"
USUARIOS_CACHE_TTL_SECONDS = 60


def get_cached_usuarios() -> list[dict] | None:
    raw_data = redis_client.get(USUARIOS_CACHE_KEY)
    if not raw_data:
        return None
    return json.loads(raw_data)


def set_cached_usuarios(usuarios: list[dict]) -> None:
    redis_client.setex(
        USUARIOS_CACHE_KEY,
        USUARIOS_CACHE_TTL_SECONDS,
        json.dumps(usuarios),
    )


def invalidate_usuarios_cache() -> None:
    redis_client.delete(USUARIOS_CACHE_KEY)
