import os
from pypdf import PdfReader
from bs4 import BeautifulSoup
import markdown


def read_pdf(file_path):
    """Read text from PDF."""

    text = ""

    reader = PdfReader(file_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def read_html(file_path):
    """Read text from HTML."""

    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    return soup.get_text(separator=" ")


def read_markdown(file_path):
    """Read text from Markdown."""

    with open(file_path, "r", encoding="utf-8") as file:
        html = markdown.markdown(file.read())

    soup = BeautifulSoup(html, "html.parser")

    return soup.get_text(separator=" ")


def load_document(file_path):
    """Automatically detect document type."""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    elif extension == ".html":
        return read_html(file_path)

    elif extension == ".md":
        return read_markdown(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")