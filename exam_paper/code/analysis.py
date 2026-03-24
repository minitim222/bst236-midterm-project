#!/usr/bin/env python3
"""
Analysis script for JAMA Network Open paper:
"Geographic Distribution, Institutional Targeting, and Financial Impact
of NIH Grant Terminations in 2025: A Cross-Sectional Analysis"

Generates all tables, figures, and statistical results.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

# === JAMA FIGURE STYLING ===
JAMA_CRIMSON = '#AF1E37'
JAMA_DARK    = '#333333'
JAMA_GRAY    = '#666666'
JAMA_LIGHT   = '#C8C8C8'
JAMA_GOLD    = '#C39B32'

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'legend.frameon': False,
    'figure.figsize': (7, 5),
    'figure.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.grid': False,
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.15,
    'lines.linewidth': 1.5,
    'lines.markersize': 6,
})

# === PATHS ===
DATA_DIR  = Path('../data')
OUTPUT_DIR = Path('output')
FIG_DIR   = OUTPUT_DIR / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

print("Loading data...")

# === SECTION 1: DATA LOADING ===
df = pd.read_csv(DATA_DIR / 'nih_terminations.csv', low_memory=False)
print(f"Loaded {len(df):,} records with {len(df.columns)} columns")

# === SECTION 2: DATA CLEANING & VARIABLE CONSTRUCTION ===

# Clean status labels (remove emoji for analysis)
status_map = {
    '🔄 Possibly Reinstated':       'Possibly Reinstated',
    '🚰 Unfrozen Funding':           'Unfrozen',
    '❌ Terminated':                 'Terminated',
    '💧 Possibly Unfrozen Funding':  'Possibly Unfrozen',
    '🧊 Frozen Funding':             'Frozen',
}
df['status_clean'] = df['status'].map(status_map).fillna(df['status'])

# Binary outcome: permanently terminated vs. all others (includes possibly reinstated, unfrozen, frozen)
df['terminated'] = (df['status_clean'] == 'Terminated').astype(int)

# Binary outcome: reinstated/unfrozen (funding partially or fully restored)
df['reinstated'] = df['status_clean'].isin(['Unfrozen', 'Possibly Reinstated', 'Possibly Unfrozen']).astype(int)

# Parse dates
df['termination_date'] = pd.to_datetime(df['termination_date'], errors='coerce')
df['termination_month'] = df['termination_date'].dt.to_period('M')

# Financial variables
df['total_award_m']     = df['total_award'] / 1e6
df['total_remaining_m'] = df['total_estimated_remaining'] / 1e6
df['log_total_award']   = np.log1p(df['total_award'].clip(lower=0))

# Funding category binary
df['is_training'] = (df['funding_category'] == 'Research Training and Career Development').astype(int)
df['is_rd']       = (df['funding_category'] == 'Research and Development').astype(int)

# Institution type simplified
med_types = {'SCHOOLS OF MEDICINE', 'Independent Hospitals'}
ph_types  = {'SCHOOLS OF PUBLIC HEALTH'}
arts_types = {'SCHOOLS OF ARTS AND SCIENCES', 'UNIVERSITY-WIDE', 'GRADUATE SCHOOLS'}

def map_org_simple(ot):
    if pd.isna(ot): return 'Other'
    if ot in med_types:   return 'Medical School/Hospital'
    if ot in ph_types:    return 'School of Public Health'
    if ot in arts_types:  return 'Arts & Sciences/University'
    return 'Other'

df['org_simple'] = df['org_type'].map(map_org_simple)

# Activity code simplified
def map_activity(code):
    if pd.isna(code): return 'Other'
    c = str(code).strip()
    if c == 'R01': return 'R01'
    if c in ('F31', 'F32', 'F99'): return 'F (Fellowship)'
    if c in ('T32', 'T15', 'T90'): return 'T (Training)'
    if c in ('K01', 'K08', 'K23', 'K99', 'R00'): return 'K/R00 (Career Dev)'
    if c in ('R21', 'R03'): return 'R21/R03'
    if c in ('R35', 'R37'): return 'R35/R37'
    if c in ('U01', 'U54', 'UM1'): return 'U (Cooperative)'
    if c == 'R25': return 'R25 (Education)'
    return 'Other'

df['activity_simple'] = df['activity_code'].map(map_activity)

# Cancellation source simplified
def map_cancel(src):
    if pd.isna(src): return 'Unknown'
    if 'HHS' in str(src): return 'HHS Reported'
    if 'Court' in str(src): return 'Court Filing'
    if 'Self' in str(src): return 'Self Reported'
    return 'Other'

df['cancel_simple'] = df['cancellation_source'].map(map_cancel)

# State region grouping
northeast = {'NY', 'MA', 'CT', 'RI', 'NH', 'VT', 'ME', 'NJ', 'PA'}
southeast = {'FL', 'GA', 'NC', 'SC', 'VA', 'TN', 'AL', 'MS', 'LA', 'AR', 'KY', 'WV', 'DC', 'MD', 'DE'}
midwest   = {'IL', 'OH', 'MI', 'MN', 'WI', 'IN', 'MO', 'IA', 'KS', 'NE', 'ND', 'SD'}
west      = {'CA', 'WA', 'OR', 'CO', 'AZ', 'NM', 'NV', 'UT', 'ID', 'MT', 'WY', 'AK', 'HI'}

def map_region(st):
    if pd.isna(st): return 'Other'
    s = str(st).strip().upper()
    if s in northeast: return 'Northeast'
    if s in southeast: return 'Southeast'
    if s in midwest:   return 'Midwest'
    if s in west:      return 'West'
    return 'Other/Territory'

df['region'] = df['org_state'].map(map_region)

print(f"Status distribution:\n{df['status_clean'].value_counts()}\n")
print(f"Terminated: {df['terminated'].sum():,} ({df['terminated'].mean()*100:.1f}%)")
print(f"Reinstated/Unfrozen: {df['reinstated'].sum():,} ({df['reinstated'].mean()*100:.1f}%)")
print()

# === SECTION 3: DESCRIPTIVE STATISTICS (TABLE 1) ===
print("Computing Table 1...")

rows = []

def fmt_n_pct(n, total):
    return f"{n:,} ({n/total*100:.1f}%)"

total = len(df)
n_term = df['terminated'].sum()
n_reinst = df['reinstated'].sum()
n_frozen = (df['status_clean'].isin(['Frozen', 'Possibly Unfrozen'])).sum()

# Status
rows.append({'characteristic': 'Grant Status', 'all': f'N = {total:,}',
             'terminated': f'N = {n_term:,}', 'reinstated_unfrozen': f'N = {n_reinst:,}'})
for s, label in [('Terminated', 'Terminated'), ('Unfrozen', 'Unfrozen'),
                 ('Possibly Reinstated', 'Possibly Reinstated'),
                 ('Frozen', 'Frozen'), ('Possibly Unfrozen', 'Possibly Unfrozen')]:
    n = (df['status_clean'] == s).sum()
    rows.append({'characteristic': f'  {label}',
                 'all': fmt_n_pct(n, total), 'terminated': '', 'reinstated_unfrozen': ''})

# Funding category
rows.append({'characteristic': 'Funding Category', 'all': '', 'terminated': '', 'reinstated_unfrozen': ''})
for cat in ['Research and Development', 'Research Training and Career Development',
            'Other Transactions', 'Small Business']:
    sub = df[df['funding_category'] == cat]
    n_all  = len(sub)
    n_t    = sub['terminated'].sum()
    n_r    = sub['reinstated'].sum()
    rows.append({'characteristic': f'  {cat}',
                 'all': fmt_n_pct(n_all, total),
                 'terminated': fmt_n_pct(n_t, max(n_all,1)),
                 'reinstated_unfrozen': fmt_n_pct(n_r, max(n_all,1))})

# Activity code
rows.append({'characteristic': 'Activity Code (Top)', 'all': '', 'terminated': '', 'reinstated_unfrozen': ''})
top_act = df['activity_simple'].value_counts().head(8).index
for act in top_act:
    sub = df[df['activity_simple'] == act]
    n_all = len(sub); n_t = sub['terminated'].sum(); n_r = sub['reinstated'].sum()
    rows.append({'characteristic': f'  {act}',
                 'all': fmt_n_pct(n_all, total),
                 'terminated': fmt_n_pct(n_t, max(n_all,1)),
                 'reinstated_unfrozen': fmt_n_pct(n_r, max(n_all,1))})

# Institution type
rows.append({'characteristic': 'Institution Type', 'all': '', 'terminated': '', 'reinstated_unfrozen': ''})
for ot in ['Medical School/Hospital', 'Arts & Sciences/University', 'School of Public Health', 'Other']:
    sub = df[df['org_simple'] == ot]
    n_all = len(sub); n_t = sub['terminated'].sum(); n_r = sub['reinstated'].sum()
    rows.append({'characteristic': f'  {ot}',
                 'all': fmt_n_pct(n_all, total),
                 'terminated': fmt_n_pct(n_t, max(n_all,1)),
                 'reinstated_unfrozen': fmt_n_pct(n_r, max(n_all,1))})

# Geographic region
rows.append({'characteristic': 'Geographic Region', 'all': '', 'terminated': '', 'reinstated_unfrozen': ''})
for reg in ['Northeast', 'Midwest', 'Southeast', 'West', 'Other/Territory']:
    sub = df[df['region'] == reg]
    n_all = len(sub); n_t = sub['terminated'].sum(); n_r = sub['reinstated'].sum()
    rows.append({'characteristic': f'  {reg}',
                 'all': fmt_n_pct(n_all, total),
                 'terminated': fmt_n_pct(n_t, max(n_all,1)),
                 'reinstated_unfrozen': fmt_n_pct(n_r, max(n_all,1))})

# Financial metrics
valid = df[df['total_award'] > 0]
rows.append({'characteristic': 'Financial Metrics (Awards with Positive Value)',
             'all': f'N = {len(valid):,}', 'terminated': '', 'reinstated_unfrozen': ''})

def med_mean(sub, col):
    v = sub[col].dropna()
    v = v[v > 0]
    if len(v) == 0: return 'N/A'
    return f"${v.mean()/1e6:.2f}M (median: ${v.median()/1e6:.2f}M)"

rows.append({'characteristic': '  Mean (Median) Total Award',
             'all': med_mean(valid, 'total_award'),
             'terminated': med_mean(valid[valid['terminated']==1], 'total_award'),
             'reinstated_unfrozen': med_mean(valid[valid['reinstated']==1], 'total_award')})

total_at_risk = df['total_estimated_remaining'].sum()
term_at_risk  = df[df['terminated']==1]['total_estimated_remaining'].sum()
reinst_at_risk = df[df['reinstated']==1]['total_estimated_remaining'].sum()

rows.append({'characteristic': '  Total Estimated Remaining Funds',
             'all': f'${total_at_risk/1e9:.2f}B',
             'terminated': f'${term_at_risk/1e9:.2f}B',
             'reinstated_unfrozen': f'${reinst_at_risk/1e9:.2f}B'})

rows.append({'characteristic': '  Total Obligated Award Amount',
             'all': f'${df["total_award"].sum()/1e9:.2f}B',
             'terminated': f'${df[df["terminated"]==1]["total_award"].sum()/1e9:.2f}B',
             'reinstated_unfrozen': f'${df[df["reinstated"]==1]["total_award"].sum()/1e9:.2f}B'})

# Cancellation source
rows.append({'characteristic': 'Cancellation Source', 'all': '', 'terminated': '', 'reinstated_unfrozen': ''})
for src in ['HHS Reported', 'Self Reported', 'Court Filing', 'Unknown']:
    sub = df[df['cancel_simple'] == src]
    n_all = len(sub); n_t = sub['terminated'].sum(); n_r = sub['reinstated'].sum()
    rows.append({'characteristic': f'  {src}',
                 'all': fmt_n_pct(n_all, total),
                 'terminated': fmt_n_pct(n_t, max(n_all,1)),
                 'reinstated_unfrozen': fmt_n_pct(n_r, max(n_all,1))})

table1 = pd.DataFrame(rows)
table1.to_csv(OUTPUT_DIR / 'table1.csv', index=False)
print(f"Table 1 saved: {len(table1)} rows")

# === SECTION 4: MAIN REGRESSION ===
print("\nRunning main logistic regression...")

# Prepare regression sample
reg_df = df[df['total_award'] > 0].copy()

# Create dummies for categorical variables
activity_dummies = pd.get_dummies(reg_df['activity_simple'], prefix='act', drop_first=True)
org_dummies      = pd.get_dummies(reg_df['org_simple'],     prefix='org', drop_first=True)
region_dummies   = pd.get_dummies(reg_df['region'],         prefix='reg', drop_first=True)
cancel_dummies   = pd.get_dummies(reg_df['cancel_simple'],  prefix='src', drop_first=True)

X_cols_df = pd.concat([
    reg_df[['log_total_award', 'is_training']].reset_index(drop=True),
    activity_dummies.reset_index(drop=True),
    org_dummies.reset_index(drop=True),
    region_dummies.reset_index(drop=True),
    cancel_dummies.reset_index(drop=True),
], axis=1)

X_cols_df = X_cols_df.astype(float)
y = reg_df['terminated'].values

# Drop rows with any NaN
mask = ~(X_cols_df.isna().any(axis=1) | pd.isna(y))
X_clean = sm.add_constant(X_cols_df[mask].astype(float))
y_clean = y[mask]

print(f"  Regression N = {mask.sum():,}")

try:
    logit_model = sm.Logit(y_clean, X_clean).fit(
        method='bfgs', maxiter=200, disp=False
    )
    
    # Extract results
    params = logit_model.params
    conf   = logit_model.conf_int()
    pvals  = logit_model.pvalues
    
    # Odds ratios
    or_df = pd.DataFrame({
        'variable':  params.index,
        'log_odds':  params.values,
        'or':        np.exp(params.values),
        'ci_lower':  np.exp(conf[0].values),
        'ci_upper':  np.exp(conf[1].values),
        'p_value':   pvals.values,
        'n_obs':     mask.sum(),
    })
    or_df.to_csv(OUTPUT_DIR / 'main_results.csv', index=False)
    print(f"  Main results saved: {len(or_df)} rows")

    # Print key results
    key_vars = [c for c in params.index if c != 'const']
    for v in key_vars[:10]:
        print(f"    {v}: OR={np.exp(params[v]):.3f}, p={pvals[v]:.3f}")
        
except Exception as e:
    print(f"  Logit failed: {e}. Trying simpler model...")
    # Simpler model: just training flag + log award
    X_simple = sm.add_constant(reg_df[['log_total_award', 'is_training']].dropna().astype(float))
    y_simple = reg_df.loc[X_simple.index, 'terminated'].values
    logit_model = sm.Logit(y_simple, X_simple).fit(disp=False)
    params = logit_model.params
    conf   = logit_model.conf_int()
    pvals  = logit_model.pvalues
    or_df = pd.DataFrame({
        'variable':  params.index,
        'log_odds':  params.values,
        'or':        np.exp(params.values),
        'ci_lower':  np.exp(conf[0].values),
        'ci_upper':  np.exp(conf[1].values),
        'p_value':   pvals.values,
        'n_obs':     len(y_simple),
    })
    or_df.to_csv(OUTPUT_DIR / 'main_results.csv', index=False)

# === SECTION 5: SUBGROUP ANALYSES ===
print("\nRunning subgroup analyses...")

subgroup_rows = []

# Subgroup 1: By funding category
for cat_name, cat_val in [('Research and Development', 0), ('Research Training', 1)]:
    sub = reg_df[reg_df['is_training'] == cat_val].copy()
    
    # Simple logistic: terminated ~ log_total_award + region_dummies
    region_dum = pd.get_dummies(sub['region'], prefix='reg', drop_first=True).reset_index(drop=True)
    X_sub = pd.concat([
        sub[['log_total_award']].reset_index(drop=True),
        region_dum
    ], axis=1).astype(float)
    y_sub = sub['terminated'].reset_index(drop=True).values
    
    mask_s = ~(X_sub.isna().any(axis=1) | pd.isna(y_sub))
    try:
        m = sm.Logit(y_sub[mask_s], sm.add_constant(X_sub[mask_s])).fit(disp=False, maxiter=200)
        # Award size effect
        subgroup_rows.append({
            'subgroup': f'{cat_name}',
            'variable': 'log_total_award',
            'or': np.exp(m.params.get('log_total_award', np.nan)),
            'ci_lower': np.exp(m.conf_int().loc['log_total_award', 0]) if 'log_total_award' in m.params else np.nan,
            'ci_upper': np.exp(m.conf_int().loc['log_total_award', 1]) if 'log_total_award' in m.params else np.nan,
            'p_value': m.pvalues.get('log_total_award', np.nan),
            'n_obs': mask_s.sum(),
            'pct_terminated': f"{sub['terminated'].mean()*100:.1f}%"
        })
    except Exception as e:
        print(f"  Subgroup {cat_name} failed: {e}")
        subgroup_rows.append({
            'subgroup': cat_name, 'variable': 'log_total_award',
            'or': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan,
            'p_value': np.nan, 'n_obs': mask_s.sum(),
            'pct_terminated': f"{sub['terminated'].mean()*100:.1f}%"
        })

# Subgroup 2: By institution type
for inst_name in ['Medical School/Hospital', 'School of Public Health', 'Arts & Sciences/University']:
    sub = reg_df[reg_df['org_simple'] == inst_name].copy()
    if len(sub) < 50:
        continue
    
    X_sub = sub[['log_total_award', 'is_training']].dropna().astype(float)
    y_sub = sub.loc[X_sub.index, 'terminated'].values
    
    try:
        m = sm.Logit(y_sub, sm.add_constant(X_sub)).fit(disp=False, maxiter=200)
        subgroup_rows.append({
            'subgroup': inst_name,
            'variable': 'log_total_award',
            'or': np.exp(m.params.get('log_total_award', np.nan)),
            'ci_lower': np.exp(m.conf_int().loc['log_total_award', 0]) if 'log_total_award' in m.params else np.nan,
            'ci_upper': np.exp(m.conf_int().loc['log_total_award', 1]) if 'log_total_award' in m.params else np.nan,
            'p_value': m.pvalues.get('log_total_award', np.nan),
            'n_obs': len(y_sub),
            'pct_terminated': f"{sub['terminated'].mean()*100:.1f}%"
        })
    except Exception as e:
        print(f"  Subgroup {inst_name} failed: {e}")
        subgroup_rows.append({
            'subgroup': inst_name, 'variable': 'log_total_award',
            'or': np.nan, 'ci_lower': np.nan, 'ci_upper': np.nan,
            'p_value': np.nan, 'n_obs': len(y_sub),
            'pct_terminated': f"{sub['terminated'].mean()*100:.1f}%"
        })

sub_df = pd.DataFrame(subgroup_rows)
sub_df.to_csv(OUTPUT_DIR / 'subgroup_results.csv', index=False)
print(f"  Subgroup results saved: {len(sub_df)} rows")

# === SECTION 6: ROBUSTNESS CHECKS ===
print("\nRunning robustness checks...")

# OLS on log remaining funds (continuous outcome)
robust_rows = []

ols_df = df[df['total_estimated_remaining'] > 0].copy()
ols_df['log_remaining'] = np.log(ols_df['total_estimated_remaining'])

act_d = pd.get_dummies(ols_df['activity_simple'], prefix='act', drop_first=True).reset_index(drop=True)
org_d = pd.get_dummies(ols_df['org_simple'], prefix='org', drop_first=True).reset_index(drop=True)
reg_d = pd.get_dummies(ols_df['region'], prefix='reg', drop_first=True).reset_index(drop=True)

X_ols = pd.concat([
    ols_df[['log_total_award', 'is_training']].reset_index(drop=True),
    act_d, org_d, reg_d
], axis=1).astype(float)
y_ols = ols_df['log_remaining'].reset_index(drop=True).values

mask_ols = ~(X_ols.isna().any(axis=1) | np.isnan(y_ols))
try:
    ols_model = sm.OLS(y_ols[mask_ols], sm.add_constant(X_ols[mask_ols])).fit(cov_type='HC1')
    for var in ['log_total_award', 'is_training']:
        if var in ols_model.params.index:
            robust_rows.append({
                'model': 'OLS_log_remaining',
                'variable': var,
                'coefficient': ols_model.params[var],
                'ci_lower': ols_model.conf_int().loc[var, 0],
                'ci_upper': ols_model.conf_int().loc[var, 1],
                'p_value': ols_model.pvalues[var],
                'n_obs': mask_ols.sum()
            })
    print(f"  OLS robustness N = {mask_ols.sum():,}")
except Exception as e:
    print(f"  OLS robustness failed: {e}")

# Unadjusted logistic (no covariates) as comparison
try:
    X_unadj = sm.add_constant(reg_df[['log_total_award']].dropna().astype(float))
    y_unadj = reg_df.loc[X_unadj.index, 'terminated'].values
    m_unadj = sm.Logit(y_unadj, X_unadj).fit(disp=False, maxiter=200)
    robust_rows.append({
        'model': 'Logit_unadjusted',
        'variable': 'log_total_award',
        'coefficient': np.exp(m_unadj.params['log_total_award']),
        'ci_lower': np.exp(m_unadj.conf_int().loc['log_total_award', 0]),
        'ci_upper': np.exp(m_unadj.conf_int().loc['log_total_award', 1]),
        'p_value': m_unadj.pvalues['log_total_award'],
        'n_obs': len(y_unadj)
    })
except Exception as e:
    print(f"  Unadjusted logit failed: {e}")

robust_df = pd.DataFrame(robust_rows)
robust_df.to_csv(OUTPUT_DIR / 'robustness_results.csv', index=False)
print(f"  Robustness results saved: {len(robust_df)} rows")

# === SECTION 7: FIGURES ===
print("\nGenerating figures...")

# ---- FIGURE 1: Monthly Trend of Grant Disruptions ----
print("  Figure 1: Monthly termination trends...")

term_by_month = df[df['termination_date'].notna()].copy()
term_by_month = term_by_month[term_by_month['termination_date'] >= '2025-01-01']
term_by_month = term_by_month[term_by_month['termination_date'] <= '2026-01-01']
monthly = term_by_month.groupby([term_by_month['termination_date'].dt.to_period('M'), 'status_clean']).size().unstack(fill_value=0)

fig, axes = plt.subplots(2, 1, figsize=(8, 9))

# Panel A: Stacked bar by status
ax1 = axes[0]
months = monthly.index.astype(str)
colors = {'Terminated': JAMA_CRIMSON, 'Unfrozen': JAMA_DARK,
          'Possibly Reinstated': JAMA_GRAY, 'Frozen': JAMA_GOLD, 'Possibly Unfrozen': JAMA_LIGHT}
bottom = np.zeros(len(months))
for status in ['Terminated', 'Frozen', 'Possibly Reinstated', 'Unfrozen', 'Possibly Unfrozen']:
    if status in monthly.columns:
        vals = monthly[status].values
        ax1.bar(months, vals, bottom=bottom, color=colors.get(status, JAMA_GRAY),
                label=status, width=0.7)
        bottom += vals

ax1.set_xlabel('Month')
ax1.set_ylabel('Number of Grant Actions')
ax1.set_title('A', loc='left', fontsize=12, fontweight='bold')
ax1.text(0.5, 1.02, 'Monthly NIH Grant Disruptions, 2025',
         transform=ax1.transAxes, ha='center', fontsize=11)
ax1.legend(loc='upper right', fontsize=8)
ax1.tick_params(axis='x', rotation=45)

# Panel B: Cumulative disruptions over time
ax2 = axes[1]
daily = df[df['termination_date'].notna()].copy()
daily = daily[daily['termination_date'] >= '2025-01-01']
daily = daily[daily['termination_date'] <= '2025-12-31']
daily_count = daily.groupby('termination_date').size().reset_index(name='n')
daily_count = daily_count.sort_values('termination_date')
daily_count['cumulative'] = daily_count['n'].cumsum()

# Also compute cumulative financial
daily_fin = daily.groupby('termination_date')['total_award'].sum().reset_index()
daily_fin = daily_fin.sort_values('termination_date')
daily_fin['cum_award_b'] = daily_fin['total_award'].cumsum() / 1e9

ax2b = ax2.twinx()
ax2.plot(daily_count['termination_date'], daily_count['cumulative'],
         '-', color=JAMA_CRIMSON, linewidth=2, label='Cumulative grants')
ax2b.plot(daily_fin['termination_date'], daily_fin['cum_award_b'],
          '--', color=JAMA_DARK, linewidth=1.5, label='Cumulative award ($B)')

ax2.set_xlabel('Date')
ax2.set_ylabel('Cumulative Grant Actions', color=JAMA_CRIMSON)
ax2b.set_ylabel('Cumulative Award Amount (Billion $)', color=JAMA_DARK)
ax2.set_title('B', loc='left', fontsize=12, fontweight='bold')
ax2.text(0.5, 1.02, 'Cumulative NIH Grant Disruptions and Financial Impact',
         transform=ax2.transAxes, ha='center', fontsize=11)

lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)

plt.tight_layout()
fig.savefig(FIG_DIR / 'figure1.pdf', dpi=300, bbox_inches='tight')
fig.savefig(FIG_DIR / 'figure1.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Figure 1 saved.")

# ---- FIGURE 2: Geographic Distribution ----
print("  Figure 2: Geographic distribution...")

state_summary = df.groupby('org_state').agg(
    total_grants=('terminated', 'count'),
    n_terminated=('terminated', 'sum'),
    n_reinstated=('reinstated', 'sum'),
    total_award_b=('total_award', lambda x: x.sum() / 1e9),
    total_remaining_m=('total_estimated_remaining', lambda x: x.sum() / 1e6),
).reset_index()
state_summary['pct_terminated'] = state_summary['n_terminated'] / state_summary['total_grants'] * 100
state_top15 = state_summary.nlargest(15, 'total_grants').sort_values('total_grants')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7))

# Panel A: Total grants by state
ax1.barh(state_top15['org_state'], state_top15['total_grants'],
         color=JAMA_CRIMSON, height=0.7, edgecolor='white')
ax1.set_xlabel('Number of Disrupted Grants')
ax1.set_title('A', loc='left', fontsize=12, fontweight='bold')
ax1.text(0.5, 1.02, 'Top 15 States by Number of Disrupted Grants',
         transform=ax1.transAxes, ha='center', fontsize=10)
for i, (val, state) in enumerate(zip(state_top15['total_grants'], state_top15['org_state'])):
    ax1.text(val + 10, i, f'{val:,}', va='center', fontsize=8)

# Panel B: Total award amount at risk
ax2.barh(state_top15['org_state'], state_top15['total_award_b'],
         color=JAMA_DARK, height=0.7, edgecolor='white')
ax2.set_xlabel('Total Award Amount (Billion $)')
ax2.set_title('B', loc='left', fontsize=12, fontweight='bold')
ax2.text(0.5, 1.02, 'Top 15 States by Total Award Amount Disrupted',
         transform=ax2.transAxes, ha='center', fontsize=10)
for i, (val, state) in enumerate(zip(state_top15['total_award_b'], state_top15['org_state'])):
    ax2.text(val + 0.01, i, f'${val:.2f}B', va='center', fontsize=8)

plt.tight_layout()
fig.savefig(FIG_DIR / 'figure2.pdf', dpi=300, bbox_inches='tight')
fig.savefig(FIG_DIR / 'figure2.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Figure 2 saved.")

# ---- FIGURE 3: Forest Plot of Odds Ratios ----
print("  Figure 3: Forest plot (odds ratios)...")

try:
    or_data = pd.read_csv(OUTPUT_DIR / 'main_results.csv')
    # Select key variables for forest plot
    exclude = ['const']
    plot_vars = or_data[~or_data['variable'].isin(exclude)].copy()
    
    # Clean up variable names for display
    def clean_var_name(v):
        v = str(v)
        if v.startswith('act_'): return 'Grant type: ' + v[4:].replace('_', ' ')
        if v.startswith('org_'): return 'Inst type: ' + v[4:].replace('_', ' ')
        if v.startswith('reg_'): return 'Region: ' + v[4:].replace('_', ' ')
        if v.startswith('src_'): return 'Source: ' + v[4:].replace('_', ' ')
        if v == 'log_total_award': return 'Log(Award Size)'
        if v == 'is_training':     return 'Training Grant (vs R&D)'
        return v
    
    plot_vars['label'] = plot_vars['variable'].map(clean_var_name)
    
    # Filter to reasonable OR range
    plot_vars = plot_vars[
        (plot_vars['or'] > 0) & (plot_vars['or'] < 100) &
        (plot_vars['ci_lower'] > 0) & (plot_vars['ci_upper'] < 200)
    ].head(15).reset_index(drop=True)
    
    # Sort by OR
    plot_vars = plot_vars.sort_values('or', ascending=True).reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(9, max(5, len(plot_vars)*0.5 + 1)))
    
    y_pos = range(len(plot_vars))
    colors_or = [JAMA_CRIMSON if p < 0.05 else JAMA_GRAY for p in plot_vars['p_value']]
    
    ax.errorbar(plot_vars['or'], list(y_pos),
                xerr=[plot_vars['or'] - plot_vars['ci_lower'],
                      plot_vars['ci_upper'] - plot_vars['or']],
                fmt='o', color=JAMA_CRIMSON, capsize=3, capthick=1, markersize=6)
    
    # Color significant ones differently
    for i, (or_val, p) in enumerate(zip(plot_vars['or'], plot_vars['p_value'])):
        c = JAMA_CRIMSON if p < 0.05 else JAMA_GRAY
        ax.plot(or_val, i, 'o', color=c, markersize=7)
    
    ax.axvline(x=1.0, color=JAMA_LIGHT, linewidth=0.8, linestyle='--')
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(plot_vars['label'], fontsize=8)
    ax.set_xlabel('Odds Ratio (95% CI)')
    
    # Add OR text on right
    x_max = ax.get_xlim()[1]
    for i, row in plot_vars.iterrows():
        idx = list(plot_vars.index).index(i)
        ax.text(x_max * 1.02, idx,
                f"{row['or']:.2f} [{row['ci_lower']:.2f}, {row['ci_upper']:.2f}]",
                va='center', fontsize=7, color=JAMA_CRIMSON if row['p_value'] < 0.05 else JAMA_GRAY)
    
    ax.set_title('Factors Associated with Permanent Termination of NIH Grants\n(Logistic Regression, Odds Ratios)')
    plt.tight_layout()
    fig.savefig(FIG_DIR / 'figure3.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(FIG_DIR / 'figure3.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("  Figure 3 saved.")
    
except Exception as e:
    print(f"  Figure 3 failed: {e}")

# ---- FIGURE 4: Termination Rate by Institution Type and Funding Category ----
print("  Figure 4: Termination rate by subgroup...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

# Panel A: by institution type
inst_stats = df.groupby('org_simple').agg(
    n=('terminated', 'count'),
    n_term=('terminated', 'sum')
).reset_index()
inst_stats['pct_term'] = inst_stats['n_term'] / inst_stats['n'] * 100
inst_stats = inst_stats.sort_values('pct_term', ascending=True)

bars = ax1.barh(inst_stats['org_simple'], inst_stats['pct_term'],
                color=JAMA_CRIMSON, height=0.6, edgecolor='white')
ax1.set_xlabel('Permanent Termination Rate (%)')
ax1.set_title('A', loc='left', fontsize=12, fontweight='bold')
ax1.text(0.5, 1.02, 'Termination Rate by Institution Type',
         transform=ax1.transAxes, ha='center', fontsize=10)
for bar, (pct, n) in zip(bars, zip(inst_stats['pct_term'], inst_stats['n'])):
    ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{pct:.1f}% (N={n:,})', va='center', fontsize=8)
ax1.set_xlim(0, 35)

# Panel B: by activity code
act_stats = df.groupby('activity_simple').agg(
    n=('terminated', 'count'),
    n_term=('terminated', 'sum')
).reset_index()
act_stats['pct_term'] = act_stats['n_term'] / act_stats['n'] * 100
act_stats = act_stats[act_stats['n'] >= 50].sort_values('pct_term', ascending=True)

bars2 = ax2.barh(act_stats['activity_simple'], act_stats['pct_term'],
                 color=JAMA_DARK, height=0.6, edgecolor='white')
ax2.set_xlabel('Permanent Termination Rate (%)')
ax2.set_title('B', loc='left', fontsize=12, fontweight='bold')
ax2.text(0.5, 1.02, 'Termination Rate by Grant Mechanism',
         transform=ax2.transAxes, ha='center', fontsize=10)
for bar, (pct, n) in zip(bars2, zip(act_stats['pct_term'], act_stats['n'])):
    ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f'{pct:.1f}% (N={n:,})', va='center', fontsize=8)
ax2.set_xlim(0, 50)

plt.tight_layout()
fig.savefig(FIG_DIR / 'figure4.pdf', dpi=300, bbox_inches='tight')
fig.savefig(FIG_DIR / 'figure4.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("  Figure 4 saved.")

# === SUMMARY STATISTICS FOR PAPER ===
print("\n=== KEY NUMBERS FOR PAPER ===")
print(f"Total disrupted grants: {len(df):,}")
print(f"Permanently terminated: {df['terminated'].sum():,} ({df['terminated'].mean()*100:.1f}%)")
print(f"Reinstated/Unfrozen: {df['reinstated'].sum():,} ({df['reinstated'].mean()*100:.1f}%)")
print(f"Total award value: ${df['total_award'].sum()/1e9:.2f}B")
print(f"Total estimated remaining: ${df['total_estimated_remaining'].sum()/1e9:.2f}B")
print(f"Terminated amount: ${df[df['terminated']==1]['total_award'].sum()/1e9:.2f}B")
print(f"Top state: {df['org_state'].value_counts().index[0]} (N={df['org_state'].value_counts().iloc[0]:,})")
print(f"Top org type: {df['org_type'].value_counts().index[0]} (N={df['org_type'].value_counts().iloc[0]:,})")
print(f"R01 grants: {(df['activity_code']=='R01').sum():,}")
print(f"Training grants total: {df['is_training'].sum():,}")

# Check logistic regression key findings
if 'is_training' in or_df['variable'].values:
    row = or_df[or_df['variable'] == 'is_training'].iloc[0]
    print(f"\nTraining grant OR: {row['or']:.2f} (95% CI: {row['ci_lower']:.2f}-{row['ci_upper']:.2f}), p={row['p_value']:.3f}")
if 'log_total_award' in or_df['variable'].values:
    row = or_df[or_df['variable'] == 'log_total_award'].iloc[0]
    print(f"Log award OR: {row['or']:.2f} (95% CI: {row['ci_lower']:.2f}-{row['ci_upper']:.2f}), p={row['p_value']:.3f}")

print("\nAnalysis complete. Outputs saved to:", OUTPUT_DIR)
