# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('assets', 'assets'), ('*.py', '.')]
binaries = []
hiddenimports = ['tkinter', 'ttk', 'sqlite3', 'serial', 'serial.tools.list_ports', 'reportlab', 'win32print', 'win32api', 'win32con', 'cv2', 'PIL', 'numpy', 'queue', 'threading', 'datetime', 'json', 'csv', 'os', 'sys', 'hashlib', 'getpass', 'atexit', 'base64', 'secrets', 'io', 'tempfile', 'subprocess', 're', 'shutil', 'logging', 'functools', 'contextlib', 'typing', 'enum', 'time', 'decimal', 'uuid', 'inspect', 'importlib', 'traceback', 'math', 'statistics', 'constants', 'config_manager', 'database_manager', 'ui_manager', 'tab_manager', 'error_handler', 'refactored_app', 'camera_manager', 'serial_manager', 'messagebox', 'pdf_print_manager', 'ui_components', 'config', 'database', 'tkinter.messagebox', 'tkinter.filedialog', 'tkinter.simpledialog', 'tkinter.scrolledtext', 'tkinter.ttk', 'tkinter.font', 'tkinter.colorchooser', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageDraw', 'PIL.ImageFont', 'cv2.VideoCapture', 'cv2.destroyAllWindows', 'cv2.waitKey', 'cv2.imshow', 'serial.Serial', 'serial.tools.list_ports.comports', 'serial.SerialException', 'reportlab.pdfgen', 'reportlab.lib.pagesizes', 'reportlab.lib.units', 'reportlab.platypus', 'reportlab.lib.styles', 'reportlab.pdfbase', 'reportlab.pdfbase.ttfonts', 'reportlab.lib.enums', 'win32print.GetDefaultPrinter', 'win32api.GetProfileString', 'win32con.CW_USEDEFAULT', 'win32print.OpenPrinter', 'win32print.StartDocPrinter', 'win32print.StartPagePrinter', 'win32print.EndPagePrinter', 'win32print.EndDocPrinter', 'win32print.ClosePrinter']
tmp_ret = collect_all('cv2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PIL')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('numpy')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('reportlab')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('serial')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'scipy', 'jupyter', 'IPython', 'sphinx', 'pytest', 'setuptools', 'pip', 'wheel', 'distutils', 'ensurepip', 'venv', 'pipenv', 'conda', 'anaconda'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='WeighingScaleApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets\\app_icon.ico'],
)
