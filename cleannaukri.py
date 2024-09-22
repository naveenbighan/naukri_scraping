import pandas as pd

df = pd.read_csv("naukri1_com.csv")
pd.options.display.max_rows=50999
df.drop_duplicates(inplace=True)
print(df)