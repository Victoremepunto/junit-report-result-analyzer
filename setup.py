from setuptools import setup

setup(
  name='check-junit-results',
  version='0.1.0',
  py_modules=['main'],
  install_requires=[
      'Click',
      'junitparser'
  ],
  entry_points={
    'console_scripts': [
        'check-junit-results = main:cli',
    ],
  },
)
