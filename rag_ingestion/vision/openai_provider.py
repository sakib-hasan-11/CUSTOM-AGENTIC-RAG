import base64
import time
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


class OpenAIVisionProvider:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-mini",
    ):
        self.llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=0,
        )
        self.model_name=model

    @staticmethod
    def _encode_image(image_path: Path) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def summarize(
        self,
        image_path: Path,
        context: str | None = None,
    ) -> tuple[str, float]:
        image = self._encode_image(image_path)

        prompt = f"""
        You are analyzing an image extracted from a PDF.

        The surrounding text has already been extracted separately.

        Your job is NOT to repeat nearby paragraphs.

        Instead:

        - Describe information only visible in the image.
        - Explain diagrams, arrows, workflows and relationships.
        - Read text inside the image.
        - Explain tables and charts.
        - Expand abbreviations when possible.
        - Use the nearby context only to understand what the figure represents.
        - If the nearby text already explains something, avoid repeating it.


        Return concise Markdown with short paragraphs.
        Do not invent information.

        - what the figure represents
        - abbreviations
        - labels
        - arrows
        - relationships
        - tables
        - graphs
        - diagrams

        Do NOT repeat nearby paragraphs.

        Instead:

        - enrich them
        - explain visual relationships
        - explain hidden information

        Nearby Context

        {context}

        Return plain text only.
        """

        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                },
            ]
        )

        start = time.perf_counter()

        response = self.llm.invoke([message])

        latency = (time.perf_counter() - start) * 1000

        return response.content, latency
