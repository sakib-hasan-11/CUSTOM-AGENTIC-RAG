from enum import Enum # prevent typo mismatch issue .

# PAGE CONTENT SCHEMA.
# page metadata schema for each page objects like image,title,paragraph . 
# telling unstructure to store in this schema for all pdf.

class ElementType(str, Enum):
    TITLE = "Title"

    TEXT = "NarrativeText"

    IMAGE = "Image"

    TABLE = "Table"

    CAPTION = "FigureCaption"

    LIST = "ListItem"

    HEADER = "Header"

    FOOTER = "Footer"

    UNKNOWN = "Unknown"
