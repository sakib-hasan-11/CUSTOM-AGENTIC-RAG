from pathlib import Path
import logging
import os

from dotenv import load_dotenv

from parsers.pdf_parser import PDFParser

from chunking.section_builder import SectionBuilder
from chunking.chunk_builder import ChunkBuilder

from vision.processor import VisionProcessor
from vision.openai_provider import OpenAIVisionProvider

import shutil
import subprocess

logger = logging.getLogger(__name__)
from embedding.processor import EmbeddingProcessor
from embedding.openai_provider import OpenAIEmbeddingProvider

from utils.markdown_renderer import MarkdownRenderer
from utils.pdf_splitter import PDFSplitter

from vectorstore.pinecone_writer import PineconeWriter
from bootstrap import Bootstrap
load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(filename)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def validate_environment() -> None:
    """
    Validate that all required external dependencies are installed
    before the ingestion pipeline starts.
    Raises RuntimeError if anything is missing.
    """

    Bootstrap().run()

    logger.info("=" * 60)
    logger.info("Environment validation completed successfully.")
    logger.info("=" * 60)

class IngestionPipeline:

    def __init__(
        self,
        parser: PDFParser,
        section_builder: SectionBuilder,
        chunk_builder: ChunkBuilder,
        vision_processor: VisionProcessor,
        embedding_processor: EmbeddingProcessor,
        pinecone_writer: PineconeWriter,
        pages_per_batch: int = 100,
    ):
        self.parser = parser
        self.section_builder = section_builder
        self.chunk_builder = chunk_builder
        self.vision_processor = vision_processor
        self.embedding_processor = embedding_processor
        self.pinecone_writer = pinecone_writer
        self.pages_per_batch = pages_per_batch





    def ingest(
        self,
        pdf_path: Path,
        document_id: str,
    ) -> None:

        logger.info(
            "step=ingest_start file=%s document_id=%s",
            pdf_path.name,
            document_id,
        )

        for pdf_batch in PDFSplitter.split(
            pdf_path=pdf_path,
            document_id=document_id,
            pages_per_batch=self.pages_per_batch,
        ):
            try:
                logger.info(
                    "step=parse_batch file=%s batch=%s",
                    pdf_path.name,
                    pdf_batch,
                )
                elements = self.parser.parse(pdf_batch)

                logger.info(
                    "step=build_sections file=%s batch=%s",
                    pdf_path.name,
                    pdf_batch,
                )
                sections = self.section_builder.build(elements)

                for section in sections:
                    try:
                        logger.info(
                            "step=process_section file=%s section_id=%s",
                            pdf_path.name,
                            section.section_id,
                        )

                        enriched_section = self.vision_processor.enrich(section)

                        logger.info(
                            "step=chunk_section file=%s section_id=%s",
                            pdf_path.name,
                            section.section_id,
                        )
                        chunks = list(self.chunk_builder.build(enriched_section))

                        if not chunks:
                            logger.info(
                                "step=skip_empty_chunks file=%s section_id=%s",
                                pdf_path.name,
                                section.section_id,
                            )
                            continue

                        logger.info(
                            "step=embed_chunks file=%s section_id=%s chunk_count=%s",
                            pdf_path.name,
                            section.section_id,
                            len(chunks),
                        )
                        vectors = self.embedding_processor.embed_chunks(chunks)

                        logger.info(
                            "step=upsert_vectors file=%s section_id=%s vector_count=%s",
                            pdf_path.name,
                            section.section_id,
                            len(vectors),
                        )
                        self.pinecone_writer.upsert(vectors)
                    except Exception:
                        logger.exception(
                            "step=section_failed file=%s section_id=%s",
                            pdf_path.name,
                            getattr(section, "section_id", "unknown"),
                        )
                        raise
            except Exception:
                logger.exception(
                    "step=batch_failed file=%s batch=%s",
                    pdf_path.name,
                    pdf_batch,
                )
                raise

        logger.info(
            "step=ingest_complete file=%s document_id=%s",
            pdf_path.name,
            document_id,
        )



# Main


load_dotenv()


def main():

    logger.info("step=bootstrap_start file=%s", Path(__file__).name)

    validate_environment()

    pipeline = IngestionPipeline(

        parser=PDFParser(
            image_output_dir=Path("temp/images"),
        ),

        section_builder=SectionBuilder(),

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

    logger.info("step=bootstrap_complete file=%s", Path(__file__).name)


if __name__ == "__main__":
    main()