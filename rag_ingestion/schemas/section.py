from dataclasses import dataclass, field

from schemas.element import DocumentElement


@dataclass(slots=True)
class DocumentSection:
    """
    Represents one logical document section
    beginning with a Title.
    """

    section_id: str

    title: str | None

    elements: list[DocumentElement] = field(default_factory=list)