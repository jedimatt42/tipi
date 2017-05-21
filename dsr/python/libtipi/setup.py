
from distutils.core import setup, Extension

moduletipi = Extension('tipiports', sources = ['tipiports.c'])

setup (name = 'tipiports', version = '1.0', description = 'low level tipi io', ext_modules = [moduletipi])


