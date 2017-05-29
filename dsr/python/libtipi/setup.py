
from distutils.core import setup, Extension

moduletipi = Extension('tipiports', sources = ['tipiports.c'], libraries = ['wiringPi'] )

setup (name = 'tipiports', version = '1.0', description = 'low level tipi io', ext_modules = [moduletipi])


