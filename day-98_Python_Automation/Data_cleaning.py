"""
This file is responsible for cleaning the data.
"""

import pandas as pd
from main import data
from scipy.stats import zscore

# Load your dataset
df = pd.read_csv(data)

"""1. Handling Missing Values: """
# Check for missing values
missing_values = df.isnull().sum()

# Drop rows with missing values
df_cleaned = df.dropna()

# Fill missing values with a specific value
df_filled = df.fillna(value=0)

# Fill missing values with the mean of the column
df_mean_filled = df.fillna(df.mean())

# Interpolate missing values
df_interpolated = df.interpolate()

# Drop columns with missing values
df_no_missing_columns = df.dropna(axis=1)

"""2. Handling Duplicate Values: """
# Drop duplicate rows
df_no_duplicates = df.drop_duplicates()

# asking user to enter the column name to drop duplicates
column_name = input("Enter the column name to drop duplicates separated by comma: ")
column_name = column_name.split(",")
if len(column_name) != 0:
    # Drop duplicate rows based on specific columns
    df_no_duplicates_specific_cols = df.drop_duplicates(subset=column_name)

# Count and display duplicate rows
duplicate_count = df.duplicated().sum()
duplicates = df[df.duplicated()]

# Remove duplicates and keep the first occurrence
df_first_occurrence = df.drop_duplicates(keep='first')

"""3. Handling Outliers:"""
# Identify outliers using z-score for a specific column

# all columns heaving data type as int64
numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

for column_name in numerical_columns:
    # Calculate z-scores
    z_scores = zscore(df[column_name])
    outliers = df[(z_scores > 3) | (z_scores < -3)]

    # Remove outliers based on z-score for a specific column
    df_no_outliers = df[(z_scores > -3) & (z_scores < 3)]

    # Remove outliers based on IQR (Interquartile Range) for a specific column
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    df_no_outliers_iqr = df[(df[column_name] >= Q1 - 1.5 * IQR) & (df[column_name] <= Q3 + 1.5 * IQR)]

cleaned_data = df
