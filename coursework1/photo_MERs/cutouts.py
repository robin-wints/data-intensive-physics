import os 
import random
from pathlib import Path
from argparse import ArgumentParser
from astropy.io import fits 
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.nddata import Cutout2D
from astropy.wcs import WCS

from mosaics.mosaics import grid_plot, rgb_plot, single_plot

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-N', default='1', help='Number of cutouts to plot')
    args = parser.parse_args()

    i=1
    while i <= int(args.N):
        path = 'data/EUC_MER_FINAL-CUTOUTS-CAT_TILE102159484-73BCF1_20241025T145359.184204Z_00.00.fits'
        paths = Path('./data').glob(f'*MOSAIC*')
        out_dir = f'outputs/cutouts/cutout_{i}'
        os.makedirs(out_dir, exist_ok=True)

        # Obtain central coordinates and corners
        with fits.open(path, memmap=True) as hdu:
            data = hdu[1].data
            idx = random.randint(0, len(data))
            ra = data[idx]['RIGHT_ASCENSION']
            dec = data[idx]['DECLINATION']
            ras = [
                data[idx]['CORNER_0_RA'],
                data[idx]['CORNER_1_RA'],
                data[idx]['CORNER_2_RA'],
                data[idx]['CORNER_3_RA']
            ]
            decs = [
                data[idx]['CORNER_0_dec'],
                data[idx]['CORNER_1_dec'],
                data[idx]['CORNER_2_dec'],
                data[idx]['CORNER_3_dec']
            ]

        centre = SkyCoord(ra*u.deg, dec*u.deg)
        width = (max(ras) - min(ras)) * u.deg
        height = (max(decs) - min(decs)) * u.deg

        # Get cutouts for each band
        # Here I assume the WCS' might be different for each band.
        # It could be worth checking if they are the same to speed up obtaining
        # cutouts in a potential future pipeline.
        cutouts={}
        for path in paths:
            with fits.open(path, memmap=True) as hdu:
                wcs = WCS(hdu[0].header)
                cutout = Cutout2D(hdu[0].data, centre, (height, width), wcs=wcs, copy=True)
                band = path.name.split("MOSAIC-")[1].split("_TILE")[0]
                cutouts[band] = cutout.data

        # Plots
        grid_plot(cutouts, os.path.join(out_dir, 'cutout_bands.png'))
        rgb_plot(cutouts, os.path.join(out_dir, 'H-J-VIS-cutout.png'))
        single_plot(cutouts, 'VIS', os.path.join(out_dir,'VIS-cutout.png'))

        i+=1

