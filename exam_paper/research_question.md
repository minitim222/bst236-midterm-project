# Research Question and Analysis Plan

## Research Question

**Formal JAMA-style objective:**
To characterize the geographic distribution, institutional concentration, scientific focus areas, and financial impact of NIH grant terminations and funding disruptions in 2025, and to examine factors associated with permanent termination versus reinstatement among disrupted awards.

## Background
In early 2025, the Trump administration initiated an unprecedented wave of NIH grant terminations and funding freezes, disrupting thousands of federally funded biomedical research projects. This study uses data from Grant Witness, a public tracker of federal grant disruptions, to provide a comprehensive cross-sectional analysis of 5,419 affected awards.

## Exposure / Treatment Variable
- NIH grant disruption status: Terminated (❌), Frozen (🧊), Unfrozen (🚰), Possibly Reinstated (🔄)

## Outcome Variables
1. **Binary outcome**: Permanent termination (1) vs. non-termination (0) — primary outcome
2. **Continuous outcome**: Estimated remaining (unspent) funding at risk ($) — financial impact

## Population
NIH-funded research institutions and investigators whose grants were disrupted in 2025

## Study Design
Cross-sectional analysis of grant termination records

## Covariates / Factors
- Grant mechanism (activity code: R01, F31, R21, R35, T32, etc.)
- Funding category (Research and Development vs. Research Training)
- Institution type (Schools of Medicine, Arts and Sciences, Public Health, etc.)
- Geographic location (state)
- Total award amount
- Cancellation source (HHS reported, court filing, self-reported)

## Hypotheses
1. Research training grants (F31, T32, R25) targeting DEI-related populations will be disproportionately terminated vs. reinstated
2. Schools of Medicine will bear the largest absolute financial burden due to higher average award amounts
3. States with more grants (NY, MA, CA, IL) will face greater total financial disruption
4. Larger awards ($>$2M) are more likely to be contested/reinstated via litigation

## Subgroup Analyses
1. **By funding category**: Research and Development vs. Research Training (training grants were specifically targeted in the DEI-rollback)
2. **By institution type**: Schools of Medicine vs. Schools of Public Health vs. other

## Analysis Plan

### Table 1: Descriptive Statistics
- N grants by status category
- Financial metrics by status (mean/median award, total at risk)
- Geographic distribution (top 10 states)
- Institutional type distribution
- Top activity codes

### Main Analysis
- Logistic regression: Pr(terminated = 1) ~ activity_code + funding_category + org_type + org_state + log(total_award)
- Focus: Which grant types are most likely to receive permanent termination vs. reinstatement

### Subgroup Analysis  
1. By funding_category: Compare terminated vs. reinstated within R&D vs. Training
2. By org_type: Compare terminated vs. reinstated within medical schools vs. others

### Robustness Check
- OLS regression on log(total_estimated_remaining) among all disrupted grants
- Alternative: multinomial logit across all 5 status categories

### Figures
1. **Figure 1**: Time trend of grant terminations by month (bar chart) + cumulative disruptions
2. **Figure 2**: Geographic map (horizontal bar chart) — total awards at risk by state
3. **Figure 3**: Forest plot of odds ratios from logistic regression (factors associated with permanent termination)
