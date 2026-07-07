from pathlib import Path

from schemas.section import DocumentSection
from schemas.element_type import ElementType
from utils.tocken_counter import count_tokens
from vision.openai_provider import OpenAIVisionProvider


class VisionProcessor:
    """
    Enrich IMAGE elements with GPT Vision summaries.

    Runs BEFORE chunking so the model can see the complete section
    instead of only a small embedding chunk.
    """

    def __init__(
        self,
        provider: OpenAIVisionProvider,
        max_context_tokens: int = 500,
        model:str='gpt-4o-mini'
    ):
        self.model_name = model
        self.provider = provider
        self.max_context_tokens = max_context_tokens

    def enrich(
        self,
        section: DocumentSection,
    ) -> DocumentSection:

        for idx, element in enumerate(section.elements):

            if element.element_type != ElementType.IMAGE:
                continue

            image_path = Path(element.metadata["image_path"])

            context = self._build_context(
                section=section,
                image_index=idx,
            )

            summary, latency = self.provider.summarize(
                image_path=image_path,
                context=context,
            )

            element.enrichment = {
                "vision_summary": summary,
                "vision_model": self.provider.model_name,
                "context_used": context,
                "latency_ms": round(latency, 2),
            }

            # Tell the ChunkBuilder this image should never
            # be separated from surrounding paragraphs.
            element.metadata["atomic"] = True

        return section

    def _build_context(
        self,
        section: DocumentSection,
        image_index: int,
    ) -> str:
        """
        Builds surrounding context using a token budget instead
        of a fixed number of paragraphs.
        """

        context = []

        total_tokens = 0

        left = image_index - 1
        right = image_index + 1

        while (
            total_tokens < self.max_context_tokens
            and (left >= 0 or right < len(section.elements))
        ):

            if left >= 0:

                element = section.elements[left]

                if (
                    element.element_type != ElementType.IMAGE
                    and element.text.strip()
                ):

                    text = f"[{element.element_type.value}]\n{element.text}"

                    tokens = count_tokens(text)

                    if total_tokens + tokens <= self.max_context_tokens:
                        context.insert(0, text)
                        total_tokens += tokens

                left -= 1

            if right < len(section.elements):

                element = section.elements[right]

                if (
                    element.element_type != ElementType.IMAGE
                    and element.text.strip()
                ):

                    text = f"[{element.element_type.value}]\n{element.text}"

                    tokens = count_tokens(text)

                    if total_tokens + tokens <= self.max_context_tokens:
                        context.append(text)
                        total_tokens += tokens

                right += 1

        return "\n\n".join(context)