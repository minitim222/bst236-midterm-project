# Rule 03: Statistical Analysis Plan

## Purpose

Choose the correct statistical method based on the data structure and research question, then write a comprehensive analysis script that produces all outputs needed for the paper.

---

## Method Selection Decision Tree

Work through this tree from top to bottom. The first matching pattern determines the method.

### 1. Staggered Policy Adoption (Preferred for Policy Evaluation)

**When to use:** Multiple units (states) adopted a policy at DIFFERENT times, and you want to estimate the causal effect.

**Identifying features in the data:**
- A policy table with announcement/implementation dates per state
- Dates vary across states
- Control states that never adopted the policy
- Individual-level or aggregate outcome data over time

**Method:** Staggered difference-in-differences

**Implementation options (in order of preference):**

Option A — Sun & Abraham (2021) estimator:
```python
# Using interaction-weighted estimator
# Group treated states into cohorts by adoption timing
# Estimate cohort-specific ATTs, then aggregate
import statsmodels.api as sm
# Manual implementation: create cohort x relative-time interactions
# Estimate via OLS with state and time fixed effects
```

Option B — Callaway & Sant'Anna (2021) via `differences` or manual:
```python
# Group-time ATT estimation
# Requires: group (cohort), time, outcome, treatment indicator
```

Option C — Standard two-way fixed effects (TWFE) as robustness:
```python
import statsmodels.api as sm
# Y = alpha + beta*POST*TREAT + X'gamma + state_FE + time_FE + epsilon
model = sm.OLS(y, X).fit(cov_type='cluster', cov_kwds={'groups': state_ids})
```

**Always report:** Event study coefficients (pre-treatment should be near zero for parallel trends).

**CRITICAL — State Fixed Effects:**
Always include individual state dummies (not just a binary treatment group indicator) when using DID. A single `mandate_state` dummy only controls for the average mandate-vs-non-mandate difference. Individual state dummies control for ALL time-invariant state-level confounders (political leaning, healthcare infrastructure, population density, etc.).

```python
# CORRECT: state fixed effects in the main DID model
state_dummies = pd.get_dummies(df['EST_ST'], prefix='st', drop_first=True)
df = pd.concat([df, state_dummies], axis=1)
st_cols = [c for c in df.columns if c.startswith('st_')]

# Main DID regression with state FE (note: NO mandate_state — it's absorbed by state FE)
# Keep post_mandate and did, plus covariates, plus week dummies, plus state dummies
X_cols = ['post_mandate', 'did'] + covariates + race_cols + week_cols + st_cols
X = sm.add_constant(df[X_cols].astype(float))
model = sm.WLS(y, X, weights=df['weight']).fit(
    cov_type='cluster', cov_kwds={'groups': df['EST_ST']}
)
# The 'did' coefficient is the DID estimate
# NOTE: Do NOT include 'mandate_state' — it is perfectly collinear with the state dummies
```

**CRITICAL — Event Study Collinearity:**
When treatment timing is staggered and you include both event-time dummies and week fixed effects, collinearity can occur. To avoid this:
- Do NOT include `mandate_state` in the event study model (absorbed by state FE)
- Use state FE instead of a `mandate_state` indicator
- If standard errors blow up or pre-trend coefficients are erratic, simplify by dropping week FE and using only event-time dummies plus state FE
- When you hit a `LinAlgError: Singular matrix`, it means perfect collinearity. Drop week FE first, then try dropping some event-time dummies.

```python
# CORRECT: event study with state FE, no week FE (avoids collinearity in staggered setting)
# Create event-time dummies (reference period = earliest event time)
ref_time = min(event_times)
event_dummies = {}
for et in event_times:
    if et == ref_time:
        continue
    col = f'evt_{int(et)}'.replace('-', 'neg')
    df[col] = (df['event_time'] == et).astype(float)
    event_dummies[et] = col

X_es_cols = list(event_dummies.values()) + covariates + race_cols + st_cols
# NOTE: no week_cols here to avoid collinearity with event-time dummies
X_es = sm.add_constant(df[X_es_cols].astype(float))
model_es = sm.WLS(y, X_es, weights=df['weight']).fit(
    cov_type='cluster', cov_kwds={'groups': df['EST_ST']}
)
```

### 2. Single Treatment Date (Simpler DID)

**When to use:** All treated units adopt the policy at the same time.

**Method:** Standard difference-in-differences

```python
import statsmodels.api as sm
# Create: treated (0/1), post (0/1), treated*post interaction
# Y = beta0 + beta1*treated + beta2*post + beta3*treated*post + X'gamma + eps
# beta3 is the DID estimate
X = sm.add_constant(df[['treated', 'post', 'treated_post'] + covariates])
model = sm.OLS(df['outcome'], X).fit(cov_type='cluster', cov_kwds={'groups': df['state']})
```

### 3. Interrupted Time Series (Aggregate Trends)

**When to use:** Single aggregate time series (e.g., national-level) with a known intervention date.

**Method:** Segmented regression

```python
# Y_t = beta0 + beta1*time + beta2*intervention + beta3*time_after + eps
# beta2 = level change, beta3 = slope change
```

### 4. Cross-Sectional with Binary Outcome

**When to use:** Single time point, outcome is 0/1.

**Method:** Logistic regression

```python
import statsmodels.api as sm
X = sm.add_constant(df[exposure_cols + covariate_cols])
model = sm.Logit(df['outcome'], X).fit(cov_type='cluster', cov_kwds={'groups': df['state']})
# Report odds ratios: np.exp(model.params), np.exp(model.conf_int())
```

### 5. Cross-Sectional with Continuous Outcome

**When to use:** Single time point, continuous outcome (rate, score, count).

**Method:** OLS with robust or clustered standard errors

```python
import statsmodels.api as sm
X = sm.add_constant(df[exposure_cols + covariate_cols])
model = sm.OLS(df['outcome'], X).fit(cov_type='HC1')
```

### 6. Panel Data (Same Units Over Time)

**When to use:** Same units observed repeatedly.

**Method:** Fixed effects panel regression

```python
from linearmodels.panel import PanelOLS
df = df.set_index(['unit_id', 'time'])
model = PanelOLS(df['outcome'], df[covariates], entity_effects=True, time_effects=True)
result = model.fit(cov_type='clustered', cluster_entity=True)
```

---

## Survey Weights

If the data includes survey weights (common in Census/HPS data):

- Use weighted estimation throughout
- For OLS: use WLS (weighted least squares)
```python
model = sm.WLS(y, X, weights=df['weight']).fit(cov_type='cluster', cov_kwds={'groups': df['state']})
```
- For descriptive stats: compute weighted means and weighted percentages
```python
weighted_mean = np.average(df['var'], weights=df['weight'])
# For categorical: weighted frequency = sum of weights per category / total weight
```
- State in the paper: "All analyses incorporated individual-level survey weights."
- Report "unweighted N (weighted %)" in Table 1

---

## Table 1: Descriptive Statistics

This table is **mandatory** for every paper. It compares the treatment and control groups.

### Structure

| Characteristic | All (N = total) | Treatment Group (n = n1) | Control Group (n = n2) |
|---|---|---|---|

### Required rows

Include ALL of these if the data has them. Missing any of these will be noticed by reviewers:
- **Sex**: Female, Male (count and %)
- **Age**: grouped into 2-4 categories (count and %)
- **Race**: Black, White, Other (count and %)
- **Ethnicity**: Hispanic, Non-Hispanic (count and %)
- **Marital status**: Married, Unmarried (count and %) — use `MS` variable if available
- **Education**: Less than college, College or higher (count and %)
- **Income**: 3-4 brackets (count and %) — use `INCOME` variable grouped into <$35K, $35K-$100K, >$100K, Unknown
- **Outcome variables split by pre/post period**: This is CRITICAL. Report:
  - Ever vaccinated in pre-period (e.g., weeks 31-33)
  - Ever vaccinated in post-period (e.g., weeks 34-39)
  - Primary series completed in pre-period
  - Primary series completed in post-period
  This allows readers to visually verify the DID pattern directly from the table.

```python
# CODE SNIPPET: computing pre/post outcome split for Table 1
# Define pre and post periods based on the earliest mandate announcement week
pre_weeks = [31, 32, 33]  # adjust based on the data
post_weeks = [34, 35, 36, 37, 38, 39]  # adjust based on the data

for period_name, week_list in [('premandate', pre_weeks), ('postmandate', post_weeks)]:
    period_df = df[df['WEEK'].isin(week_list)]
    for grp_name, grp_mask in [('All', slice(None)), ('Treatment', df['mandate_state']==1), ('Control', df['mandate_state']==0)]:
        sub = period_df[grp_mask] if isinstance(grp_mask, slice) else period_df[period_df.index.isin(grp_mask[grp_mask].index)]
        n_vacc = (sub['vaccinated'] == 1).sum()
        wpct = np.average(sub['vaccinated'], weights=sub['weight']) * 100
        # Store: f"Ever vaccinated in {period_name} period" -> f"{n_vacc:,} ({wpct:.1f})"
```

```python
# CODE SNIPPET: computing income brackets for Table 1
# INCOME: 1=<$25K, 2=$25-35K, 3=$35-50K, 4=$50-75K, 5=$75-100K, 6=$100-150K, 7=$150-200K, 8=$200K+
# -88=missing, -99=not selected
df['income_group'] = pd.cut(
    df['INCOME'].replace({-88: np.nan, -99: np.nan}),
    bins=[0, 2, 5, 8],  # <$35K, $35K-$100K, >$100K
    labels=['<$35,000', '$35,000-$100,000', '>$100,000']
)
# Add "Income unknown" for missing
```

```python
# CODE SNIPPET: marital status for Table 1
# MS: 1=now married, 2=widowed, 3=divorced, 4=separated, 5=never married
# -88=missing, -99=not selected
df['married'] = df['MS'].map({1: 'Married', 2: 'Unmarried', 3: 'Unmarried', 4: 'Unmarried', 5: 'Unmarried'})
df.loc[df['MS'] < 0, 'married'] = np.nan
```

### Formatting rules

- Numbers >= 1000: use thousands separator → `24\,294`
- Percentages: one decimal place → `(72.1)`
- Format: `Count (Percentage)` for categoricals, `Mean (SD)` for continuous
- If survey weights exist: report unweighted counts with weighted percentages
- Group headers in bold, individual categories indented with `\quad`

### Footnotes

Always include:
- Whether percentages are weighted
- Definition of treatment and control groups (list states if applicable)
- Definition of time periods (pre-mandate, post-mandate)
- Explanation of any grouped categories (e.g., "Other race includes Asian, multiracial, and any other race")

### Export format

Save to `exam_paper/output/table1.csv` with columns: `characteristic`, `all`, `treatment`, `control`.

---

## Main Regression Results

### What to report

For each regression, extract and save:
- Coefficient (or odds ratio for logistic)
- 95% confidence interval (lower, upper)
- P value
- Number of observations
- Baseline outcome level (weighted mean in the reference period)
- Percentage effect = coefficient / baseline × 100

### Export format

Save to `exam_paper/output/main_results.csv`:

```csv
model,outcome,event_time,coefficient,ci_lower,ci_upper,p_value,n_obs,baseline,pct_effect
main,ever_vaccinated,0,1.59,-0.46,3.65,0.13,31142,87.98,1.81
main,ever_vaccinated,2,3.46,0.29,6.63,0.03,31142,87.98,3.93
```

### Standard errors

- Always cluster at the unit of treatment (usually state level)
- Use `cov_type='cluster'` in statsmodels
- Report: "Standard errors were clustered at the state level"

---

## Subgroup / Stratified Analyses

Run the identical main model on at least 2 subsamples:

1. **Stratification by policy feature** (e.g., test-out option vs. no test-out)
2. **Stratification by demographic** (e.g., age 25-49 vs. 50-64)

For each subgroup:
- Re-estimate the full model on the restricted sample
- Report the same outputs (coefficient, CI, P, baseline, % effect)
- Save to `exam_paper/output/subgroup_results.csv`

---

## Robustness Checks

Run at least one of these:

1. **Alternative estimator**: If using Sun-Abraham, also run TWFE
2. **Unadjusted model**: Run without covariates (to show direction is stable)
3. **Alternative sample**: Exclude borderline units or use different inclusion criteria
4. **Placebo test**: If time series, test a fake treatment date to confirm no spurious effects

Save to `exam_paper/output/robustness_results.csv`.

---

## Analysis Script Structure

The script `exam_paper/code/analysis.py` must follow this layout:

```python
#!/usr/bin/env python3
"""
Analysis script for JAMA Network Open paper.
Generates all tables, figures, and statistical results.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Apply JAMA figure styling (from rules/04-visualization-style.md)
# ... (matplotlib rcParams here)

# === PATHS ===
DATA_DIR = Path('data')  # or wherever the data lives
OUTPUT_DIR = Path('output')
FIG_DIR = OUTPUT_DIR / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# === SECTION 1: DATA LOADING ===
# Load each dataset, handle encoding and date parsing

# === SECTION 2: DATA CLEANING & VARIABLE CONSTRUCTION ===
# Merge datasets, create treatment indicators, outcome variables, covariates
# Apply sample restrictions

# === SECTION 3: DESCRIPTIVE STATISTICS (TABLE 1) ===
# Compute N, weighted %, means, SDs by group
# Export to OUTPUT_DIR / 'table1.csv'

# === SECTION 4: MAIN REGRESSION ===
# Run primary model
# Export to OUTPUT_DIR / 'main_results.csv'

# === SECTION 5: SUBGROUP ANALYSES ===
# Run stratified models
# Export to OUTPUT_DIR / 'subgroup_results.csv'

# === SECTION 6: ROBUSTNESS CHECKS ===
# Run alternative specifications
# Export to OUTPUT_DIR / 'robustness_results.csv'

# === SECTION 7: FIGURES ===
# Generate Figure 1 (main results), Figure 2 (subgroup), etc.
# Save to FIG_DIR

print("Analysis complete. Outputs saved to:", OUTPUT_DIR)
```

---

## Common Pitfalls to Avoid

1. **Don't hardcode column names.** Read them from the data and adapt.
2. **Check for multicollinearity** before running regressions (drop redundant dummies).
3. **Handle the constant term**: use `sm.add_constant()` for OLS/Logit. But do NOT add a constant when you already include a full set of state or week dummies — one must be dropped.
4. **Drop NaN rows** before regression or use `missing='drop'` in statsmodels.
5. **Don't use more covariates than the data can support.** Rule of thumb: at least 10 observations per parameter.
6. **If DID is chosen**, verify parallel pre-trends by checking that pre-treatment coefficients are statistically insignificant. If pre-trends are noisy (large swings even though individually insignificant), acknowledge this honestly in the paper rather than claiming clean pre-trends.
7. **If logistic regression**, report odds ratios (exponentiated coefficients), not raw log-odds.
8. **Handle missing values in outcome-related variables carefully.** For survey data, coded values like -88 (missing) and -99 (question seen but not answered) should be set to NaN, NOT treated as valid responses. For secondary outcomes (e.g., DOSES), missing values among people who answered the primary outcome (RECVDVACC=1) should be explicitly handled — either impute or restrict the sample and report the restriction.
9. **Always use state fixed effects** (individual state dummies) in DID models, not just a binary treatment/control indicator. This is the standard in applied microeconomics.
10. **When using `pd.get_dummies` with a prefix, always exclude non-dummy columns** from the column selection. For example, if you create `race_cat` as a string column AND race dummies with `prefix='race'`, filter with `c.startswith('race_') and c != 'race_cat'`.
