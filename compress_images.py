# -*- coding: utf-8 -*-
"""
Compress images ro reduce file size.

Download the photos folder from Drive and place this .py in the same directory.
Rename the 'folder' variable with the folder name.
Test which quality should be used,
consider file size and time to load on field scan.

@author: Eduardo Pelanda
"""

import os
import pandas as pd
from PIL import Image

# %% name of the directory with subfolders and photos
folder = 'imagens_360_convertidas_resolução original'

# create new directory to save compressed files
new_folder = f'G:\\Drives compartilhados\\Modec\\MV30\\fotos_embarque_2024\\imagens_360_convertidas_para_scan_points\\{folder} compressed'


def create_path(path):
    """Receive a directory path (single folder or folder and subfolders),
    and create it if not exists."""
    if not os.path.exists(path):
        os.makedirs(path)


# %%


def compress_image(filepath, new_filepath, quality=90):
    """Compress an image keeping the resolution"""
    image = Image.open(filepath)
    image = image.convert('RGB')
    image.save(new_filepath, "JPEG", optimize=True, quality=quality)


# %% folders and files loop
for root, dirs, files in os.walk(folder, topdown=True):
    for index, file in enumerate(files):
        filepath = os.path.join(root, file)
        new_root = root.replace(folder, new_folder, 1)
        create_path(new_root)
        new_filepath = os.path.join(new_root, file)
        compress_image(filepath, new_filepath)
        print(root.split('\\', 1)[1],
              f': {index + 1}/{len(files)}, {file}')

# %% create empty daframe with given columns
columns = ['path', 'file', 'extension', 'size', 'MB_in', 'MB_out']
df = pd.DataFrame(columns=columns)

for root, dirs, files in os.walk(new_folder, topdown=True):
    for index, file in enumerate(files):
        new_filepath = os.path.join(root, file)
        old_root = root.replace(' compressed', '')
        old_filepath = os.path.join(old_root, file)

        extension = os.path.splitext(new_filepath)[1].lower()
        size_mb_in = os.path.getsize(old_filepath) / (1024 * 1024)
        size_mb_out = os.path.getsize(new_filepath) / (1024 * 1024)
        image = Image.open(new_filepath)
        size_pixels = image.size

        dfi = pd.DataFrame([[root, file, extension, size_pixels,
                             size_mb_in, size_mb_out]], columns=columns)
        df = pd.concat([df, dfi])

df['path'] = df['path'].str.replace(f'{new_folder}\\', '', regex=False)
df['module'] = df['path'].str.split('\\').str[0]
df['MB_ratio'] = df['MB_out']/df['MB_in']
total_GB_in = df['MB_in'].sum() / 1024
total_GB_out = df['MB_out'].sum() / 1024
print(f'{total_GB_in = :.2f}')
print(f'{total_GB_out = :.2f}')

df.to_excel(f'photos_list_{folder}.xlsx', index=False)

# %% save spreadsheet with numbers of photos by module
pivot = df.groupby('module').size().reset_index(name='photos')

pivot.to_excel(f'photos_by_module_{folder}.xlsx', index=False)
