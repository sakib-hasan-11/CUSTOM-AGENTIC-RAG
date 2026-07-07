from schemas.element import DocumentElement
from schemas.element_type import ElementType
from unstructured.partition.pdf import partition_pdf
from utils.pdf_splitter import PDFBatch

CATEGORY_MAP = {
    "Title": ElementType.TITLE,
    "NarrativeText": ElementType.TEXT,
    "Image": ElementType.IMAGE,
    "Table": ElementType.TABLE,
    "FigureCaption": ElementType.CAPTION,
    "ListItem": ElementType.LIST,
    "Header": ElementType.HEADER,
    "Footer": ElementType.FOOTER,
}


class PDFParser:
    def __init__(self, image_output_dir):
        self.image_output_dir = image_output_dir

    def parse(
        self, batch: PDFBatch
    ):  # this will parse the content from 100 page batch .
        self.image_output_dir.mkdir(parents=True, exist_ok=True)

        elements = partition_pdf(
            filename=str(batch.batch_path),  # batch location
            strategy="hi_res",  # algorithm that will featch the content
            infer_table_structure=True,  # keep table structures in text format .
            extract_image_block_types=["Image"],  # separate images
            extract_image_block_output_dir=str(
                self.image_output_dir
            ),  # save images here .
            # chunking_strategy="by_title",
        )

        for idx, el in enumerate(elements):
            metadata = el.metadata.to_dict()

            # Keep original document information
            metadata["source_file"] = batch.original_pdf.name
            metadata["source_path"] = str(batch.original_pdf)
            metadata["document_id"] = batch.document_id

            # Adjust page number to match the original PDF
            page_number = metadata.get("page_number")
            if page_number is not None:
                metadata["page_number"] = metadata["page_number"] + batch.start_page - 1

            yield DocumentElement(
                element_id=f"element_{batch.start_page}_{idx}",
                element_type=CATEGORY_MAP.get(
                    el.category,
                    ElementType.UNKNOWN,
                ),
                text=el.text if el.text is not None else "",
                metadata=metadata,
            )
