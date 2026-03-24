# Rule 02: Research Question Formulation

## Purpose

Formulate a research question that is novel, testable, and publishable in JAMA Network Open, based on the data summary from Stage 1.

---

## Step 1: Check for an Existing Question

If a `Question.md` file exists in the data folder, **use that question** as the primary research question. You still need to formalize it and plan subgroup analyses, but the topic is predetermined.

---

## Step 2: Pattern Recognition

If no `Question.md` exists, identify which study pattern the data best supports:

### Pattern A: Policy Evaluation (Causal Inference)

**Data signature:** A policy/mandate/intervention was enacted at different times in different geographic units (states, counties). There is a date column indicating when the policy was announced or implemented.

**Question template:** "To examine the association between [state/county policy X] and [health outcome Y] among [population Z]."

**Statistical approach:** Difference-in-differences, event study, staggered DID.

**Example:** "To examine the association between state COVID-19 vaccine mandates for health care workers and vaccine uptake in this population."

### Pattern B: Association / Risk Factor Study

**Data signature:** Cross-sectional or pooled data with an exposure variable (behavioral, environmental, demographic) and a health outcome. No policy timing variation.

**Question template:** "To examine the association between [exposure X] and [outcome Y] among [population Z], adjusting for [confounders]."

**Statistical approach:** Logistic or linear regression with covariates.

**Example:** "To examine the association between household income and COVID-19 vaccination rates among adults in the US."

### Pattern C: Trend / Time Series Analysis

**Data signature:** Aggregate-level data (state or national) measured repeatedly over time. A key event or intervention occurred at a known date.

**Question template:** "To assess changes in [outcome Y] following [event X] across [units Z]."

**Statistical approach:** Interrupted time series, segmented regression, pre-post comparison.

**Example:** "To assess changes in COVID-19 mortality rates following the introduction of federal vaccine mandates."

### Pattern D: Disparity / Equity Study

**Data signature:** Individual or group-level data with demographic stratifiers (race, income, education, geography) and a health outcome. Focus is on differences across groups.

**Question template:** "To examine [racial/socioeconomic/geographic] disparities in [outcome Y] among [population Z]."

**Statistical approach:** Stratified analysis, interaction terms, decomposition methods.

**Example:** "To examine racial and ethnic disparities in COVID-19 vaccination rates among health care workers."

---

## Step 3: Formalize the Research Question

Write the research question using this exact JAMA structure:

> **Objective:** To [examine/determine/compare/assess] [the association between / the effect of / changes in] [exposure/intervention] [and/on] [outcome] [among/in] [population].

Key principles:
- Use "association" not "effect" or "impact" (unless a randomized trial)
- Be specific about the population and setting
- The question must be answerable with the available data
- The question should imply the study design

---

## Step 4: Define Core Elements

Document each of these explicitly:

**Exposure/Treatment:**
- Variable name in the data
- How it is measured (binary, categorical, continuous, date-based)
- For policy studies: announcement date vs. implementation date

**Primary Outcome:**
- Variable name in the data
- How it is measured
- Is it binary (→ logistic) or continuous (→ OLS)?

**Secondary Outcome(s):**
- At least one alternative outcome for robustness

**Population:**
- Who is included (age range, occupation, geography)
- Exclusion criteria and why

**Study Design:**
- Cross-sectional, repeated cross-sectional, cohort, panel
- Time window

**Covariates:**
- Demographics: sex, age, race, ethnicity, education, income, marital status
- Time-varying: pandemic intensity, prior trends
- Geographic: state/region fixed effects

---

## Step 5: Plan Subgroup Analyses

Identify at least 2 meaningful stratifications. Good candidates:

1. **By policy stringency** (e.g., test-out option vs. no test-out)
2. **By age group** (e.g., younger vs. older workers)
3. **By race/ethnicity** (e.g., racial disparities in treatment effects)
4. **By geography** (e.g., urban vs. rural, or by region)
5. **By income/education** (e.g., socioeconomic gradient)
6. **By time period** (e.g., early vs. late adopters)

Each subgroup analysis should have a substantive justification (not just "because we can").

---

## Step 6: Generate Hypotheses

State the expected direction of the main effect and why:

> **Hypothesis:** We hypothesize that [exposure] is associated with [increased/decreased] [outcome] because [mechanism]. We further hypothesize that the association is [stronger/weaker] among [subgroup 1] compared with [subgroup 2] because [reason].

---

## Output

Save to `exam_paper/research_question.md`:

```markdown
# Research Question

## Objective
To [full formal statement].

## Study Design
[Cross-sectional / repeated cross-sectional / panel / time series]

## Exposure
[Variable, measurement, source]

## Primary Outcome
[Variable, measurement, source]

## Secondary Outcome
[Variable, measurement, source]

## Population
[Inclusion/exclusion criteria]

## Covariates
[Full list]

## Subgroup Analyses
1. [Stratification 1]: [Justification]
2. [Stratification 2]: [Justification]

## Hypotheses
[Directional predictions with reasoning]

## Statistical Approach
[Method name chosen from the decision tree in 03-analysis-plan.md]
```
