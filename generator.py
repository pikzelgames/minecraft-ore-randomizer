import numpy as np
import sys
import json
from PIL import Image
import os

options = json.load(open('options.json', 'r'))
properties = {}

if len(sys.argv) == 2:
    np.random.seed(int(sys.argv[1]))

def choice(l):
    return l[np.random.randint(0, len(l))]

for k, v in options.items():
    if type(v) == list:
        properties[k] = choice(v)
        print(k + ': ', properties[k])
    elif v == 'random-rgb':
        properties[k] = [np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)]

print('RGB: ' + str(properties['colour']))

properties['colour-rgba'] = (properties['colour'][0], properties['colour'][1], properties['colour'][2], 0)
solid_colour_img = Image.new('RGB', (16, 16), color=(properties['colour-rgba']))

base_block_img = Image.open(os.path.join(os.getcwd(), 'textures', 'base-blocks', properties['base-block'] + '.png'))
ore_type_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-masks', properties['ore-type'] + '.png'))
ore_type_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'ore-silhouettes', properties['ore-type'] + '.png'))
item_type_mask = Image.open(os.path.join(os.getcwd(), 'textures', 'item-masks', properties['item-type'] + '.png'))
item_type_silhouette = Image.open(os.path.join(os.getcwd(), 'textures', 'item-silhouettes', properties['item-type'] + '.png'))

ore_texture_img = base_block_img
ore_overlay_img = Image.composite(solid_colour_img, ore_type_silhouette, ore_type_mask)
ore_texture_img.paste(ore_overlay_img, (0, 0), ore_overlay_img)
ore_texture_img.resize((512, 512)).show()

item_texture_img = Image.composite(solid_colour_img, item_type_silhouette, item_type_mask)
item_texture_img.resize((512, 512)).show()