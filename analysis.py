import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.style as style

# Get a list of all CSV files in the 'processed-data' directory
files = os.listdir('processed-data')

# Constants
concentration = 0.05  # units mg ml-1
light_path_length = 0.341  # units cm

def generate_combined_df(files):
    # Initialize an empty dataframe to hold the combined data
    combined_df = pd.DataFrame()

    for file in files:
        # Load the CSV file
        df = pd.read_csv(f'processed-data/{file}')

        # If combined_df is empty, copy the 'Wavelength' column from df
        if combined_df.empty:
            combined_df['Wavelength'] = df['Wavelength']

        # Add the 'Absorption' column to combined_df
        # Use the file name (without the extension) as the column name
        column_name = os.path.splitext(file)[0]
        combined_df[column_name] = df['Absorption']

    # Calculate the mean and standard deviation of absorption at each wavelength
    combined_df['Mean Absorption'] = combined_df.iloc[:, 1:].mean(axis=1)
    combined_df['Absorption Std Dev'] = combined_df.iloc[:, 1:-1].std(axis=1)

    combined_df.to_csv('data-table.csv')
    return combined_df


combined_df = generate_combined_df(files)

def calculate_absorption_coefficient(df):
    def Beer_Lambert(A, c, l):
        return A / (l*c)

    # Create new column with absorption coefficient for mean absorption
    df['Mean Absorption Coefficient'] = Beer_Lambert(df['Mean Absorption'], concentration, light_path_length)

    # Error propagation for division in Beer-Lambert law
    # Assuming that errors in concentration and light path length are negligible compared to error in absorption
    df['Absorption Coefficient Std Dev'] = df['Absorption Std Dev'] / (light_path_length * concentration)

    return df

combined_df = calculate_absorption_coefficient(combined_df)


def plot_data(df):
    # Use an academic style for the plot
    style.use('seaborn-whitegrid')

    # Create a new figure
    plt.figure(figsize=(10, 6))

    # Plot the mean absorption coefficient with a line
    plt.plot(df['Wavelength'], df['Mean Absorption Coefficient'], color='black', label='Mean Absorption Coefficient')

    # Add a shaded region for the standard deviation
    plt.fill_between(df['Wavelength'],
                     df['Mean Absorption Coefficient'] - df['Absorption Coefficient Std Dev'],
                     df['Mean Absorption Coefficient'] + df['Absorption Coefficient Std Dev'],
                     color='gray', alpha=0.3, label='Standard Deviation')

    # Add labels and title
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Absorption Coefficient (ml mg-1 cm-1)')
    plt.title('Mean Protein Absorption Coefficient')

    # Add a legend
    plt.legend()

    plt.savefig('absorption-coefficient.png', dpi=300)

    # Show the plot
    plt.show()

# Call the function to plot the data
plot_data(combined_df)

