from pathlib import Path

from pypdf import PdfReader, PdfWriter
from schemas.element import PDFBatch


class PDFSplitter:
    @staticmethod
    def split(
        pdf_path: Path,
        document_id: str = "NOT GIVEN",  # unique string id for each document.
        pages_per_batch: int = 100,
    ):
        reader = PdfReader(pdf_path)  # read the pdf .
        total_pages = len(reader.pages)

        temp_dir = Path("temp/temp_batches")  # create a temp folder to store the pages.
        temp_dir.mkdir(exist_ok=True,parents=True)

        for start in range(
            0, total_pages, pages_per_batch
        ):  # read 100 pages at a time .
            writer = PdfWriter()  # emply pdf object .

            end = min(start + pages_per_batch, total_pages)

            for page in range(start, end):
                writer.add_page(
                    reader.pages[page]
                )  # add 100 pages in the empy pdf object .

            temp_file = (
                temp_dir / f"{pdf_path.stem}_{start + 1}_{end}.pdf"
            )  # add this batch into the temp folder

            with open(temp_file, "wb") as f:
                writer.write(f)

            # using the schema for consitant same metadata structure .
            yield PDFBatch(  # store one pdf at a time . then delete the previous one after new batch added.
                batch_path=temp_file,
                original_pdf=pdf_path,
                start_page=start + 1,
                end_page=end,
                document_id=document_id,
            )
