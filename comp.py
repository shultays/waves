from distutils.core import setup
import py2exe
import matplotlib

setup(console=['WaveShift.py'], 
data_files=matplotlib.get_py2exe_datafiles(),
options = {'py2exe': {'bundle_files': 1, 'compressed': True}}
)