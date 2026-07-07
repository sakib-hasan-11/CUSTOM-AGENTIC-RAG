import os
from pathlib import Path

from chunking.chunk_builder import ChunkBuilder
from embedding.openai_provider import OpenAIEmbeddingProvider
from embedding.processor import EmbeddingProcessor
from parsers.pdf_parser import PDFParser
from utils.markdown_renderer import MarkdownRenderer
from utils.pdf_splitter import PDFSplitter
from vision.openai_provider import OpenAIVisionProvider
from vision.processor import VisionProcessor
from dotenv import load_dotenv

load_dotenv()

def main():
    parser = PDFParser(image_output_dir=Path("artifacts/images"))

    builder = ChunkBuilder()

    vision = VisionProcessor(OpenAIVisionProvider(api_key=os.getenv("OPENAI_API_KEY")))

    renderer = MarkdownRenderer()

    embedder = EmbeddingProcessor(
        provider=OpenAIEmbeddingProvider(api_key=os.getenv("OPENAI_API_KEY")),
        renderer=renderer,
    )

    batches = PDFSplitter.split(
        Path("docs/sample.pdf"),
        document_id="doc_001",
    )

    for batch in batches:
        elements = parser.parse(batch)

        chunks = builder.build(elements)

        for chunk in chunks:
            chunk = vision.enrich(chunk)

            record = embedder.embed(chunk)

            print(record.id)
            print(len(record.values))
            print(record.metadata["text"][:300])
            return


if __name__ == "__main__":
    main()

# python -m tests.test_embedding