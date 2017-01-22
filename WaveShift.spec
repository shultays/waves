# -*- mode: python -*-

block_cipher = None


a = Analysis(['WaveShift.py'],
             pathex=['C:\\Users\\Twn015\\Desktop\\t'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='WaveShift',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='ship_big.ico')
