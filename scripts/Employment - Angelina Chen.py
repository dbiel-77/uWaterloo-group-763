import pandas as pd
import numpy as np

df = pd.read_csv('Employment - Angelina Chen.csv')
df_e2021 = df[df["Year"] == 2021]
df_e2021["Employment Rate"] = pd.to_numeric(df_e2021["Employment Rate"], error="coerce")
df_e2021 = df_e2021.dropna(subset=["Employment Rate"])


avg_employment = (
    df_e2021
    .groupby("Locality", as_index=False)["Employment Rate"]
    .apply(np.mean)
)

avg_employment.columns = ["Locality", "Average Employment Rate (2021)"]

avg_employment["Average Employment Rate (2021)"] = \
    avg_employment["Average Employment Rate (2021)"].round(2)

print(avg_employment.to_string(index=False))
