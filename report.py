def generate_report(original_df, cleaned_df):
    print("📊 Summary Report")
    print("Original Shape:", original_df.shape)
    print("Cleaned Shape:", cleaned_df.shape)
    print("\nMissing Values Before:\n", original_df.isnull().sum())
    print("\nMissing Values After:\n", cleaned_df.isnull().sum())
    print("\nDuplicates Removed:", original_df.duplicated().sum())
