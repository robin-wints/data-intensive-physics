import os
from astropy.io import fits
import astropy.units as u
import matplotlib.pyplot as plt
import seaborn as sns
from umap import UMAP
from sklearn.preprocessing import StandardScaler
import pandas as pd


path = 'data/EUC_MER_FINAL-CAT_TILE102159484-EF6D85_20241026T003047.133877Z_00.00.fits'
out_dir = 'outputs/photo_MER'
os.makedirs(out_dir, exist_ok=True)

with fits.open(path, memmap=True) as hdu:
    data = hdu[1].data
    ra = data['RIGHT_ASCENSION']
    dec = data['DECLINATION']

    # Star-gal sep and point like prob
    sg_sep = data['MAG_STARGAL_SEP']
    pl_prob = data['POINT_LIKE_PROB']

    # Magnitudes for colour indicies
    VIS = (data['FLUX_VIS_SERSIC'] * u.uJy).to(u.ABmag)
    Y = (data['FLUX_Y_SERSIC'] * u.uJy).to(u.ABmag)
    J = (data['FLUX_J_SERSIC'] * u.uJy).to(u.ABmag)
    H = (data['FLUX_H_SERSIC'] * u.uJy).to(u.ABmag)
    U = (data['FLUX_U_EXT_DECAM_SERSIC'] * u.uJy).to(u.ABmag)
    G = (data['FLUX_G_EXT_DECAM_SERSIC'] * u.uJy).to(u.ABmag)
    R = (data['FLUX_R_EXT_DECAM_SERSIC'] * u.uJy).to(u.ABmag)
    I = (data['FLUX_Z_EXT_DECAM_SERSIC'] * u.uJy).to(u.ABmag)
    Z = (data['FLUX_Z_EXT_DECAM_SERSIC'] * u.uJy).to(u.ABmag)

# Sky Density plot
fig, ax = plt.subplots(1,1,figsize=(10,8))
hb = ax.hexbin(ra, dec, bins='log')
ax.set_xlabel('RA (deg)')
ax.set_ylabel('Dec (deg)')
fig.colorbar(hb, ax=ax, label='log(count)')
ax.set_title('HexBin Sky Density Plot')
fig.savefig(os.path.join(out_dir, 'hexbin_skyplot.png'), bbox_inches='tight')

# KDE Sky Density Plot
fig, ax = plt.subplots(1,1,figsize=(10, 8))
sns.kdeplot(
    x=ra,
    y=dec,
    fill=True,
    cmap='viridis',
    cbar=True,
    ax=ax
)
ax.set_xlabel('RA (deg)')
ax.set_ylabel('Dec (deg)')
ax.set_title('KDE Sky Density Plot')
fig.savefig(os.path.join(out_dir, 'kde_skyplot.png'), bbox_inches='tight')

# Star-Galaxy Separation vs Point-Like Probability
fig, ax = plt.subplots(1,1,figsize=(10, 8))
ax.scatter(sg_sep, pl_prob, s=3, alpha=0.25)
ax.set_xlabel('Star-Galaxy Separation')
ax.set_ylabel('Point-Like Probability')
fig.savefig(os.path.join(out_dir, 'sg_sepVSpl_prob.png'), bbox_inches='tight')

# Colour Index Information
types = [
    ('u-g', (U, G)), # bluer/UV
    ('g-r', (G, R)), # optical/bluer
    ('r-i', (R, I)), # optical/redder
    ('i-z', (I, Z)), # redder
    ('z-y', (Z, Y)), # optical/NIR
    ('y-j', (Y, J)), # NIR
    ('j-h', (J, H)), # NIR
    ('vis-y', (VIS, Y)), # optical/NIR
    ('g-h', (G, H)), # longer diff
    ('i-h', (I, H)) #longer diff
]

colors = {}
for t in types:
    colors[t[0]] = t[1][0] - t[1][1]

fig, ax = plt.subplots(1,1,figsize=(10, 8))
ax.scatter(colors['u-g'], colors['i-z'], alpha=0.25)
ax.set_xlabel('u-g colour index')
ax.set_ylabel('i-z colour index')
os.makedirs(os.path.join(out_dir, 'color_index'), exist_ok=True)
fig.savefig(os.path.join(out_dir, 'color_index', 'u_gVSi_z.png'), bbox_inches='tight')

fig, ax = plt.subplots(1,1,figsize=(10, 8))
ax.scatter(colors['vis-y'], colors['y-j'], s=3, alpha=0.25)
ax.set_xlabel('vis-y colour index')
ax.set_ylabel('y-j colour index')
fig.savefig(os.path.join(out_dir, 'color_index', 'vis_yVSy_j.png'), bbox_inches='tight')

# Umap on color information
reducer = UMAP()

df = pd.DataFrame(colors)
print('Number of instances before cleaning:', len(df))
print('Number of color indexes before cleaning:', len(df.columns))
# Remove columns if every entry is NaN and then drop rows with a NaN in them.
df_clean = df.dropna(axis=1, how='all').dropna(axis=0)
print('Number of instances after cleaning:', len(df_clean))
print('Number of color indexes after cleaning:', len(df_clean.columns))
print('Columns:', df_clean.columns)
scaled_colors = StandardScaler().fit_transform(df_clean)

embedding = reducer.fit_transform(scaled_colors)

fig, ax = plt.subplots(1,1,figsize=(10, 8))
ax.scatter(embedding[:, 0], embedding[:, 1], s=3, alpha=0.25)
ax.set_xlabel('UMAP dim 1')
ax.set_ylabel('UMAP dim 2')
ax.set_title('UMAP Embedding of the Colour Index Information')
fig.savefig(os.path.join(out_dir, 'color_index', 'umap.png'), bbox_inches='tight')

# Fraction of NaNs in each column
missing_fraction = df.isna().mean()

# NaNs plot
fig, ax = plt.subplots(1,1,figsize=(10, 8))
ax.bar(df.columns, missing_fraction)
ax.set_xlabel('Column')
ax.set_ylabel('NaN fraction')
ax.tick_params(axis='x', rotation=90)
fig.savefig(os.path.join(out_dir, 'color_index', 'nans.png'), bbox_inches='tight')
