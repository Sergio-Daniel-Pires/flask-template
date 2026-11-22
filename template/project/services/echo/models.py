from __future__ import annotations

import dataclasses as dc
from typing import Any

ECHO_TYPES = ("None", "Reverse", "Mirror")


@dc.dataclass(frozen=True)
class EchoMessage:
    message: str
    echo_type: str = "None"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EchoMessage:
        fields = {field.name for field in dc.fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in fields})

    def reverse(self) -> str:
        return self.message[::-1]
