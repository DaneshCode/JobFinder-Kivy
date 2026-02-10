# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Job Finder Windows build
"""
import os
from pathlib import Path

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None

# Get the project root directory
PROJECT_ROOT = Path(SPECPATH)

# Collect all Python files
python_files = []
for folder in ['screens', 'components', 'database', 'utils']:
    folder_path = PROJECT_ROOT / folder
    if folder_path.exists():
        for py_file in folder_path.glob('*.py'):
            python_files.append((str(py_file), folder))

a = Analysis(
    ['main.py'],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[
        ('screens', 'screens'),
        ('components', 'components'),
        ('database', 'database'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'kivymd.uix.screen',
        'kivymd.uix.card',
        'kivymd.uix.button',
        'kivymd.uix.textfield',
        'kivymd.uix.label',
        'kivymd.uix.dialog',
        'kivymd.uix.navigationbar',
        'kivymd.uix.boxlayout',
        'kivymd.uix.scrollview',
        'kivymd.icon_definitions',
        'screens.welcome_screen',
        'screens.login_screen',
        'screens.register_screen',
        'screens.main_screen',
        'screens.job_detail_screen',
        'components.ad_banner',
        'components.job_card',
        'database.db_manager',
        'database.models',
        'utils.helpers',
    ],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='JobFinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here: 'assets/icon.ico'
)
