from setuptools import setup, find_packages

from blueskyutils import __version__

test_requirements = []
with open('requirements-test.txt') as f:
    test_requirements = [r for r in f.read().splitlines()]

setup(
    name='blueskyutils',
    version=__version__,
    license='GPLv3+',
    author='Joel Dubowy',
    author_email='jdubowy@gmail.com',
    packages=find_packages(),
    scripts=[
        'bin/extract-point-pm25-time-series',
        'bin/merge-emissions',
        'bin/merge-fires',
        'bin/process-bluesky-kmz',
        'bin/run-bluesky'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.5",
        "Operating System :: POSIX",
        "Operating System :: MacOS"
    ],
    url='https://github.com/pnwairfire/blueskyutils',
    description='BlueSky python utilities for AirFire team.',
    install_requires=[
        "pyairfire>=1.2.0,<2.0.0",
        "xmltodict==0.10.2",
        "netCDF4==1.2.4"
    ],
    dependency_links=[
        "https://pypi.smoke.airfire.org/simple/pyairfire/"
    ],
    tests_require=test_requirements
)
