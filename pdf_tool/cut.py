# filename, direction, ratio, pages to keep (1, 2L, 3R) or (R, L)

from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from typing import Tuple

from PyPDF2 import PageObject

from pdf_tool.util import read_pdf, write_pdf


@dataclass
class AngleProperties:

    width: str

    left: str
    right: str

    height: str

    top: str
    bottom: str

    positive_ratio: bool


ANGLES_PROPERTIES = {
    0: AngleProperties(
        width="width",
        left="left",
        right="right",
        height="height",
        top="top",
        bottom="bottom",
        positive_ratio=True,
    ),
    90: AngleProperties(
        width="height",
        left="bottom",
        right="top",
        height="width",
        top="left",
        bottom="right",
        positive_ratio=True,
    ),
    180: AngleProperties(
        width="width",
        left="right",
        right="left",
        height="height",
        top="top",
        bottom="bottom",
        positive_ratio=False,
    ),
    270: AngleProperties(
        width="height",
        left="top",
        right="bottom",
        height="width",
        top="right",
        bottom="left",
        positive_ratio=False,
    ),
}


class CutDirection(Enum):

    VERTICALLY = auto()
    HORIZONTALLY = auto()


def cut_page_vertically(
    page: PageObject, ratio: float
) -> Tuple[PageObject, PageObject]:
    properties = ANGLES_PROPERTIES[page.rotation]

    width: Decimal = getattr(page.cropbox, properties.width)

    middle_width = (
        width * Decimal(ratio)
        if properties.positive_ratio
        else width * (1 - Decimal(ratio))
    )

    left = deepcopy(page)
    setattr(left.cropbox, properties.right, middle_width)

    right = deepcopy(page)
    setattr(right.cropbox, properties.left, middle_width)

    return left, right


def cut_page_horizontally(
    page: PageObject, ratio: float
) -> Tuple[PageObject, PageObject]:
    properties = ANGLES_PROPERTIES[page.rotation]

    height: Decimal = getattr(page.cropbox, properties.height)

    middle_height = (
        height * Decimal(ratio)
        if properties.positive_ratio
        else height * (1 - Decimal(ratio))
    )

    top = deepcopy(page)
    setattr(top.cropbox, properties.bottom, middle_height)

    bottom = deepcopy(page)
    setattr(bottom.cropbox, properties.top, middle_height)

    return top, bottom


def cut_page(
    page: PageObject, ratio: float, direction: CutDirection
) -> Tuple[PageObject, PageObject]:
    if direction == CutDirection.VERTICALLY:
        return cut_page_vertically(page=page, ratio=ratio)
    elif direction == CutDirection.HORIZONTALLY:
        return cut_page_horizontally(page=page, ratio=ratio)

    else:
        raise NotImplementedError


def cut_pdf(
    file_path: str, destination: str, ratio: float, direction: CutDirection
) -> None:
    pdf = read_pdf(file_path=file_path)

    result = []

    for page in pdf.pages:
        result.extend(cut_page(page=page, ratio=ratio, direction=direction))

    write_pdf(pages=result, output_path=destination, metadatas=pdf.metadata)


if __name__ == "__main__":
    ratio = 0.75

    path = "pdfs/genevieve_chorus.pdf"
    output = "pdfs/genevieve_chorus-cut.pdf"
    path = "pdfs/bol.pdf"
    output = "pdfs/bol-cut.pdf"

    cut_pdf(
        file_path=path,
        destination=output,
        ratio=ratio,
        direction=CutDirection.VERTICALLY,
    )

    # pdf = read_pdf(file_path=path)

    # # new_pages = [get_right_side(page=page, ratio=ratio) for page in pdf.pages]

    # cut_pages = []

    # for page in pdf.pages:
    #     cut_pages.extend(cut_page_horizontally(page=page, ratio=ratio))
    #     # cut_pages.append(get_left_side(page=page, ratio=ratio))
    #     # cut_pages.append(get_right_side(page=page, ratio=ratio))

    # write_pdf(pages=cut_pages, output_path=output, metadatas=pdf.metadata)
