import pandas as pd
from cleaner import auto_clean
from report import generate_report

# Load the dataset
df = pd.read_csv("sample.csv")

# Clean the data
cleaned_df = auto_clean(df)

# Save cleaned data
cleaned_df.to_csv("cleaned_data.csv", index=False)
print("✅ Cleaned data saved to cleaned_data.csv")

# Report
generate_report(df, cleaned_df)
