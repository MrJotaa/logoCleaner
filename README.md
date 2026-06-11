# LogoCleaner

LogoCleaner is a Python-first command line tool for removing uniform backgrounds from logo images.

It is designed for cases where logos are placed on simple, mostly uniform backgrounds, such as white, black, or flat-color backgrounds. The project focuses on predictable, user-controlled background removal instead of trying to guess everything automatically.

## Current status

LogoCleaner is currently in **MVP stage**.

The first version provides:

* a Python package;
* a command line interface;
* two explicit background removal strategies;
* automatic background color detection from image borders;
* PNG export with transparency;
* Docker support;
* tests and linting setup.

There is no frontend yet, no web API, and no AI-based background removal in this version.

## Why LogoCleaner?

Many background removal tools are built for photos, products, or people. Logos often need a different approach:

* flat backgrounds;
* sharp edges;
* small text;
* internal white or light details;
* transparent PNG output;
* predictable behavior.

LogoCleaner starts with simple, controllable strategies that are easy to understand, test, and improve.

## Installation

### Local development installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/logocleaner.git
cd logocleaner
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode:

```bash
pip install -e ".[dev]"
```

Check that the CLI works:

```bash
logocleaner --help
```

## Usage

The main command is:

```bash
logocleaner clean INPUT OUTPUT --mode MODE
```

Example:

```bash
logocleaner clean input.png output.png --mode global
```

With automatic background color detection:

```bash
logocleaner clean input.png output.png --mode border --bg auto --tolerance 30
```

With a manual background color:

```bash
logocleaner clean input.png output.png --mode global --bg "#ffffff" --tolerance 40
```

The output must be a PNG file, because transparency is required.

## Cleaning modes

LogoCleaner does not choose a cleaning strategy by default. The user must explicitly select one.

This is intentional: different logos need different behavior.

### `global` mode

```bash
logocleaner clean input.png output.png --mode global --bg "#ffffff" --tolerance 40
```

The `global` strategy removes every pixel in the image that is similar to the selected background color.

This is useful when:

* the logo is on a flat background;
* the background color is not used as part of the real logo;
* you want to remove matching pixels everywhere in the image.

Example use case:

* a red/blue/black logo on a white background.

Be careful with this mode if the logo contains white or light-colored details, because those pixels may also be removed.

### `border` mode

```bash
logocleaner clean input.png output.png --mode border --bg auto --tolerance 30
```

The `border` strategy removes only background-like pixels connected to the image border.

This is useful when:

* the logo object is centered;
* the background surrounds the logo;
* the logo contains internal white, gray, or light details that should be preserved.

Example use case:

* a circular badge logo on a white background, where the text or highlights inside the badge should not be removed.

This mode is usually safer for complex logos because it does not remove matching pixels that are enclosed inside the logo.

## Background color

LogoCleaner supports two ways to choose the background color.

### Automatic detection

```bash
--bg auto
```

This estimates the background color from the image border.

This works best when the logo is centered and the background touches the image edges.

### Manual color

```bash
--bg "#ffffff"
```

Manual color selection is useful when you already know the background color.

Examples:

```bash
--bg "#ffffff"
--bg "#000000"
--bg "#f2f2f2"
```

## Tolerance

`tolerance` controls how similar a pixel must be to the background color to be removed.

```bash
--tolerance 30
```

Lower values are more conservative.

Higher values are more aggressive.

Suggested starting points:

* `20` — conservative, good for clean PNGs;
* `30` — default, good general starting point;
* `40-60` — useful for JPEGs, antialiasing, or slightly dirty backgrounds;
* `80+` — aggressive, may remove parts of the logo.

## Docker usage

Build the Docker image:

```bash
docker build -t logocleaner .
```

Run LogoCleaner using the current directory as a mounted workspace:

```bash
docker run --rm -v "$PWD:/work" logocleaner \
  clean /work/input.png /work/output.png \
  --mode border --bg auto --tolerance 30
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Check formatting:

```bash
ruff format --check .
```

Apply formatting:

```bash
ruff format .
```

## Project structure

```text
src/logocleaner/
  cli.py
  exceptions.py

  background/
    detect.py

  core/
    colors.py
    pipeline.py
    types.py
    validation.py

  image_io/
    load.py
    save.py

  masks/
    alpha.py

  strategies/
    base.py
    global_color.py
    border_connected.py

tests/
```

The core idea is that each strategy creates a background mask:

```text
True  = background pixel, should become transparent
False = logo pixel, should be preserved
```

The common pipeline then applies that mask and exports a transparent PNG.

## Design principles

LogoCleaner follows a few simple principles:

* no hidden default strategy;
* explicit user choice;
* simple strategies before AI;
* predictable behavior;
* testable image processing logic;
* extensible architecture.

Future strategies should be able to plug into the same pipeline by implementing the same mask-generation contract.

## Roadmap

Possible future improvements:

* CLI tests with Typer `CliRunner`;
* preview images with checkerboard background;
* edge cleanup and feathering;
* automatic transparent padding trim;
* batch processing;
* strategy recommendation command;
* manual color picker in a future UI;
* optional AI-based background removal;
* web interface;
* export presets for favicons and web assets.

## Known limitations

LogoCleaner currently works best with logos on uniform backgrounds.

It may struggle with:

* complex photographic backgrounds;
* shadows or gradients;
* logos touching the image border;
* backgrounds with strong compression artifacts;
* logos that use the same color as the background.

For difficult images, try adjusting `--tolerance` or switching between `global` and `border` mode.

## License

This project is licensed under the MIT License.

