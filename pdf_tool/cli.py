import os

import click

from click_aliases import ClickAliasedGroup

from pdf_tool import util

from pdf_tool.exceptions import PdfReorganizeInvalidIndexesException
from pdf_tool.info import display_pdf_info
from pdf_tool.contrast import change_pdf_contrast
from pdf_tool.split import split_pdf_by_interval, split_pdf_by_ranges
from pdf_tool.reorganize import reorganize_pdf
from pdf_tool.cli_validators import validate_ranges, validate_order


@click.group(cls=ClickAliasedGroup)
@click.version_option("0.0.1", "--version", "-V", prog_name="pdf-tool")
def cli():
    """PDF editing tools."""
    pass


@cli.command(aliases=["i"], no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--output-json", "--json", is_flag=True, default=False, help="Output data as JSON instead of table.")
@click.help_option("-h", "--help")
def info(file, output_json):
    """Display PDF info.
    
    \b
    Ex:
      pdf-tool info file.pdf
      pdf-tool i --json file.pdf
    """
    display_pdf_info(file_path=file, output_json=output_json)


@cli.command(aliases=["cs"], no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--contrast", "-c", type=float, default=2, help="Contrast ratio. Defaults to 2.")
@click.option("--output", "-o", type=click.Path(exists=False, dir_okay=False), help="Output file. Defaults to '-contrasted' suffixed filename.")
@click.help_option("-h", "--help")
def contrast(file, output, contrast):
    """Increase PDF contrast.

    \b
    Contrast ratio notes:
    - 2 is often optimal, higher will not have much effect
    - 1 makes no changes
    - Lower than 1 brightens the PDF, but with artifacts
    
    \b
    Ex:
      pdf-tool contrast file.pdf
      pdf-tool contrast --contrast 1.5 file.pdf
      pdf-tool cs -c 1.8 -o new.pdf file.pdf
    """

    if output is None:
        output = util.append_suffix_to_filename(file, "-contrasted")

    change_pdf_contrast(pdf_path=file, output_path=output, contrast=contrast)


@cli.command(aliases=["sr"], no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("ranges", type=str, required=True, nargs=-1, callback=validate_ranges)
@click.option("--destination", "-d", type=click.Path(exists=False, dir_okay=True), help="Output directory. Defaults to a new directory named after the input filename.")
@click.option("--name", "-n", type=str, help="Output file name with '{i}' as split index. Defaults to the input filename with the split index.")
@click.help_option("-h", "--help")
def split_range(file, ranges, destination, name):
    """Split PDF pages by ranges.
    
    \b
    Ex:
      pdf-tool split-range file.pdf 1-2
      pdf-tool split-range --name "New file.pdf" file.pdf 1-2 3 4-6
      pdf-tool sr -d new/dir -n "New file {i}.pdf" file.pdf 1-10 5-6 11 3
    """

    if destination is None:
        destination = os.path.join(
            util.get_file_parent(file_path=file),
            util.get_filename(file_path=file)
        )

    if name is None:
        name = util.get_filename(file_path=file)

    if "{i}" not in name and len(ranges) > 1:
        name = name.strip() + " {i}"

    split_pdf_by_ranges(
        file_path=file, destination=destination, output_name=name, ranges=ranges)


@cli.command(aliases=["si"], no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--interval", "-i", type=int, default=1, help="Interval used to split PDF. Defaults to 1.")
@click.option("--destination", "-d", type=click.Path(exists=False, dir_okay=True), help="Output directory. Defaults to a new directory named after the input filename.")
@click.option("--name", "-n", type=str, help="Output file name with '{i}' as split index. Defaults to the input filename with the split index.")
@click.help_option("-h", "--help")
def split_interval(file, interval, destination, name):
    """Split PDF pages by interval.
    
    \b
    Ex:
      pdf-tool split-interval file.pdf
      pdf-tool split-interval --interval 3 --name "New file.pdf" file.pdf
      pdf-tool si -i 2 -d new/dir -n "New file {i}.pdf" file.pdf
    """

    if destination is None:
        destination = os.path.join(
            util.get_file_parent(file_path=file),
            util.get_filename(file_path=file)
        )

    if name is None:
        name = util.get_filename(file_path=file)

    if "{i}" not in name:
        name = name.strip() + " {i}"

    split_pdf_by_interval(
        file_path=file, destination=destination, output_name=name, interval=interval)


@cli.command(aliases=["r"], no_args_is_help=True)
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.argument("order", type=str, required=True, nargs=-1, callback=validate_order)
@click.option("--output", "-o", type=click.Path(exists=False, dir_okay=False), help="Output file. Defaults to '-reorganized' suffixed filename.")
@click.help_option("-h", "--help")
def reorganize(file, order, output):
    """Reorganize PDF pages.
    
    \b
    Ex:
      pdf-tool reorganize file.pdf 1 3 2 5
      pdf-tool reorganize --output new.pdf file.pdf 1 1 3 2
      pdf-tool r -o new.pdf file.pdf 1 2 1 2 8 5
    """

    if output is None:
        output = util.append_suffix_to_filename(file, "-reorganized")

    try:
        reorganize_pdf(file_path=file, destination=output, pages_order=order)
    except PdfReorganizeInvalidIndexesException as error:
        raise click.BadArgumentUsage(str(error))


if __name__ == "__main__":
    cli()
