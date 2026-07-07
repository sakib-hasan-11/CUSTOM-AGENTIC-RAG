from pathlib import Path
from uuid import uuid4

from parsers.pdf_parser import PDFParser
from utils.pdf_splitter import PDFSplitter


def main():
    pdf_path = Path("docs/sample.pdf")

    document_id = str(uuid4())

    parser = PDFParser(image_output_dir=Path("artifacts/images"))

    splitter = PDFSplitter()

    total_elements = 0

    for batch in splitter.split(
        pdf_path=pdf_path,
        document_id=document_id,
        pages_per_batch=100,
    ):
        print("\n" + "=" * 80)
        print(f"Processing Pages {batch.start_page}-{batch.end_page}")
        print("=" * 80)

        batch_count = 0

        for element in parser.parse(batch):
            batch_count += 1
            total_elements += 1

            print(f"\nElement ID : {element.element_id}")
            print(f"Type       : {element.element_type}")
            print(f"Page       : {element.metadata.get('page_number')}")
            print(f"Document   : {element.metadata.get('document_id')}")
            print(f"Source     : {element.metadata.get('source_file')}")
            print(f"Text       : {element.text[:150]}")

        print(f"\nBatch Elements : {batch_count}")

        # Optional: remove the temporary PDF after processing
        batch.batch_path.unlink(missing_ok=True)

    print("\n" + "=" * 80)
    print(f"Total Elements Parsed : {total_elements}")
    print("=" * 80)


if __name__ == "__main__":
    main()

# python -m tests.test1