# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Main.py'],
             pathex=['C:\\Users\\viguv\\OneDrive\\Desktop\\FlappyBird'],
             binaries=[],
             datas=[('./Pipe.png','.'),('./Background.png','.'),('./Bird1.png','.'),('./Bird2.png','.'),('./Bird3.png','.'),('./Loading.png','.'),('./Lose.png','.'),('./Floor.png','.'),('./BGM.wav','.'),('./lose.wav','.'),('./score.wav','.'),('./LTEnergy.ttf','.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='Main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='Icon.ico')
