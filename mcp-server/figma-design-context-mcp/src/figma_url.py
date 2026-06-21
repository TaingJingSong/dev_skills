from dataclasses import dataclass
import re
from urllib.parse import parse_qs, urlparse


ALLOWED_FIGMA_HOSTS = {"figma.com", "www.figma.com"}
SUPPORTED_FILE_ROUTES = {"design", "file", "proto"}


@dataclass(frozen=True)
class ParsedFigmaUrl:
    file_key: str
    node_id: str | None = None


def parse_figma_url(figma_url: str) -> ParsedFigmaUrl:
    if not isinstance(figma_url, str) or not figma_url.strip():
        raise ValueError("Figma URL is required.")

    parsed = urlparse(figma_url.strip())
    hostname = (parsed.hostname or "").lower()

    if parsed.scheme != "https" or hostname not in ALLOWED_FIGMA_HOSTS:
        raise ValueError("Figma URL must use https://www.figma.com or https://figma.com.")

    route_pattern = "|".join(sorted(SUPPORTED_FILE_ROUTES))
    match = re.search(rf"/(?:{route_pattern})/([A-Za-z0-9_-]+)", parsed.path)
    if not match:
        raise ValueError(
            "Invalid Figma URL. Expected /design/{fileKey}, /file/{fileKey}, "
            "or /proto/{fileKey}."
        )

    query = parse_qs(parsed.query)
    raw_node_id = query.get("node-id", [None])[0]
    node_id = raw_node_id.replace("-", ":") if raw_node_id else None

    if node_id and not re.fullmatch(r"\d+:\d+", node_id):
        raise ValueError("Invalid Figma node-id. Expected a value such as 12-34 or 12:34.")

    return ParsedFigmaUrl(
        file_key=match.group(1),
        node_id=node_id,
    )
