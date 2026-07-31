from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class runId:

    id: str

    @classmethod
    def create(cls):
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S%f"
        )

        return cls(
            id=f"run_{timestamp}"
        )