# BlueSkyUtils

...

***This software is provided for research purposes only. Use at own risk.***

## Python 2 and 3 Support

The code in package was originally developed to support python 2.7, but
has since been refactored to support 3.5. Attempts to support both 2.7
and 3.5 have been made but are not guaranteed.

## Non-python Dependencies

Whether cloning the repo or installing with pip, if you'll be using
blueskyutils to generate single point graphs from bluesky output,
you'll first need to manually install gdal, and netcdf, which
blueskyutils depends on.

On a mac, you can do so with [Homebrew](http://brew.sh/):

    brew install homebrew/science/netcdf
    brew install gdal --with-netcdf --enable-unsupported

Note that the '--with-netcdf' option is required to build gdal with the
netCDF driver. See http://trac.osgeo.org/gdal/wiki/NetCDF for more information.

On ubuntu, the following should be sufficient:

    sudo apt-get install libnetcdf-dev
    sudo apt-get install python-gdal
    sudo apt-get install libgdal1-1.7.0

You may also need to install libffi-dev on ubuntu:

    sudo apt-get install libffi-dev

## Development

### Clone Repo

Via ssh:

    git clone git@github.com:pnwairfire/blueskyutils.git

or http:

    git clone https://github.com/pnwairfire/blueskyutils.git

### Install Dependencies

After installing the non-python dependencies (mentioned above), run the
following to install required python packages:

    pip install -r requirements.txt

### Setup Environment

To import blueskyutils in development, you'll have to add the repo root
directory to the search path. Some of the scripts bin do this automatically.

Another environmental variable that sometimes needs to be set, depending
on your platform, is DYLD_LIBRARY_PATH, which needs to include the directory
that contains libhdf5_hl.7.dylib, needed by netCDF4.  That can be set on
the command line, such as in the following:

    DYLD_LIBRARY_PATH=/path/to/hdf5-1.8.9-2/lib/ ./bin/extract_point_pm25_time_series.py
    DYLD_LIBRARY_PATH=/path/to/hdf5-1.8.9-2/lib/

## Running tests

First, install test-specific packages:

    pip install -r requirements-test.txt

Once installed, you can run tests with pytest:

    py.test
    py.test ./test/blueskyutils/bsf/dispersionnc_tests.py
    py.test ./test/blueskyutils/bsf/

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

Use the '-s' option to see output:

    py.test -s

## Installation

### Installing With pip

First, install pip (with sudo if necessary):

    apt-get install python-pip

Then, to install, for example, v0.1.0, use the following (with sudo if
necessary):

    pip install --trusted-host pypi.smoke.airfire.org -i http://pypi.smoke.airfire.org/simple blueskyutils==0.1.0

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

## Usage

Use the ```-h``` option to see the usage for each script in this package.
