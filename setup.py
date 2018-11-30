from setuptools import setup, find_packages

from cache_utils import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='cache-utils',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/kornov-rooman/cache-utils',
    license='MIT',
    author='Kornov Rooman',
    author_email='kornov.rooman@gmail.com',
    description='',
    long_description=long_description,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    requires=[]
)
