# File: cart/redis_client.py
# Minimal Redis wrapper (optional). For demo, we use in-memory dict when redis not configured.
import os
try:
    import redis
    REDIS_AVAILABLE = True
except Exception:
    REDIS_AVAILABLE = False

class SimpleCartStorage:
    _store = {}

    @classmethod
    def get_cart(cls, user_id):
        return cls._store.get(str(user_id), {})

    @classmethod
    def set_cart(cls, user_id, data):
        cls._store[str(user_id)] = data

if REDIS_AVAILABLE and os.environ.get('REDIS_URL'):
    r = redis.from_url(os.environ['REDIS_URL'])
    # production usage would implement Redis operations here
else:
    r = SimpleCartStorage
