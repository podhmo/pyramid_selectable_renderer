import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    "pyramid"
    ]


setup(name='pyramid_selectable_renderer',
      version='0.0',
      description='using multi template on one view_config',
      long_description=open("readme.txt"), 
      author='podhmo',
      author_email='',
      url='',
      package_dir={'': '.'},
      packages=find_packages('.'),
      include_package_data=True,
      zip_safe=False,
      test_suite='src',
      install_requires = requires,
      entry_points = """
      """,
      )

