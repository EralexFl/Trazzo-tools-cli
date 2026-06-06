# trazzo-tools

CLI for creating, exporting, viewing, and editing Trazzo brush archives (`.tzb`).

## Requirements

- Python 3.10+

## Installation

```bash
pip install trazzo-tools
```

After installation, the `trazzo-tools` command will be available in your terminal.

## Commands

### `create`

Creates a `.tzb` archive from a brush definition.

```bash
trazzo-tools create --data brush.json --preview preview.png [--texture texture.png] [--output ./output]
```

| Option | Short | Required | Description |
|---|---|---|---|
| `--data` | `-d` | Yes | Path to JSON brush definition |
| `--preview` | `-p` | Yes | Path to preview image |
| `--texture` | `-t` | No | Path to texture image |
| `--output` | `-o` | No | Output directory (default: `.`) |

**Output:** `<output>/<name>.tzb`

---

### `export`

Exports a `.tzb` archive back to its source files.

```bash
trazzo-tools export brush.tzb [--output ./output]
```

**Output:**
- `<name>.json` — brush definition
- `<name>_preview.png` — preview image
- `<name>_texture.png` — texture image

---

### `view`

Displays the contents of a `.tzb` archive.

```bash
trazzo-tools view brush.tzb
```

---

### `edit`

Edits a `.tzb` archive. Without flags, enters interactive mode.

```bash
# Interactive mode
trazzo-tools edit brush.tzb

# Direct mode (applies changes without prompting)
trazzo-tools edit brush.tzb --name "New Name" --radius 35.0
```

| Option | Type | Description |
|---|---|---|
| `--name` | string | Brush name |
| `--author` | string | Author |
| `--engine` | string | Engine (`pixel`) |
| `--category` | string | Category (`pen`) |
| `--radius` | float | Radius |
| `--opacity` | float | Opacity (0.0–1.0) |
| `--hardness` | float | Hardness (0.0–1.0) |
| `--spacing` | float | Spacing |
| `--flow` | float | Flow (0.0–1.0) |
| `--jitter` | float | Jitter |
| `--rotation` | float | Rotation (degrees) |
| `--elliptical-ratio` | float | Elliptical ratio |
| `--elliptical-angle` | float | Elliptical angle |
| `--eraser` / `--no-eraser` | bool | Eraser mode |
| `--blend-mode` | string | Blend mode (`normal`) |
| `--rotation-random` | float | Rotation random |
| `--rotation-zoom` | float | Rotation zoom |
| `--size-pressure` / `--no-size-pressure` | bool | Size pressure |
| `--opacity-pressure` / `--no-opacity-pressure` | bool | Opacity pressure |
| `--preview` | string | Path to preview image |
| `--texture` | string | Path to texture image |

---

## Brush definition (JSON)

```json
{
  "name": "My Brush",
  "author": "Author",
  "engine": "pixel",
  "category": "pen",
  "format": "tzbrush-v1",
  "params": {
    "radius": 20.0,
    "opacity": 1.0,
    "hardness": 0.8,
    "spacing": 0.3,
    "flow": 1.0,
    "jitter": 0.0,
    "rotation": 0.0,
    "ellipticalRatio": 1.0,
    "ellipticalAngle": 90.0
  },
  "modifiers": {
    "eraser": false,
    "blendMode": "normal",
    "rotationRandom": 0.0,
    "rotationZoom": 0.0,
    "sizePressure": false,
    "opacityPressure": false
  }
}
```

## .tzb format

A `.tzb` file is a SQLite database with the following tables:

| Table | Description |
|---|---|
| `brushes` | General brush info (name, author, engine, category) |
| `brush_params` | Stroke parameters |
| `brush_modifiers` | Behavior modifiers |
| `brush_texture` | Texture image (blob) |
| `brush_preview` | Preview image (blob) |
| `tzb_meta` | Format metadata |
