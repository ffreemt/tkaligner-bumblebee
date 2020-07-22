# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['tkaligner\\__main__.py'],
             pathex=['C:\\dl\\Dropbox\\mat-dir\\myapps\\pypi-projects\\tkaligner-bumblebee'],
             binaries=[],
             datas=[
                # (r'bee_aligner\bumblebee.pt', r'bee_aligner'),
                (r'tkaligner\align.ico', r'tkaligner'),
             ],
             hiddenimports=[
                'pickletools',
                "tkinter",
                # "tkaligner",
                # "bee_aligner",
                # "pandas",
                # "pandastable",
                # 'langid',
                # 'diskcache',
                # 'sacremoses',
                # 'joblib',
                # 'tqdm',
                # 'subword_nmt',
                # 'transliterate',
                # 'torch',
                # 'jieba',
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[
                "PyQt5",
                'PyQt4',
                'gtk',
                'PySide',
                "botocore",
             ],
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
          name='tkaligner-bumblebee',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tkaligner-bumblebee')
