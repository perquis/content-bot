from setuptools import setup

setup(
  name="contentbot",
  version="0.0.1",
  py_modules=[
    "main",
    "instructions",
    "prompts",
    "utils",
    "models"
    ],
  install_requires=[
        "Click",
        "html2text",
        "InquirerPy",
        "openai",
        "python-dotenv",
        "requests",
        "tqdm",
        "md2pdf"
  ],
  entry_points={
      'console_scripts': [
          'contentbot = main:main',
          'cbot = main:main'
      ]
  }
)