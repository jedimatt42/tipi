from distutils.core import setup, Extension

moduletipi = Extension(
    'tipiports',
    sources=['tipiports.c','websock.c','sha1/sha1.c'],
    libraries=['wiringPi'],
    extra_compile_args=['-O3'])

setup(
    name="tipiports",
    version="1.0",
    description="low level tipi io",
    ext_modules=[moduletipi],
)
