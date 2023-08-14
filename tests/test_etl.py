import sys
sys.path.append('../scripts')  # Append path to the scripts directory

import unittest
from etl import extract_main_dataframes

class TestETL(unittest.TestCase):

    def test_extract_main_dataframes(self):
        main_dfs = extract_main_dataframes(start_year=1995, end_year=1999)
        #TODO: expand to all dataframes
        test_df = main_dfs[list(main_dfs.keys())[0]]
        #change to the new year
        expected_columns = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', '1995', '1996', '1997', '1998', '1999']
        self.assertListEqual(test_df.columns.tolist(), expected_columns)

if __name__ == '__main__':
    unittest.main()