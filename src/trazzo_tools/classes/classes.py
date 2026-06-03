import json
from dataclasses import dataclass, field
from os import getenv
EXTENSION = getenv("EXTENSION")
FORMAT_VERSION = getenv("FORMAT_VERSION") 

@dataclass
class BrushParams:
    radius: float = 20.0
    opacity: float = 1.0
    hardness: float = 0.8
    spacing: float = 0.3
    flow: float = 1.0
    jitter: float = 0.0
    rotation: float = 0.0
    ellipticalRatio: float = 1.0
    ellipticalAngle: float = 90.0


@dataclass
class BrushModifiers:
    eraser: bool = False
    blendMode: str = "normal"
    rotationRandom: float = 0.0
    rotationZoom: float = 0.0
    sizePressure: bool = False
    opacityPressure: bool = False


@dataclass
class TzBrush:
    name: str = "output"
    author: str = ""
    engine: str = "pixel"
    category: str = "pen"
    format: str = FORMAT_VERSION
    params: BrushParams = field(default_factory=BrushParams)
    modifiers: BrushModifiers = field(default_factory=BrushModifiers)

    @staticmethod
    def from_json(path: str) -> "TzBrush":
        with open(path) as f:
            data = json.load(f)
        return TzBrush(
            name=data["name"],
            author=data.get("author", ""),
            engine=data.get("engine", "pixel"),
            category=data.get("category", "pen"),
            format=data.get("format", "tzbrush-v1"),
            params=BrushParams(**data.get("params", {})),
            modifiers=BrushModifiers(**data.get("modifiers", {})),
        )

    def to_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.__dict__, f, indent=2, default=vars)
