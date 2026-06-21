import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()
FIGMA_API_BASE_URL = "https://api.figma.com/v1"


def _read_int(name: str, default: int, minimum: int) -> int:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer.") from exc

    if value < minimum:
        raise RuntimeError(f"{name} must be at least {minimum}.")

    return value


@dataclass(frozen=True)
class Settings:
    figma_access_token: str
    figma_api_base_url: str
    request_timeout_seconds: int
    request_retries: int
    cache_dir: Path
    cache_ttl_seconds: int
    max_nodes: int
    max_text_labels: int
    max_prompt_input_chars: int


def load_settings() -> Settings:
    token = os.getenv("FIGMA_ACCESS_TOKEN", "").strip()
    if not token:
        raise RuntimeError("FIGMA_ACCESS_TOKEN is required.")

    return Settings(
        figma_access_token=token,
        figma_api_base_url=FIGMA_API_BASE_URL,
        request_timeout_seconds=_read_int("FIGMA_REQUEST_TIMEOUT_SECONDS", 30, 1),
        request_retries=_read_int("FIGMA_REQUEST_RETRIES", 3, 0),
        cache_dir=Path(
            os.getenv(
                "FIGMA_CACHE_DIR",
                str(Path.home() / ".cache" / "figma-design-context-mcp"),
            )
        ).expanduser(),
        cache_ttl_seconds=_read_int("FIGMA_CACHE_TTL_SECONDS", 600, 0),
        max_nodes=_read_int("FIGMA_MAX_NODES", 1500, 1),
        max_text_labels=_read_int("FIGMA_MAX_TEXT_LABELS", 250, 1),
        max_prompt_input_chars=_read_int("FIGMA_MAX_PROMPT_INPUT_CHARS", 20000, 100),
    )
