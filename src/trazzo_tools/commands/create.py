import click
from trazzo_tools.classes.classes import TzBrush
import trazzo_tools.classes.dbClasses as dbClasses
from datetime import datetime
import os
EXTENSION = os.getenv("EXTENSION")

def create(data: str, preview: str, texture: str = None, output: str = ".") -> None:
    path = output or "."
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    brush_data = TzBrush.from_json(data)
    name = brush_data.name

    if os.path.exists(os.path.join(path, f"{name}.{EXTENSION}")):
        click.echo(f"Brush {name} already exists")
        return

    dbClasses.init_db(os.path.join(path, name))
    brush = dbClasses.Brush.create(
        name=name,
        author=brush_data.author,
        engine=brush_data.engine,
        category=brush_data.category,
        format=brush_data.format,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    dbClasses.TzbMeta.create(brush=brush, key="author", value=brush_data.author)
    dbClasses.TzbMeta.create(brush=brush, key="format", value=brush_data.format)
    dbClasses.TzbMeta.create(brush=brush, key="created_at", value=str(datetime.now()))

    dbClasses.BrushParams.create(brush=brush, **vars(brush_data.params))
    dbClasses.BrushModifiers.create(brush=brush, **vars(brush_data.modifiers))

    with open(preview, "rb") as f:
        preview_blob = f.read()
        dbClasses.BrushPreview.create(brush=brush, data=preview_blob)

    texture_blob = None
    if texture:
        with open(texture, "rb") as f:
            texture_blob = f.read()
    dbClasses.BrushTexture.create(brush=brush, data=texture_blob)