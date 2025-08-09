from redis.asyncio import Redis

from app.config.env_config import settings

_token_blacklist = Redis.from_url(settings.REDIS_URI)


async def add_jti_to_blacklist(jti: str):
    await _token_blacklist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacklist.exists(jti)
