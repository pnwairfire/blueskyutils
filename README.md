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

    pip install --extra-index https://pypi.airfire.org/simple -r requirements.txt
    pip install -r requirements-test.txt
    pip install -r requirements-dev.txt

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

Run tests with pytest:

    py.test
    py.test ./test/blueskyutils/netcdf/
    py.test ./test/blueskyutils/csv/test_merge.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

Use the '-s' option to see output:

    py.test -s

## Installation

### Installing With pip

First, install pip (with sudo if necessary):

    apt-get install python-pip

Then, to install, for example, v0.3.0, use the following (with sudo if
necessary):

    pip3 install --extra-index https://pypi.airfire.org/simple blueskyutils==0.3.0

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

## Usage

Use the ```-h``` option to see the usage for any script in this package.

### Filtering and Merging fires

There are two scripts for merging fire related csv data - ```merge-fires```
and ```merge-emissions```.

#### ```merge-emissions```

Suppose you have two BSF runs - one run for the US which contains mostly US
fires but also some CA fires nad one run for the CA which contains mostly CA
fires but also some US fires.  And suppose you want to take the US fires
from the US run and merge them with the CA fires from the CA run (i.e.
filter out the fires from the other country in each run).  Assume you have
the following files

    fire_locations_US.csv
    fire_events_US.csv
    fire_emissions_US.csv
    fire_locations_CA.csv
    fire_events_CA.csv
    fire_emissions_CA.csv

To create the files for this example, run the following.
(Note that the content is truncatedwhich are truncated for this example,
to make it easier to visually process):

```
echo "id,event_id,latitude,longitude,type,area,date_time,elevation,slope,state,county,country
SF11C2272827860649060,SF11E120330,50.236,-114.801,WF,91.9999997715,201508080000-07:00,0.0,10.0,,,CA
SF11C2272827860649060,SF11E120330,50.236,-114.801,WF,91.9999997715,201508090000-07:00,0.0,10.0,,,CA
SF11C2272827860649060,SF11E120330,50.236,-114.801,WF,91.9999997715,201508100000-07:00,0.0,10.0,,,CA
SF11C2272827860649060,SF11E120330,50.236,-114.801,WF,91.9999997715,201508110000-07:00,0.0,10.0,,,CA
SF11C2272837860649060,SF11E120916,48.903,-116.548,WF,1011.99999749,201508080000-07:00,0.0,10.0,ID,,USA
SF11C2272837860649060,SF11E120916,48.903,-116.548,WF,1011.99999749,201508090000-07:00,0.0,10.0,ID,,USA
SF11C2272837860649060,SF11E120916,48.903,-116.548,WF,1011.99999749,201508100000-07:00,0.0,10.0,ID,,USA
SF11C2272837860649060,SF11E120916,48.903,-116.548,WF,1011.99999749,201508110000-07:00,0.0,10.0,ID,,USA
SF11C2272847860649060,SF11E120916,48.923,-116.617,WF,91.9999997715,201508080000-07:00,0.0,10.0,ID,,USA
SF11C2272847860649060,SF11E120916,48.923,-116.617,WF,91.9999997715,201508090000-07:00,0.0,10.0,ID,,USA
SF11C2272847860649060,SF11E120916,48.923,-116.617,WF,91.9999997715,201508100000-07:00,0.0,10.0,ID,,USA
SF11C2272847860649060,SF11E120916,48.923,-116.617,WF,91.9999997715,201508110000-07:00,0.0,10.0,ID,,USA" \
> fire_locations_US.csv

echo "id,event_name,total_area
SF11E120330,\"Unnamed fire in Canada\",367.999999086
SF11E120916,\"Unnamed fire in Boundary County, Idaho\",400.999999086" \
> fire_events_US.csv

echo "fire_id,hour,ignition_date_time,date_time,area_fract,flame_profile,smolder_profile,residual_profile,pm25_emitted,pm10_emitted
SF11C2272827860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,0.306839,0.362069
SF11C2272827860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,0.306839,0.362069
SF11C2272837860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,3.375223,3.982763
SF11C2272837860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,3.375223,3.982763
SF11C2272847860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,0.306839,0.362069
SF11C2272847860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,0.306839,0.362069" \
> fire_emissions_US.csv


echo "id,event_id,latitude,longitude,type,area,date_time,elevation,slope,state,county,country
SF11C2272897860649060,SF11E123542,47.883,-117.613,WF,45.9999998858,201508080000-07:00,0.0,10.0,WA,,USA
SF11C2272897860649060,SF11E123542,47.883,-117.613,WF,45.9999998858,201508090000-07:00,0.0,10.0,WA,,USA
SF11C2272897860649060,SF11E123542,47.883,-117.613,WF,45.9999998858,201508100000-07:00,0.0,10.0,WA,,USA
SF11C2272897860649060,SF11E123542,47.883,-117.613,WF,45.9999998858,201508110000-07:00,0.0,10.0,WA,,USA
SF11C2272907860649060,SF11E123588,50.763,-117.703,WF,99.9999997516,201508080000-07:00,0.0,10.0,,,CA
SF11C2272907860649060,SF11E123588,50.763,-117.703,WF,99.9999997516,201508090000-07:00,0.0,10.0,,,CA
SF11C2272907860649060,SF11E123588,50.763,-117.703,WF,99.9999997516,201508100000-07:00,0.0,10.0,,,CA
SF11C2272907860649060,SF11E123588,50.763,-117.703,WF,99.9999997516,201508110000-07:00,0.0,10.0,,,CA
SF11C2272917860649060,SF11E123588,50.759,-117.732,WF,99.9999997516,201508080000-07:00,0.0,10.0,,,CA
SF11C2272917860649060,SF11E123588,50.759,-117.732,WF,99.9999997516,201508090000-07:00,0.0,10.0,,,CA
SF11C2272917860649060,SF11E123588,50.759,-117.732,WF,99.9999997516,201508100000-07:00,0.0,10.0,,,CA
SF11C2272917860649060,SF11E123588,50.759,-117.732,WF,99.9999997516,201508110000-07:00,0.0,10.0,,,CA" \
> fire_locations_CA.csv

echo "id,event_name,total_area
SF11E123542,\"Unnamed fire in USA\",234.34
SF11E123588,\"Unnamed fire in Canada\",545.343" \
> fire_events_CA.csv

echo "fire_id,hour,ignition_date_time,date_time,area_fract,flame_profile,smolder_profile,residual_profile,pm25_emitted,pm10_emitted
SF11C2272897860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,0.001301,0.001535
SF11C2272897860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,0.001301,0.001535
SF11C2272907860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,0.120195,0.14183
SF11C2272907860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,0.120195,0.14183
SF11C2272917860649060,0,201508080000-07:00,201508080000-07:00,0.0057,0.0057,0.0057,0.0057,0.428734,0.505906
SF11C2272917860649060,1,201508080000-07:00,201508080100-07:00,0.0057,0.0057,0.0057,0.0057,0.428734,0.505906" \
> fire_emissions_CA.csv
```

To get a merged set of files, you'd run

    merge-emissions \
        fire_emissions_US.csv:fire_events_US.csv:fire_locations_US.csv:USA \
        fire_emissions_CA.csv:fire_events_CA.csv:fire_locations_CA.csv:CA \
        -e fire_emissions_merged.csv \
        -v fire_events_merged.csv \
        -f fire_locations_merged.csv

And you'd end up with the following:

**fire_locations_merged.csv**

```
area,country,county,date_time,elevation,event_id,id,latitude,longitude,slope,state,type
1011.99999749,USA,,201508080000-07:00,0.0,SF11E120916,SF11C2272837860649060,48.903,-116.548,10.0,ID,WF
1011.99999749,USA,,201508090000-07:00,0.0,SF11E120916,SF11C2272837860649060,48.903,-116.548,10.0,ID,WF
1011.99999749,USA,,201508100000-07:00,0.0,SF11E120916,SF11C2272837860649060,48.903,-116.548,10.0,ID,WF
1011.99999749,USA,,201508110000-07:00,0.0,SF11E120916,SF11C2272837860649060,48.903,-116.548,10.0,ID,WF
91.9999997715,USA,,201508080000-07:00,0.0,SF11E120916,SF11C2272847860649060,48.923,-116.617,10.0,ID,WF
91.9999997715,USA,,201508090000-07:00,0.0,SF11E120916,SF11C2272847860649060,48.923,-116.617,10.0,ID,WF
91.9999997715,USA,,201508100000-07:00,0.0,SF11E120916,SF11C2272847860649060,48.923,-116.617,10.0,ID,WF
91.9999997715,USA,,201508110000-07:00,0.0,SF11E120916,SF11C2272847860649060,48.923,-116.617,10.0,ID,WF
99.9999997516,CA,,201508080000-07:00,0.0,SF11E123588,SF11C2272907860649060,50.763,-117.703,10.0,,WF
99.9999997516,CA,,201508090000-07:00,0.0,SF11E123588,SF11C2272907860649060,50.763,-117.703,10.0,,WF
99.9999997516,CA,,201508100000-07:00,0.0,SF11E123588,SF11C2272907860649060,50.763,-117.703,10.0,,WF
99.9999997516,CA,,201508110000-07:00,0.0,SF11E123588,SF11C2272907860649060,50.763,-117.703,10.0,,WF
99.9999997516,CA,,201508080000-07:00,0.0,SF11E123588,SF11C2272917860649060,50.759,-117.732,10.0,,WF
99.9999997516,CA,,201508090000-07:00,0.0,SF11E123588,SF11C2272917860649060,50.759,-117.732,10.0,,WF
99.9999997516,CA,,201508100000-07:00,0.0,SF11E123588,SF11C2272917860649060,50.759,-117.732,10.0,,WF
99.9999997516,CA,,201508110000-07:00,0.0,SF11E123588,SF11C2272917860649060,50.759,-117.732,10.0,,WF
```

**fire_events_merged.csv**

```
event_name,id,total_area
"Unnamed fire in Boundary County, Idaho",SF11E120916,400.999999086
Unnamed fire in Canada,SF11E123588,545.343
```

**fire_emissions_merged.csv**

```
area_fract,date_time,fire_id,flame_profile,hour,ignition_date_time,pm10_emitted,pm25_emitted,residual_profile,smolder_profile
0.0057,201508080000-07:00,SF11C2272837860649060,0.0057,0,201508080000-07:00,3.982763,3.375223,0.0057,0.0057
0.0057,201508080100-07:00,SF11C2272837860649060,0.0057,1,201508080000-07:00,3.982763,3.375223,0.0057,0.0057
0.0057,201508080000-07:00,SF11C2272847860649060,0.0057,0,201508080000-07:00,0.362069,0.306839,0.0057,0.0057
0.0057,201508080100-07:00,SF11C2272847860649060,0.0057,1,201508080000-07:00,0.362069,0.306839,0.0057,0.0057
0.0057,201508080000-07:00,SF11C2272907860649060,0.0057,0,201508080000-07:00,0.14183,0.120195,0.0057,0.0057
0.0057,201508080100-07:00,SF11C2272907860649060,0.0057,1,201508080000-07:00,0.14183,0.120195,0.0057,0.0057
0.0057,201508080000-07:00,SF11C2272917860649060,0.0057,0,201508080000-07:00,0.505906,0.428734,0.0057,0.0057
0.0057,201508080100-07:00,SF11C2272917860649060,0.0057,1,201508080000-07:00,0.505906,0.428734,0.0057,0.0057
```

(Note that column order is not preserved.)

##### Running in two steps

In the situation where two agencies are running BSF, one agency in the USA and one in CA,
filtering may be done as a separate step from the merge.  Using the example files above,
The USA agency would run

    merge-emissions \
        fire_emissions_US.csv:fire_events_US.csv:fire_locations_US.csv:USA \
        -e fire_emissions_US_filtered.csv \
        -v fire_events_US_filtered.csv \
        -f fire_locations_US_filtered.csv

And the CA agency would run:

    merge-emissions \
        fire_emissions_CA.csv:fire_events_CA.csv:fire_locations_CA.csv:CA \
        -e fire_emissions_CA_filtered.csv \
        -v fire_events_CA_filtered.csv \
        -f fire_locations_CA_filtered.csv

Then, the two sets of files can be merged with:

    merge-emissions \
        fire_emissions_US_filtered.csv:fire_events_US_filtered.csv:fire_locations_US_filtered.csv \
        fire_emissions_CA_filtered.csv:fire_events_CA_filtered.csv:fire_locations_CA_filtered.csv \
        -e fire_emissions_merged.csv \
        -v fire_events_merged.csv \
        -f fire_locations_merged.csv

At this point, you'd have the same set of *_merged.csv files listed above.

## Docker

BlueSkyUtils is installed as part of the
[bluesky package](https://github.com/pnwairfire/bluesky/),
and so it is included in the
[bluesky docker image](https://hub.docker.com/r/pnwairfire/bluesky/).
To use it in docker, first install docker (see
https://docs.docker.com/engine/installation/linux/ubuntulinux/), and then
run something like the following (adjusting the command to point to your actual file directory
and file names, etc.):

    sudo docker run --rm -v /path/to/csv/files/:/files/ -w /files/ pnwairfire/bluesky \
        merge-emissions \
        fire_emissions_20160622.csv:fire_events_20160622.csv:fire_locations_20160622.csv:USA \
        -e fire_emissions_20160622_US.csv \
        -v fire_events_20160622_US.csv \
        -f fire_locations_20160622_US.csv
