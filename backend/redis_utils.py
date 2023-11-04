import redis as r
from typing import Optional, Any
import json

redis = r.Redis(connection_pool=r.ConnectionPool(host='localhost', port=6379))

def recurse_to_json(obj):
    if isinstance(obj, dict):
        return {k: recurse_to_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recurse_to_json(v) for v in obj]
    elif hasattr(obj, 'to_json'):
        return obj.to_json()
    else:
        return obj


def rget(key: str, game_id: Optional[str] = None) -> Optional[str]:
    if game_id is not None:
        key = f"{key}:{game_id}"
    raw_result = redis.get(key)
    return raw_result.decode('utf-8') if raw_result is not None else None


def can_be_inted(x):
    try:
        int(x)
        return True
    except:
        return False


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k) if can_be_inted(k) else k:v for k,v in x.items()}
    return x


def rget_json(key: str, game_id: Optional[str] = None) -> Optional[Any]:
    raw_result = rget(key, game_id)
    return json.loads(raw_result, object_hook=jsonKeys2int) if raw_result is not None else None


def rset(key: str, value: Any, game_id: Optional[str] = None) -> None:
    ex = None
    if game_id is not None:
        key = f"{key}:{game_id}"
        ex = 60*60*24*7
    redis.set(key, value, ex=ex)

def rset_json(key: str, value: Any, game_id: Optional[str] = None) -> None:
    rset(key, json.dumps(value), game_id)