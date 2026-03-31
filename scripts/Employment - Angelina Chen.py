import pandas as pd
import numpy as np

with open('Employment - Angelina Chen.csv', 'r', encoding = 'utf-8') as file:
    lines = file.readlines()

end_index = next(i for i, line in enumerate(lines) if "Footnotes" in line)

df = pd.read_csv('Employment - Angelina Chen.csv',
                 skiprows=8, 
                 nrows=end_index - 8,
                 engine='python'
)

df = df.dropna(axis=1, how='all')

df.columns = df.columns.str.strip()
df = df.rename(columns={df.columns[0]: "Locality"})
df = df[
    ~df["Locality"].str.contains("Statistics|Geography|Estimate|Percent", na=False)
]

months_2021 = df.columns[1:]  

df[months_2021] = df[months_2021].apply(pd.to_numeric, errors='coerce')

df["Average Unemployment Rate (2021)"] = df[months_2021].mean(axis=1) 

avg_unemployment = df[["Locality", "Average Unemployment Rate (2021)"]]

avg_unemployment["Average Unemployment Rate (2021)"] = (
    avg_unemployment["Average Unemployment Rate (2021)"].round(2)
)

avg_unemployment = avg_unemployment.dropna()
avg_unemployment = avg_unemployment.drop_duplicates()

avg_unemployment.to_csv("Average Unemployment Rate.csv", index=False)
