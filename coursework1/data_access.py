from astroquery.esa.euclid import Euclid
Euclid.get_status_messages()

# Inspect table names
tables = Euclid.load_tables(only_names=True, include_shared_tables=True)
print(table.name for table in tables)

# Sample TILE ID
tile_id = 102159484

# Query
query = ""
job = Euclid.launch_job_async(query, verbose=False)
print(job)