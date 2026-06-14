from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import re

@dataclass
class ParsedFigmaUrl: 
    file_key: str
    node_id: str | None = None

def parse_figma_url(figma_url: str) -> ParsedFigmaUrl: 
    parsed = urlparse(figma_url)

    match = re.search(r"/(?:file|design)/([^/]+)", parsed.path)
    if not match:
        raise ValueError("Invalid Figma URL. Expected /file/{fileKey} or /design/{fileKey}.")

    query = parse_qs(parsed.query)
    raw_node_id = query.get("node-id", [None])[0]

    return ParsedFigmaUrl(
        file_key=match.group(1),
        node_id=raw_node_id.replace("-", ":") if raw_node_id else None,
    )