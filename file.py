import cx_Freeze
import sys
import os

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("gvc.py", base=base, icon="gas.ico",)]

# Function to collect files from a directory and its subdirectories
def collect_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append((os.path.join(root, filename), os.path.relpath(os.path.join(root, filename), start=directory)))
    return files

# Collect files from the gui directory and its subdirectories
gui_files = collect_files('gui')
# Collect files from the gui/icons directory and its subdirectories
icons_files = collect_files('gui/icons')
# Collect files from the gui/sound directory and its subdirectories
sound_files = collect_files('gui/sound')

cx_Freeze.setup(
    name="Gestion Commerciale des Ventes - GAS",
    options={"build_exe": {"packages": ["PyQt5", "numba"], "include_files": gui_files + icons_files + sound_files}},
    version="1.0",
    description="Gestion Commerciale des Ventes",
    executables=executables
)
