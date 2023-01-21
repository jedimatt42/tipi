from distutils.core import setup, Extension

moduletipi = Extension(
    'tipiports_chardev',
    sources=['tipiports.c'],
    extra_compile_args=['-O3'])

setup(
    name="tipiports_chardev",
    version="1.0",
    description="low level tipi io over kernel driver",
    ext_modules=[moduletipi],
)
