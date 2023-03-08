from PyPDF2 import PdfReader, PdfWriter


def compress_pdf(file_path: str, output: str):
    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    compress_pdf("pdfs/bol.pdf", "pdfs/compressed.pdf")
