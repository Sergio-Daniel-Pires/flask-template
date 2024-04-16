import dataclasses as dc
import inspect
from typing import Any, Self


@dc.dataclass
class EchoMessage:
    message: str
    echo_type: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**{
            key: value for key, value in data.items()
            if key in inspect.signature(cls).parameters
        })

    def reverse (self):
        return self.message[::-1]
