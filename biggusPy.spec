# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['Release\\biggusFolder'],
    binaries=[],
    datas=[("elements", "BiggusMain/elements"), ("Menu", "BiggusMain/Menu"), ("graphicEngine", "BiggusMain/graphicEngine"), ("elements/Nodes/oldNodes", "BiggusMain/elements/Nodes/oldNodes"), ("elements/Nodes/oldNodes/openCvNode", "BiggusMain/elements/Nodes/oldNodes/openCvNode"), ("elements/Nodes/oldNodes/pyqt5Node", "BiggusMain/elements/Nodes/oldNodes/pyqt5Node"), ("elements/Nodes/oldNodes/PythonNodes", "BiggusMain/elements/Nodes/oldNodes/PythonNodes"), ("elements/Nodes/oldNodes/testNodes", "BiggusMain/elements/Nodes/oldNodes/testNodes"), ("elements/Plugs", "BiggusMain/elements/Plugs"), ("elements/Nodes/AbstractClass", "BiggusMain/elements/Nodes/AbstractClass"), ("elements/object", "BiggusMain/elements/object"), ("elements/tools", "BiggusMain/elements/tools"), ("BiggusMain/Menu", "BiggusMain/Menu"), ("BiggusMain/graphicEngine", "BiggusMain/graphicEngine"), ("BiggusMain/BiggusMain", "BiggusMain")],
    hiddenimports=['cv2', 'numpy', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QMultimedia', 'PyQt5.QtMultimediaWidgets],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='biggusPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir='biggusTemp\\',
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\aless\\OneDrive\\Desktop\\ArchivioPy\\biggusPy1.3.1\\Release\\biggusFolder\\imgs\\icon\\biggusIcon\\BiggusIcon.ico'],
)
