import hashlib
import json
import time
from pathlib import Path
from typing import Any


CACHE_DIR = Path(".figma_cache")
CACHE_TTL_SECONDS = 60 * 10  # 10 minutes


def _cache_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_cached_json(key: str) -> Any | None:
    CACHE_DIR.mkdir(exist_ok=True)

    path = CACHE_DIR / f"{_cache_key(key)}.json"

    if not path.exists():
        return None

    payload = json.loads(path.read_text(encoding="utf-8"))

    if time.time() - payload["created_at"] > CACHE_TTL_SECONDS:
        return None

    return payload["data"]


def set_cached_json(key: str, data: Any) -> None:
    CACHE_DIR.mkdir(exist_ok=True)

    path = CACHE_DIR / f"{_cache_key(key)}.json"

    payload = {
        "created_at": time.time(),
        "data": data,
    }

    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )