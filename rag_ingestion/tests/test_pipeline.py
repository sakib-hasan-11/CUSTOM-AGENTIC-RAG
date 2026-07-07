import os
from pathlib import Path

from chunking.chunk_builder import ChunkBuilder
from dotenv import load_dotenv
from embedding.openai_provider import OpenAIEmbeddingProvider
from embedding.processor import EmbeddingProcessor
from main import IngestionPipeline
from parsers.pdf_parser import PDFParser
from utils.markdown_renderer import MarkdownRenderer
from vectorstore.pinecone_writer import PineconeWriter
from vision.openai_provider import OpenAIVisionProvider
from vision.processor import VisionProcessor

load_dotenv()


def main():
    pipeline = IngestionPipeline(
        parser=PDFParser(
            image_output_dir=Path("temp/images"),
        ),
        chunk_builder=ChunkBuilder(),
        vision_processor=VisionProcessor(
            OpenAIVisionProvider(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        ),
        embedding_processor=EmbeddingProcessor(
            provider=OpenAIEmbeddingProvider(
                api_key=os.getenv("OPENAI_API_KEY"),
            ),
            renderer=MarkdownRenderer(),
        ),
        pinecone_writer=PineconeWriter(
            api_key=os.getenv("PINECONE_API"),
            index_name=os.getenv("INDEX_NAME"),
        ),
    )

    pipeline.ingest(
        pdf_path=Path("docs/sample.pdf"),
        document_id="doc_001",
    )


if __name__ == "__main__":
    main()


# python -m tests.test_pipeline
