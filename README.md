# Parking-Lot
Object-oriented implementation of parking-lot helping vehicles park and exit parking-lot, deviced as per user-defined specs.

# Tech used
Core language: Python3.7.3(64 bit)
Core libraries adapted: unittest, cmd(light use)

# Features
Project is built with object-oriented principles and effective design patterns providing extensibility and maintainability.

# Installation
Install python3.7.3: https://www.python.org/downloads/release/python-373/
- **sudo apt update**
- **sudo apt install python3.7**
- **python3.7 --version**
## Linux:
```
1. Download the source-code share as zip to any folder
2. Install unzip tool: 
    sudo apt install unzip
3. sudo unzip parking-lot-1.0.zip -d /path/to/destination-folder/
4. Set PYTHONPATH to project folder:
    export PYTHONPATH=/path/to/destination-folder/:$PYTHONPATH
```
# Tests
Perform unittests placed in **parking_lot/tests/** package.
## Linux:
```
cd /path/to/destination-folder/
python3 -m unittest tests/*
```

# How to use?
## command-line-prompt:

```
python3 command_line_prompt.py
```
*sample-commands:*
> - **create_parking_lot** *6*
> - **park** *KA-01-HH-1234 White*
> - **leave** *1*
> - **registration_numbers_for_cars_with_colour** *White*
> - **slot_numbers_for_cars_with_colour** *White*
> - **slot_number_for_registration_number** *KA-01-HH-1234*
> - **slot_number_for_registration_number** *MH-04-AY-1111*


## file based command execution:
```
python3 command_line_prompt.py
```
*target-command:*
> - **playback** *path/to/target-commands-file.txt*

# License
**MIT License**
