# type: ignore
# From: https://bugreports.qt.io/browse/PYSIDE-2215?gerritIssueType=IssueOnly
"""
The Sphinx object inventory that currently (August 2023) ships with the
PySide6 documentation is broken. For example, it includes lines like
```
PySide6.QtWidgets.PySide6.QtWidgets.QWidget py:class 1 PySide6/QtWidgets/QWidget.html#$
```
instead of
```
PySide6.QtWidgets.QWidget py:class 1 PySide6/QtWidgets/QWidget.html#$
```

This script fixes that in a local copy of the inventory file, which can
then be given to InterSphinx, in `conf.py`:
```
intersphinx_mapping = {
    'PySide6': ('https://doc.qt.io/qtforpython-6', 'PySide6.inv'),
}
```
"""

# script dependencies:
#   requests
#   sphobjinv

import re
from pathlib import Path
from subprocess import run

import requests

here = Path(__file__).parent
original_inv = here / "PySide6-original.inv"
original_txt = here / "PySide6-original.txt"
fixed_txt = here / "PySide6-fixed.txt"
fixed_inv = here / "source/PySide6.inv"

url = "https://doc.qt.io/qtforpython-6/objects.inv"
response = requests.get(url, allow_redirects=True)
original_inv.write_bytes(response.content)

run(["sphobjinv", "convert", "plain", original_inv, original_txt], check=True)

with fixed_txt.open("w", encoding="UTF-8") as stream:
    for line in original_txt.open(encoding="UTF-8"):
        if match := re.match(r"^(PySide6\..*)\.(\1)\.(.*)$", line):
            stream.write(f"{match.group(1)}.{match.group(3)}\n")
        else:
            stream.write(line)

run(["sphobjinv", "convert", "zlib", fixed_txt, fixed_inv], check=True)
