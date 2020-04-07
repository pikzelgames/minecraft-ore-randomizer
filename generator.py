import numpy as np
import sys
import json
from PIL import Image
import os
import time
import getopt

VERSION = '0.3.2'

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


base_block_tool_key = {'stone': 'pickaxe', 'sand': 'shovel', 'dirt': 'shovel', 'netherrack': 'pickaxe', 'gravel': 'shovel', 'andesite': 'pickaxe', 'diorite': 'pickaxe', 'granite': 'pickaxe'}
properties['harvest-tool'] = base_block_tool_key[properties['ore-base-block']]

properties['colour-rgba'] = (properties['colour'][0], properties['colour'][1], properties['colour'][2], 0)
solid_colour = Image.new('RGB', (16, 16), color=(properties['colour-rgba']))

if properties['ore-base-block'] == 'netherrack':
    properties['spawning-rules'] = 'quartz'

if properties['minimum-tool-level'] == 'level-below':
    properties['minimum-tool-level'] = properties['tool-harvesting-level'] - 1


ore_base_block_img = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-base-blocks', properties['ore-base-block'] + '.png'))

ore_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-masks', properties['ore-mask'] + '.png'))
ore_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-silhouettes', properties['ore-mask'] + '.png'))

refined_item_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-item-masks', properties['refined-item-mask'] + '.png'))
refined_item_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-item-silhouettes', properties['refined-item-mask'] + '.png'))

refined_block_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-block-masks', properties['refined-block-mask'] + '.png'))
refined_block_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'refined-block-silhouettes', properties['refined-block-mask'] + '.png'))

sword_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-masks', 'sword.png'))
sword_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-silhouettes', 'sword.png'))

pickaxe_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-masks', 'pickaxe.png'))
pickaxe_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-silhouettes', 'pickaxe.png'))

axe_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-masks', 'axe.png'))
axe_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-silhouettes', 'axe.png'))

shovel_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-masks', 'shovel.png'))
shovel_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'tool-silhouettes', 'shovel.png'))

helmet_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'helmet.png'))
helmet_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'helmet.png'))

chestplate_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'chestplate.png'))
chestplate_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'chestplate.png'))

leggings_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'leggings.png'))
leggings_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'leggings.png'))

boots_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'boots.png'))
boots_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'boots.png'))

armour_layer_1_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'layer1.png'))
armour_layer_1_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'layer1.png'))

armour_layer_2_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-masks', 'layer2.png'))
armour_layer_2_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'armour-silhouettes', 'layer2.png'))


ore_texture = ore_base_block_img
ore_overlay = Image.composite(solid_colour, ore_silhouette, ore_mask)
ore_texture.paste(ore_overlay, (0, 0), ore_overlay)

refined_item_texture = Image.composite(solid_colour, refined_item_silhouette, refined_item_mask)

refined_block_texture = Image.composite(solid_colour, refined_block_silhouette, refined_block_mask)

sword_texture = Image.composite(solid_colour, sword_silhouette, sword_mask)

pickaxe_texture = Image.composite(solid_colour, pickaxe_silhouette, pickaxe_mask)

axe_texture = Image.composite(solid_colour, axe_silhouette, axe_mask)

shovel_texture = Image.composite(solid_colour, shovel_silhouette, shovel_mask)

helmet_texture = Image.composite(solid_colour, helmet_silhouette, helmet_mask)

chestplate_texture = Image.composite(solid_colour, chestplate_silhouette, chestplate_mask)

leggings_texture = Image.composite(solid_colour, leggings_silhouette, leggings_mask)

boots_texture = Image.composite(solid_colour, boots_silhouette, boots_mask)

armour_layer_1_texture = Image.composite(solid_colour.resize((64, 32)), armour_layer_1_silhouette, armour_layer_1_mask)

armour_layer_2_texture = Image.composite(solid_colour.resize((64, 32)), armour_layer_2_silhouette, armour_layer_2_mask)


if not original_size:
    ore_texture = ore_texture.resize((512, 512))
    refined_item_texture = refined_item_texture.resize((512, 512))
    refined_block_texture = refined_block_texture.resize((512, 512))
    
    sword_texture = sword_texture.resize((512, 512))
    pickaxe_texture = pickaxe_texture.resize((512, 512))
    axe_texture = axe_texture.resize((512, 512))
    shovel_texture = shovel_texture.resize((512, 512))

    helmet_texture = helmet_texture.resize((512, 512))
    chestplate_texture = chestplate_texture.resize((512, 512))
    leggings_texture = leggings_texture.resize((512, 512))
    boots_texture = boots_texture.resize((512, 512))

    armour_layer_1_texture = armour_layer_1_texture.resize((2048, 1024))
    armour_layer_2_texture = armour_layer_2_texture.resize((2048, 1024))



if original_size:
    size = 16
else:
    size = 512


combined_image = Image.new('RGBA', (size * 4, size * 7), color=(255, 255, 255, 255))

combined_image.paste(ore_texture, (int(size * 0.5), 0), ore_texture)
combined_image.paste(refined_item_texture, (int(size * 1.5), 0), refined_item_texture)
combined_image.paste(refined_block_texture, (int(size * 2.5), 0), refined_block_texture)

combined_image.paste(sword_texture, (0, size * 1), sword_texture)
combined_image.paste(pickaxe_texture, (size, size * 1), pickaxe_texture)
combined_image.paste(axe_texture, (size * 2, size * 1), axe_texture)
combined_image.paste(shovel_texture, (size * 3, size * 1), shovel_texture)

combined_image.paste(helmet_texture, (0, size * 2), helmet_texture)
combined_image.paste(chestplate_texture, (size, size * 2), chestplate_texture)
combined_image.paste(leggings_texture, (size * 2, size * 2), leggings_texture)
combined_image.paste(boots_texture, (size * 3, size * 2), boots_texture)

combined_image.paste(armour_layer_1_texture, (0, size * 3), armour_layer_1_texture)

combined_image.paste(armour_layer_2_texture, (0, size * 5), armour_layer_2_texture)


if show_image:
    combined_image.show()


if save_location != None:
    combined_image.save(os.path.join(save_location, 'combined-textures.png'))

    ore_texture.save(os.path.join(save_location, 'ore.png'))
    refined_item_texture.save(os.path.join(save_location, 'refined-item.png'))
    refined_block_texture.save(os.path.join(save_location, 'refined-block.png'))

    sword_texture.save(os.path.join(save_location, 'sword.png'))
    pickaxe_texture.save(os.path.join(save_location, 'pickaxe.png'))
    axe_texture.save(os.path.join(save_location, 'axe.png'))
    shovel_texture.save(os.path.join(save_location, 'shovel.png'))

    helmet_texture.save(os.path.join(save_location, 'helmet.png'))
    chestplate_texture.save(os.path.join(save_location, 'chestplate.png'))
    leggings_texture.save(os.path.join(save_location, 'leggings.png'))
    boots_texture.save(os.path.join(save_location, 'boots.png'))
    
    armour_layer_1_texture.save(os.path.join(save_location, 'armour-layer-1.png'))
    armour_layer_2_texture.save(os.path.join(save_location, 'armour-layer-2.png'))

    json.dump(properties, open(os.path.join(save_location, 'info.json'), 'w'), sort_keys=True, indent=4)