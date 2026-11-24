"""
Query for mosaics, MER, SPE and PHZ.
Check if products already exist, if not download products.
"""

import os
from argparse import ArgumentParser

from astroquery.esa.euclid import Euclid
print(Euclid.get_status_messages())

# Command line arguments
parser = ArgumentParser()
parser.add_argument('-l', '--login_file', help='File path containing login details')
parser.add_argument('-o', '--output_dir', help='Output directiory to download files to')
args = parser.parse_args()

Euclid.login(credentials_file=args.login_file)
os.makedirs(args.output_dir, exist_ok=True)

# Variables
tile_id = 102159484
schema = 'Q1_R1'
files = []

print('Querying...')

# Get file names for mosaics
q = f"""
SELECT *
FROM q1.mosaic_product
WHERE tile_index = {tile_id}
AND instrument_name IN ('NISP', 'VIS')
"""
tbl = Euclid.launch_job(q).get_results()
for row in tbl:
	files.append(row['file_name'])

# Get file names for MER, SPE and PHZ
for catalogue in ['q1.mer_final_catalogue', 'q1.spe_catalogue', 'q1.phz_catalogue']:
	q = f'SELECT * FROM {catalogue}'
	tbl = Euclid.launch_job(q).get_results()
	row = tbl[tbl['tile_index_list'] == f'({tile_id})']
	files.extend(row['file_name_list'][0][1:-1].split(', '))

# Download fits files if not already downloaded
print('Downloading...')
for file_name in files:
	path = os.path.join(args.output_dir, file_name)
	if os.path.exists(path):
		print(f'{file_name} already exists at {path}.')
	else:
		_ = Euclid.get_product(
			file_name=file_name,
			schema=schema,
			output_file=path
		)
		print(f'downloaded file to {path}')




