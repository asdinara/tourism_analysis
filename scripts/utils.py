#paths to all source files
DATA_PATH_MAIN = "../data/input/main/"
DATA_PATH_META = "../data/input/meta/"
DATA_PATH = "../data/input/"

#used for renaming dataframe fields
COLUMN_MAPPING_DICT = {
    'Region': 'region',
    'IncomeGroup': 'income_group',
    'SpecialNotes': 'special_notes',
    'Country Code': 'country_code',
    'Country Name': 'country_name',
    'Indicator Name': 'indicator_name',
    'Indicator Code': 'indicator_code',
    'Year': 'year',
    'Indicator Value': 'indicator_value'
}

#custom grouping for report level
INCOME = ['low income', 'lower middle income', 'middle income', 'high income', 'upper middle income']
AGGREGATES = ['world', 'euro area', 'european union']
DEMOGRAPHIC = ['early-demographic dividend', 'late-demographic dividend', 'pre-demographic dividend', 'post-demographic dividend']
