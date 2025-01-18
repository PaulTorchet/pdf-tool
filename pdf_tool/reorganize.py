from typing import List

from PyPDF2 import PdfReader, PdfWriter

from pdf_tool.exceptions import PdfReorganizeInvalidIndexesException
from pdf_tool.util import reorganize_array, write_pdf


def reorganize_pdf(file_path: str, destination: str, pages_order: List[int]):
    pdf = PdfReader(file_path)

    pages_count = len(pdf.pages)

    if max(pages_order) > pages_count or min(pages_order) < 1:
        raise PdfReorganizeInvalidIndexesException(
            f"Indexes must be between 1 and {pages_count}."
        )

    reorganized_pages = reorganize_array(pdf.pages, order=pages_order)

    writer = PdfWriter()

    for page in reorganized_pages:
        writer.add_page(page)

    write_pdf(pdf_writer=writer, output_path=destination, metadatas=pdf.metadata)
