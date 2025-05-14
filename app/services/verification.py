import random
import string
import redis.asyncio as redis


r = redis.Redis(host="localhost", port=6379, decode_responses=True) # 개발
# r = redis.Redis(host="redis", port=6379, decode_responses=True) # 로컬(도커)

def generate_code(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


async def store_code(email: str, code: str, expires_in: int = 300):
    await r.set(f"verify:{email}", code, ex=expires_in)


async def validate_code(email: str, code: str) -> bool:
    saved = await r.get(f"verify:{email}")
    return saved == code