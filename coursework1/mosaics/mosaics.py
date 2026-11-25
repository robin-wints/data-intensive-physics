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

# Plot the 4 cutouts in a grid to compare
fig, axs = plt.subplots(2, 2, figsize=(12, 12))
for ax, (band, cutout) in zip(axs.ravel(), cutouts.items()):
    norm = ImageNormalize(
        cutout,
        interval=PercentileInterval(99.0),
        stretch=AsinhStretch()
    )
    ax.imshow(cutout, norm=norm, cmap='gray', origin='lower')
    ax.set_title(band)
    ax.set_axis_off()

fig.savefig(os.path.join(out_dir, 'cutout_bands.png'), dpi=300, bbox_inches='tight')

# Plot a fake rgb composite image.
fig, ax = plt.subplots(1, 1, figsize=(8,8))
rgb = make_lupton_rgb(
    cutouts['NIR-H'],
    cutouts['NIR-J'],
    cutouts['VIS'],
    interval=PercentileInterval(99.0),
    Q=10,
)
ax.imshow(rgb, origin='lower')
ax.set_title(f'{slice_size} x {slice_size} Pixel Composite Cutout (H-J-VIS)')
ax.set_axis_off()
fig.tight_layout()
fig.savefig(os.path.join(out_dir, 'H-J-VIS-cutout.png'), dpi=300, bbox_inches='tight')

# Plot just the VIS image
fig, ax = plt.subplots(1, 1, figsize=(8,8))
norm = ImageNormalize(
    cutouts['VIS'],
    interval=PercentileInterval(99.0),
    stretch=AsinhStretch()
)
ax.imshow(cutouts['VIS'], norm=norm, cmap='gray', origin='lower')
ax.set_title(f'{slice_size} x {slice_size} Pixel VIS Cutout')
ax.set_axis_off()
fig.tight_layout()
fig.savefig(os.path.join(out_dir, 'VIS-cutout.png'), dpi=300, bbox_inches='tight')