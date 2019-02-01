from distutils.core import setup
import setuptools

setup(name='Mario',
      version='0.1',
      package_dir={'': '.'},
      packages=setuptools.find_packages('.'),
      test_suite='pytest',
      tests_require=['Pytest'],
      )
