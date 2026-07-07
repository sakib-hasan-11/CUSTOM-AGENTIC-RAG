import os
from pathlib import Path

from chunking.chunk_builder import ChunkBuilder
from parsers.pdf_parser import PDFParser
from utils.pdf_splitter import PDFSplitter
from vision.openai_provider import OpenAIVisionProvider
from vision.processor import VisionProcessor
from dotenv import load_dotenv
load_dotenv()

def main():
    parser = PDFParser(image_output_dir=Path("artifacts/images"))

    builder = ChunkBuilder()

    provider = OpenAIVisionProvider(api_key=os.getenv("OPENAI_API_KEY"))

    vision = VisionProcessor(provider)

    batches = PDFSplitter.split(
        Path("docs/sample.pdf"),
        document_id="doc_001",
    )

    for batch in batches:
        elements = parser.parse(batch)

        chunks = builder.build(elements)

        for chunk in chunks:
            chunk = vision.enrich(chunk)

            for element in chunk.elements:
                if element.enrichment:
                    print("=" * 80)

                    print(element.enrichment["vision_summary"])

                    return


if __name__ == "__main__":
    main()

# python -m tests.test_vission