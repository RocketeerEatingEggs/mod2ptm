# mod2ptm pyinstall.py
# code for pyinstaller to make an executable for mod2ptm
# by RocketeerEatingEggs

import PyInstaller.__main__

PyInstaller.__main__.run([
    'mod2ptm volcmd.py',
    '--onefile',
])
