from trazzo_tools.classes.classes import TzBrush, BrushParams, BrushModifiers
import trazzo_tools.classes.dbClasses as dbClasses
import re

from rich.console import Console
from rich.table import Table
from rich import box
from dataclasses import asdict

def view(file: str, output: str = "."):
    dbClasses.load_db(file)

    brush = dbClasses.Brush.get_by_id(1)
    params = dbClasses.BrushParams.get_by_id(1)
    modifiers = dbClasses.BrushModifiers.get_by_id(1)

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
                rotationRandom=modifiers.rotationRandom,
                rotationZoom=modifiers.rotationZoom,
                sizePressure=modifiers.sizePressure,
                opacityPressure=modifiers.opacityPressure,
            ),
        )
        
    console = Console()
    data = asdict(tz)
    width = min(console.width, 40)

    # Info general
    info = Table(box=box.ROUNDED, show_header=False, title=f"🖌 Brush: {tz.name}", width=width)
    info.add_column("Campo", style="bold", width=25)
    info.add_column("Valor", width=15)
    for k in ["name", "author", "engine", "category", "format"]:
        info.add_row(camel_to_label(k), str(data[k]))
    console.print(info)

    # Params
    infoParams = Table(box=box.ROUNDED, show_header=False, title="Params", width=width)
    infoParams.add_column("Campo", style="bold", width=25)
    infoParams.add_column("Valor", width=15)
    for k, v in data["params"].items():
        infoParams.add_row(camel_to_label(k), str(v))
    console.print(infoParams)

    # Modifiers
    infoModifiers = Table(box=box.ROUNDED, show_header=False, title="Modifiers", width=width)
    infoModifiers.add_column("Campo", style="bold", width=25)
    infoModifiers.add_column("Valor", width=15)
    for k, v in data["modifiers"].items():
        infoModifiers.add_row(camel_to_label(k), str(v))
    console.print(infoModifiers)
        
    
def camel_to_label(name: str) -> str:
    return re.sub(r'([A-Z])', r' \1', name).title()