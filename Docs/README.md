# Overview

This folder contains the following elements:

- all infos about the mod in the folder `Infos`
- python scripts can be found in the folder `Tools`
- maps are located in the folder `Maps`

## Spawning maps

The colors on the spawning maps show the following stability areas:

- cyan: core area
- green: historically stable area
- yellow: potentially stable area
- red: outer area

## How to generate map images

The Python scripts `./Tools/map_renderer.py` parse a `WBSave` and generate differents maps.

This script need at least Python >= 3.9 and the dependencies located in the `requirements-dev.txt` file.

Exemple of usage:

```shell
python Docs/Tools/map_renderer.py -f ./PrivateMaps/RFCEurope\ 1200AD.CivBeyondSwordWBSave -d Docs/Maps --all
```

Here the full help message of the script.

```shell
usage: map_renderer.py [-h] [-f FILE] [-d DESTINATION] [--format {bmp,png}] [--rivers] [--features] [--terrains] [--bonuses] [--provinces] [--provinces-stability] [--all]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  WBSave to convert.
  -d DESTINATION, --destination DESTINATION
                        Destination folder.
  --format {bmp,png}    File saving format, ie. bmp or png. Default to png
  --rivers              Draw rivers map. Default to False.
  --features            Draw features map. Default to False.
  --terrains            Draw terrains map. Default to False.
  --bonuses             Draw bonuses map. Default to False.
  --provinces           Draw provinces map. Default to False
  --provinces-stability Draw provinces stability map. Default to True
  --all                 Draw all maps. Default to False.
```

## Map data converter

The old maps data was a python list of lists for each civ in a python module. They've been converted to csv files with the following similar command:

```shell
python Docs/Tools/map_csv_converter.py convert-civ-dict Assets/Python/data/maps/SettlerMapData.py SETTLERS_MAP
```

## Acknowledgements

The Python script for map rendering is an inspiration from [this post](https://forums.civfanatics.com/threads/wbs-to-bmp-converter.667302/).
