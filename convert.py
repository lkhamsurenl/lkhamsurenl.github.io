"""Turn a Jupyter notebook into a Markdown blog post.

The post lands in _posts/ with front matter, and its charts in
assets/images/<slug>/, so it renders in the site layout and shows up on the
Writing page and in the feed like any hand-written post.

    python convert.py assets/notebooks/glucose/2023-02-19-CGM.ipynb
    python convert.py notebook.ipynb --title "My CGM data" --date 2023-02-19

The date comes from a YYYY-MM-DD- prefix on the notebook's file name, else
--date, else today. The title comes from the notebook's first "# " heading,
else --title, else the file name.
"""

import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--title", help="Post title, if the notebook has no '# ' heading.")
    parser.add_argument("--date", help="Post date (YYYY-MM-DD), if the file name has none.")
    parser.add_argument("--no-execute", action="store_true",
                        help="Use the outputs saved in the notebook instead of rerunning it.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing post.")
    args = parser.parse_args()

    notebook = args.file.resolve()
    if notebook.suffix != ".ipynb":
        sys.exit(f"Input must be an .ipynb file: {args.file}")

    match = DATED.match(notebook.stem)
    date = match.group(1) if match else (args.date or datetime.date.today().isoformat())
    slug = slugify(match.group(2) if match else notebook.stem)
    post = ROOT / "_posts" / f"{date}-{slug}.md"
    images = ROOT / "assets" / "images" / slug
    if post.exists() and not args.force:
        sys.exit(f"{post.relative_to(ROOT)} already exists; pass --force to overwrite it.")

    with tempfile.TemporaryDirectory() as tmp:
        command = ["jupyter", "nbconvert", "--to", "markdown", "--output-dir", tmp]
        if not args.no_execute:
            # Run from the notebook's folder so relative data paths resolve.
            command += ["--execute", f"--ExecutePreprocessor.cwd={notebook.parent}"]
        subprocess.run(command + [str(notebook)], check=True)

        body = (Path(tmp) / f"{notebook.stem}.md").read_text()

        # nbconvert writes charts to <stem>_files/ and links them relatively;
        # move them under assets/ and point the links at their site path.
        files = Path(tmp) / f"{notebook.stem}_files"
        if files.exists():
            if images.exists():
                shutil.rmtree(images)
            shutil.copytree(files, images)
            body = body.replace(f"({files.name}/", f"(/assets/images/{slug}/")

    # The first "# " heading becomes the title rather than a second H1 on the page.
    heading = re.search(r"^# (.+)$", body, flags=re.MULTILINE)
    title = args.title or (heading.group(1).strip() if heading else slug.replace("-", " "))
    if heading and not args.title:
        body = body[: heading.start()] + body[heading.end():]

    front_matter = "\n".join([
        "---",
        # A JSON string is a valid YAML string, quotes in the title included.
        f"title: {json.dumps(title, ensure_ascii=False)}",
        "categories:",
        "  - Blog",
        "---",
    ])
    post.write_text(front_matter + "\n\n" + body.strip() + "\n")

    print(f"Wrote {post.relative_to(ROOT)}")
    if images.exists():
        print(f"Charts in {images.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
