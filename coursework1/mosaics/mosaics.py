import os
import random
from astropy.io import fits
from astropy.visualization import ImageNormalize, PercentileInterval, AsinhStretch
import matplotlib.pyplot as plt


path = './data/EUC_MER_BGSUB-MOSAIC-VIS_TILE102159484-116033_20241025T015934.885975Z_00.00.fits'
out_dir = 'outputs/first_plots'
slice_size = 500 # pixels
with fits.open(path, memmap=True) as hdul:
    shape = hdul[0].shape
    assert shape[0] == shape[1], f'Image has shape {shape} but should be square.'

    # Slice a random 500x500 pixel slice
    start = random.randint(0, shape[0]-slice_size)
    cutout = hdul[0].section[start:start+slice_size, start:start+slice_size]

norm = ImageNormalize(
    cutout,
    interval=PercentileInterval(99.0),
    stretch=AsinhStretch()
)

fig, ax = plt.subplots(1, 1, figsize=(10,10))
ax.imshow(cutout, norm=norm, cmap='grey')
fig.savefig(os.path.join(out_dir, 'VIS_cutout.png'), dpi=300, bbox_inches='tight')

