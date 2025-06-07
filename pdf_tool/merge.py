"""PDF Merging submodule."""

from pdf_tool.util import merge_arrays, read_pdf, write_pdf


def merge_pdfs(file_paths: list[str], destination: str) -> None:
    first_pdf = read_pdf(file_path=file_paths[0])

    pdfs = [read_pdf(file_path=file_path) for file_path in file_paths]

    merged_pages = merge_arrays(arrays=[pdf.pages for pdf in pdfs])

    write_pdf(pages=merged_pages, output_path=destination, metadatas=first_pdf.metadata)
