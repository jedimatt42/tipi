from distutils.core import setup, Extension

moduletipi = Extension(
    'tipiports_gpio',
    sources=['tipiports.c'],
    extra_compile_args=['-O3'])

setup(
    name="tipiports_gpio",
    version="1.0",
    description="low level tipi io",
    ext_modules=[moduletipi],
)
