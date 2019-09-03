# Minecraft Ore Randomizer

This is a project inspired by Jay Exci's video [here](https://www.youtube.com/watch?v=CS5DQVSp058) on how infinite features could be added to Minecraft. The end goal for this project is to have a mod which allows you to have fully working and unique random ores naturally found in the world.

## Installation

- Download or clone this repository
- Run `setup.bat` to download the core library files ([click here](https://github.com/pikzelgames/filehosting/Minecraft%20Ore%20Randomizer/venv.zip)) (first-time setup)
- Run `generator.bat` to start the program

NOTE: The `setup.bat` and `generator.bat` files will only be usable on Windows systems. To use on other operating systems, follow these instructions:

For first time setup:

- Open a terminal
- Navigate to the repository directory
- Type `source setupvenv/bin/activate`
- Type `python setup.py`

To run the program:

- Open a terminal
- Navigate to the repository directory
- Type `source venv/bin/activate`
- Type `python generator.py`

## Known Issues

- If `refined-block-mask` is `iron`, the program produces a solid colour output for the refined block texture (block of x)

## Changelog

- 0.x
  - 0.1.x
    - 0.1.0
      - Initial commit
      - Created a generator that has 5 different random properties (1 currently unused)
      - Wrote a program to use that information to make both an ore texture and an 'ingot' texture randomly
    - 0.2.0
      - Added 33 more properties for a total of 38
      - Edited the program to make a texture for the 'Block of x'
      - Added an easy setup file to decrease the initial download size and set up any dependencies
      - Added a legend to explain the contents of `options.json`
