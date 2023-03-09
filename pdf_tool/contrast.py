import os

import img2pdf
import pdf2image

from PIL import ImageEnhance, Image

from util import get_filename, get_file_directory

DEFAULT_DPI = 300
# DEFAULT_TILE_SIZE = (128, 128)
DEFAULT_TILE_SIZE = (64, 64)


def list_files(folder_path: str):

    return sorted(os.listdir(folder_path))


def pdf_to_images(pdf_path: str, output_folder: str, format: str = "jpeg", dpi: int = DEFAULT_DPI):
    filename = get_filename(pdf_path)

    pdf2image.convert_from_path(
        pdf_path, output_folder=output_folder, fmt=format, dpi=dpi, output_file=filename)

    files = [path for path in list_files(
        output_folder) if path.startswith(filename)]

    return [os.path.join(output_folder, path) for path in files]


def images_to_pdf(images_paths: list[str], output_path: str):
    images = [open(image, "rb") for image in images_paths]

    with open(output_path, "wb") as output_stream:
        img2pdf.convert(*images, outputstream=output_stream)


def change_image_contrast(image_path: str, contrast: float, tile_size: tuple[int, int] = DEFAULT_TILE_SIZE):

    with Image.open(image_path) as img:
        img_width, img_height = img.size
        enhanced_img = Image.new("RGB", (img_width, img_height))

        for i in range(0, img_height, tile_size[1]):
            for j in range(0, img_width, tile_size[0]):
                box = (j, i, j + tile_size[0], i + tile_size[1])
                tile = img.crop(box)
                enhancer = ImageEnhance.Contrast(tile)
                tile = enhancer.enhance(contrast)
                enhanced_img.paste(tile, box)

        enhanced_img.save(image_path)

        return image_path


def change_pdf_contrast(pdf_path: str, output_path: str, contrast: float):

    tmp_folder = os.path.join(get_file_directory(pdf_path), "tmp")

    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    images_paths = pdf_to_images(pdf_path=pdf_path, output_folder=tmp_folder)

    for image_path in images_paths:
        change_image_contrast(image_path=image_path, contrast=contrast)

    images_to_pdf(images_paths=images_paths, output_path=output_path)

    for image_path in images_paths:
        os.remove(image_path)

    os.rmdir(tmp_folder)


if __name__ == "__main__":
    input_file = "./pdfs/gray.pdf"
    output_file = "./pdfs/contrasted.pdf"

    change_pdf_contrast(
        pdf_path=input_file,
        output_path=output_file,
        contrast=3
    )
