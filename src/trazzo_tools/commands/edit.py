import click
import trazzo_tools.classes.dbClasses as dbClasses
from datetime import datetime
from dataclasses import asdict

def edit(file: str, visual_mode: bool = False, **kwargs):
    dbClasses.load_db(file)
    dbClasses.edit_db()

    brush = dbClasses.Brush.get_by_id(1)
    params = dbClasses.BrushParams.get_by_id(1)
    modifiers = dbClasses.BrushModifiers.get_by_id(1)
    texture, _ = dbClasses.BrushTexture.get_or_create(brush=brush)
    preview, _ = dbClasses.BrushPreview.get_or_create(brush=brush)

    if visual_mode:
        brush.name = click.prompt("Name:", default=brush.name)
        brush.category = click.prompt("Category:", default=brush.category)
        brush.engine = click.prompt("Engine:", default=brush.engine)
        brush.author = click.prompt("Author:", default=brush.author)
        dbClasses.TzbMeta.replace(key="author", value=brush.author).execute()

        params.radius = click.prompt("Radius:", default=params.radius)
        params.opacity = click.prompt("Opacity:", default=params.opacity)
        params.hardness = click.prompt("Hardness:", default=params.hardness)
        params.spacing = click.prompt("Spacing:", default=params.spacing)
        params.flow = click.prompt("Flow:", default=params.flow)
        params.jitter = click.prompt("Jitter:", default=params.jitter)
        params.rotation = click.prompt("Rotation:", default=params.rotation)
        params.ellipticalRatio = click.prompt("Elliptical ratio:", default=params.ellipticalRatio)
        params.ellipticalAngle = click.prompt("Elliptical angle:", default=params.ellipticalAngle)

        modifiers.eraser = click.prompt("Eraser:", default=modifiers.eraser)
        modifiers.blendMode = click.prompt("Blend mode:", default=modifiers.blendMode)
        modifiers.randomRotation = click.prompt("Rotation random:", default=modifiers.randomRotation)
        modifiers.randomZoom = click.prompt("Rotation zoom:", default=modifiers.randomZoom)
        modifiers.sizePressure = click.prompt("Size pressure:", default=modifiers.sizePressure)
        modifiers.opacityPressure = click.prompt("Opacity pressure:", default=modifiers.opacityPressure)

        pathTexture = click.prompt("Texture:", default="")
        if pathTexture:
            with open(pathTexture, "rb") as f:
                texture.data = f.read()
            texture.save()

        pathPreview = click.prompt("Preview:", default="")
        if pathPreview:
            with open(pathPreview, "rb") as f:
                preview.data = f.read()
            preview.save()
    else:
        for key, value in kwargs.items():
            if value is None: 
                continue
            key = snake_to_camel(key)
            if key in brush._meta.fields:
                setattr(brush, key, value)
            elif key in params._meta.fields:
                setattr(params, key, value)
            elif key in modifiers._meta.fields:
                setattr(modifiers, key, value)
            elif key == "preview":
                with open(value, "rb") as f:
                    preview.data = f.read()
                preview.save()
            elif key == "texture":
                with open(value, "rb") as f:
                    texture.data = f.read()
                texture.save()

    brush.updated_at = datetime.now()
    
    brush.save()
    params.save()
    modifiers.save()
    dbClasses.save_db()


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])