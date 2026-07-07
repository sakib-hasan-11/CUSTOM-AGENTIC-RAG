from dataclasses import dataclass
from typing import Any

# this will for pinecone db metadata store .
@dataclass(slots=True)
class VectorRecord:
    id: str

    values: list[float]

    metadata: dict[str, Any]