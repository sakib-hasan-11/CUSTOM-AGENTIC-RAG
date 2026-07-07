from schemas.chunk import DocumentChunk
from schemas.element_type import ElementType


class MarkdownRenderer:
    """
    Converts a DocumentChunk into markdown text for embedding.
    """

    def render(
        self,
        chunk: DocumentChunk,
    ) -> str:
        lines: list[str] = []

        for element in chunk.elements:
            match element.element_type:
                case ElementType.TITLE:
                    lines.append(f"# {element.text}")

                case ElementType.TEXT:
                    lines.append(element.text)

                case ElementType.TABLE:
                    lines.append("## Table")
                    lines.append(element.text)

                case ElementType.CAPTION:
                    lines.append(f"*{element.text}*")

                case ElementType.LIST:
                    lines.append(f"- {element.text}")

                case ElementType.IMAGE:
                    summary = ""

                    if element.enrichment:
                        summary = element.enrichment.get(
                            "vision_summary",
                            "",
                        )

                    if summary:
                        lines.append("## Figure")
                        lines.append(summary)

                case _:
                    lines.append(element.text)

        return "\n\n".join(lines)
