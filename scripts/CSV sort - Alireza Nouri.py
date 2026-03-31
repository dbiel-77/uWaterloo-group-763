import pandas as pd
import numpy as np
FilteredColumn = pd.read_csv(r'C:\Users\salir\Downloads\MAIN DATA.csv', encoding='cp1252')

FilteredColumn = FilteredColumn[['DGUID', 'GEO_LEVEL', 'CENSUS_YEAR', 'GEO_NAME', 'TOTAL_GENDER (1)', 'CHARACTERISTIC_NAME', 'AGE']]
FilteredColumn = FilteredColumn[
    (
        (FilteredColumn['GEO_LEVEL'] == "Census subdivision") |
        (FilteredColumn['GEO_LEVEL'] == "Provincial/territorial combined CSDs with 2021 population under 10,000")
    ) &
    (
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  0 to 14 years") |
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  15 to 64 years") |
        (FilteredColumn['CHARACTERISTIC_NAME'] == "  65 years and over")
    )
]

FilteredColumn = FilteredColumn.drop_duplicates()

FilteredColumn = FilteredColumn.pivot_table(
    index=['DGUID', 'GEO_LEVEL', 'CENSUS_YEAR', 'GEO_NAME'],
    columns='CHARACTERISTIC_NAME',
    values='TOTAL_GENDER (1)',
    aggfunc='first'
).reset_index()

FilteredColumn.to_csv('test.csv', index=False, encoding='utf-8-sig')
