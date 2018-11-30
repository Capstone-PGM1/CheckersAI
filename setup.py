import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Checkers",
    version = "1.0",
    description = "Project Lyra - Checkers Game",
    options = {
        "build_exe": {"packages": ["pygame", "PodSixNet", "numpy"],
                      "include_files": ["wood.jpg", "white.jpg", "tan.png", "king.png", "grey.png", "black.png", "Carlito-BoldItalic.ttf", "450000_exp4.npy"]}
    },
    executables = [Executable("gamepage.py", base = base, targetName="checkers.exe")])