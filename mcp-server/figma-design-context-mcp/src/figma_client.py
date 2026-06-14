import os
import httpx
from dotenv import load_dotenv

load_dotenv()

FIGMA_API_BASE_URL = "https://api.figma.com/v1"


def get_figma_token() -> str:
    token = os.getenv("FIGMA_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Missing FIGMA_ACCESS_TOKEN in environment.")
    return token


async def figma_get(path: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{FIGMA_API_BASE_URL}{path}",
            headers={"X-Figma-Token": get_figma_token()},
        )

    if response.status_code >= 400:
        raise RuntimeError(f"Figma API error {response.status_code}: {response.text}")

    return response.json()


async def get_figma_file(file_key: str) -> dict:
    return await figma_get(f"/files/{file_key}")


async def get_figma_node(file_key: str, node_id: str) -> dict:
    return await figma_get(f"/files/{file_key}/nodes?ids={node_id}")