import numpy as np
import sys
import json
from PIL import Image
import os
import time
import getopt

VERSION = '0.2.4'

def error(msg, exit_code, wait_for_exit=False):
    print(msg)
    if wait_for_exit:
        input('Press ENTER to exit...')
    sys.exit(exit_code)

def choice(l):
    return l[np.random.randint(0, len(l))]

if 'venv' not in os.listdir():
    print('Core library files not detected! Make sure to run setup.bat for first-time setup, and make sure not to rename the "venv" folder! Exiting in 5 seconds...')
    time.sleep(5)
    sys.exit(1)

try:
    options, arguments = getopt.getopt(sys.argv[1:], 'hp:s:S:v', ['help', 'preset=', 'save=', 'seed=', 'version'])
except getopt.GetoptError:
    error('Usage: generator.py [options]\nFor a list of options, use -h', 2)

preset = {}
save_location = None

for option, argument in options:
    if option in ('-h', '--help'):
        with open('cmd-help.txt', 'r') as file:
            print(file.read())
            sys.exit(0)
    elif option in ('-p', '--preset'):
        if os.path.isfile(argument):
            if argument.endswith('.json'):
                with open(argument, 'r') as file:
                    preset = json.load(file)
            else:
                error('Preset file is not a JSON file!', 1)
        else:
            error('Preset file not found!', 2)
    elif option in ('-s', '--save'):
        if argument.endswith('.png'):
            save_location = argument
        else:
            error('Save filename does not end with .png!', 2)
    elif option in ('-S', '--seed'):
        try:
            if int(argument) >= 0 and int(argument) < 2**32:
                np.random.seed(int(argument))
            else:
                error('Seed is out of range!', 2)
        except ValueError:
            error('Seed is not a number!', 2)
    elif option in ('-v', '--version'):
        print('Minecraft Ore Randomizer v' + VERSION)
        sys.exit(0)

print(f'\nMINECRAFT ORE RANDOMIZER | VERSION {VERSION} | github.com/pikzelgames\n')

options = json.load(open('options.json', 'r'))
properties = {}

for k, v in options.items():
    if type(v) == list:
        if v[0] != 'range-inclusive':
            properties[k] = choice(v)
            if k in list(preset.keys()):
                if preset[k] in v:
                    properties[k] = preset[k]
                else:
                    error(f'Preset value is not an option at "{k}"!', 1)
        else:
            properties[k] = np.random.randint(v[1], v[2] + 1)
            if k in list(preset.keys()):
                if type(preset[k]) == int:
                    if preset[k] >= v[1] and preset[k] <= v[2]:
                        properties[k] == preset[k]
                    else:
                        error(f'Preset value out of range at "{k}"!', 1)
                else:
                    error(f'Incorrect preset value format at "{k}"!', 1)
    elif v == 'random-rgb':
        properties[k] = [np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)]
        if k in list(preset.keys()):
            if len(preset[k]) == 3:
                for value in preset[k]:
                    if type(value) == int:
                        if value >= 0 and value <= 255:
                            properties[k] = preset[k]
                        else:
                            error(f'Preset value out of range at "{k}"!', 1)
                    else:
                        error(f'Incorrect preset value format at "{k}"!', 1)
            else:
                error(f'Not enough preset RGB values at "{k}"!', 1)
    print(k + ': ', properties[k])

properties['colour-rgba'] = (properties['colour'][0], properties['colour'][1], properties['colour'][2], 0)
solid_colour = Image.new('RGB', (16, 16), color=(properties['colour-rgba']))

ore_base_block_img = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-base-blocks', properties['ore-base-block'] + '.png'))
ore_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-masks', properties['ore-mask'] + '.png'))
ore_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-silhouettes', properties['ore-mask'] + '.png'))
refined_item_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-item-masks', properties['refined-item-mask'] + '.png'))
refined_item_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-item-silhouettes', properties['refined-item-mask'] + '.png'))
refined_block_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-block-masks', properties['refined-block-mask'] + '.png'))
refined_block_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-block-silhouettes', properties['refined-block-mask'] + '.png'))

ore_texture = ore_base_block_img
ore_overlay = Image.composite(solid_colour, ore_silhouette, ore_mask)
ore_texture.paste(ore_overlay, (0, 0), ore_overlay)

refined_item_texture = Image.composite(solid_colour, refined_item_silhouette, refined_item_mask)

refined_block_texture = Image.composite(solid_colour, refined_block_silhouette, refined_block_mask)

combined_image = Image.new('RGBA', (1536, 512), color=(255, 255, 255, 255))
combined_image.paste(ore_texture.resize((512, 512)), (0, 0), ore_texture.resize((512, 512)))
combined_image.paste(refined_item_texture.resize((512, 512)), (512, 0), refined_item_texture.resize((512, 512)))
combined_image.paste(refined_block_texture.resize((512, 512)), (1024, 0), refined_block_texture.resize((512, 512)))
combined_image.show()

if save_location != None:
    combined_image.save(save_location)