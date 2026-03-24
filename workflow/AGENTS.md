# JAMA Network Open Paper Generation — Master Orchestrator

When the user says **"Write a paper using the data in the folder"** (or any variation), follow this pipeline exactly. Each stage references a rule file in `workflow/rules/` for detailed instructions.

---

## Stage 1: Data Discovery (~3 min)

1. **Locate the data folder.** Look for a folder containing CSV/XLSX/MD files. Check these paths in order:
   - Any path the user explicitly provides
   - `exam_paper/data/`
   - `exam_folder_sample/data/`
   - `sample/data/`
   - Any subfolder named `data/` in the project root

2. **Read `Data_Description.md`** in that folder first. It describes every dataset, its columns, and how to obtain any external data.

3. **Run the data profiler.** Execute:
   ```
   python workflow/scripts/data_profiler.py <data_folder_path>
   ```
   Save the output to `exam_paper/data_summary.md`.

4. **Download external data** if `Data_Description.md` includes download instructions (e.g., shell scripts for Census data). Run those commands, then re-run the profiler on the downloaded files.

5. **Read the profiler output** and synthesize a mental model of the full dataset: what units are observed, what time periods are covered, what potential treatment/exposure variables exist, what outcomes are available, and how datasets can be linked.

Follow `workflow/rules/01-data-exploration.md` for detailed guidance on data understanding.

---

## Stage 2: Research Question Formulation (~2 min)

1. **Read** `workflow/rules/02-research-question.md`.

2. Based on the data summary from Stage 1, identify:
   - **Exposure/treatment**: A policy, intervention, or exposure variable
   - **Outcome**: A health or behavioral outcome
   - **Population**: Who is being studied
   - **Study design**: Cross-sectional, repeated cross-sectional, panel, etc.

3. Formulate a formal research question in JAMA style:
   > "To [examine/determine/compare] [the association between / the effect of] [exposure] [and/on] [outcome] [among/in] [population]"

4. Identify at least 2 subgroup/stratification analyses (e.g., by age, by policy stringency, by region, by demographic group).

5. **If a `Question.md` file exists** in the data folder, use that as the research question instead of generating one.

6. Save the research question, hypotheses, and analysis plan to `exam_paper/research_question.md`.

---

## Stage 3: Write and Run Analysis Code (~10 min)

1. **Read** `workflow/rules/03-analysis-plan.md` for the statistical method decision tree.

2. **Read** `workflow/rules/04-visualization-style.md` for figure styling specifications.

3. **Create the output directory**:
   ```
   mkdir -p exam_paper/code exam_paper/output/figures exam_paper/tex
   ```

4. **Write a single comprehensive Python script** at `exam_paper/code/analysis.py`. The script must:

   - **Section 1 — Data Loading**: Load and merge all datasets. Handle encoding issues, date parsing, and column name standardization.
   - **Section 2 — Data Cleaning**: Construct analysis variables (binary outcomes, treatment indicators, time periods, demographic categories). Handle missing values. Apply sample restrictions matching the research question.
   - **Section 3 — Descriptive Statistics (Table 1)**: Compute counts, weighted percentages (if survey weights exist), means, and SDs by treatment/control group. Export to `exam_paper/output/table1.csv`.
   - **Section 4 — Main Regression**: Run the primary statistical model chosen via the decision tree. Export coefficients, CIs, P values to `exam_paper/output/main_results.csv`.
   - **Section 5 — Subgroup Analyses**: Run the same model on at least 2 subsamples. Export to `exam_paper/output/subgroup_results.csv`.
   - **Section 6 — Robustness Checks**: Run at least one alternative specification. Export to `exam_paper/output/robustness_results.csv`.
   - **Section 7 — Figures**: Generate all figures using the JAMA style spec. Save to `exam_paper/output/figures/`.

   Apply the matplotlib styling from `workflow/rules/04-visualization-style.md` at the top of the script.

5. **Run the script**:
   ```
   cd exam_paper && python code/analysis.py
   ```

6. **Verify outputs exist**: Check that `table1.csv`, `main_results.csv`, and at least one figure PDF were created. If the script fails:
   - Read the error traceback
   - Fix the issue in `analysis.py`
   - Re-run (up to 2 retries)
   - If still failing, simplify: drop the subgroup or robustness analysis, use a simpler model (e.g., OLS instead of DID), remove problematic datasets

---

## Stage 4: Write the Paper and References (~10 min)

1. **Read** `workflow/rules/05-paper-writing.md` for section-by-section instructions.

2. **Read** `workflow/rules/06-references.md` for citation guidelines.

3. **Copy the template**:
   ```
   cp workflow/templates/template.tex exam_paper/tex/paper.tex
   ```

4. **Read the analysis outputs**: Load `table1.csv`, `main_results.csv`, `subgroup_results.csv`, and `robustness_results.csv` to get exact numbers for the paper.

5. **Edit `exam_paper/tex/paper.tex`** section by section, replacing all placeholder text with actual content:
   - Update `\jamashorttitle` and title
   - Fill in the author line with team members and AI models used
   - Write all 7 abstract sections with real numbers from the analysis
   - Fill in Key Points (Question, Findings, Meaning)
   - Write Introduction (3-5 paragraphs, ~500-700 words)
   - Write Methods: Data, Outcome Measures, Statistical Analysis
   - Write Results with inline numbers, referencing Table and Figures
   - Replace the placeholder Table 1 with actual data from `table1.csv`
   - Insert `\includegraphics` for each figure in `exam_paper/output/figures/`
   - Write Discussion with Limitations subsection
   - Write Conclusions
   - Write Supplement: eAppendix with model equations, eTables, eFigures

6. **Generate `exam_paper/tex/references.bib`** simultaneously:
   - Use web search to find real papers relevant to the topic
   - Generate 25-35 BibTeX entries
   - Insert `\cite{key}` markers throughout the paper text
   - Ensure every `\cite` key exists in the `.bib` file

7. **Copy figures** to the tex directory so LaTeX can find them:
   ```
   cp exam_paper/output/figures/*.pdf exam_paper/tex/
   ```

---

## Stage 5: Quality Review and Compile (~5 min)

1. **Read** `workflow/rules/07-quality-checklist.md`.

2. **MANDATORY SELF-CHECK before compiling.** Open `exam_paper/tex/paper.tex` and verify ALL of these. If any fail, FIX BEFORE COMPILING:

   **[ ] Table 1 Completeness:** Does Table 1 have rows for Sex, Age, Race, Education, Income, Marital Status, AND vaccination rates split by pre/post-mandate period? If any are missing, add them now using data from `table1.csv`.

   **[ ] State Fixed Effects:** Does the Methods section say "state fixed effects" (not "mandate state indicator")? The word "state fixed effects" must appear in the Statistical Analysis subsection.

   **[ ] DID Coefficient in Abstract:** Does the Abstract's Findings section include the exact DID estimate, 95% CI, and P value? Numbers must appear, not just "no significant association."

   **[ ] DID Coefficient in Conclusions:** Does the Conclusions section restate the exact DID estimate and 95% CI? It must.

   **[ ] Discussion Length:** Does the Discussion have at least 5 paragraphs and ~800+ words? Count them. If fewer than 5 paragraphs, expand using the template from `05-paper-writing.md`.

   **[ ] Mechanisms Discussed:** Does the Discussion mention at least 3 of: timing, secular trends, ceiling effects, composition effects, survey measurement? If not, add them.

   **[ ] Policy Implications:** Is there a dedicated paragraph about policy implications? Not just one sentence — a full 4-5 sentence paragraph.

   **[ ] Figures Referenced:** Are Figure 1, 2, and 3 all referenced in the Results text and do the `.pdf` files exist in the tex directory?

   **[ ] At least 20 citations:** Count the unique `\cite{...}` keys. Must be ≥20.

3. **Fix any issues found** by editing `exam_paper/tex/paper.tex` and/or `exam_paper/tex/references.bib`.

4. **Ensure `vancouver.bst` is installed** (required for JAMA bibliography style):
   ```
   tlmgr install vancouver 2>/dev/null || true
   ```

5. **Compile the PDF**:
   ```
   cd exam_paper/tex && bash ../../workflow/scripts/compile_latex.sh paper.tex
   ```

6. **Check compilation output** for errors. If compilation fails:
   - Read the `.log` file for the first error
   - Fix the LaTeX issue (usually missing `}`, bad `\cite` key, or missing figure)
   - If a `.bst` or `.sty` file is missing, install it: `tlmgr install <package_name>`
   - Re-compile (up to 3 retries)
   - If a figure is causing issues, remove it from the paper rather than blocking compilation

7. **Copy the final PDF**:
   ```
   cp exam_paper/tex/paper.pdf exam_paper/output/paper.pdf
   ```

8. **Verify**: Confirm `exam_paper/output/paper.pdf` exists and report completion.

---

## Critical Quality Requirements

These requirements were identified from test runs and MUST be followed:

### Table 1 Must Include ALL of These
- Sex, Age groups, Race, Ethnicity, Marital status (if available), Education, Income brackets
- **Vaccination outcomes SPLIT by pre-mandate and post-mandate periods** (not just overall)
- This is what the sample paper shows and graders will notice if missing

### Regression Models Must Include State Fixed Effects
- Use individual state dummies, NOT just a binary mandate/non-mandate indicator
- This controls for all time-invariant state-level confounders
- It is the standard approach in the DID literature

### Event Study Must Be Honest About Pre-Trends
- If pre-trend coefficients are noisy (large magnitude swings even if individually insignificant), say so
- Do not claim "clean pre-trends" if the coefficients bounce around by 3+ percentage points

### Handle Missing Coded Values
- Survey variables often use -88 (missing) and -99 (not selected) — set these to NaN
- For DOSES variable: missing among vaccinated people should be handled explicitly (restrict sample or impute)

### Discussion Must Address Null/Negative Results
- If the DID estimate is null or negative, the Discussion MUST include:
  1. Announcement vs enforcement timing distinction
  2. Secular trends (Delta surge driving vaccination in all states)
  3. Ceiling effects (mandate states had higher baseline rates)
  4. Composition/selection effects (workforce attrition)
  5. A dedicated policy implications paragraph

### Install `vancouver.bst` Before First Compile
- Run `tlmgr install vancouver` before the first `pdflatex` call

---

## Error Handling and Fallback Strategies

At every stage, if something fails:

1. **Read the error message carefully.** Most failures are fixable (typos, missing columns, wrong file paths).

2. **Retry up to 2 times** with fixes applied.

3. **Escalate by simplifying:**
   - Stage 3 fails → Drop subgroup analysis. Use OLS instead of DID. Use fewer covariates.
   - Stage 4 fails → Write shorter sections. Use fewer references. Skip the supplement.
   - Stage 5 fails → Remove problematic figures/tables. Fix LaTeX syntax errors.

4. **Never block on a single issue for more than 5 minutes.** Move forward with a simpler version and come back to improve later if time permits.

5. **The goal is always a compilable paper.pdf.** A simpler but complete paper is better than a sophisticated but broken one.

---

## Final Output Checklist

When the pipeline completes, these files should exist:

```
exam_paper/
  research_question.md           # Research question and analysis plan
  data_summary.md                # Data profiler output
  code/
    analysis.py                  # Full analysis script
  output/
    paper.pdf                    # THE DELIVERABLE
    table1.csv                   # Descriptive statistics
    main_results.csv             # Primary regression results
    subgroup_results.csv         # Subgroup analysis results
    robustness_results.csv       # Robustness check results
    figures/
      figure1.pdf                # Main results figure
      figure2.pdf                # Subgroup/stratified figure
      ...                        # Additional figures
  tex/
    paper.tex                    # Final LaTeX source
    references.bib               # Bibliography
    figure1.pdf                  # Figures (copied for LaTeX)
    ...
```
