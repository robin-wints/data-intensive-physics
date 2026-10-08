from setuptools import setup
from Cython.Build import cythonize

setup(name="picalc_pyx1",
      ext_modules=cythonize("picalc_pyx1.pyx"))

