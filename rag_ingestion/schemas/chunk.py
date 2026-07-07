from dataclasses import dataclass,field
from typing import Any
from schemas.element import DocumentElement
from schemas.element_type import ElementType


# after getting the 100 pages content this will help to chunk semanticly from them . 
# from schemas.chunk_element import ChunkElement
@dataclass(slots=True)
class ChunkElement:
    """
    A single semantic component inside a chunk.
    """

    element_type: ElementType

    text: str

    metadata: dict[str, Any]


@dataclass(slots=True)
class DocumentChunk:

    chunk_id: str

    elements: list[DocumentElement] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)