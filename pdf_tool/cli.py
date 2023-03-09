import click
from click_aliases import ClickAliasedGroup

from pdf_tool.info import display_pdf_info
from pdf_tool.contrast import change_pdf_contrast

from pdf_tool import util


@click.group(cls=ClickAliasedGroup)
@click.version_option(prog_name="pdf-tool")
def cli():
    """CLI with pdf tools."""
    pass


@cli.command(aliases=["i"])
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--output-json", "--json", is_flag=True, default=False, help="Output data as JSON instead of table.")
def info(file, output_json):
    """Display PDF info."""
    display_pdf_info(file_path=file, output_json=output_json)


@cli.command(aliases=["cs"])
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", type=click.Path(exists=False, dir_okay=False), help="Output file.")
@click.option("--contrast", "-c", type=float, default=2, help="Contrast ratio. Default to 2.")
def contrast(file, output, contrast):
    """Increase PDF contrast."""

    if output is None:
        output = util.append_suffix_to_filename(file, "-contrasted")

    change_pdf_contrast(pdf_path=file, output_path=output, contrast=contrast)


if __name__ == "__main__":
    cli()
