import logging
import traceback
from collections.abc import Callable

import flask


class Middleware:
    def __init__(self) -> None:
        pass

    def __call__(self, f: Callable):
        def wrapper(*args, **kwargs):
            status_code = 200
            response = { "result": None, "message": "Ok" }

            try:
                result = f(*args, **kwargs)

                # Return file
                if isinstance(result, flask.Response):
                    return result

                response["result"] = result

            except Exception as exc:
                # Pretty error on server-side
                logging.error(traceback.format_exc)
                status_code = 400
                response["message"] = f"{type(exc).__name__} Error: {exc}"

            # Return json
            return response, status_code

        return wrapper
