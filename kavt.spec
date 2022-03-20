# -*- mode: python ; coding: utf-8 -*-
import os
import sysconfig
site_packages_path = sysconfig.get_paths()["purelib"]

block_cipher = None

a = Analysis(['kavt.py'],
             pathex=[os.path.join(site_packages_path, "paddleocr"), os.path.join(site_packages_path, "paddle", "libs")],
             binaries=[(os.path.join(site_packages_path, "paddle", "libs"), '.')],
             datas=[],
             hiddenimports=["skimage.filters.edges", "easyocr.model.vgg_model"],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=["matplotlib"],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='kavt',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='kavt')