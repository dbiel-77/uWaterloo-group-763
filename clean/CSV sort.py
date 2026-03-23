import pandas as pd
import numpy as np
import os
FilteredColumn = pd.read_csv(r'C:\Users\salir\Downloads\MAIN DATA.csv', encoding ='latin1')
FilteredColumn = FilteredColumn[['DGUID', 'GEO_LEVEL', 'CENSUS_YEAR', 'GEO_NAME', 'TOTAL_GENDER (1)', 'CHARACTERISTIC_NAME', 'AGE']]
FilteredColumn = FilteredColumn[
    (
        (FilteredColumn['GEO_LEVEL'] == "Census subdivision") |
        (FilteredColumn['GEO_LEVEL'] == "Provincial/territorial combined CSDs with 2021 population under 10,000")
    ) &
    (FilteredColumn['AGE'] == "Total - Age") &
    (
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  0 to 14 years") |
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  15 to 64 years") |
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  65 years and over")
    )
]

FilteredColumn = FilteredColumn.drop_duplicates()
FilteredColumn.to_csv('test.csv', index=False)

print(os.getcwd())
