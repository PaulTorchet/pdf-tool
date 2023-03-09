import os


def get_filename(file_path: str, include_extension: bool = False) -> str:
    """Get file name without path nor extension.

    Args:
        file_path (str): File path.

    Returns:
        str: File name.
    """
    filename = file_path.split(os.path.sep)[-1]

    if not include_extension:
        filename = filename.split(".")[0]

    return filename


def get_file_directory(file_path: str) -> str:
    return os.path.dirname(file_path)


def append_suffix_to_filename(file_path: str, suffix) -> str:
    new_filename = get_filename(file_path) + suffix + ".pdf"
    directory = get_file_directory(
        file_path)

    return os.path.join(directory, new_filename)


def get_file_size(file_path: str):
    b_size = os.stat(file_path).st_size

    kb_size = b_size / 1024
    mb_size = kb_size / 1024

    return {
        "bytes": round(b_size, 2),
        "kilobytes": round(kb_size, 2),
        "megabytes": round(mb_size, 2),
    }


if __name__ == "__main__":
    print(append_suffix_to_filename("pdfs/Oblivion.PDF", "-compressed"))
