import os
from astropy.io import fits
import matplotlib.pyplot as plt
import seaborn as sns

path = 'data/EUC_MER_FINAL-CAT_TILE102159484-EF6D85_20241026T003047.133877Z_00.00.fits'
out_dir = 'outputs/photo_MER'
os.makedirs(out_dir, exist_ok=True)

with fits.open(path, memmap=True) as hdu:
    data = hdu[1].data.copy()

# Sky Density plot
fig, ax = plt.subplots(1,1,figsize=(10,8))
hb = ax.hexbin(data['RIGHT_ASCENSION'], data['DECLINATION'], bins='log')
ax.set_xlabel('RA (deg)')
ax.set_ylabel('Dec (deg)')
fig.colorbar(hb, ax=ax, label='log')
ax.set_title('HexBin Sky Density Plot')
fig.savefig(os.path.join(out_dir, 'hexbin_skyplot.png'), bbox_inches='tight')

# KDE Sky Density Plot
fig, ax = plt.subplots(figsize=(10, 8))
sns.kdeplot(
    x=data['RIGHT_ASCENSION'],
    y=data['DECLINATION'],
    fill=True,
    cmap='viridis',
    cbar=True,
    ax=ax
)
ax.set_xlabel('RA (deg)')
ax.set_ylabel('Dec (deg)')
ax.set_title('KDE Sky Density Plot')
fig.savefig(os.path.join(out_dir, 'kde_skyplot.png'), bbox_inches='tight')

# Simple flux hist
flux = data['FLUX_VIS_SERSIC']
fig, ax = plt.subplots(figsize=(10, 8))
ax.hist(flux[flux > 0], bins=500, log=True)
ax.set_xscale('log')
ax.set_xlabel('Visible Sersic Flux')
ax.set_ylabel('Count')
fig.savefig('outputs/first_plots/flux_hist.png', bbox_inches='tight')

"""
A
"""