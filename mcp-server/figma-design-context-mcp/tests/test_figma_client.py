import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx

from config import Settings
from figma_client import FigmaApiError, FigmaClient


def settings(cache_dir: Path) -> Settings:
    return Settings(
        figma_access_token="test-token",
        figma_api_base_url="https://api.figma.com/v1",
        request_timeout_seconds=5,
        request_retries=0,
        cache_dir=cache_dir,
        cache_ttl_seconds=60,
        max_nodes=100,
        max_text_labels=20,
        max_prompt_input_chars=1000,
    )


class FigmaClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_caches_successful_response(self) -> None:
        requests = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal requests
            requests += 1
            return httpx.Response(200, json={"document": {"name": "Demo"}})

        with tempfile.TemporaryDirectory() as directory:
            client = httpx.AsyncClient(
                base_url="https://api.figma.com/v1",
                transport=httpx.MockTransport(handler),
            )
            async with client:
                figma = FigmaClient(settings(Path(directory)), http_client=client)
                first = await figma.get_file("abc")
                second = await figma.get_file("abc")

        self.assertEqual(first, second)
        self.assertEqual(requests, 1)

    async def test_auth_error_does_not_expose_response_body(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(401, text="secret upstream detail")

        with tempfile.TemporaryDirectory() as directory:
            client = httpx.AsyncClient(
                base_url="https://api.figma.com/v1",
                transport=httpx.MockTransport(handler),
            )
            async with client:
                figma = FigmaClient(settings(Path(directory)), http_client=client)
                with self.assertRaises(FigmaApiError) as raised:
                    await figma.get_file("abc")

        self.assertNotIn("secret upstream detail", str(raised.exception))

    async def test_rate_limit_fails_immediately_with_actionable_headers(self) -> None:
        requests = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal requests
            requests += 1
            return httpx.Response(
                429,
                headers={
                    "Retry-After": "120",
                    "X-Figma-Plan-Tier": "starter",
                    "X-Figma-Rate-Limit-Type": "low",
                },
            )

        with tempfile.TemporaryDirectory() as directory:
            configured = settings(Path(directory))
            configured = Settings(
                **{
                    **configured.__dict__,
                    "request_retries": 3,
                }
            )
            client = httpx.AsyncClient(
                base_url="https://api.figma.com/v1",
                transport=httpx.MockTransport(handler),
            )
            async with client:
                figma = FigmaClient(configured, http_client=client)
                with patch("figma_client.asyncio.sleep", new=AsyncMock()) as sleep:
                    with self.assertRaises(FigmaApiError) as raised:
                        await figma.get_file("abc")

        message = str(raised.exception)
        self.assertEqual(requests, 1)
        sleep.assert_not_awaited()
        self.assertIn("retry after 120 seconds", message)
        self.assertIn("plan tier: starter", message)
        self.assertIn("rate-limit type: low", message)
        self.assertIn("Automatic retries were skipped", message)


if __name__ == "__main__":
    unittest.main()
