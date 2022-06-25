import os

WINDOW_TITLE = "JPEG-MetaFilter"
SELECT_FOLDER = "Folder containing JPEGs to filter"
INVALID_DIR = "Select a valid directory"
NO_IMAGES_IN_DIR = "No images found in the directory"
SEARCH_BUTTON_TEXT_ANY = "Search files with ANY of these tags"
SEARCH_BUTTON_TEXT_ALL = "Search files with ALL of these tags"
FILTER_BY_TAGS_BUTTON_TEXT = "Filter by tags"

TMP_DIR = ".tmp_JPEG-MetaFilter"

ACCEPTED_EXTENSIONS = (".jpg", ".jpeg")

OPENING_META_TAG = b"<x:xmpmeta xmlns:x=\"adobe:ns:meta/\">"
CLOSE_META_TAG = b"</x:xmpmeta>"
FIRST_LI_OPEN = b"<rdf:li>"
FIRST_LI_CLOSE = b"</rdf:li>"

LOGO_PATH = os.path.join("UI", "JPEG-MetaFilter-logo.ico")
if not os.path.isfile(LOGO_PATH):
    LOGO_PATH = os.path.join("..", LOGO_PATH)