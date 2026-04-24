from setuptools import setup, Extension
import pybind11

stl_module = Extension(
    name='stlmodule',
    sources=['stlmodule.cpp'],
    include_dirs=[pybind11.get_include()],
    language='c++',
    extra_compile_args=['-std=c++11'],
)

setup(
    name='stlmodule',
    version='1.0',
    ext_modules=[stl_module],
)
