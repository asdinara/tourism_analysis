import pandas as pd
import os
import utils

def extract_dataframes_from_directory(directory, skiprows=None):
    """
    Extract dataframes from a given directory from CSV format files.

    Parameters:
    - directory (str): Path to the directory containing CSV files.
    - skiprows (int, optional): Number of rows to skip at the beginning. Defaults to None.

    Returns:
    - dict: A dictionary where keys are filenames and values are corresponding dataframes.
    """
    #create an empty dictionary for input files
    dataframes = {}
    #iterate over files in directory
    for csv_file in os.listdir(directory):
        if csv_file.endswith('.csv'):
            df_name = csv_file.split('.')[0]
            df = pd.read_csv(os.path.join(directory, csv_file), skiprows=skiprows)
            dataframes[df_name] = df
    return dataframes


def extract_main_dataframes(start_year=1995, end_year=2019):
    """
    Extract main dataframes with specified year columns.

    Parameters:
    - start_year (int): Starting year. Defaults to 1995.
    - end_year (int): Ending year. Defaults to 2019.

    Returns:
    - dict: A dictionary containing main dataframes with required columns.
    """
    year_columns = [str(year) for year in range(start_year, end_year + 1)]
    required_columns = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + year_columns

    main_dataframes = extract_dataframes_from_directory(utils.DATA_PATH_MAIN, skiprows=3)

    for key in main_dataframes:
        main_dataframes[key] = main_dataframes[key][required_columns]

    return main_dataframes


def extract_meta_dataframes():
    """
    Extract metadata dataframes and ISO country codes.

    Returns:
    - tuple: A tuple containing metadata dataframes and a list of ISO country codes.
    """
    meta_dataframes = extract_dataframes_from_directory(utils.DATA_PATH_META)
    iso_mapping = pd.read_csv(os.path.join(utils.DATA_PATH, 'iso_mapping.csv'))
    return meta_dataframes, iso_mapping['alpha-3'].tolist()


def merge_dataframes(main_df, meta_df, meta_columns):
    """
    Merge main and metadata dataframes on 'Country Code'.

    Parameters:
    - main_df (DataFrame): The main dataframe.
    - meta_df (DataFrame): The metadata dataframe.
    - meta_columns (list): List of metadata columns to keep.

    Returns:
    - DataFrame: A merged dataframe.
    """
    return main_df.merge(meta_df[meta_columns], on="Country Code", how="left", indicator=True)


def transform(main_dfs):
    """
    Transform main dataframes by merging with metadata and reshaping.

    Parameters:
    - main_dfs (dict): Dictionary containing main dataframes.

    Returns:
    - DataFrame: A transformed dataframe ready for analysis.
    """
    meta_dfs, iso_countries = extract_meta_dataframes()
    transformed_dfs = {}

    meta_columns = ['Region', 'IncomeGroup', 'SpecialNotes', 'Country Code']
    for key in main_dfs:
        metadata_key = f"metadata_country_{key}"
        if metadata_key in meta_dfs:
            transformed_dfs[key] = merge_dataframes(main_dfs[key], meta_dfs[metadata_key], meta_columns)

    tourism_df = pd.concat(transformed_dfs.values(), ignore_index=True)
    tourism_df = tourism_df[tourism_df['_merge'] != 'left_only']

    id_vars = ['Region', 'IncomeGroup', 'SpecialNotes', 'Country Code', 'Country Name', 'Indicator Name', 'Indicator Code']
    tourism_df = pd.melt(tourism_df, id_vars=id_vars, var_name="Year", value_name="Indicator Value")
    tourism_df.rename(columns=utils.COLUMN_MAPPING_DICT, inplace=True)

    tourism_df['report_view'] = tourism_df.apply(lambda row: classify_country(row, iso_countries), axis=1)
    return tourism_df

def classify_country(row, iso_countries):
    """
    Classify country based on name, region, or other criteria.

    Parameters:
    - row (Series): A row from a dataframe.
    - iso_countries (list): List of ISO country codes.

    Returns:
    - str: A classification label for the country.
    """
    country_name = row['country_name'].lower()
    if country_name in utils.INCOME:
        return 'income'
    if country_name in utils.AGGREGATES:
        return 'aggregates'
    if country_name in utils.DEMOGRAPHIC:
        return 'demographic'
    if row['country_code'] in iso_countries:
        return 'countries'    
    return 'other'

def load(df, output_path):
    """
    Save the transformed dataframe to a CSV file.

    Parameters:
    - df (DataFrame): The dataframe to save.
    - output_path (str): Path where the CSV file should be saved.
    """
    df.to_csv(output_path, index=False)