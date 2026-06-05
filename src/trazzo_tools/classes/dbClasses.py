from peewee import *
from os import getenv
EXTENSION = getenv("EXTENSION")
FORMAT_VERSION = getenv("FORMAT_VERSION") 
DB_JOURNAL_MODE = getenv("DB_JOURNAL_MODE")
DB_FOREIGN_KEYS = getenv("DB_FOREIGN_KEYS")

db = SqliteDatabase(None)  # se inicializa después con el path real

class BaseModel(Model):
    class Meta:
        database = db


class TzbMeta(BaseModel):
    key = TextField(primary_key=True)
    value = TextField()

    class Meta:
        table_name = "tzb_meta"


class Brush(BaseModel):
    format = TextField(default=FORMAT_VERSION)
    name = TextField()
    author = TextField(default="")
    engine = TextField(default="pixel")
    category = TextField(default="pen")
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = "brushes"


class BrushParams(BaseModel):
    brush = ForeignKeyField(
        Brush, primary_key=True, backref="params", on_delete="CASCADE"
    )
    radius = FloatField(default=20.0)
    opacity = FloatField(default=1.0)
    hardness = FloatField(default=0.8)
    spacing = FloatField(default=0.3)
    flow = FloatField(default=1.0)
    jitter = FloatField(default=0.0)
    rotation = FloatField(default=0.0)
    ellipticalRatio = FloatField(default=1.0)
    ellipticalAngle = FloatField(default=90.0)

    class Meta:
        table_name = "brush_params"


class BrushModifiers(BaseModel):
    brush = ForeignKeyField(
        Brush, primary_key=True, backref="modifiers", on_delete="CASCADE"
    )
    eraser = BooleanField(default=False)
    blendMode = TextField(default="normal")
    randomRotation = FloatField(default=0.0)
    randomZoom = FloatField(default=0.0)
    sizePressure = BooleanField(default=False)
    opacityPressure = BooleanField(default=False)

    class Meta:
        table_name = "brush_modifiers"


class BrushTexture(BaseModel):
    brush = ForeignKeyField(
        Brush, primary_key=True, backref="texture", on_delete="CASCADE"
    )
    data = BlobField(null=True)
    base64 = TextField(null=True)

    class Meta:
        table_name = "brush_texture"


class BrushPreview(BaseModel):
    brush = ForeignKeyField(
        Brush, primary_key=True, backref="preview", on_delete="CASCADE"
    )
    data = BlobField(null=True)
    base64 = TextField(null=True)

    class Meta:
        table_name = "brush_preview"


def init_db(name: str = "brushes"):

    db.init(
        name + f".{EXTENSION.lower()}",
        pragmas={
            "journal_mode": DB_JOURNAL_MODE,
            "foreign_keys": DB_FOREIGN_KEYS,
        },
    )
    db.connect()
    db.create_tables(
        [TzbMeta, Brush, BrushParams, BrushModifiers, BrushTexture, BrushPreview],
        safe=True,
    )

def load_db(file: str):
    db.init(file, pragmas={"foreign_keys": DB_FOREIGN_KEYS})
    db.connect()
    return db

def edit_db():
    db.begin()

def save_db():
    db.commit()

def close_db():
    if not db.is_closed():
        db.close() 
