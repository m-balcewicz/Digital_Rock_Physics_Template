"""Autogenerate documentation from reference notebooks and inject examples into docstrings.

Relocated Script
----------------
This script now lives under docs/scripts/ so that generated markdown and
API example extraction tooling are co-located with the documentation tree.
Run it whenever you add or modify notebooks in examples/<module>/reference/.

Workflow:
1. Scan examples/<module>/reference/*.ipynb for each top-level subpackage in drp_template.
2. Extract first markdown cell as short description and code cells as usage examples.
3. Build a Markdown docs tree under docs/ with one file per subpackage and per function.
4. For target functions listed in FUNCTION_MAP, update their docstring to append an 'Examples' section
   derived from the corresponding notebook (if not already present).

Note: The original location was scripts/generate_docs.py. The header in generated
markdown now points to docs/scripts/generate_docs.py.
"""
from __future__ import annotations
import json
import ast
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[2]  # docs/scripts -> project root
EXAMPLES_ROOT = PROJECT_ROOT / "examples"
DOCS_ROOT = PROJECT_ROOT / "docs"
PACKAGE_ROOT = PROJECT_ROOT / "drp_template"

FUNCTION_MAP: Dict[str, List[str]] = {
    "image": ["ortho_slice", "ortho_views", "histogram", "volume_rendering", "create_rotation_animation"],
    "tools": ["get_model_properties", "check_binary"],
    "io": ["import_model", "export_model"],
}
SUPPORTED_EXT = ".ipynb"

def load_notebook(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def extract_example_from_notebook(nb: Dict) -> Tuple[str, List[str]]:
    description = ""
    code_snippets: List[str] = []
    for cell in nb.get("cells", []):
        cell_type = cell.get("cell_type")
        source = cell.get("source", [])
        if cell_type == "markdown" and not description:
            description = "".join(source).strip()
        elif cell_type == "code":
            code = "".join(source).strip()
            if code:
                code_snippets.append(code)
    return description, code_snippets

def find_reference_notebooks(module: str) -> List[Path]:
    ref_dir = EXAMPLES_ROOT / module / "reference"
    if not ref_dir.exists():
        return []
    return sorted([p for p in ref_dir.glob(f"*{SUPPORTED_EXT}")])

def ensure_docs_root():
    DOCS_ROOT.mkdir(exist_ok=True)

def sanitize_md(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

MD_HEADER = "<!-- AUTO-GENERATED: DO NOT EDIT DIRECTLY. Run docs/scripts/generate_docs.py -->\n"

def build_markdown_for_module(module: str, examples: Dict[str, Dict]) -> str:
    lines = [MD_HEADER, f"# {module.capitalize()} Reference Examples", ""]
    for nb_name, info in examples.items():
        desc = info.get("description", "")
        lines.append(f"## {nb_name}")
        if desc:
            lines.append(desc)
        for i, code in enumerate(info.get("code", []), 1):
            lines.append("\n### Example Code Block {}".format(i))
            lines.append("```python")
            lines.append(code)
            lines.append("```")
        lines.append("")
    return sanitize_md("\n".join(lines))

class DocstringPatcher(ast.NodeTransformer):
    def __init__(self, examples_map: Dict[str, Dict[str, Dict]]):
        self.examples_map = examples_map
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        fn_name = node.name
        for module, fns in FUNCTION_MAP.items():
            if fn_name in fns:
                example_data = self.examples_map.get(module, {})
                chosen = None
                for nb_name, info in example_data.items():
                    if fn_name.lower() in nb_name.lower():
                        chosen = info
                        break
                if chosen is None and example_data:
                    chosen = next(iter(example_data.values()))
                if chosen:
                    example_blocks = []
                    for code in chosen.get("code", [])[:1]:
                        example_blocks.append(code)
                    example_section = "\n\nExamples (auto-generated):\n\n```python\n" + "\n\n".join(example_blocks) + "\n```\n"
                    has_doc = (
                        len(node.body) > 0 and isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) and isinstance(getattr(node.body[0].value, "value", None), str)
                    )
                    if has_doc:
                        original_doc = node.body[0].value.value
                        if "Examples (auto-generated):" not in original_doc:
                            new_doc = original_doc + example_section
                        else:
                            new_doc = original_doc
                        node.body[0] = ast.Expr(value=ast.Constant(value=new_doc))
                    else:
                        new_doc = example_section.strip()
                        node.body.insert(0, ast.Expr(value=ast.Constant(value=new_doc)))
        return node

def patch_docstrings_in_file(py_path: Path, examples_map: Dict[str, Dict[str, Dict]]):
    src = py_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return
    patcher = DocstringPatcher(examples_map)
    new_tree = patcher.visit(tree)
    ast.fix_missing_locations(new_tree)
    try:
        new_src = ast.unparse(new_tree)
    except Exception:
        return
    py_path.write_text(new_src, encoding="utf-8")

def main():
    ensure_docs_root()
    examples_map: Dict[str, Dict[str, Dict]] = {}
    for module in FUNCTION_MAP.keys():
        notebooks = find_reference_notebooks(module)
        module_examples: Dict[str, Dict] = {}
        for nb_path in notebooks:
            nb = load_notebook(nb_path)
            desc, code_snips = extract_example_from_notebook(nb)
            module_examples[nb_path.stem] = {"description": desc, "code": code_snips}
        examples_map[module] = module_examples
        md_content = build_markdown_for_module(module, module_examples)
        (DOCS_ROOT / f"{module}_examples.md").write_text(md_content, encoding="utf-8")
    for module in FUNCTION_MAP.keys():
        mod_dir = PACKAGE_ROOT / module
        if mod_dir.exists():
            for py_file in mod_dir.glob("*.py"):
                patch_docstrings_in_file(py_file, examples_map)
    print("Documentation generation complete.")

if __name__ == "__main__":
    main()
