# Logistics Data Cleaning and Preprocessing
# Week 2 Internship Project
# Author: Anand Bunkar

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv("logistics_data.csv")

print("Original Dataset:")
print(df.head())

# Check dataset information
print("\nDataset Information:")
print(df.info())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

print("\nDuplicate Records Removed")

# Handle missing values
numeric_columns = [
    "Shipping_Cost_INR",
    "Delivery_Time_Days",
    "Distance_KM"
]

for col in numeric_columns:
    df[col] = df[col].fillna(df[col].median())

print("\nMissing Values Handled")

# Detect Outliers using IQR Method
outlier_rows = pd.DataFrame()

for col in numeric_columns:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    detected = df[
        (df[col] < lower_limit) |
        (df[col] > upper_limit)
    ]

    outlier_rows = pd.concat(
        [outlier_rows, detected]
    ).drop_duplicates()

# Save outliers separately for review
outlier_rows.to_csv(
    "outlier_review.csv",
    index=False
)

print("\nOutlier Detection Completed")

# Data Normalization
for col in numeric_columns:

    minimum = df[col].min()
    maximum = df[col].max()

    if maximum != minimum:

        df[col + "_Normalized"] = (
            (df[col] - minimum) /
            (maximum - minimum)
        )

    else:
        df[col + "_Normalized"] = 0

print("\nData Normalization Completed")

# Save cleaned dataset
df.to_csv(
    "cleaned_logistics_data.csv",
    index=False
)

print("\nCleaned Dataset:")
print(df.head())

print("\nFinal Dataset Shape:", df.shape)

print("\nData Preprocessing Completed Successfully!")
