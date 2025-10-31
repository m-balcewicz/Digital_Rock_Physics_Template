# Contributing

Thank you for your interest in contributing to the Digital Rock Physics Template!

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/m-balcewicz/Digital_Rock_Physics_Template.git
   cd Digital_Rock_Physics_Template
   ```

2. **Create a development environment**
   ```bash
   conda create -n drp_dev python=3.10
   conda activate drp_dev
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   pip install -r docs/requirements.txt  # For documentation
   ```

## Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use NumPy-style docstrings for all functions
- Keep functions focused and well-documented

### Example Docstring

```python
def my_function(data, threshold, verbose=False):
    """
    Brief one-line description.
    
    Longer description explaining what the function does,
    when to use it, and any important details.
    
    Parameters
    ----------
    data : numpy.ndarray
        3D array of shape (nz, ny, nx) containing the data
    threshold : float
        Threshold value for segmentation
    verbose : bool, optional
        If True, print progress messages (default: False)
        
    Returns
    -------
    numpy.ndarray
        Segmented data with same shape as input
        
    Raises
    ------
    ValueError
        If threshold is outside valid range
        
    Examples
    --------
    >>> data = np.random.rand(100, 100, 100)
    >>> result = my_function(data, threshold=0.5)
    >>> print(result.shape)
    (100, 100, 100)
    
    Notes
    -----
    This function modifies the input in-place if memory constraints
    are important. Use data.copy() to preserve the original.
    ```

## Submitting Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes**
   - Write code
   - Add/update docstrings
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run any existing tests
   # Test manually with example data
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add feature: description"
   git push origin feature/my-new-feature
   ```

5. **Open a Pull Request**
   - Describe your changes
   - Link any related issues
   - Wait for review

## Adding New Features

When adding new functionality:

1. **Add to appropriate module** (`input_output`, `image`, `tools`, `math`, etc.)
2. **Write comprehensive docstrings** (NumPy style)
3. **Update API documentation** in `docs/api/`
4. **Add examples** to `examples/` folder
5. **Update CHANGELOG** in `docs/changelog.md`

## Documentation

Build and preview documentation locally:

```bash
cd docs
make serve  # Opens at http://localhost:8000
```

## Questions?

Open an issue on GitHub or contact the maintainer.
