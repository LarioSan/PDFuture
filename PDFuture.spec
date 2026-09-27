# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main3.py'],
    pathex=[],
    binaries=[],
    datas=[('burocrazia_ui.py', '.'), ('compress_ui.py', '.'), ('image_ui.py', '.'), ('redact_ui.py', '.'), ('rotate_ui.py', '.'), ('search_ui.py', '.'), ('split_ui.py', '.'), ('icona.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='PDFuture',
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
    icon=['icona.ico'],
)
