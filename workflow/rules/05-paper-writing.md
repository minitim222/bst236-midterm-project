# Rule 05: Paper Writing Guide

## Purpose

Write a complete JAMA Network Open research paper by filling in the LaTeX template section by section. Every section has specific requirements for content, length, style, and formatting.

---

## General Writing Conventions

### Voice and Tense
- **Methods and Results**: Third person, past tense ("We used...", "The sample included...", "Results indicated...")
- **Introduction**: Mix of present tense (for established facts) and past tense (for prior studies)
- **Discussion**: Mix of past tense (for findings) and present tense (for implications)
- **Conclusions**: Past tense for findings, present tense for implications

### Causal Language
- NEVER say "caused," "led to," or "resulted in" unless discussing an RCT
- USE: "associated with," "linked to," "correlated with"
- For policy studies: "mandate-associated increase" not "mandate-caused increase"

### Numbers
- Spell out one through nine; use numerals for 10 and above
- Exception: always use numerals with units (e.g., "3 percentage points," "2 weeks")
- Exception: start sentences with spelled-out numbers ("Twenty-five states...")
- Percentages: one decimal place (72.1%), use % symbol after the number
- Use "percentage point" (pp) for absolute differences between proportions
- Use "percent" or "%" for relative differences

### P Values
- Format: italic *P* with capital P, no leading zero: *P* = .03, *P* < .001
- LaTeX: `\textit{P}~= .03` or `\textit{P}~< .001`
- Do not write *P* < .05 unless the value is truly between .01 and .05; give exact values

### Confidence Intervals
- Format: (95% CI, lower-upper)
- Example: "3.46-pp (95% CI, 0.29-6.63 pp; *P* = .03) increase"
- Use en-dash between bounds in the CI range

### Abbreviations
- Define on first use: "health care workers (HCWs)"
- After first use, use the abbreviation consistently
- Do NOT abbreviate in the title
- Standard abbreviations that need no definition: US, CI, SD, OR

### Thousands Separator
- In LaTeX body text, use thin spaces: `31\,142` renders as 31 142
- In plain text: use commas: 31,142

---

## Template Modifications

When editing `exam_paper/tex/paper.tex`, update these template fields:

### Running Title
```latex
\newcommand{\jamashorttitle}{Short Version of Your Title}
```

### Title Block
```latex
{\sffamily\bfseries\fontsize{18}{21}\selectfont\color{jamadarkgray}
Your Full Paper Title Here\par}
```

### Author Line
```latex
{\fontsize{9.5}{11.5}\selectfont\color{jamadarkgray}
Team Member One; Team Member Two; Claude 4 Opus (Anthropic); Cursor AI\par}
```

---

## Section-by-Section Instructions

### Abstract

The abstract has exactly 7 labeled sections. Each must be filled in.

**IMPORTANCE** (1-2 sentences)
- Why this topic matters to public health
- What gap in knowledge exists
- Pattern: "[Context about the problem]. Prior research [was limited to X / focused on Y], and [more evidence is needed / the association with Z remains unclear]."
- Example: "Seventeen states introduced COVID-19 vaccine mandates for health care workers (HCWs) in mid-2021. Prior research on the effect of these mandates was centered on the nursing home sector, and more evidence is needed for their effect on the entire HCW population."

**OBJECTIVE** (1 sentence)
- Begin with an infinitive phrase
- Pattern: "To [examine/determine/compare] [the association between / the effect of] [exposure] [and/on] [outcome] [among/in] [population]."
- Example: "To examine the association between state COVID-19 vaccine mandates for HCWs and vaccine uptake in this population."

**DESIGN, SETTING, AND PARTICIPANTS** (2-3 sentences)
- Sentence 1: Study design and data source with dates
- Sentence 2: Population definition and inclusion criteria
- Sentence 3: "Analyses were conducted between [month year] and [month year]."
- Example: "This repeated cross-sectional study included biweekly, individual-level data for adults aged 25 to 64 years who were working or volunteering in health care settings obtained from the Household Pulse Survey between May 26 and October 11, 2021."

**EXPOSURE** (1 sentence)
- Name the exposure/treatment variable precisely
- Example: "Announcement of a state COVID-19 vaccine mandate for HCWs."

**MAIN OUTCOMES AND MEASURES** (2-3 sentences)
- Define outcome variables
- State the statistical method
- Mention stratification
- Example: "An indicator for whether a sampled HCW ever received a COVID-19 vaccine and an indicator for whether an HCW completed or intended to complete the primary COVID-19 vaccination series. Event study analyses using staggered difference-in-differences methods compared vaccine uptake among HCWs in mandate and nonmandate states before and after each mandate announcement."

**RESULTS** (3-5 sentences)
- Sentence 1: Sample demographics — "The study sample included N [units] (mean [SD] age, X [Y] years; Z% female)."
- Sentences 2-3: Main quantitative findings with coefficient, 95% CI, P value
- Sentence 4-5: Key subgroup findings
- Use EXACT numbers from the analysis output files
- Example: "Results indicated a mandate-associated 3.46–percentage point (pp) (95% CI, 0.29-6.63 pp; P = .03) increase in the proportion of HCWs ever vaccinated against COVID-19."

**CONCLUSIONS AND RELEVANCE** (2-3 sentences)
- Start with: "This [study design] found that [main finding]."
- End with policy/clinical implication
- Example: "This repeated cross-sectional study found that state COVID-19 vaccine mandates for HCWs were associated with increased vaccine uptake among HCWs, especially among younger HCWs and those in states with no test-out option."

### Key Points Box

**Question** (1-2 sentences)
- Frame as a yes/no question
- Pattern: "Were [exposure] associated with [outcome] among [population] in [time/setting]?"
- Example: "Were state COVID-19 vaccine mandates for US health care workers (HCWs) associated with increased vaccine uptake in this population in 2021?"

**Findings** (2-3 sentences)
- Start with: "In this [study type] of N [units]..."
- Include 1-2 specific numbers
- Example: "In this cross-sectional study of 31 142 HCWs sampled across the US, state COVID-19 vaccine mandates for HCWs were associated with increases in the proportions of ever vaccinated HCWs..."

**Meaning** (1-2 sentences)
- Pattern: "These findings suggest that [implication]."
- Example: "These findings suggest that state COVID-19 vaccine mandates were associated with increased vaccine uptake among HCWs in 2021."

### Introduction (3-5 paragraphs, 500-700 words)

**Paragraph 1 — Broad Context** (~100-150 words)
- Historical or epidemiological context for the topic
- Why this is a significant public health issue
- Cite 2-3 foundational references
- Example opening: "Since their debut in 1796, vaccines have played a pivotal role in controlling lethal epidemics..."

**Paragraph 2 — Specific Background** (~150-200 words)
- What policies/interventions exist in this area
- Timeline of key events
- Scope of the problem (how many states, how many people affected)
- Cite 4-6 references
- Include specific numbers and dates

**Paragraph 3 — Knowledge Gap** (~100-150 words)
- What existing studies have found
- What has NOT been studied
- Why more evidence is needed
- Pattern: "To our knowledge, however, [gap statement]. As far as we are aware, [what hasn't been done]."
- Cite 3-5 references (prior studies that address part of the question)

**Paragraph 4 (optional) — Debate or Additional Context** (~100 words)
- Ethical debates, political context, public opinion data
- Cite 2-3 references

**Final Paragraph — Study Objective** (~50-80 words)
- Pattern: "In this [study type], we [added to the current literature by / sought to examine] [objective]. We further explored whether [subgroup analysis 1] and [subgroup analysis 2]."
- This paragraph MUST mirror the OBJECTIVE in the abstract
- **MUST mention planned subgroup analyses explicitly** — e.g., "We further explored whether the association differed by test-out provision and worker age."
- Example: "In this repeated cross-sectional study, we added to the current literature by using nationally representative data from the Household Pulse Survey (HPS) to explore the association between state COVID-19 vaccine mandates for HCWs and changes in vaccine uptake in this population. We further examined whether the association differed by mandate stringency and worker age."

### Methods

**Data subsection** (300-400 words)
- Full name of every data source on first use
- Describe which units are included/excluded and why
- State exact date ranges
- IRB statement: "The [institution] institutional review board exempted the study from approval and informed consent because only publicly available, deidentified data were used."
- Reporting guideline: "We followed the Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) reporting guideline."
- If applicable: list all states in treatment and control groups
- Describe the study window and why those dates were chosen

**Outcome Measures subsection** (150-200 words)
- Define each outcome variable precisely
- State how each was measured (survey question text, administrative variable)
- List ALL covariates: "The analysis also controlled for self-reported individual characteristics, including sex, age, race (...), ethnicity (...), marital status, educational attainment, and income levels, and [any time-varying controls]."
- Explain why race/ethnicity were included: "Race and ethnicity were included as covariates to account for heterogeneous [outcome] behaviors and access to health care resources based on race and ethnicity."

**Statistical Analysis subsection** (250-350 words)
- Name the method with its academic citation: "We used [method] proposed by [Author] (year)."
- Explain why this method fits: "this method accommodates [staggered adoption / heterogeneous treatment effects / etc.]."
- Describe the model intuitively (save equations for supplement)
- State: "Individual-level survey weights were incorporated" (if applicable)
- State: "Standard errors were clustered at the state level to account for serial correlation in [outcome] within a state over time."
- State: "Statistical tests were 2-sided, with P < .05 considered statistically significant."
- State software: "Analyses were conducted using Python (version 3.x) with the statsmodels (version 0.14) and pandas (version 2.x) packages."
- State dates: "Analyses were conducted between [month year] and [month year]."
- Reference the supplement: "An in-depth description is available in eAppendix 1 in Supplement 1."

### Results (500-700 words)

**Paragraph 1 — Sample Description** (~150 words)
- Start with: "The sample included N [units] (mean [SD] age, X [Y] years; N [Z%] female; N [Z%] male)."
- Report key demographic breakdowns from Table 1
- Compare treatment vs. control groups: "Compared with [control group], [treatment group] were more likely to be [characteristic] (N [%] vs N [%])."
- Reference Table 1: "...are presented in Table 1" or "(Table)."

**Paragraph 2+ — Main Findings** (~200-300 words)
- Present event study / regression results
- Pattern: "[Figure X] displays [event study / regression] estimates of [what]. [The exposure] was associated with a [coefficient]-[unit] (95% CI, [lower]-[upper]; P = [value]) [increase/decrease] in [outcome] [time specification]."
- Always contextualize: "representing a X% increase relative to a baseline proportion of Y%."
- Reference figure: "(Figure 1)" or "Figure 1 displays..."
- If event study: describe both pre-treatment (should show no effect) and post-treatment periods

**Paragraph 3+ — Subgroup Findings** (~150-200 words)
- Present each subgroup separately
- Pattern: "In the analyses stratified by [variable], [finding in subgroup 1] (Figure 2A). Regarding [subgroup 2], results revealed [finding] (Figure 2B)."
- Highlight which subgroups show significant effects and which do not

### Discussion (600-800 words)

**Paragraph 1 — Context and Main Contribution** (~150 words)
- What this study adds to the literature
- Frame the policy context

**Paragraph 2 — Interpretation of Main Findings** (~150-200 words)
- Explain WHY the effects were observed
- Discuss mechanisms
- Compare effect magnitude to prior studies

**Paragraph 3 — Comparison with Prior Literature** (~150-200 words)
- Cite 4-6 prior studies
- Note similarities and differences
- Pattern: "Our results [are consistent with / differ from] prior research on [topic]."

**Paragraph 4 — Composition/Selection Effects** (~100-150 words)
- If findings are null or negative, ALWAYS discuss composition effects:
  - Workers may leave (quit, retire, relocate) in response to mandates, changing who is in the sample
  - Survey non-response may differ between mandate and nonmandate states
  - HCWs in mandate states may be more likely to under-report vaccination due to backlash
- If findings are positive, discuss whether the effect reflects genuine behavior change or selection (e.g., only compliant workers remain)
- This paragraph is critical for credibility when results are surprising

**Paragraph 5 — Policy Implications** (~100-150 words)
- What do the findings mean for policymakers?
- Are there conditions under which the intervention is more effective?
- If null/negative results: discuss whether mandates need enforcement mechanisms, longer time horizons, or complementary interventions (e.g., education, incentives)
- If positive results: discuss generalizability and cost-effectiveness
- Discuss the federal CMS mandate and whether state mandates added incremental value

**Limitations subsection** (~200 words)
- List 3-5 specific limitations with mitigations
- Common limitations:
  1. Cross-sectional design / repeated cross-sections (different individuals each wave)
  2. Self-reported outcome data (subject to bias)
  3. Potential contamination from concurrent policies
  4. Limited external validity
  5. Unmeasured confounders
- For each: state the limitation, then how you partially addressed it
- Pattern: "First, [limitation]. To address this concern, we [mitigation]."

### Conclusions (1 paragraph, ~100 words)

- Restate main findings **with the actual coefficient and CI**: "...were associated with a −1.45 percentage point change (95% CI, −2.78 to −0.11) in..."
- State the policy takeaway
- Do NOT introduce new findings or speculation
- Pattern: "This [study type] found that [exposure] was associated with [effect sizes] in [outcome]. [Key subgroup finding]. The study demonstrated [broader implication]."
- **IMPORTANT:** Do not just say "were not associated" without numbers. Always include the specific estimate so readers can judge the magnitude.

### Supplement

**eAppendix 1 — Statistical Model Details**
- Write out the formal equation for the main model
- For DID: $Y_{ist} = \alpha + \sum_e \sum_l \beta_{el}(\mathbf{1}\{E_s = e\} \cdot \mathbf{1}\{t - E_s = l\}) + \gamma X_{ist} + \delta Z_{s,t-1} + \mu_s + \tau_t + \varepsilon_{ist}$
- Define every term
- Explain the aggregation formula for final treatment effects

**eTable 1** — Policy summary table or additional descriptive statistics
- For policy studies: list each state, policy scope, test-out option, announcement date

**eTable 2-3** — Full regression results with alternative estimators
- Show results from at least 2 estimators side by side
- Include both adjusted and unadjusted estimates

**eFigure 1-2** — Alternative specification figures
- Unadjusted event study
- Robustness check results

---

## Handling Null or Negative Results

If the DID or regression estimates are null (not statistically significant) or negative (opposite of the expected direction), do NOT panic. Null and negative results are publishable and scientifically valuable. Follow these guidelines:

### In the Abstract
- Report the actual coefficients with CIs and P values — do not hide them
- Frame using: "were not associated with differential increases" rather than "had no effect"
- Avoid causal language even more carefully than with positive results

### In the Results
- Present results identically to how you would with positive findings
- Do not editorialize — save interpretation for Discussion

### In the Discussion
Write at least 5-6 substantial paragraphs (~800-1000 words total) using this template:

- **Paragraph 1 — Principal findings:** "In this cross-sectional study using nationally representative survey data from [N] health care workers across [N] US states, state-level COVID-19 vaccine mandates announced during [date range] were not associated with statistically significant differential increases in self-reported vaccination uptake (DID estimate: [X] pp; 95% CI, [Y] to [Z]). These findings persisted across subgroup analyses by [subgroup 1] and [subgroup 2] and were robust to [robustness check]."

- **Paragraph 2 — Reconcile with prior literature:** Explain why your results differ from studies reporting positive effects. Cite at least 3 prior studies and explain the design differences:
  - Study design differences (pre-post vs DID — pre-post conflates secular trends with treatment)
  - Different time period (announcement vs enforcement — our study captures announcements only, before penalties applied)
  - Different population (all HCWs vs nursing home staff only — CMS mandate studies show stronger effects in captive populations)
  - Ceiling effects (high baseline rates leave little room for improvement — mandate states had [X]% vaccination at baseline)

- **Paragraph 3 — Mechanisms for null results:** ALWAYS discuss at least 4 of these:
  1. **Timing**: Our study period captures announcement, not enforcement. Behavioral responses to mandates may require credible enforcement threats.
  2. **Secular trends**: The Delta variant surge (June-September 2021) independently drove vaccination across all states, potentially overwhelming any mandate-specific effect.
  3. **Ceiling effects**: If mandate states already had high baseline vaccination rates, the marginal effect of mandates is bounded.
  4. **Composition/selection effects**: Workforce attrition among unvaccinated workers. If vaccine-hesitant HCWs quit or were fired, this could paradoxically raise measured vaccination rates even absent mandates (survivorship bias). Conversely, if these workers disproportionately left mandate states, the composition shift could mask true mandate effects.
  5. **Survey measurement**: HPS samples US households, not current employees. Workers who left healthcare employment are still surveyed, potentially diluting measured HCW vaccination rates.

- **Paragraph 4 — Policy implications:** This is REQUIRED and must be specific:
  "These findings have several policy implications. First, mandate announcements alone — absent enforcement mechanisms and compliance deadlines — may be insufficient to produce measurable behavioral change. Second, the strong secular trend toward vaccination suggests that public health campaigns, employer encouragement, and peer effects may have been primary drivers of uptake during this period. Third, future mandate policies should consider pairing announcements with clear enforcement timelines, accessible vaccination sites, and educational programs tailored to vaccine-hesitant subgroups. Fourth, policymakers should anticipate potential workforce disruptions and develop strategies to retain essential healthcare workers during mandate implementation."

- **Paragraph 5 — Limitations:** List at least 5 specific limitations (see Limitations template below)

- **Paragraph 6 — Strengths:** List at least 3 specific strengths of the study design

### In Conclusions
Use this template — you MUST include the actual DID coefficient and CI:

"In this cross-sectional study of [N] self-identified US health care workers surveyed from [date] to [date], state-level COVID-19 vaccine mandate announcements were not associated with statistically significant differential changes in vaccination uptake (adjusted DID estimate: [X] percentage points; 95% CI, [Y] to [Z]). These findings suggest that mandate announcements alone, without enforcement and compliance deadlines, were insufficient to produce measurable incremental gains beyond concurrent national vaccination trends. Future research should examine the effects of mandate enforcement periods with longer follow-up and investigate complementary strategies to increase vaccine uptake among health care workers."

Key rules for Conclusions:
- MUST restate the exact DID coefficient and 95% CI
- MUST mention the sample size and study period
- MUST suggest at least one future direction
- Keep to 1 paragraph, 4-6 sentences max

---

## Handling Survey Weight Artifacts

When HPS person weights are calibrated to the general population (not the HCW population), demographic distributions may look unusual. For example:
- Female percentage may be pulled toward 50% even though HCWs are predominantly female
- This is because the weights adjust for general population representativeness, not occupation-specific

**How to handle in the paper:**
- Report the weighted percentages as-is (they are correct for population inference)
- Add a limitation noting that survey weights were designed for the general population
- Compare unweighted and weighted demographics in a supplement eTable if the discrepancy is large

---



- Escape special characters: `%`, `$`, `&`, `#`, `_` must be `\%`, `\$`, `\&`, `\#`, `\_`
- Use `\,` for thousands separator: `31\,142`
- Use `\textit{P}` for P values
- Use `\textsuperscript{1,2}` for citation numbers (natbib handles this with `\cite{}`)
- Use `~` for non-breaking spaces: `\textit{P}~= .03`, `Figure~1`
- Use `--` for en-dash in ranges: `95\% CI, 0.29--6.63`
- Use `\ldots` instead of `...`
- Use `\enspace` for medium spaces in formatted elements
- Use `\par` to end paragraphs inside minipage environments
