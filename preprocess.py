import pandas as pd
import numpy as np
import os

# List of CSV files
files = ['Hem.csv', 'Chymo..csv', 'HSA.csv', 'Lys.csv', 'hum. IgG.csv', 'bov. IgG.csv']

# Initialize a dictionary to hold the dataframes
dfs = {}

# Define new_wavelength outside the loop
new_wavelength = np.arange(195, 301, 1)

for file in files:
    path = os.path.join('raw-data', file)
    # Load the CSV file
    df = pd.read_csv(path, header=None, names=['Wavelength', 'Absorption'])

    # Sort the dataframe by wavelength
    df = df.sort_values('Wavelength')

    # Reset the index after sorting
    df = df.reset_index(drop=True)

    # Interpolate at 2 nm intervals
    new_df = pd.DataFrame({'Wavelength': new_wavelength})
    new_df['Absorption'] = np.interp(new_wavelength, df['Wavelength'], df['Absorption'])
    new_df.to_csv(f'processed-data/{file}', index=False)

    # Store the new dataframe in the dictionary
    dfs[file] = new_df