import json

from rich import print
from rich.table import Table

from PyPDF2 import PdfReader
from pdf_tool import util


def get_pdf_info(file_path: str):
    pdf = PdfReader(file_path)

    info = {
        "pages_count": len(pdf.pages),
        "file_name": util.get_filename(file_path, include_extension=True),
        "pdf_title": pdf.metadata.title,
        "size": util.get_file_size(file_path),
        "author": pdf.metadata.author
    }

    return info


def print_info_table(pdf_info):
    table = Table()

    table.add_column("Property")
    table.add_column("Value")

    table.add_row("File name", pdf_info["file_name"])
    table.add_row("PDF title", pdf_info["pdf_title"])
    table.add_row(
        "Pages count", f"{pdf_info['pages_count']} page{'s' if pdf_info['pages_count'] > 1 else None}")
    table.add_row("File size", f"{pdf_info['size']['megabytes']} Mb")

    print(table)


def display_pdf_info(file_path: str, output_json: bool = False):
    pdf_info = get_pdf_info(file_path=file_path)

    if output_json:
        print(json.dumps(pdf_info))
    else:
        print_info_table(pdf_info)


if __name__ == "__main__":
    display_pdf_info("pdfs/Oblivion.PDF", True)
