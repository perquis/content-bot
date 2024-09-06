from setuptools import setup

setup(
  name="briefify",
  version="0.0.1",
  py_modules=["main"],
  install_requires=[
        'Click',
  ],
  entry_points={
      'console_scripts': [
          'briefify = main:main'
      ]
  }
)