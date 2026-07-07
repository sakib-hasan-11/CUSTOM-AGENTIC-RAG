from collections.abc import Iterable

from schemas.element import DocumentElement
from schemas.element_type import ElementType
from schemas.section import DocumentSection


class SectionBuilder:
    """
    Groups elements into logical sections.

    A new section starts whenever a TITLE is found.
    """

    def build(
        self,
        elements: Iterable[DocumentElement],
    ):
        section_number = 1

        current_title = None
        current_elements: list[DocumentElement] = []


        for element in elements:

            # Ignore document noise
            if element.element_type in (
                ElementType.HEADER,
                ElementType.FOOTER,
            ):
                continue

            # New title starts a new section
            if (
                element.element_type == ElementType.TITLE
                and current_elements
            ):
                yield DocumentSection(
                    section_id=f"section_{section_number}",
                    title=current_title,
                    elements=current_elements,
                )

                section_number += 1
                current_elements = []

            if element.element_type == ElementType.TITLE:
                current_title = element.text

            current_elements.append(element)

        if current_elements:
            yield DocumentSection(
                section_id=f"section_{section_number}",
                title=current_title,
                elements=current_elements,
            )