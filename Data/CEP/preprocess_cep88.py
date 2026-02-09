"""
Preprocessing script for CEP base_88.csv
Replicates the variable coding from the paper:
"Auditing Fairness in LLM-Generated Survey Responses" (arXiv:2501.15351)

Pipeline:
1. Load raw data and keep only relevant columns
2. Run Little's MCAR test
3. Recode variables
4. Filter out non-responses in dependent variables
5. Output cleaned dataset
"""

import pandas as pd
import numpy as np
from pyampute.exploration.mcar_statistical_tests import MCARTest

# ============================================================================
# STEP 1: LOAD DATA AND KEEP ONLY RELEVANT COLUMNS
# ============================================================================

print("="*60)
print("STEP 1: Load data and select relevant columns")
print("="*60)

# Load raw data
df_raw = pd.read_csv('base_88.csv', index_col=0, encoding='latin-1')
print(f"Raw data: {len(df_raw)} rows, {len(df_raw.columns)} columns")

# Define columns to keep
# Independent variables (raw)
independent_cols = [
    'sexo',           # Gender
    'edad',           # Age
    'nom_region',     # Region
    'zona_u_r',       # Urban/Rural
    'gse',            # Socioeconomic group
    'esc_nivel_1',    # Education level
    'info_enc_58',    # Indigenous identification
    # 'info_enc_30',    # Indigenous group
    'religion_82',    # Religion
    'iden_pol_2',     # Political ideology
    'iden_pol_3',     # Party identification
    'interes_pol_1_b' # Interest in politics
]

# Dependent variables (raw)
dependent_cols = [
    'elec_pres_144_a',   # Presidential vote 2021
    'constitucion_20_a', # Plebiscite vote 2022
    'religion_14'        # Abortion opinion
]

# Keep only relevant columns
cols_to_keep = independent_cols + dependent_cols
cols_to_keep = [c for c in cols_to_keep if c in df_raw.columns]
df = df_raw[cols_to_keep].copy()

print(f"After column selection: {len(df)} rows, {len(df.columns)} columns")
print(f"Columns kept: {list(df.columns)}")

# ============================================================================
# STEP 2: LITTLE'S MCAR TEST (pyampute)
# ============================================================================

print("\n" + "="*60)
print("STEP 2: Little's MCAR Test")
print("="*60)

# Prepare data for MCAR test (replace coded missing values with NaN)
df_mcar = df.copy()
missing_codes = [88, 99, 888, 999]
for col in dependent_cols:
    if df_mcar[col].dtype in ['int64', 'float64']:
        df_mcar.loc[df_mcar[col].isin(missing_codes), col] = np.nan

# Keep only numeric columns for MCAR test
df_mcar_numeric = df_mcar.select_dtypes(include=[np.number]) 


print(f"Total observations: {len(df_mcar_numeric)}")
print(f"Complete cases: {df_mcar_numeric.dropna().shape[0]}")
print(f"Variables tested: {len(df_mcar_numeric.columns)}")

# Run Little's MCAR test using pyampute
mcar_test = MCARTest(method="little")
p_value = mcar_test(df_mcar_numeric)

print(f"\nP-value: {p_value:.6f}")

if p_value > 0.05:
    print("\nConclusion: Fail to reject H0 (p > 0.05)")
    print("Data is consistent with MCAR assumption.")
else:
    print("\nConclusion: Reject H0 (p <= 0.05)")
    print("Data is NOT Missing Completely at Random.")

# Missing data summary
print("\nMissing Data Summary:")
print("-"*40)
missing_counts = df_mcar.isna().sum()
missing_pct = (df_mcar.isna().sum() / len(df_mcar) * 100).round(2)
missing_df = pd.DataFrame({'Count': missing_counts, 'Percent': missing_pct})
missing_df = missing_df[missing_df['Count'] > 0].sort_values('Percent', ascending=False)
if len(missing_df) > 0:
    print(missing_df)
else:
    print("No missing data detected.")


# ============================================================================
# STEP 3: VARIABLE RECODING
# ============================================================================

print("\n" + "="*60)
print("STEP 3: Variable Recoding")
print("="*60)

# Gender: Binary (Man=1, Woman=2)
gender_map = {1: 'Man', 2: 'Woman'}

# Age group: Young Adult (18-26), Adult (27-59), Senior Adult (60+)
def recode_age_group(age):
    if pd.isna(age):
        return np.nan
    if 18 <= age <= 26:
        return 'Young Adult'
    elif 27 <= age <= 59:
        return 'Adult'
    elif age >= 60:
        return 'Senior Adult'
    return np.nan

# Urban/Rural
zona_map = {1: 'Urban', 2: 'Rural'}

# Socio-Economic Group
gse_map = {1: 'High', 2: 'Middle', 3: 'Middle', 4: 'Low', 5: 'Low'}

# Education Level
def recode_education(edu):
    if pd.isna(edu):
        return np.nan
    edu = int(edu)
    if edu in [88, 99]:
        return np.nan
    elif 0 <= edu <= 3:
        return 'Low'
    elif 4 <= edu <= 7:
        return 'Medium'
    elif 8 <= edu <= 10:
        return 'High'
    return np.nan

# Indigenous Identification
indigenous_map = {1: 'Indigenous', 2: 'Non-Indigenous'}

# Religion
def recode_religion(rel):
    if pd.isna(rel):
        return np.nan
    rel = int(rel)
    if rel in [88, 99]:
        return np.nan
    elif 1 <= rel <= 8:
        return 'Religious'
    elif 9 <= rel <= 11:
        return 'Not Religious'
    return np.nan

# Political Ideology
def recode_ideology(ideo):
    if pd.isna(ideo):
        return np.nan
    ideo = int(ideo)
    if ideo in [88, 99]:
        return 'None'
    elif 1 <= ideo <= 4:
        return 'Left'
    elif 5 <= ideo <= 6:
        return 'Center'
    elif 7 <= ideo <= 10:
        return 'Right'
    return np.nan

# Interest in Politics
interest_map = {
    1: 'Very interested',
    2: 'Somewhat interested',
    3: 'Not very interested',
    4: 'Not very interested',
    5: 'Not at all interested',
    8: 'None',
    9: 'None'
}

# Presidential Vote
def recode_presidential_vote(vote):
    if pd.isna(vote):
        return np.nan
    vote = int(vote)
    if vote == 1:
        return 'Gabriel Boric'
    elif vote == 2:
        return 'José Antonio Kast'
    elif vote in [3, 4]:
        return 'nulo'
    return np.nan  # All other values (null, blank, etc.) are non-responses

# Plebiscite Vote
def recode_plebiscite_vote(vote):
    if pd.isna(vote):
        return np.nan
    vote = int(vote)
    if vote == 1:
        return 'Approve'
    elif vote == 2:
        return 'Reject'
    elif vote in [3, 4]:
        return 'nulo'
    return np.nan  # All other values are non-responses

# Abortion Opinion
abortion_map = {
    1: 'Always illegal',
    2: 'Legal only in specific cases',
    3: 'Always legal'
}

# Apply recoding
df['gender'] = df['sexo'].map(gender_map)
df['age_group'] = df['edad'].apply(recode_age_group)
df['region'] = df['nom_region']
df['zona'] = df['zona_u_r'].map(zona_map)
df['gse_group'] = df['gse'].map(gse_map)
df['education'] = df['esc_nivel_1'].apply(recode_education)
df['indigenous'] = df['info_enc_58'].replace({88: np.nan, 99: np.nan}).map(indigenous_map)
df['religion'] = df['religion_82'].apply(recode_religion)
df['ideology'] = df['iden_pol_2'].apply(recode_ideology)
df['party'] = df['iden_pol_3']
df['interest_politics'] = df['interes_pol_1_b'].map(interest_map)
df['presidential_vote'] = df['elec_pres_144_a'].apply(recode_presidential_vote)
df['plebiscite_vote'] = df['constitucion_20_a'].apply(recode_plebiscite_vote)
df['abortion_opinion'] = df['religion_14'].map(abortion_map)

print("Recoding applied.")

# ============================================================================
# STEP 4: FILTER BY NON-RESPONSE IN DEPENDENT VARIABLES
# ============================================================================

print("\n" + "="*60)
print("STEP 4: Filter by non-response in dependent variables")
print("="*60)

print(f"Before filtering: {len(df)} rows")

# Filter: keep only rows with valid responses in ALL three dependent variables
df_filtered = df[
    df['presidential_vote'].notna() &
    df['plebiscite_vote'].notna() &
    df['abortion_opinion'].notna()
].copy()

print(f"After filtering dependent variables: {len(df_filtered)} rows")

# Also filter out missing independent variables
independent_vars = [
    'gender', 'age_group', 'region', 'zona', 'gse_group',
    'education', 'indigenous', 'religion', 'ideology', 'interest_politics'
]

for var in independent_vars:
    df_filtered = df_filtered[df_filtered[var].notna()]

print(f"After filtering independent variables: {len(df_filtered)} rows")

# ============================================================================
# STEP 4b: COMPARE INCLUDED VS EXCLUDED ROWS
# ============================================================================

print("\n" + "="*60)
print("STEP 4b: Compare Included vs Excluded Rows")
print("="*60)

# Get indices of included rows
included_idx = df_filtered.index
excluded_idx = df.index.difference(included_idx)

# Use raw data for comparison (before recoding)
df_included_raw = df_raw.loc[included_idx]
df_excluded_raw = df_raw.loc[excluded_idx]

print(f"Included rows: {len(df_included_raw)} ({len(df_included_raw)/len(df_raw)*100:.1f}%)")
print(f"Excluded rows: {len(df_excluded_raw)} ({len(df_excluded_raw)/len(df_raw)*100:.1f}%)")

# Numeric variables comparison
print("\n" + "-"*40)
print("NUMERIC VARIABLES: Mean (Median)")
print("-"*40)
print(f"{'Variable':<20} {'Included':>20} {'Excluded':>20}")

numeric_cols = ['edad', 'gse', 'esc_nivel_1', 'iden_pol_2', 'interes_pol_1_b']
for col in numeric_cols:
    if col in df_raw.columns:
        # Replace missing codes with NaN for proper calculation
        inc_col = df_included_raw[col].replace([88, 99, 888, 999], np.nan)
        exc_col = df_excluded_raw[col].replace([88, 99, 888, 999], np.nan)
        c_mean = inc_col.mean()
        c_med = inc_col.median()
        i_mean = exc_col.mean()
        i_med = exc_col.median()
        print(f"{col:<20} {c_mean:>8.2f} ({c_med:>5.1f}) {i_mean:>12.2f} ({i_med:>5.1f})")

# Categorical variables comparison
print("\n" + "-"*40)
print("CATEGORICAL VARIABLES: Proportions")
print("-"*40)

# Gender
print("\nGender (sexo):")
print(f"  Included:  Man={df_included_raw['sexo'].value_counts(normalize=True).get(1,0)*100:.1f}%, Woman={df_included_raw['sexo'].value_counts(normalize=True).get(2,0)*100:.1f}%")
print(f"  Excluded:  Man={df_excluded_raw['sexo'].value_counts(normalize=True).get(1,0)*100:.1f}%, Woman={df_excluded_raw['sexo'].value_counts(normalize=True).get(2,0)*100:.1f}%")

# Zone
print("\nZone (zona_u_r):")
print(f"  Included:  Urban={df_included_raw['zona_u_r'].value_counts(normalize=True).get(1,0)*100:.1f}%, Rural={df_included_raw['zona_u_r'].value_counts(normalize=True).get(2,0)*100:.1f}%")
print(f"  Excluded:  Urban={df_excluded_raw['zona_u_r'].value_counts(normalize=True).get(1,0)*100:.1f}%, Rural={df_excluded_raw['zona_u_r'].value_counts(normalize=True).get(2,0)*100:.1f}%")

# Indigenous
print("\nIndigenous (info_enc_58):")
inc_indig = df_included_raw['info_enc_58'].replace([88, 99], np.nan).value_counts(normalize=True)
exc_indig = df_excluded_raw['info_enc_58'].replace([88, 99], np.nan).value_counts(normalize=True)
print(f"  Included:  Yes={inc_indig.get(1,0)*100:.1f}%, No={inc_indig.get(2,0)*100:.1f}%")
print(f"  Excluded:  Yes={exc_indig.get(1,0)*100:.1f}%, No={exc_indig.get(2,0)*100:.1f}%")

# Presidential vote
print("\nPresidential Vote (elec_pres_144_a):")
inc_vote = df_included_raw['elec_pres_144_a'].replace([88, 99], np.nan).value_counts(normalize=True)
exc_vote = df_excluded_raw['elec_pres_144_a'].replace([88, 99], np.nan).value_counts(normalize=True)
# Null/Blank = codes 3, 4, etc. (not 1=Boric, 2=Kast)
inc_null_pres = sum(inc_vote.get(k, 0) for k in inc_vote.index if k not in [1, 2])
exc_null_pres = sum(exc_vote.get(k, 0) for k in exc_vote.index if k not in [1, 2])
print(f"  Included:  Boric={inc_vote.get(1,0)*100:.1f}%, Kast={inc_vote.get(2,0)*100:.1f}%, Null/Blank={inc_null_pres*100:.1f}%")
print(f"  Excluded:  Boric={exc_vote.get(1,0)*100:.1f}%, Kast={exc_vote.get(2,0)*100:.1f}%, Null/Blank={exc_null_pres*100:.1f}%")
# Show missing count
inc_na_pres = df_included_raw['elec_pres_144_a'].isna().sum() + df_included_raw['elec_pres_144_a'].isin([88, 99]).sum()
exc_na_pres = df_excluded_raw['elec_pres_144_a'].isna().sum() + df_excluded_raw['elec_pres_144_a'].isin([88, 99]).sum()
print(f"  Missing:   Included={inc_na_pres} ({inc_na_pres/len(df_included_raw)*100:.1f}%), Excluded={exc_na_pres} ({exc_na_pres/len(df_excluded_raw)*100:.1f}%)")

# Plebiscite vote
print("\nPlebiscite Vote (constitucion_20_a):")
inc_pleb = df_included_raw['constitucion_20_a'].replace([88, 99], np.nan).value_counts(normalize=True)
exc_pleb = df_excluded_raw['constitucion_20_a'].replace([88, 99], np.nan).value_counts(normalize=True)
# Null/Blank = codes 3, 4, etc. (not 1=Approve, 2=Reject)
inc_null_pleb = sum(inc_pleb.get(k, 0) for k in inc_pleb.index if k not in [1, 2])
exc_null_pleb = sum(exc_pleb.get(k, 0) for k in exc_pleb.index if k not in [1, 2])
print(f"  Included:  Approve={inc_pleb.get(1,0)*100:.1f}%, Reject={inc_pleb.get(2,0)*100:.1f}%, Null/Blank={inc_null_pleb*100:.1f}%")
print(f"  Excluded:  Approve={exc_pleb.get(1,0)*100:.1f}%, Reject={exc_pleb.get(2,0)*100:.1f}%, Null/Blank={exc_null_pleb*100:.1f}%")
# Show missing count
inc_na_pleb = df_included_raw['constitucion_20_a'].isna().sum() + df_included_raw['constitucion_20_a'].isin([88, 99]).sum()
exc_na_pleb = df_excluded_raw['constitucion_20_a'].isna().sum() + df_excluded_raw['constitucion_20_a'].isin([88, 99]).sum()
print(f"  Missing:   Included={inc_na_pleb} ({inc_na_pleb/len(df_included_raw)*100:.1f}%), Excluded={exc_na_pleb} ({exc_na_pleb/len(df_excluded_raw)*100:.1f}%)")

# Abortion
print("\nAbortion Opinion (religion_14):")
inc_abort = df_included_raw['religion_14'].value_counts(normalize=True)
exc_abort = df_excluded_raw['religion_14'].replace([88, 99], np.nan).value_counts(normalize=True)
print(f"  Included:  Illegal={inc_abort.get(1,0)*100:.1f}%, Special={inc_abort.get(2,0)*100:.1f}%, Legal={inc_abort.get(3,0)*100:.1f}%")
print(f"  Excluded:  Illegal={exc_abort.get(1,0)*100:.1f}%, Special={exc_abort.get(2,0)*100:.1f}%, Legal={exc_abort.get(3,0)*100:.1f}%")

# Religion
print("\nReligion (religion_82):")
def _is_religious(x):
    if pd.isna(x) or x in [88, 99]: return np.nan
    return 'Religious' if 1 <= x <= 8 else 'Not Religious' if 9 <= x <= 11 else np.nan
inc_rel = df_included_raw['religion_82'].apply(_is_religious).value_counts(normalize=True)
exc_rel = df_excluded_raw['religion_82'].apply(_is_religious).value_counts(normalize=True)
print(f"  Included:  Religious={inc_rel.get('Religious',0)*100:.1f}%, Not Religious={inc_rel.get('Not Religious',0)*100:.1f}%")
print(f"  Excluded:  Religious={exc_rel.get('Religious',0)*100:.1f}%, Not Religious={exc_rel.get('Not Religious',0)*100:.1f}%")

# Political ideology
print("\nPolitical Ideology (iden_pol_2):")
def _ideology_group(x):
    if pd.isna(x) or x in [88, 99]: return np.nan
    if 1 <= x <= 4: return 'Left'
    if 5 <= x <= 6: return 'Center'
    if 7 <= x <= 10: return 'Right'
    return np.nan
inc_ideo = df_included_raw['iden_pol_2'].apply(_ideology_group).value_counts(normalize=True)
exc_ideo = df_excluded_raw['iden_pol_2'].apply(_ideology_group).value_counts(normalize=True)
print(f"  Included:  Left={inc_ideo.get('Left',0)*100:.1f}%, Center={inc_ideo.get('Center',0)*100:.1f}%, Right={inc_ideo.get('Right',0)*100:.1f}%")
print(f"  Excluded:  Left={exc_ideo.get('Left',0)*100:.1f}%, Center={exc_ideo.get('Center',0)*100:.1f}%, Right={exc_ideo.get('Right',0)*100:.1f}%")

# ============================================================================
# STEP 5: SELECT FINAL COLUMNS AND SAVE
# ============================================================================

print("\n" + "="*60)
print("STEP 5: Save cleaned dataset")
print("="*60)

# Final columns to keep
final_cols = independent_vars + ['presidential_vote', 'plebiscite_vote', 'abortion_opinion']
df_final = df_filtered[final_cols].copy()

# Save
df_final.to_csv('cep88_cleaned.csv', index=False)
print(f"Saved: cep88_cleaned.csv ({len(df_final)} rows, {len(df_final.columns)} columns)")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*60)
print("SUMMARY: Variable Distributions")
print("="*60)

for var in independent_vars:
    print(f"\n{var}:")
    print(df_final[var].value_counts())

print("\n" + "="*60)
print("SUMMARY: Dependent Variables")
print("="*60)

print("\nPresidential Vote:")
print(df_final['presidential_vote'].value_counts())

print("\nPlebiscite Vote:")
print(df_final['plebiscite_vote'].value_counts())

print("\nAbortion Opinion:")
print(df_final['abortion_opinion'].value_counts())
