import cx_Freeze
import sys


base = None
if sys.platform == 'win32':
    base = "Win32GUI"

executables = [cx_Freeze.Executable("subd.py", base=base, icon = "icon.ico")]

cx_Freeze.setup(
    name = "Subtitle Downloader - By MKG",
    options = {"build_exe":{"packages":["tkinter","bs4","googlesearch","requests","os"], "include_files":["icon.ico"]}},
    version = "1.0",
    description = "Subtitle Downloader for a local Collection of movies. Prepared by - Mayank Kumar Giri",
    executables = executables
)