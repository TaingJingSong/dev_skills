import asyncio
from typing import Any

import httpx

from config import Settings, load_settings
from figma_cache import get_cached_json, set_cached_json


RETRYABLE_STATUS_CODES = {500, 502, 503, 504}


class FigmaApiError(RuntimeError):
    """Safe Figma API error that does not expose response bodies or credentials."""


def _rate_limit_message(response: httpx.Response) -> str:
    retry_after = response.headers.get("Retry-After")
    plan_tier = response.headers.get("X-Figma-Plan-Tier")
    limit_type = response.headers.get("X-Figma-Rate-Limit-Type")

    details = []
    if retry_after and retry_after.isdigit():
        details.append(f"retry after {retry_after} seconds")
    if plan_tier:
        details.append(f"plan tier: {plan_tier}")
    if limit_type:
        details.append(f"rate-limit type: {limit_type}")

    suffix = f" ({'; '.join(details)})" if details else ""
    return (
        "Figma API rate limit reached (HTTP 429)"
        f"{suffix}. Automatic retries were skipped to avoid a long wait and additional "
        "quota usage. Wait for the indicated period, then retry once. If this persists, "
        "check the seat and plan for the requested file. Successful responses are cached."
    )


class FigmaClient:
    def __init__(
        self,
        settings: Settings,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings
        self._http_client = http_client
        self._owns_client = http_client is None

    async def __aenter__(self) -> "FigmaClient":
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                base_url=self.settings.figma_api_base_url,
                timeout=self.settings.request_timeout_seconds,
                headers={"X-Figma-Token": self.settings.figma_access_token},
            )
        return self

    async def __aexit__(self, *_: object) -> None:
        if self._owns_client and self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    async def get_file(self, file_key: str) -> dict[str, Any]:
        return await self._get_json(f"/files/{file_key}")

    async def get_node(self, file_key: str, node_id: str) -> dict[str, Any]:
        return await self._get_json(
            f"/files/{file_key}/nodes",
            params={"ids": node_id},
        )

    async def _get_json(
        self,
        path: str,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if self._http_client is None:
            raise RuntimeError("FigmaClient must be used as an async context manager.")

        cache_key = f"{path}?{sorted((params or {}).items())}"
        cached = get_cached_json(
            self.settings.cache_dir,
            cache_key,
            self.settings.cache_ttl_seconds,
        )
        if isinstance(cached, dict):
            return cached

        for attempt in range(self.settings.request_retries + 1):
            try:
                response = await self._http_client.get(path, params=params)
            except httpx.RequestError as exc:
                if attempt >= self.settings.request_retries:
                    raise FigmaApiError(
                        "Figma API request failed. Check network connectivity and retry."
                    ) from exc
                await asyncio.sleep(2**attempt)
                continue

            if response.status_code == 429:
                raise FigmaApiError(_rate_limit_message(response))

            if response.status_code in RETRYABLE_STATUS_CODES:
                if attempt >= self.settings.request_retries:
                    raise FigmaApiError(
                        f"Figma API temporarily unavailable (HTTP {response.status_code})."
                    )
                retry_after = response.headers.get("Retry-After")
                delay = int(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
                await asyncio.sleep(min(delay, 30))
                continue

            if response.status_code in {401, 403}:
                raise FigmaApiError(
                    "Figma authentication failed. Verify token access to the requested file."
                )

            if response.status_code == 404:
                raise FigmaApiError("Figma file or node was not found.")

            if response.status_code >= 400:
                raise FigmaApiError(
                    f"Figma API request failed (HTTP {response.status_code})."
                )

            try:
                data = response.json()
            except ValueError as exc:
                raise FigmaApiError("Figma API returned an invalid JSON response.") from exc

            if not isinstance(data, dict):
                raise FigmaApiError("Figma API returned an unexpected response shape.")

            if self.settings.cache_ttl_seconds > 0:
                set_cached_json(self.settings.cache_dir, cache_key, data)
            return data

        raise FigmaApiError("Figma API request failed.")


async def get_figma_file(file_key: str) -> dict[str, Any]:
    async with FigmaClient(load_settings()) as client:
        return await client.get_file(file_key)


async def get_figma_node(file_key: str, node_id: str) -> dict[str, Any]:
    async with FigmaClient(load_settings()) as client:
        return await client.get_node(file_key, node_id)
