import requests
import zipfile
import os
import time
import sys

if 'venv.zip' in os.listdir() or 'venv' in os.listdir():
    print('You already have the core library files! Exiting in 5 seconds...')
    time.sleep(5)
    sys.exit(1)

print('Downloading core library files from GitHub (29.7MB)...', end=' ', flush=True)
response = requests.get('https://github.com/pikzelgames/filehosting/blob/master/Minecraft%20Ore%20Randomizer/venv.zip?raw=true')
with open('venv.zip', 'wb') as file:
    file.write(response.content)
print('Done')

print('Extracting core library files...', end=' ', flush=True)
with zipfile.ZipFile(open('venv.zip', 'rb')) as file:
    file.extractall()
print('Done')

print('\nFiles added: venv.zip\nFolders added: venv/\nDisk space change: +29.7MB')
print('Exiting in 5 seconds...')
time.sleep(5)
sys.exit(0)