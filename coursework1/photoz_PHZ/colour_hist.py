import os 
from astropy.io import fits
import matplotlib.pyplot as plt

os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np

path = './data/EUC_PHZ_PHZCAT__20241120T003850.158262Z_00.00.fits'
out_dir = 'outputs/first_plots'

with fits.open(path, memmap=True) as hdu:
    data = hdu[1].data
    Y = data['FLUX_Y_UNIF']
    H = data['FLUX_H_UNIF']

c = Y/H
mask = np.isfinite(c)
color = c[mask]

fig, ax = plt.subplots(1, 1, figsize=(8,8))
ax.hist(
    color,
    bins=500,
    range=(np.percentile(color, 0.5), np.percentile(color, 99.5))
)
ax.set_xlabel('Y/H')
ax.set_ylabel('Count')
ax.set_title('Flux Ratio Distribution')
fig.savefig(os.path.join(out_dir, 'color_hist.png'), bbox_inches='tight')
