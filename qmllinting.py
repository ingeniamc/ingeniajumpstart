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

command += qml_files

print(f"Linting {len(qml_files)} QML files in {directory}")

subprocess.run(command, stderr=subprocess.PIPE)
