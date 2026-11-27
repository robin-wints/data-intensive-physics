import os
import random
from pathlib import Path
from astropy.io import fits
from astropy.visualization import ImageNormalize, PercentileInterval, AsinhStretch, make_lupton_rgb
import matplotlib.pyplot as plt

paths = Path('./data').glob(f'*MOSAIC*')
out_dir = 'outputs/mosaics'
os.makedirs(out_dir, exist_ok=True)

mosaic_size = 19_200 # Found in fits_test notebook
slice_size = 500 # pixels
y_0 = random.randint(0, mosaic_size-slice_size)
x_0 = random.randint(0, mosaic_size-slice_size)

# Get cutouts for each band
cutouts={}
for path in paths:
    with fits.open(path, memmap=True) as hdu:
        cutout = hdu[0].section[y_0:y_0+slice_size, x_0:x_0+slice_size]
        band = path.name.split("MOSAIC-")[1].split("_TILE")[0]
        cutouts[band] = cutout

# Define plots as functions so they can be reused in other scripts

# Plots the 4 bands in a grid to compare
def grid_plot(cutouts_dir, out_path):
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    for ax, (band, cutout) in zip(axs.ravel(), cutouts_dir.items()):
        norm = ImageNormalize(
            cutout,
            interval=PercentileInterval(99.0),
            stretch=AsinhStretch()
        )
        ax.imshow(cutout, norm=norm, cmap='gray', origin='lower')
        ax.set_title(band)
        ax.set_axis_off()

    fig.savefig(out_path, dpi=300, bbox_inches='tight')

# Plots a fake rgb composite image, combining VIS, H and J.
def rgb_plot(cutouts_dir, out_path):
    size=len(cutouts_dir['VIS'])
    rgb = make_lupton_rgb(
        cutouts_dir['NIR-H'],
        cutouts_dir['NIR-J'],
        cutouts_dir['VIS'],
        interval=PercentileInterval(99.0),
        Q=10,
    )

    fig, ax = plt.subplots(1, 1, figsize=(8,8))
    ax.imshow(rgb, origin='lower')
    ax.set_title(f'{size} x {size} Pixel Composite Cutout (H-J-VIS)')
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')

# Plots the image for just one band
def single_plot(cutouts_dir, band, out_path):
    cutout = cutouts_dir[band]
    size= len(cutout) 
    norm = ImageNormalize(
        cutout,
        interval=PercentileInterval(99.0),
        stretch=AsinhStretch()
    )

    fig, ax = plt.subplots(1, 1, figsize=(8,8))
    ax.imshow(cutout, norm=norm, cmap='gray', origin='lower')
    ax.set_title(f'{size} x {size} Pixel {band} Cutout')
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')

grid_plot(cutouts, os.path.join(out_dir, 'cutout_bands.png'))
rgb_plot(cutouts, os.path.join(out_dir, 'H-J-VIS-cutout.png'))
single_plot(cutouts, 'VIS', os.path.join(out_dir,'VIS-cutout.png'))



