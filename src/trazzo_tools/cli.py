import click
from dotenv import load_dotenv
load_dotenv()
from importlib.metadata import version
from trazzo_tools.commands.create import create
from trazzo_tools.commands.export import export
from trazzo_tools.commands.view import view
from trazzo_tools.commands.edit import edit

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
help_view = f"""View .{EXTENSION.upper()} archive for Trazzo."""
help_edit = f"""Edit .{EXTENSION.upper()} file metadata and brush parameters.

    \b
    Without flags: opens interactive visual editor.
    With flags: directly updates the specified fields and saves.
    """


@click.version_option(version=version("trazzo-tools"),prog_name="trazzo-tools", help="Show version number.")
@click.group(context_settings={"help_option_names": ["-h", "--help"]}, help=help_main)
def main(): pass

@main.command("create", help=help_create, epilog="Example: trazzo-tools create --data brush.json --preview preview.png [--texture texture.png] [--output ./output]")
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


@main.command("export", help=help_export, epilog=f"Example: trazzo-tools export brush.{EXTENSION} [--output ./output]")
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

@main.command("edit", help=help_edit, epilog=f"Example: trazzo-tools edit brush.{EXTENSION}")
@click.argument("file", metavar="FILE")
# Brush info
@click.option("--name",                   default=None,              help="Brush name")
@click.option("--author",                 default=None,              help="Author")
@click.option("--engine",                 default=None,              help="Engine (e.g. pixel)")
@click.option("--category",               default=None,              help="Category (e.g. pen)")
# Params
@click.option("--radius",                 default=None, type=float,  help="Radius")
@click.option("--opacity",                default=None, type=float,  help="Opacity (0.0–1.0)")
@click.option("--hardness",               default=None, type=float,  help="Hardness (0.0–1.0)")
@click.option("--spacing",                default=None, type=float,  help="Spacing")
@click.option("--flow",                   default=None, type=float,  help="Flow (0.0–1.0)")
@click.option("--jitter",                 default=None, type=float,  help="Jitter")
@click.option("--rotation",               default=None, type=float,  help="Rotation (degrees)")
@click.option("--elliptical-ratio",       default=None, type=float,  help="Elliptical ratio")
@click.option("--elliptical-angle",       default=None, type=float,  help="Elliptical angle")
# Modifiers
@click.option("--eraser/--no-eraser",     default=None,              help="Eraser mode")
@click.option("--blend-mode",             default=None,              help="Blend mode (e.g. normal)")
@click.option("--random-rotation",        default=None, type=float,  help="Random rotation")
@click.option("--random-zoom",          default=None, type=float,  help="Random zoom")
@click.option("--size-pressure/--no-size-pressure",     default=None, help="Size pressure")
@click.option("--opacity-pressure/--no-opacity-pressure", default=None, help="Opacity pressure")
def edit_command(file: str, **kwargs):
    has_flag = any(v is not None for v in kwargs.values())
    edit(file, not has_flag, **kwargs)

if __name__ == "__main__":
    main()
