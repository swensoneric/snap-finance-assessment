# Basic Cleaning
# Convert numeric columns to floats (some columns are mixed types)
numeric_cols_outcomes = ['fpd_30', 'fpd_60', 'g_fctr', 'pd_30_amt', 'pd_60_amt', 'pd_120_amt', 
                         'fpr', 'cpo', 'epo', 'net_paid_amt', 'net_funded_amt']
for col in numeric_cols_outcomes:
    outcomes_df[col] = pd.to_numeric(outcomes_df[col], errors='coerce')

# Convert date columns in details_df
date_cols_details = ['submit_dt', 'approved_dt', 'complete_dt', 'funded_dt']
for col in date_cols_details:
    details_df[col] = pd.to_datetime(details_df[col], errors='coerce')

# Check for missing values
print("Missing values in outcomes_df:\n", outcomes_df.isna().sum())
print("\nMissing values in details_df:\n", details_df.isna().sum())

# Merge Datasets
# ------------------------------
# Merge on application_id
full_df = pd.merge(details_df, outcomes_df, on="application_id", how="left")
print("Merged dataset shape:", full_df.shape)
full_df.head()
