"""Utilities submodule."""

import itertools
import os
from pathlib import Path
from typing import Any

from PyPDF2 import PageObject, PdfReader, PdfWriter


def get_filename(file_path: str, *, with_extension: bool = False) -> str:
    """Get file name.

    Args:
        file_path (str): File path.
        with_extension (bool): Flag to include extension.

    Returns:
        str: File name.
    """
    if with_extension:
        return Path(file_path).name

    return Path(file_path).stem


def get_file_extension(file_path: str) -> str:
    """Get file extension.

    Ex: path/to/file.ext -> .ext
    Ex: path/to/file.ext.exp -> .ext.exp

    Args:
        file_path (str): File path.

    Returns:
        str: File extension.
    """
    return "".join(Path(file_path).suffixes)


def get_file_parent(file_path: str) -> str:
    """Get file parent.

    Ex: path/to/file.ext -> path/to

    Args:
        file_path (str): File path.

    Returns:
        str: File parent.
    """
    return Path(file_path).parent


def append_suffix_to_filename(file_path: str, suffix: str) -> str:
    """Append a suffix to a filename.

    Ex: path/to/file.ext + -suffix -> path/to/file-suffix.ext

    Args:
        file_path (str): File path.
        suffix (str): Suffix to append.

    Returns:
        str: Path with suffixed filename.
    """
    parent = get_file_parent(file_path=file_path)
    filename = get_filename(file_path=file_path)
    extension = get_file_extension(file_path=file_path)

    new_filename = filename + suffix + extension

    return os.path.join(parent, new_filename)


def get_file_size(file_path: str) -> dict[str, float]:
    """Return a dictionary with file size in bytes, Mb and Kb.

    Returns:
        Dict[str, float]: Dictionary with file sizes.
    """
    b_size = os.stat(file_path).st_size

    kb_size = b_size / 1024
    mb_size = kb_size / 1024

    return {
        "bytes": round(b_size, 2),
        "kilobytes": round(kb_size, 2),
        "megabytes": round(mb_size, 2),
    }


def reorganize_array(array: list, order: list[int]) -> str:
    """Reorganize an array with a list of indexes.

    Args:
        array (list): Array to reorganize
        order (list[int]): List of indexes.

    Returns:
        str: Reorganized array.
    """
    organized_array = []

    for index in order:
        organized_array.append(array[index - 1])

    return organized_array


def merge_arrays(arrays: list[list]) -> list:
    """Merge multiple arrays.

    Args:
        arrays (list[list]): Arrays to merge

    Returns:
        list: Merged arrays in one.
    """
    return list(itertools.chain(*arrays))


def sanitize_metadatas(metadatas: dict[str, Any]) -> dict[str, str]:
    """Transform metadatas dictionary values to strings.

    Args:
        metadatas (Dict[str, Any]): Input metadatas dictionary.

    Returns:
        Dict[str, str]: Sanitized metadatas dictionary.
    """
    return {key: str(value) for key, value in metadatas.items()}


def read_pdf(file_path: str) -> PdfReader:
    """Read a PDF file.

    Args:
        file_path (str): PDF file path.

    Returns:
        PdfReader: PdfReader object.
    """
    return PdfReader(file_path)


def write_pdf(
    pages: list[PageObject],
    output_path: str,
    metadatas: dict[str, Any] | None = None,
) -> None:
    """Write a PDF file.

    Args:
        pages (List[PageObject]): List of PDF PageObjects to write.
        output_path (str): PDF file output path.
        metadatas (Dict[str, Any], optional): PDF metadatas. Defaults to None.
    """
    custom_metadatas = {
        "/Producer": "PDF-Tool by PaulTorchet",
        "/Author": "PDF-Tool by PaulTorchet",
        "/Title": get_filename(output_path),
    }

    output_metadata = sanitize_metadatas(metadatas=metadatas) if metadatas else {}

    output_metadata.update(custom_metadatas)

    writer = PdfWriter()

    for page in pages:
        writer.add_page(page=page)

    writer.add_metadata(output_metadata)

    with open(output_path, "wb") as file:
        writer.write(file)
