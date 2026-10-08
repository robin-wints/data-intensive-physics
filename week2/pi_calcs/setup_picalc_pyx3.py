from setuptools import setup
from Cython.Build import cythonize

setup(name="picalc_pyx3",
      ext_modules=cythonize("picalc_pyx3.pyx"))

