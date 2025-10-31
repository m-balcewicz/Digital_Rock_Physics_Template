# Documentation

This directory contains the Sphinx documentation for the Digital Rock Physics Template.

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
│   ├── input_output.md
│   ├── image.md
│   ├── tools.md
│   ├── math.md
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
import drp_template.input_output as io
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

**Issue: Port 8000 already in use**
```bash
# Use a different port
cd _build/html
python -m http.server 8080  # Use port 8080 instead
```
