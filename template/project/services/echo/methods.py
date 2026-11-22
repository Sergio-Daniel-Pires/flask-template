from collections.abc import Mapping
from typing import Any

from project.services.echo.models import ECHO_TYPES, EchoMessage

VALID_ECHO_TYPES = frozenset(echo_type.lower() for echo_type in ECHO_TYPES)


def echo_message(user_data: Mapping[str, Any]) -> str:
    """Return the message transformed according to ``echo_type``."""
    try:
        echo = EchoMessage.from_dict(dict(user_data))
    except TypeError as exc:
        raise ValueError(f"Missing fields: {exc}") from exc

    echo_type = echo.echo_type.strip().lower()
    if echo_type not in VALID_ECHO_TYPES:
        raise ValueError(f"'{echo.echo_type}' is not a valid echo type")

    if echo_type == "mirror":
        return f"{echo.message} | {echo.reverse()}"
    if echo_type == "reverse":
        return echo.reverse()
    return echo.message
