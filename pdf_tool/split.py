import os

from PyPDF2 import PdfReader, PdfWriter, PageObject

from util import get_filename


def split_array_by_interval(array: list, interval: int) -> list[list]:
    """Split an array by interval.

    Args:
        array (list): Array to split.
        interval (int): Size of the chunks.

    Returns:
        list[list]: List of splitted chunks.
    """
    splitted_array = []

    for i in range(0, len(array), interval):
        splitted_array.append(array[i:i+interval])

    return splitted_array


def split_array_by_ranges(array: list, ranges: list[tuple]) -> list[list]:
    """Split an array by ranges.

    Args:
        array (list): List to split.
        ranges (list[tuple]): Ranges as list of tuples (end, start).

    Returns:
        list[list]: List of splitted chunks.
    """
    splitted_array = []

    for start, end in ranges:
        sub_array = array[start - 1:end]
        if sub_array:
            splitted_array.append(sub_array)

    return splitted_array


def write_pdf_chunks(pdf_chunks: list, destination: str, filename: str):

    if not os.path.exists(destination):
        os.makedirs(destination)

    for index, chunk in enumerate(pdf_chunks):
        writer = PdfWriter()

        chunk_name = filename.strip() + " " + str(index + 1) + ".pdf"

        for page in chunk:
            writer.add_page(page)

        with open(os.path.join(destination, chunk_name), "wb") as output_pdf:
            writer.write(output_pdf)


def split_pdf_by_interval(file_path: str, destination: str, output_name: str, interval: int):
    pdf = PdfReader(file_path)

    pdf_chunks = split_array_by_interval(array=pdf.pages, interval=interval)

    write_pdf_chunks(
        pdf_chunks=pdf_chunks,
        destination=destination,
        filename=output_name
    )


def split_pdf_by_ranges(file_path: str, destination: str, output_name: str, ranges: list[tuple]):
    pdf = PdfReader(file_path)

    pdf_chunks = split_array_by_ranges(array=pdf.pages, ranges=ranges)

    write_pdf_chunks(
        pdf_chunks=pdf_chunks,
        destination=destination,
        filename=output_name
    )


if __name__ == "__main__":
    # split_pdf_by_interval(
    #     file_path="pdfs/bol.pdf",
    #     destination="pdfs/Best Of Lady Gaga",
    #     output_name="Best Of Lady Gaga - Trompette",
    #     interval=2
    # )
    split_pdf_by_ranges(
        file_path="pdfs/bol.pdf",
        destination="pdfs/Best Of Lady Gaga",
        output_name="Best Of Lady Gaga - Trompette",
        ranges=[(1, 2), (3, 4), (5, 6)]
    )
