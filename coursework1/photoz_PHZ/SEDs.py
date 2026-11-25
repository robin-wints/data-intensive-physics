import os 
import random
import math
from astropy.io import fits
import matplotlib.pyplot as plt

path = './data/EUC_PHZ_STARSED__20241120T003936.665995Z_00.00.fits'
out_dir = 'outputs/first_plots'

ws = []
fluxes = []
fluxerrs = []

with fits.open(path, memmap=True) as hdu:
    data = hdu[1].data
    data = data[data['PHZ_FLAGS']!=-1]
    idx = random.randint(0, len(data)-1) 

    # Get flux columns sorted by wavelength
    flux_cols = sorted(
        [col.name for col in data.columns if col.name.startswith("FLUX_")],
        key=lambda x: int(x.split('_')[1])
    )

    for col in flux_cols:
        _, w1, w2 = col.split('_')

        avg_w = (int(w1) + int(w2))/2
        f = data[idx][col]
        ferr = data[idx][f"FLUXERR_{w1}_{w2}"]
    if math.isfinite(f) and math.isfinite(ferr):
        ws.append(avg_w)
        fluxes.append(f)
        fluxerrs.append(ferr)

print(f"Number of wavelengths found: {len(ws)}")

fig, ax = plt.subplots(1, 1, figsize=(8,8))
ax.errorbar(
    ws,
    fluxes,
    yerr=fluxerrs,
    fmt='o-'
)

ax.set_xlabel('Mean Wavelength')
ax.set_ylabel('Flux')
fig.savefig(os.path.join(out_dir, 'SED.png'), bbox_inches='tight')