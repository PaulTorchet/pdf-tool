
from pdf_tool.exceptions import PdfReorganizeInvalidIndexesException
from pdf_tool.util import read_pdf, reorganize_array, write_pdf


def reorganize_pdf(file_path: str, destination: str, pages_order: list[int]):
    pdf = read_pdf(file_path)

    pages_count = len(pdf.pages)

    if max(pages_order) > pages_count or min(pages_order) < 1:
        raise PdfReorganizeInvalidIndexesException(
            f"Indexes must be between 1 and {pages_count}."
        )

    reorganized_pages = reorganize_array(pdf.pages, order=pages_order)

    write_pdf(pages=reorganized_pages, output_path=destination, metadatas=pdf.metadata)
