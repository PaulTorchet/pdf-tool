"""PDF Rotation submodule."""

# filename, direction, ratio, pages to keep (1, 2L, 3R) or (R, L)

# ruff: noqa: T201

from copy import copy

from PyPDF2 import PageObject

from pdf_tool.util import read_pdf, write_pdf


def manipulate_page(page: PageObject) -> PageObject:
    print(page.cropbox)
    print(page.rotation)

    copied_page = copy(page)

    # width = copied_page.cropbox.right
    # copied_page.cropbox.right = width / 2
    copied_page.rotate(-copied_page.rotation)

    print(copied_page.rotation)

    return copied_page


if __name__ == "__main__":
    path = "pdfs/bol-rotated.pdf"
    output = "pdfs/bol-cut.pdf"

    pdf = read_pdf(file_path=path)

    new_pages = [manipulate_page(page=page) for page in pdf.pages]

    write_pdf(pages=new_pages, output_path=output, metadatas=pdf.metadata)
