from typing import Any

from project.services.echo.models import EchoMessage


def echo_message(user_data: dict[str, Any]):
    """
    Get a message and echo type and return result transform

    :param user_data: User data with message and echo type
    """
    try:
        echo_message = EchoMessage.from_dict(user_data)

    except TypeError as exc:
        raise TypeError(f"Missing fields: {exc.args}")

    except ValueError as exc:
        raise ValueError(f"'{echo_message.echo_type}' is not an valid echo type!")

    if echo_message.echo_type.lower() == "mirror":
        return f"{echo_message.message} | {echo_message.reverse()}"

    elif echo_message.echo_type.lower() == "reverse":
        return echo_message.reverse()

    return echo_message.message
