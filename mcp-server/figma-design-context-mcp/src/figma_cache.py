import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any


def _cache_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_cached_json(
    cache_dir: Path,
    key: str,
    ttl_seconds: int,
) -> Any | None:
    if ttl_seconds == 0:
        return None

    path = cache_dir / f"{_cache_key(key)}.json"

    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        created_at = float(payload["created_at"])
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        path.unlink(missing_ok=True)
        return None

    if time.time() - created_at > ttl_seconds:
        path.unlink(missing_ok=True)
        return None

    return payload.get("data")


def set_cached_json(cache_dir: Path, key: str, data: Any) -> None:
    cache_dir.mkdir(parents=True, mode=0o700, exist_ok=True)
    cache_dir.chmod(0o700)
    path = cache_dir / f"{_cache_key(key)}.json"
    temporary_path = path.with_suffix(f".{os.getpid()}.tmp")

    payload = {
        "created_at": time.time(),
        "data": data,
    }

    temporary_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_path.chmod(0o600)
    temporary_path.replace(path)
