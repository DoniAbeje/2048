##import  os
##from cx_Freeze import*
###set TCL_LIBRARY and TK_LIBRARY
##
##os.environ['TCL_LIBRARY'] ='C:\\Users\\ROM K\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6'
##os.environ['TK_LIBRARY'] = 'C:\\Users\\ROM K\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6'
##
##setup(name='PGN', version='1.0.0', options={'build_exe':{'include_msvcr':True,}}, executables=[Executable('Game.py', base='win32GUI')])
from distutils.core import setup
import py2exe
import sys
data = [('img',['./img/icon.png']), ('font',['./font/hemi.ttf']), ('sound',['./sound/arrow.wav'])]
if len(sys.argv) == 1:
    sys.argv.append('py2exe')
setup(name='PGN', version='1.0.0', url="http://github.com/doniabeje", author="Doni Abeje", windows = [{'dest_base':'Game','script': 'Game.py', 'icon_resources': [[1, './Logo_256.ico']]}],data_files = data, options={'py2exe':{'compressed':True,'bundle_files':2, 'optimize':2}}, zipfile=None)
