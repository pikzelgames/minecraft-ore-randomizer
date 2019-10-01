import numpy as np
import sys
import json
from PIL import Image
import os
import time
import getopt

VERSION = '0.3.1'

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
    options, arguments = getopt.getopt(sys.argv[1:], 'hl:nop:s:S:v', ['help',  'legend=', 'no-image', 'original-size', 'preset=', 'save=', 'seed=', 'version'])
except getopt.GetoptError:
    error('Usage: generator.py [options]\nFor a list of options, use -h', 2)

preset = {}
save_location = None
show_image = True
original_size = False

for option, argument in options:
    if option in ('-h', '--help'):
        with open('cmd-help.txt', 'r') as file:
            print(file.read())
            sys.exit(0)
    elif option in ('-l', '--legend'):
        legend = json.load(open('options-legend.json'))
        if argument in list(legend['keys'].keys()):
            print(legend['keys'][argument])
            sys.exit(0)
        else:
            error('Specified parameter does not exist in legend!', 2)
    elif option in ('-n', '--no-image'):
        show_image = False
    elif option in ('-o', '--original-size'):
        original_size = True
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
        if not os.path.exists(argument) or os.path.isfile(argument):
            os.mkdir(argument)
        if sum([int(file in os.listdir(argument)) for file in ('combined-textures.png', 'ore.png', 'refined-item.png', 'refined-block.png', 'info.json')]) == 0:
            save_location = argument
        else:
            while True:
                user_input = input('Files would be overwritten in the save location? Do you want to continue? (y/n) ')
                if user_input.lower() == 'y':
                    save_location = argument
                    break
                elif user_input.lower() == 'n':
                    print('Exiting...')
                    sys.exit(0)
                else:
                    print('Invalid input')
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

if not original_size:
    ore_texture = ore_texture.resize((512, 512))
    refined_item_texture = refined_item_texture.resize((512, 512))
    refined_block_texture = refined_block_texture.resize((512, 512))

if original_size:
    size = 16
else:
    size = 512

combined_image = Image.new('RGBA', (size * 3, size), color=(255, 255, 255, 255))
combined_image.paste(ore_texture, (0, 0), ore_texture)
combined_image.paste(refined_item_texture, (size, 0), refined_item_texture)
combined_image.paste(refined_block_texture, (size * 2, 0), refined_block_texture)
if show_image:
    combined_image.show()

if save_location != None:
    combined_image.save(os.path.join(save_location, 'combined-textures.png'))
    ore_texture.save(os.path.join(save_location, 'ore.png'))
    refined_item_texture.save(os.path.join(save_location, 'refined-item.png'))
    refined_block_texture.save(os.path.join(save_location, 'refined-block.png'))
    json.dump(properties, open(os.path.join(save_location, 'info.json'), 'w'), sort_keys=True, indent=4)