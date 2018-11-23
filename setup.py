from os import listdir
from setuptools import setup, find_packages

setup(
    name='askomig',
    version='0.1',
    description='Database migration tools for AskOmics',
    author='Xavier Garnier',
    author_email='xavier.garnier@irisa.fr',
    url='https://github.com/askomics/askomigr',
    download_url='https://github.com/askomics/askocli/archive/0.1.tar.gz',
    install_requires=['SPARQLWrapper'],
    packages=find_packages(),
    license='AGPL',
    platforms='Posix; MacOS X; Windows',
    scripts=['askomig'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ])
