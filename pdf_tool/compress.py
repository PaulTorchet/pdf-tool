from pdf_tool.util import read_pdf, write_pdf


def compress_pdf(file_path: str, output: str):
    pdf = read_pdf(file_path)

    for page in pdf.pages:
        page.compress_content_streams()  # This is CPU intensive!

    write_pdf(pages=pdf.pages, output_path=output, metadatas=pdf.metadata)


if __name__ == "__main__":
    compress_pdf("pdfs/gray.pdf", "pdfs/compressed.pdf")
