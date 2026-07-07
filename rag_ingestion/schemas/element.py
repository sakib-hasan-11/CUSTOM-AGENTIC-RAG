from dataclasses import dataclass
from typing import Any
from schemas.element_type import ElementType
from pathlib import Path

# BATCH META DATA
# stable schema for each pdf batch to store metadata.
@dataclass(slots=True) # python create internal dict to store this metadata which need large storage if we have lots of pdf. slot=true dont create this dict.
class PDFBatch:
    batch_path: Path
    original_pdf: Path
    start_page: int
    end_page: int
    document_id: str


# PAGE META DATA.
# in each batch there will be 100 pages this will create the shema to save the pages contenct .
@dataclass(slots=True)
class DocumentElement:
    element_id: str

    element_type: ElementType # Stores the content type like image,text,title perfectly from the schema 

    text: str

    metadata: dict[str, Any]

    # this one if for image summary store. for text it will none .
    enrichment:dict[str,Any] | None = None


