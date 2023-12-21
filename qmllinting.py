"""Script to find all .qml files in the project and lint them with pyside6-qmllint."""
import os
import subprocess
import sys

command = ["pyside6-qmllint"]
directory = os.getcwd()
qml_files = []


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".qml"):
            path = os.path.join(root, file)
            qml_files.append(path)

if not qml_files:
    print(f"No .qml files found in {directory}")
    sys.exit(1)

# import QtQuick.Dialogs is cursed, the only way to fix it is disabling this warning
qml_files.append("--import")
qml_files.append("disable")
command += qml_files

print(command)

print(f"Linting {len(qml_files)} QML files in {directory}")

subprocess.run(command, check=True)
