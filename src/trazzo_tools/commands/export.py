from trazzo_tools.classes.classes import TzBrush, BrushParams, BrushModifiers
import trazzo_tools.classes.dbClasses as dbClasses
import os

def export(file: str, output: str = "."):
    dbClasses.load_db(file)

    brush = dbClasses.Brush.get_by_id(1)
    params = dbClasses.BrushParams.get_by_id(1)
    modifiers = dbClasses.BrushModifiers.get_by_id(1)
    texture = dbClasses.BrushTexture.get_by_id(1)
    preview = dbClasses.BrushPreview.get_by_id(1)

    base_name = brush.name
    tz = TzBrush(
            name=brush.name,
            author=brush.author,
            engine=brush.engine,
            category=brush.category,
            format=brush.format,
            params=BrushParams(
                radius=params.radius,
                opacity=params.opacity,
                hardness=params.hardness,
                spacing=params.spacing,
                flow=params.flow,
                jitter=params.jitter,
                rotation=params.rotation,
                ellipticalRatio=params.ellipticalRatio,
                ellipticalAngle=params.ellipticalAngle,
            ),
            modifiers=BrushModifiers(
                eraser=modifiers.eraser,
                blendMode=modifiers.blendMode,
                randomRotation=modifiers.randomRotation,
                randomZoom=modifiers.randomZoom,
                sizePressure=modifiers.sizePressure,
                opacityPressure=modifiers.opacityPressure,
            ),
        )

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output), exist_ok=True)

    for label, blob in [("texture", texture.data), ("preview", preview.data)]:
        if blob:
            with open(os.path.join(output, f"{base_name}_{label}.png"), "wb") as f:
                f.write(blob)
    tz.to_json(os.path.join(output, f"{base_name}.json"))
        