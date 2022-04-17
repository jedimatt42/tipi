from distutils.core import setup, Extension

moduletipi = Extension(
    'tipiports_websocket',
    sources=['tipiports.c','websock.c','sha1/sha1.c'],
    extra_compile_args=['-O3'])

setup(
    name="tipiports_websocket",
    version="1.0",
    description="low level tipi io using websocket",
    ext_modules=[moduletipi],
)
