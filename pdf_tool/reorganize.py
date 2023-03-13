from typing import List

from click.exceptions import BadArgumentUsage

from PyPDF2 import PdfReader, PdfWriter

from pdf_tool.util import reorganize_array


def reorganize_pdf(file_path: str, destination: str, pages_order: List[int]):
    pdf = PdfReader(file_path)

    pages_count = len(pdf.pages)

    if max(pages_order) > pages_count or min(pages_order) < 1:
        raise BadArgumentUsage(f"Indexes must be between 1 and {pages_count}.")

    reorganized_pages = reorganize_array(pdf.pages, order=pages_order)

    writer = PdfWriter()

    for page in reorganized_pages:
        writer.add_page(page)

    writer.add_metadata(pdf.metadata)

    with open(destination, "wb") as output_pdf:
        writer.write(output_pdf)
