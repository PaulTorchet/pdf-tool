from typing import Any, Dict

import json

from rich import print
from rich.table import Table

from pdf_tool.util import get_filename, get_file_size, read_pdf


def get_pdf_info(file_path: str) -> Dict[str, Any]:
    pdf = read_pdf(file_path)

    info = {
        "pages_count": len(pdf.pages),
        "file_name": get_filename(file_path, with_extension=True),
        "pdf_title": pdf.metadata.title,
        "size": get_file_size(file_path),
        "author": pdf.metadata.author,
    }

    return info


def print_info_table(pdf_info: Dict[str, Any]) -> None:
    table = Table()

    table.add_column("Property")
    table.add_column("Value")

    table.add_row("File name", pdf_info["file_name"])
    table.add_row("PDF title", pdf_info.get("pdf_title") or "-")
    table.add_row(
        "Pages count",
        f"{pdf_info['pages_count']} page{'s' if pdf_info['pages_count'] > 1 else ''}",
    )
    table.add_row("File size", f"{pdf_info['size']['megabytes']} Mb")
    table.add_row("Author", f"{pdf_info.get('author') or '-'}")
    table.add_row("Creat. date", f"{pdf_info.get('creation_date') or '-'}")
    table.add_row("Modif. date", f"{pdf_info.get('modification_date') or '-'}")

    print(table)


def display_pdf_info(file_path: str, output_json: bool = False) -> None:
    pdf_info = get_pdf_info(file_path=file_path)

    if output_json:
        print(json.dumps(pdf_info))
    else:
        print_info_table(pdf_info)


if __name__ == "__main__":
    display_pdf_info(file_path="pdfs/Oblivion.PDF", output_json=True)
    display_pdf_info(file_path="pdfs/Oblivion.PDF", output_json=False)
