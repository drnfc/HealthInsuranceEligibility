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

print(df[['State', 'Uninsured Rate (2010)', 'Uninsured Rate (2015)', 'Uninsured Rate Change (2010-2015)', 'Health Insurance Coverage Change (2010-2015)']])
print(df[['Employer Health Insurance Coverage (2015)', 'Marketplace Health Insurance Coverage (2016)', 'Marketplace Tax Credits (2016)', 'Average Monthly Tax Credit (2016)']])
print(df[['State Medicaid Expansion (2016)', 'Medicaid Enrollment (2013)', 'Medicaid Enrollment (2016)', 'Medicaid Enrollment Change (2013-2016)', 'Medicare Enrollment (2016)']])

df_noDC = df[df['State'] != 'District of Columbia'].reset_index(drop=True)
print(df_noDC)

df_noUS = df_noDC[:-1]
print(df_noUS)