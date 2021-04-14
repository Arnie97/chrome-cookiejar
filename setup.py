import sys
from setuptools import setup, find_packages

requires = [
    'pycrypto>=2.6.1'
]

if sys.version_info < (3, 2):
    requires.append('futures==2.2')

setup(
    name='chrome_cookiejar',
    version='1.0',
    description=("Python module to load cookies from Google Chrome browser"),
    url='https://github.com/Arnie97/chrome-cookiejar',
    author='Arnie97',
    license='Public domain',
    packages=find_packages(exclude=['tests']),
    install_requires=requires
)
