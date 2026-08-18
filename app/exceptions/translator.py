import httpx

from app.exceptions.flowise_exception import (
    FlowiseConnectionError,
    FlowiseResponseError,
    FlowiseTimeoutError,
)


def translate_flowise_exception(exc: httpx.HTTPError) -> Exception:
    if isinstance(exc, httpx.TimeoutException):
        return FlowiseTimeoutError(
            "Flowise request timed out"
        )

    if isinstance(exc, httpx.ConnectError):
        return FlowiseConnectionError(
            "Could not connect to Flowise"
        )

    if isinstance(exc, httpx.HTTPStatusError):
        status_code = exc.response.status_code

        return FlowiseResponseError(
            f"Flowise returned HTTP {status_code}"
        )

    return FlowiseConnectionError(
        "Flowise request failed"
    )