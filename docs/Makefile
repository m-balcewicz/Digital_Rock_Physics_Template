# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@echo "Copying examples to docs..."
	@mkdir -p examples
	@cp -r ../examples/* examples/ 2>/dev/null || true
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Custom target for serving docs locally
serve:
	@echo "Building HTML documentation..."
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "\n=========================================="
	@echo "Starting local documentation server..."
	@echo "Open your browser to: http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@echo "==========================================\n"
	@cd _build/html && python -m http.server 8000

# Clean and rebuild everything
clean-build:
	rm -rf _build
	rm -rf examples  # Remove copied examples
	mkdir -p examples
	@cp -r ../examples/* examples/ 2>/dev/null || true
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "Documentation built successfully!"
