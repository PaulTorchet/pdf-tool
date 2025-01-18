import os

from typing import Any, Dict, Optional

from pathlib import Path

from PyPDF2 import PdfWriter


def get_filename(file_path: str, with_extension: bool = False) -> str:
    """Get file name.

    Args:
        file_path (str): File path.
        with_extension (bool): Flag to include extension.

    Returns:
        str: File name.
    """
    if with_extension:
        return Path(file_path).name

    return Path(file_path).name.split(".")[0]


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


def get_file_size(file_path: str) -> Dict[str, float]:
    """Return a dictionary with file size in bytes, Mb and Kb.

    Args:
        file_path (str): File path.

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


def reorganize_array(array: list, order: list) -> str:
    """Reorganize an array with a list of indexes.

    Args:
        array (list): Array to reorganize
        order (list): List of indexes.

    Returns:
        str: Reorganized array.
    """
    organized_array = []

    for index in order:
        organized_array.append(array[index - 1])

    return organized_array


def write_pdf(pdf_writer: PdfWriter, output_path: str, metadata):
    custom_metadata = {
        "/Producer": "PDF-Tool by PaulTorchet",
        "/Author": "PDF-Tool by PaulTorchet",
        "/Title": get_filename(output_path),
    }

    if metadata is None:
        output_metadata = custom_metadata
    else:
        output_metadata = {**metadata, **custom_metadata}

    pdf_writer.add_metadata(output_metadata)

    with open(output_path, "wb") as file:
        pdf_writer.write(file)
