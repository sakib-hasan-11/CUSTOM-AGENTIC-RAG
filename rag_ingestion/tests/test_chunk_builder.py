from pathlib import Path

from chunking.chunk_builder import ChunkBuilder
from parsers.pdf_parser import PDFParser
from utils.pdf_splitter import PDFSplitter


def main():

    parser = PDFParser(image_output_dir=Path("artifacts/images"))

    builder = ChunkBuilder()

    # 1. split into batches 
    batches = PDFSplitter.split(
        Path("docs/sample.pdf"),
        document_id="doc_001",
        pages_per_batch=100,
    )
    # loop over each 100 page batch .
    for batch in batches:
        elements = parser.parse(batch) # extract the content

        chunks = builder.build(elements) # make semantic chunk

        for chunk in chunks:
            print("=" * 80)
            print(chunk.chunk_id)

            for el in chunk.elements:
                if el.element_type.name == "IMAGE":
                    print("=" * 80)
                    print(el.metadata)


if __name__ == "__main__":
    main()

# python -m tests.test_chunk_builder