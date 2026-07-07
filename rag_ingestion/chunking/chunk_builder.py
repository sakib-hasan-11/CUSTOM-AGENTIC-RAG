from schemas.chunk import DocumentChunk
from schemas.section import DocumentSection
from schemas.element_type import ElementType
from utils.tocken_counter import count_tokens


class ChunkBuilder:

    def __init__(
        self,
        min_tokens: int = 150,
        max_tokens: int = 800,
        overlap_tokens: int = 150,
    ):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens

    def build(self, section: DocumentSection):

        chunk_number = 1

        current_elements = []
        current_tokens = 0

        for element in section.elements:

            element_tokens = count_tokens(element.text or "")

            # -------------------------------------------------
            # Need to split?
            # -------------------------------------------------
            if (
                current_elements
                and current_tokens + element_tokens > self.max_tokens
                and current_tokens >= self.min_tokens
            ):

                # ---------------------------------------------
                # Don't end a chunk with an atomic element
                # (image summary / table summary etc.)
                # ---------------------------------------------
                carry_over = []

                while (
                    current_elements
                    and current_elements[-1].metadata.get("atomic", False)
                ):
                    moved = current_elements.pop()

                    current_tokens -= count_tokens(moved.text)

                    carry_over.insert(0, moved)

                yield DocumentChunk(
                    chunk_id=f"{section.section_id}_chunk_{chunk_number}",
                    elements=current_elements,
                    metadata={
                        "section_id": section.section_id,
                        "section_title": section.title,
                        "chunk_index": chunk_number,
                        "start_page": current_elements[0].metadata.get("page_number"),
                        "end_page": current_elements[-1].metadata.get("page_number"),
                        "document_id": current_elements[0].metadata.get("document_id"),
                    },
                )

                chunk_number += 1

                # ---------------------------------------------
                # Token overlap
                # ---------------------------------------------
                overlap = []
                overlap_size = 0

                for e in reversed(current_elements):

                    overlap.insert(0, e)

                    overlap_size += count_tokens(e.text)

                    if overlap_size >= self.overlap_tokens:
                        break

                current_elements = overlap + carry_over
                current_tokens = sum(
                    count_tokens(e.text)
                    for e in current_elements
                )

            current_elements.append(element)
            current_tokens += element_tokens

        if current_elements:

            yield DocumentChunk(
                chunk_id=f"{section.section_id}_chunk_{chunk_number}",
                elements=current_elements,
                metadata={
                    "section_id": section.section_id,
                    "section_title": section.title,
                    "chunk_index": chunk_number,
                    "start_page": current_elements[0].metadata.get("page_number"),
                    "end_page": current_elements[-1].metadata.get("page_number"),
                    "document_id": current_elements[0].metadata.get("document_id"),
                },
            )