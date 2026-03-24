# Rule 01: Data Exploration

## Purpose

Understand any dataset the exam provides before formulating a research question or writing analysis code. This stage produces a structured data summary that all subsequent stages depend on.

---

## Step-by-Step Process

### 1. Read Data_Description.md First

Before touching any data file, read `Data_Description.md` in the data folder. It explains:
- What each file contains
- What variables are in each dataset
- How to download any external data (e.g., Census microdata with shell scripts)
- How the datasets relate to each other

This file is the ground truth for understanding the data. The profiler output supplements it but does not replace it.

### 2. Run the Data Profiler

```bash
python workflow/scripts/data_profiler.py <data_folder_path>
```

The profiler automatically reports for every CSV/XLSX file:
- Shape (rows x columns)
- Column names with data types
- Missing value counts per column
- First 5 rows
- Summary statistics (mean, std, min, max, quartiles for numerics)
- Unique value counts for categorical columns (< 30 unique values)
- Date ranges for detected date columns
- Common columns across files (potential merge keys)

Save the output to `exam_paper/data_summary.md`.

### 3. Download External Data If Needed

If `Data_Description.md` includes download scripts (e.g., `wget` or `curl` commands for Census data), run them:

```bash
cd <data_folder>
# Execute the download commands from Data_Description.md
```

Then re-run the profiler on the newly downloaded files to include them in the summary.

### 4. Identify Key Data Characteristics

After reading the profiler output, determine:

**Unit of observation:**
- Individual-level (survey respondents, patients, workers)?
- State-level aggregates?
- County-level?
- Facility-level (hospitals, nursing homes)?

**Time structure:**
- Cross-sectional (single time point)?
- Repeated cross-sections (different individuals at different times)?
- Panel (same units over time)?
- Time series (aggregate counts over time)?

**Treatment/exposure variables:**
- Is there a policy variable with announcement/implementation dates?
- Is there a binary treatment indicator (treated vs. control)?
- Are there staggered adoption dates (different units adopt at different times)?
- Is there a continuous exposure variable?

**Outcome variables:**
- Binary outcomes (yes/no vaccination, death/survival)?
- Continuous outcomes (counts, rates, scores)?
- Multiple related outcomes?

**Potential confounders/covariates:**
- Demographics: age, sex, race, ethnicity, education, income
- Geographic: state, region, urban/rural
- Time-varying: pandemic intensity, prior trends

**Merge strategy:**
- What columns are common across datasets? (state name, FIPS code, date)
- What is the unit of analysis after merging?
- Do any datasets need reshaping (wide to long or vice versa)?

### 5. Flag Data Quality Issues

Note any problems that the analysis code will need to handle:
- Columns with >30% missing values
- Inconsistent state name formats across files (abbreviations vs. full names)
- Date format variations
- Duplicate rows
- Implausible values (negative counts, percentages > 100)
- Very small cell sizes for certain subgroups
- Survey weight columns (important for weighted estimation)

### 6. Output Format

Save the synthesis to `exam_paper/data_summary.md` with this structure:

```markdown
# Data Summary

## Datasets
- [filename]: [rows] x [cols], [description from Data_Description.md]
- ...

## Unit of Observation
[Individual / State / County / Facility]

## Time Structure
[Cross-sectional / Repeated cross-section / Panel / Time series]
[Date range: start to end]
[Frequency: daily / weekly / biweekly / monthly]

## Key Variables
- Treatment/Exposure: [variable name] — [description]
- Primary Outcome: [variable name] — [description]
- Secondary Outcome: [variable name] — [description]
- Covariates: [list]

## Merge Strategy
[How to join the datasets, on what keys]

## Data Quality Notes
[Any issues to handle in analysis code]

## External Data
[Any data that was downloaded, where it is stored]
```
