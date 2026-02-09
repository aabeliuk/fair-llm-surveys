"""
Preprocessing script for ANES 2020 Time Series data
Replicates the variable coding from the paper:
"Auditing Fairness in LLM-Generated Survey Responses" (arXiv:2501.15351)

Pipeline:
1. Load raw data and keep only relevant columns
2. Run Little's MCAR test
3. Recode variables
4. Filter out non-responses in dependent variables
5. Compare included vs excluded rows
6. Output cleaned dataset
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
df_raw = pd.read_csv('anes_timeseries_2020_csv_20220210.csv', low_memory=False)
print(f"Raw data: {len(df_raw)} rows, {len(df_raw.columns)} columns")

# Define columns to keep
# Independent variables (raw)
independent_cols = [
    'V201600',    # Gender
    'V201507x',   # Age
    'V201575',    # Region (state)
    'V202355',    # Rural/Urban
    'V201549x',   # Race
    'V201510',    # Education
    'V201617x',   # Income
    'V201200',    # Political Ideology
    'V201231x',   # Party Identification
    'V201435',    # Religion
    'V202406',    # Interest in Politics
]

# Dependent variables (raw)
dependent_cols = [
    'V202073',    # Presidential vote 2020
    'V201336',    # Abortion opinion
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

# Prepare data for MCAR test (replace ANES missing codes with NaN)
# ANES missing codes: -1 (inapplicable), -5 to -9 (various non-responses)
df_mcar = df.copy()

# General missing codes for all variables
general_missing = [-1, -2, -3, -4, -5, -6, -7, -8, -9, 99]

# Variable-specific additional invalid codes
# V201336 (abortion): value 5 = "Other" treated as invalid in recoding
variable_specific_invalid = {
    'V201336': [5]  # "Other" response
}

for col in dependent_cols:
    if col in df_mcar.columns:
        # Combine general missing codes with variable-specific invalid codes
        all_invalid = general_missing + variable_specific_invalid.get(col, [])
        df_mcar.loc[df_mcar[col].isin(all_invalid), col] = np.nan

# Keep only numeric columns for MCAR test
df_mcar_numeric = df_mcar[dependent_cols].select_dtypes(include=[np.number])

print(f"Total observations: {len(df_mcar_numeric)}")
print(f"Complete cases: {df_mcar_numeric.dropna().shape[0]}")
print(f"Variables tested: {list(df_mcar_numeric.columns)}")

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
missing_counts = df_mcar[dependent_cols].isna().sum()
missing_pct = (df_mcar[dependent_cols].isna().sum() / len(df_mcar) * 100).round(2)
missing_df = pd.DataFrame({'Count': missing_counts, 'Percent': missing_pct})
print(missing_df)

# ============================================================================
# STEP 3: VARIABLE RECODING
# ============================================================================

print("\n" + "="*60)
print("STEP 3: Variable Recoding")
print("="*60)

# Gender: 1=Male, 2=Female
gender_map = {1: 'Man', 2: 'Woman'}

# Age group: Young Adult (18-26), Adult (27-59), Senior Adult (60+)
def recode_age_group(age):
    if pd.isna(age) or age < 0:
        return np.nan
    if 18 <= age <= 26:
        return 'Young Adult'
    elif 27 <= age <= 59:
        return 'Adult'
    elif age >= 60:
        return 'Senior Adult'
    return np.nan

# Region: State FIPS codes to region names
region_map = {
    1: 'Alabama', 2: 'Alaska', 4: 'Arizona', 5: 'Arkansas', 6: 'California',
    8: 'Colorado', 9: 'Connecticut', 10: 'Delaware', 11: 'District of Columbia',
    12: 'Florida', 13: 'Georgia', 15: 'Hawaii', 16: 'Idaho', 17: 'Illinois',
    18: 'Indiana', 19: 'Iowa', 20: 'Kansas', 21: 'Kentucky', 22: 'Louisiana',
    23: 'Maine', 24: 'Maryland', 25: 'Massachusetts', 26: 'Michigan',
    27: 'Minnesota', 28: 'Mississippi', 29: 'Missouri', 30: 'Montana',
    31: 'Nebraska', 32: 'Nevada', 33: 'New Hampshire', 34: 'New Jersey',
    35: 'New Mexico', 36: 'New York', 37: 'North Carolina', 38: 'North Dakota',
    39: 'Ohio', 40: 'Oklahoma', 41: 'Oregon', 42: 'Pennsylvania',
    44: 'Rhode Island', 45: 'South Carolina', 46: 'South Dakota',
    47: 'Tennessee', 48: 'Texas', 49: 'Utah', 50: 'Vermont', 51: 'Virginia',
    53: 'Washington', 54: 'West Virginia', 55: 'Wisconsin', 56: 'Wyoming'
}

# Rural/Urban: 1=City, 2=Suburb, 3=Small town, 4=Rural
def recode_zona(zona):
    if pd.isna(zona) or zona < 0:
        return np.nan
    if zona in [1, 2]:  # City, Suburb
        return 'Urban'
    elif zona in [3, 4]:  # Small town, Rural
        return 'Rural'
    return np.nan

# Race: 1=White, 2=Black, 3=Hispanic, 4=Asian/PI, 5=Native American, 6=Multiple
def recode_race(race):
    if pd.isna(race) or race < 0:
        return np.nan
    if race == 1:
        return 'White'
    elif race in [2, 3, 4, 5, 6]:
        return 'Non-White'
    return np.nan

# Education: 1=Less than HS, 2=HS, 3=Some college, 4=2yr degree, 5=4yr degree, 6=Post-grad
def recode_education(edu):
    if pd.isna(edu) or edu < 0:
        return np.nan
    if edu == 1:  # Less than high school
        return 'Low'
    elif edu in [2, 3, 4, 5]:  # HS diploma, some college, associate degree
        return 'Medium'
    elif edu in [6, 7, 8]:  # Bachelor's or higher
        return 'High'
    elif edu == 95:  # Other
        return np.nan
    return np.nan

# Income (V201617x): 1-22 scale, 1=Under $5k to 22=$250k+
def recode_income(income):
    if pd.isna(income) or income < 0:
        return np.nan
    if 1 <= income <= 10:  # Under $5k to $40-50k
        return 'Low Income'
    elif 11 <= income <= 18:  # $50-60k to $125-150k
        return 'Middle Income'
    elif 19 <= income <= 22:  # $150-175k to $250k+
        return 'High Income'
    return np.nan

# Political Ideology: 1=Extremely liberal to 7=Extremely conservative
def recode_ideology(ideo):
    if pd.isna(ideo) or ideo < 0:
        return np.nan
    if ideo == 99:  # Haven't thought about it
        return 'None'
    if ideo in [1, 2, 3]:  # Extremely/Slightly Liberal
        return 'Left'
    elif ideo == 4:  # Moderate
        return 'Center'
    elif ideo in [5, 6, 7]:  # Slightly/Extremely Conservative
        return 'Right'
    return np.nan

# Party ID: 1=Strong Dem to 7=Strong Rep
def recode_party(party):
    if pd.isna(party) or party < 0:
        return np.nan
    if party in [1, 2]:  # Strong/Not very strong Democrat
        return 'Democrat'
    elif party in [3, 4, 5]:  # Independent
        return 'Independent'
    elif party in [6, 7]:  # Not very strong/Strong Republican
        return 'Republican'
    return np.nan

# Religion: 1=Protestant, 2=Catholic, etc.
def recode_religion(rel):
    if pd.isna(rel) or rel < 0:
        return np.nan
    if rel in [1, 2, 3, 4, 5, 6, 7, 8]:  # Protestant, Catholic, Orthodox, LDS, Jewish, Muslim, Buddhist, Hindu
        return 'Religious'
    elif rel in [9, 10, 11, 12]:  # Atheist, Agnostic, Something else, Nothing in particular
        return 'Not Religious'
    return np.nan

# Interest in Politics: 1=Very much, 2=Somewhat, 3=Not very much, 4=Not at all
interest_map = {
    1: 'Very interested',
    2: 'Somewhat interested',
    3: 'Not very interested',
    4: 'Not at all interested'
}

# Presidential Vote: 1=Biden, 2=Trump, 3=Jorgensen, 4=Hawkins, 5=Other
def recode_presidential_vote(vote):
    if pd.isna(vote) or vote < 0:
        return np.nan
    if vote == 1:
        return 'Joe Biden'
    elif vote == 2:
        return 'Donald Trump'
    elif vote == 3:
        return 'Jo Jorgensen'
    elif vote == 4:
        return 'Howie Hawkins'
    elif vote in [5, 7, 8, 11, 12]:  # Other candidates
        return 'Other'
    return np.nan

# Abortion Opinion: 1=Never, 2=Rape/incest/danger, 3=Other reasons clearly established, 4=Always
def recode_abortion(abort):
    if pd.isna(abort) or abort < 0:
        return np.nan
    if abort == 1:
        return 'Always illegal'
    elif abort in [2, 3]:
        return 'Legal only in specific cases'
    elif abort == 4:
        return 'Always legal'
    elif abort == 5:  # Other
        return np.nan
    return np.nan

# Apply recoding
df['gender'] = df['V201600'].map(gender_map)
df['age_group'] = df['V201507x'].apply(recode_age_group)
df['region'] = df['V201575'].map(region_map)
df['zona'] = df['V202355'].apply(recode_zona)
df['race'] = df['V201549x'].apply(recode_race)
df['education'] = df['V201510'].apply(recode_education)
df['income'] = df['V201617x'].apply(recode_income)
df['ideology'] = df['V201200'].apply(recode_ideology)
df['party'] = df['V201231x'].apply(recode_party)
df['religion'] = df['V201435'].apply(recode_religion)
df['interest_politics'] = df['V202406'].map(interest_map)
df['presidential_vote'] = df['V202073'].apply(recode_presidential_vote)
df['abortion_opinion'] = df['V201336'].apply(recode_abortion)

print("Recoding applied.")

# ============================================================================
# STEP 4: FILTER BY NON-RESPONSE IN DEPENDENT VARIABLES
# ============================================================================

print("\n" + "="*60)
print("STEP 4: Filter by non-response in dependent variables")
print("="*60)

print(f"Before filtering: {len(df)} rows")

# Filter: keep only rows with valid responses in BOTH dependent variables
df_filtered = df[
    df['presidential_vote'].notna() &
    df['abortion_opinion'].notna()
].copy()

print(f"After filtering dependent variables: {len(df_filtered)} rows")




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

numeric_cols = ['V201507x', 'V201510', 'V201617x', 'V201200']
for col in numeric_cols:
    if col in df_raw.columns:
        inc_col = df_included_raw[col].replace(list(range(-9, 0)), np.nan)
        exc_col = df_excluded_raw[col].replace(list(range(-9, 0)), np.nan)
        # Also remove 99 for ideology
        if col == 'V201200':
            inc_col = inc_col.replace(99, np.nan)
            exc_col = exc_col.replace(99, np.nan)
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
print("\nGender (V201600):")
inc_gender = df_included_raw['V201600'].replace([-9, -8], np.nan).value_counts(normalize=True)
exc_gender = df_excluded_raw['V201600'].replace([-9, -8], np.nan).value_counts(normalize=True)
print(f"  Included:  Man={inc_gender.get(1,0)*100:.1f}%, Woman={inc_gender.get(2,0)*100:.1f}%")
print(f"  Excluded:  Man={exc_gender.get(1,0)*100:.1f}%, Woman={exc_gender.get(2,0)*100:.1f}%")

# Race
print("\nRace (V201549x):")
inc_race = df_included_raw['V201549x'].replace([-9, -8], np.nan).value_counts(normalize=True)
exc_race = df_excluded_raw['V201549x'].replace([-9, -8], np.nan).value_counts(normalize=True)
print(f"  Included:  White={inc_race.get(1,0)*100:.1f}%, Non-White={sum(inc_race.get(k,0) for k in [2,3,4,5,6])*100:.1f}%")
print(f"  Excluded:  White={exc_race.get(1,0)*100:.1f}%, Non-White={sum(exc_race.get(k,0) for k in [2,3,4,5,6])*100:.1f}%")

# Presidential vote
print("\nPresidential Vote (V202073):")
inc_vote = df_included_raw['V202073'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
exc_vote = df_excluded_raw['V202073'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
inc_other = sum(inc_vote.get(k, 0) for k in inc_vote.index if k not in [1, 2])
exc_other = sum(exc_vote.get(k, 0) for k in exc_vote.index if k not in [1, 2])
print(f"  Included:  Biden={inc_vote.get(1,0)*100:.1f}%, Trump={inc_vote.get(2,0)*100:.1f}%, Other={inc_other*100:.1f}%")
print(f"  Excluded:  Biden={exc_vote.get(1,0)*100:.1f}%, Trump={exc_vote.get(2,0)*100:.1f}%, Other={exc_other*100:.1f}%")
# Show missing
inc_na = df_included_raw['V202073'].isin(list(range(-9, 0))).sum()
exc_na = df_excluded_raw['V202073'].isin(list(range(-9, 0))).sum()
print(f"  Missing:   Included={inc_na} ({inc_na/len(df_included_raw)*100:.1f}%), Excluded={exc_na} ({exc_na/len(df_excluded_raw)*100:.1f}%)")

# Abortion
print("\nAbortion Opinion (V201336):")
inc_abort = df_included_raw['V201336'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
exc_abort = df_excluded_raw['V201336'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
print(f"  Included:  Never={inc_abort.get(1,0)*100:.1f}%, Special cases={sum(inc_abort.get(k,0) for k in [2,3])*100:.1f}%, Always={inc_abort.get(4,0)*100:.1f}%")
print(f"  Excluded:  Never={exc_abort.get(1,0)*100:.1f}%, Special cases={sum(exc_abort.get(k,0) for k in [2,3])*100:.1f}%, Always={exc_abort.get(4,0)*100:.1f}%")

# Party
print("\nParty ID (V201231x):")
inc_party = df_included_raw['V201231x'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
exc_party = df_excluded_raw['V201231x'].replace(list(range(-9, 0)), np.nan).value_counts(normalize=True)
print(f"  Included:  Dem={sum(inc_party.get(k,0) for k in [1,2])*100:.1f}%, Ind={sum(inc_party.get(k,0) for k in [3,4,5])*100:.1f}%, Rep={sum(inc_party.get(k,0) for k in [6,7])*100:.1f}%")
print(f"  Excluded:  Dem={sum(exc_party.get(k,0) for k in [1,2])*100:.1f}%, Ind={sum(exc_party.get(k,0) for k in [3,4,5])*100:.1f}%, Rep={sum(exc_party.get(k,0) for k in [6,7])*100:.1f}%")

# Ideology
print("\nPolitical Ideology (V201200):")
inc_ideo = df_included_raw['V201200'].replace(list(range(-9, 0)) + [99], np.nan).value_counts(normalize=True)
exc_ideo = df_excluded_raw['V201200'].replace(list(range(-9, 0)) + [99], np.nan).value_counts(normalize=True)
print(f"  Included:  Left={sum(inc_ideo.get(k,0) for k in [1,2,3])*100:.1f}%, Center={inc_ideo.get(4,0)*100:.1f}%, Right={sum(inc_ideo.get(k,0) for k in [5,6,7])*100:.1f}%")
print(f"  Excluded:  Left={sum(exc_ideo.get(k,0) for k in [1,2,3])*100:.1f}%, Center={exc_ideo.get(4,0)*100:.1f}%, Right={sum(exc_ideo.get(k,0) for k in [5,6,7])*100:.1f}%")

# ============================================================================
# STEP 5: SELECT FINAL COLUMNS AND SAVE
# ============================================================================

print("\n" + "="*60)
print("STEP 5: Save cleaned dataset")
print("="*60)

independent_vars = [
    'gender', 'age_group', 'region', 'zona', 'race',
    'education', 'income', 'ideology', 'party', 'religion', 'interest_politics'
]

# Final columns to keep
final_cols = independent_vars + ['presidential_vote', 'abortion_opinion']
df_final = df_filtered[final_cols].copy()

# Save
df_final.to_csv('anes2020_cleaned.csv', index=False)
print(f"Saved: anes2020_cleaned.csv ({len(df_final)} rows, {len(df_final.columns)} columns)")

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

print("\nAbortion Opinion:")
print(df_final['abortion_opinion'].value_counts())
