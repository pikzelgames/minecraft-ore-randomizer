import numpy as np
import sys
import json
from PIL import Image
import os
import time

if 'venv' not in os.listdir():
    print('Core library files not detected! Make sure to run setup.bat for first-time setup, and make sure not to rename the "venv" folder! Exiting in 5 seconds...')
    time.sleep(5)
    quit()

print('\nMINECRAFT ORE RANDOMIZER | VERSION 0.2.2 | github.com/pikzelgames\n')

options = json.load(open('options.json', 'r'))
properties = {}

if len(sys.argv) == 2:
    np.random.seed(int(sys.argv[1]))

def choice(l):
    return l[np.random.randint(0, len(l))]

for k, v in options.items():
    if type(v) == list:
        if v[0] != 'range-inclusive':
            properties[k] = choice(v)
        else:
            properties[k] = np.random.randint(v[1], v[2] + 1)
    elif v == 'random-rgb':
        properties[k] = [np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)]
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