import click
from click_aliases import ClickAliasedGroup

from pdf_tool.info import display_pdf_info


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


if __name__ == "__main__":
    cli()
