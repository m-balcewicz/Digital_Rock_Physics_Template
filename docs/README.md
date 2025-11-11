# Documentation

This folder contains user and API documentation. Serve locally with Sphinx.

Scripts
-------
- docs/scripts/generate_docs.py: Autogenerates Markdown from example notebooks and injects example blocks into function docstrings. Run after adding notebooks under examples/<module>/reference/.

Usage
-----
Run the generator from the repo root (so paths resolve correctly):

```bash
conda activate dev_DRP
python docs/scripts/generate_docs.py
```

Generated files
---------------
- docs/<module>_examples.md: Per-module example roundups extracted from notebooks.
- Docstrings in drp_template/<module>/*.py may be updated to include an "Examples (auto-generated)" section.

## Auto-Generated Examples Integration

Run `python scripts/generate_docs.py` to:

1. Parse notebooks under `examples/<module>/reference/`.
2. Emit `docs/<module>_examples.md` (auto-generated – do not edit by hand).
3. Patch selected function docstrings by appending an `Examples (auto-generated)` section if not already present.

Include the generated examples pages in the table of contents by referencing them from `index.md` or a suitable section page:

```markdown
```{toctree}
:maxdepth: 1
examples/image_examples
examples/io_examples
examples/tools_examples
examples/compute_examples
```
```

Regenerate docs any time you change a reference notebook. Commit the updated Python sources (with patched docstrings) and the new `*_examples.md` pages.

## Quick Start

### 1. Install documentation dependencies

```bash
cd docs
pip install -r requirements.txt
```

### 2. Build and serve locally

**Option A: Using the convenience script (Mac/Linux)**
```bash
chmod +x serve_docs.sh
./serve_docs.sh
```

**Option B: Using Make directly**
```bash
# Build HTML docs
make html

# Serve on localhost:8000
make serve
```

**Option C: Manual build**
```bash
# Build
sphinx-build -b html . _build/html

# Serve
cd _build/html
python -m http.server 8000
```

### 3. View documentation

Open your browser to: **http://localhost:8000**

## Documentation Structure

```
docs/
├── index.md              # Home page
├── installation.md       # Installation guide
├── quickstart.md         # Quick start tutorial
├── schema_versioning.md  # Schema versioning docs
├── changelog.md          # Version history
├── api/                  # API reference
│   ├── io.md
│   ├── image.md
│   ├── tools.md
│   ├── compute.md
│   └── default_params.md
├── conf.py              # Sphinx configuration
├── Makefile             # Build commands
└── requirements.txt     # Doc dependencies
```

## Available Make Commands

```bash
make html          # Build HTML documentation
make serve         # Build and serve on localhost:8000
make clean         # Remove built documentation
make clean-build   # Clean and rebuild everything
```

## Writing Documentation

### Markdown Files

Documentation is written in Markdown using [MyST Parser](https://myst-parser.readthedocs.io/):

```markdown
# Page Title

Regular markdown content...

## Code Examples

\```python
import drp_template.io as io
data = io.import_model('data.raw', dtype='uint8', dimensions={'nz': 400, 'ny': 400, 'nx': 400})
\```
```

### API Documentation

API docs are auto-generated from docstrings using Sphinx autodoc. Make sure your docstrings follow NumPy style:

```python
def my_function(param1, param2):
    """
    Brief description.
    
    Parameters
    ----------
    param1 : type
        Description of param1
    param2 : type
        Description of param2
        
    Returns
    -------
    type
        Description of return value
    """
```

## Deploying Documentation

### ReadTheDocs (Recommended)

1. Connect your GitHub repository to [ReadTheDocs](https://readthedocs.org/)
2. RTD will automatically build and host your docs
3. Docs will be available at: `https://digital-rock-physics-template.readthedocs.io/`

### GitHub Pages

```bash
# Build docs
make html

# Push to gh-pages branch
# (configure GitHub Pages to serve from gh-pages branch)
```

## Troubleshooting

**Issue: "sphinx-build: command not found"**
```bash
pip install sphinx
```

**Issue: "Theme 'sphinx_rtd_theme' not found"**
```bash
pip install sphinx-rtd-theme
```

**Issue: "Unknown directive type 'toctree'"**
- Make sure you're using `.md` files with MyST parser
- Check that `myst-parser` is installed

## Release 0.1.0b2 Highlights (Docs Impact)

- Rock physics reorganized under `drp_template.compute.rockphysics` with focused subpackages:

```
drp_template/compute/rockphysics/
├── mixing/            # e.g., brie_fluid_mixing, density_solid_mix
├── bounds/            # voigt_reuss_hill_bounds, hashin_shtrikman_bounds
└── effective_medium/  # backus_average, gassmann
```

- Bounds/mixing return dictionaries with descriptive keys (e.g., `bulk_modulus_hill`).
- New examples and docstrings reference the updated imports:

```python
from drp_template.compute.rockphysics.effective_medium import backus_average, thomsen_params
from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds
from drp_template.compute.rockphysics.mixing import brie_fluid_mixing
```

**Issue: Port 8000 already in use**
```bash
# Use a different port
cd _build/html
python -m http.server 8080  # Use port 8080 instead
```
