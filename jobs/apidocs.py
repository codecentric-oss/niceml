"""Script for creating the API documentation and the corresponding navigation customizations."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()
for path in sorted(Path("niceml").glob("**/*.py")):
    module_path = path.relative_to("niceml").with_suffix("")
    doc_path = path.relative_to(
        "niceml",
    ).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    elif parts[-1] == "__main__":
        continue
    if len(parts) == 0:
        continue
    nav[tuple(parts)] = str(doc_path)

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(["niceml"] + parts)
        print("::: " + ident, file=fd)


with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
