import click
from dotenv import load_dotenv
load_dotenv()
from importlib.metadata import version
from trazzo_tools.commands.create import create
from trazzo_tools.commands.export import export
from trazzo_tools.commands.view import view

from os import getenv
EXTENSION = getenv("EXTENSION")


help_main = f" [ CLI for managing .{EXTENSION.upper()} brush archives ] "
help_create = f"""Create a .{EXTENSION.upper()} archive from a brush definition.

    \b
    Generates:
      <output>/<name>.{EXTENSION.lower()}   Brush archive
    """
help_export = f"""Export .{EXTENSION.upper()} archive for Trazzo.
    
    \b
    Generates:
      <output>/<name>.json         Brush definition
      <output>/<name>_texture.png  Brush texture
      <output>/<name>_preview.png  Brush preview"""
help_view = f"""View .{EXTENSION.upper()} archive for Trazzo.
    
    \b
    Format: JSON
    """


@click.version_option(version=version("trazzo-tools"),prog_name="trazzo-tools", help="Show version number.")
@click.group(context_settings={"help_option_names": ["-h", "--help"]}, help=help_main)
def main(): pass

@main.command("create", help=help_create, epilog="Example: trazzo-tools create --data brush.json --preview preview.png --texture texture.png -o ./output")
@click.option("--data","-d", type=click.Path(exists=True, dir_okay=False),
    required=True,help="Path to JSON data file.")
@click.option("--preview","-p",type=click.Path(exists=True, dir_okay=False),
    required=True, help="Path to preview image.")
@click.option("--texture","-t", type=click.Path(exists=True, dir_okay=False),
    required=False, help="Path to texture image.")
@click.option("--output","-o", type=click.Path(dir_okay=True),
    required=False, default=".", help="Path to output. Default is current directory. File name is be brush name (no extension).")
def create_command(data: str, preview: str, texture: str = None, output: str = ".") -> None:
    create(data, preview, texture, output);


@main.command("export", help=help_export, epilog=f"Example: trazzo-tools export brush.{EXTENSION} --output ./output")
@click.argument("file", required=False, default=None, metavar="FILE")
@click.option("--output","-o", type=click.Path(dir_okay=True),
    required=False, default=".", help="Path to output. Default is current directory.")
def export_command(file: str, output: str):
    export(file, output)

@main.command("view", help=help_view, epilog=f"Example: trazzo-tools view brush.{EXTENSION}")
@click.argument("file", required=False, default=None, metavar="FILE")
@click.option("--output","-o", type=click.Path(dir_okay=True),
    required=False, default=".", help="Path to output. Default is current directory.")
def view_command(file: str, output: str):
    view(file, output)



if __name__ == "__main__":
    main()
