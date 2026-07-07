import os
from pathlib import Path

from chunking.chunk_builder import ChunkBuilder
from dotenv import load_dotenv
from parsers.pdf_parser import PDFParser
from utils.markdown_renderer import MarkdownRenderer
from utils.pdf_splitter import PDFSplitter
from vision.openai_provider import OpenAIVisionProvider
from vision.processor import VisionProcessor

load_dotenv()

def main():
    parser = PDFParser(image_output_dir=Path("artifacts/images"))

    builder = ChunkBuilder()

    renderer = MarkdownRenderer()

    vision = VisionProcessor(OpenAIVisionProvider(api_key=os.getenv("OPENAI_API_KEY")))

    batches = PDFSplitter.split(
        Path("docs/sample.pdf"),
        document_id="doc_001",
    )

    for batch in batches:
        elements = parser.parse(batch)

        chunks = builder.build(elements)

        for chunk in chunks:
            chunk = vision.enrich(chunk)

            markdown = renderer.render(chunk)

            print("=" * 100)
            print(chunk.chunk_id)
            print(markdown)

            
    
    


if __name__ == "__main__":
    main()

# python -m tests.test_render
