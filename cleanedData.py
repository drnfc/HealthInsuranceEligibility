import pandas as pd

# Converts into dataframe
df = pd.read_csv("states.csv")

# Find null values in dataset
null_values = df.isnull().sum()

# Prints which features have null values
print("Null values:")
print(null_values)

print()

# Iterates over columns in dataframe
for column in df.columns:
    # If null, finds average for that column and replaces with this value
    if df[column].isnull().any():
        column_average = df[column].mean()
        
        df[column].fillna(column_average, inplace = True)
        
# Reprints
null_values = df.isnull().sum()
print(null_values)

df['State'] = df['State'].str.strip()

print(df)