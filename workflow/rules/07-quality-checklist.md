# Rule 07: Quality Review Checklist

## Purpose

Before compiling the final PDF, review the paper against every item below. Fix any failures before running `pdflatex`. This checklist is the last line of defense against embarrassing errors.

---

## Scientific Rigor

- [ ] Every numerical claim in the Abstract appears somewhere in the Results section
- [ ] Every number in the Abstract EXACTLY matches the corresponding number in Results (same coefficient, same CI, same P value)
- [ ] Sample size N is consistent across Abstract, Results text, and Table 1
- [ ] All confidence intervals are formatted: (95% CI, [lower]--[upper])
- [ ] All P values use italic capital P with no leading zero: `\textit{P}~= .03` or `\textit{P}~< .001`
- [ ] Effect sizes include proper units: "percentage points" for absolute, "percent" or "%" for relative
- [ ] Baseline outcome levels are reported when presenting effect magnitudes ("from a baseline of 87.98%")
- [ ] Causal language is avoided: "associated with" not "caused" or "led to"
- [ ] Treatment and control group sizes add up to the total sample size
- [ ] Pre-treatment event study coefficients are near zero and not statistically significant (if using DID/event study)
- [ ] **If pre-trend coefficients are noisy** (individually insignificant but with large magnitudes), this is acknowledged honestly in the text rather than glossed over as "clean pre-trends"
- [ ] Direction of effects is internally consistent (if mandates "increased" uptake in Results, Discussion should not say "decreased")
- [ ] Subgroup results are plausible relative to the full sample results
- [ ] **State fixed effects are included** in the DID model (not just a binary treatment indicator)
- [ ] **Conclusions section includes specific numbers** (coefficient and CI), not just qualitative statements

## Abstract Completeness

- [ ] IMPORTANCE section is present (1-2 sentences)
- [ ] OBJECTIVE section begins with infinitive phrase ("To examine...", "To determine...")
- [ ] DESIGN, SETTING, AND PARTICIPANTS names the study design, data source, population, and dates
- [ ] EXPOSURE section names the treatment/intervention
- [ ] MAIN OUTCOMES AND MEASURES defines outcomes and statistical method
- [ ] RESULTS begins with "The study sample included N... (mean [SD] age, X [Y] years; Z% female)"
- [ ] RESULTS includes at least 2 specific quantitative findings with CIs and P values
- [ ] CONCLUSIONS AND RELEVANCE starts with "This [study type] found that..."

## Key Points Box

- [ ] Question is framed as a yes/no or what/how question
- [ ] Findings include specific numbers and the study type
- [ ] Meaning states the implication, not just restates findings

## Introduction

- [ ] 3-5 paragraphs, approximately 500-700 words
- [ ] Paragraph 1 provides broad context with 2-3 citations
- [ ] At least one paragraph identifies a knowledge gap
- [ ] Final paragraph states the study objective (mirrors Abstract OBJECTIVE)
- [ ] Final paragraph mentions planned subgroup analyses
- [ ] No results or methods details leak into the Introduction

## Methods

- [ ] **Data** subsection names all data sources with full names
- [ ] IRB statement is included
- [ ] Reporting guideline is mentioned (STROBE, CONSORT, etc.)
- [ ] Study window dates are stated
- [ ] Exclusion criteria are listed with justification
- [ ] **Outcome Measures** defines each outcome variable precisely
- [ ] All covariates are listed
- [ ] Race/ethnicity inclusion is justified
- [ ] **Statistical Analysis** names the method with its citation
- [ ] Method choice is justified ("this method accommodates...")
- [ ] Survey weights usage is stated (if applicable)
- [ ] Standard error clustering level is stated
- [ ] Significance threshold is stated: "2-sided, P < .05"
- [ ] Software and version are stated
- [ ] Analysis date range is stated
- [ ] Supplement is referenced for technical details

## Results

- [ ] First paragraph describes sample demographics from Table 1
- [ ] Table 1 (or "Table") is referenced in text
- [ ] All figures are referenced in text (Figure 1, Figure 2, etc.)
- [ ] Main findings report: coefficient, unit, 95% CI, P value
- [ ] Effect magnitudes are contextualized with baseline values
- [ ] Subgroup findings are presented separately
- [ ] No interpretation or discussion appears in Results (save for Discussion)

## Table Quality

- [ ] Table uses JAMA style: `booktabs` rules only (no vertical lines)
- [ ] `\toprule`, `\midrule`, `\bottomrule` are used (not `\hline`)
- [ ] Numbers >= 1000 have thin-space separators: `31\,142`
- [ ] Format is "Count (Percentage)" for categoricals
- [ ] Percentages have one decimal place
- [ ] Weighted percentages are used (if survey data) and stated in footnote
- [ ] Column headers include group labels and sample sizes: "All (N = 31,142)"
- [ ] Group category headers are in bold
- [ ] Individual categories are indented with `\quad`
- [ ] **Table 1 COMPLETENESS — ALL of the following categories are present:**
  - [ ] Sex (Female, Male)
  - [ ] Age groups (at least 3 categories)
  - [ ] Race (White, Black, Other at minimum)
  - [ ] Ethnicity (Hispanic, Non-Hispanic)
  - [ ] Marital status (if data has a marital status variable)
  - [ ] Education (at least 2 categories)
  - [ ] Income (at least 3 brackets + unknown)
  - [ ] **Outcome variables split by pre/post period** (e.g., Ever vaccinated in pre-mandate, Ever vaccinated in post-mandate)
- [ ] Table has numbered footnotes explaining:
  - Whether percentages are weighted
  - Which states/units are in treatment group
  - Which states/units are in control group
  - Time period definitions (pre-mandate, post-mandate weeks)
  - Any category groupings (e.g., "Other race includes...")
  - Primary series completion definition
- [ ] Table label exists (`\label{tab:...}`) for cross-referencing

## Figure Quality

- [ ] Every figure referenced in text has a corresponding file on disk
- [ ] `\includegraphics` paths point to existing PDF files
- [ ] Figures use JAMA color palette (crimson #AF1E37, not default matplotlib blue)
- [ ] Figures have descriptive captions (not just "Figure 1")
- [ ] Event study plots have:
  - Horizontal line at y = 0
  - Vertical dashed line at event time 0
  - Error bars showing 95% CIs
  - Clear axis labels with units
- [ ] Multi-panel figures label panels A and B
- [ ] No figure has a matplotlib title (the LaTeX caption serves as title)
- [ ] All text in figures is legible (font size >= 9pt)

## Discussion

- [ ] Opens by placing findings in context of prior literature
- [ ] Discusses mechanisms for observed effects
- [ ] **If null/negative results**: discusses announcement vs enforcement timing, secular trends (Delta surge), ceiling effects, and composition/selection effects (workforce attrition)
- [ ] Compares findings with prior studies (4-6 citations)
- [ ] **Has a dedicated policy implications paragraph** (not just one sentence)
- [ ] Discusses policy implications
- [ ] **Limitations** subsection lists 3-5 specific limitations with mitigations
- [ ] Does not re-state results verbatim (interprets them instead)
- [ ] **If survey weights produce unusual demographics** (e.g., low female % in healthcare), this is acknowledged in limitations

## Conclusions

- [ ] Single paragraph, approximately 100 words
- [ ] Restates main findings with specific numbers
- [ ] States policy/practical takeaway
- [ ] Does NOT introduce new findings or new information

## Supplement

- [ ] eAppendix contains the formal statistical model equation with every term defined
- [ ] At least one eTable with robustness check results
- [ ] **eTable with policy summary**: state, scope, test-out option, announcement date
- [ ] At least one eFigure with alternative specification results (e.g., unadjusted event study)
- [ ] All eTables and eFigures have titles
- [ ] Data sharing statement with URLs to public data sources

## References

- [ ] Every `\cite{key}` in the paper has a matching entry in `references.bib`
- [ ] 25-35 references total
- [ ] No duplicate BibTeX keys
- [ ] All entries have at least: title, author, year
- [ ] Journal articles have: journal, volume, year
- [ ] Acronyms in titles are protected: `{COVID-19}`, `{US}`, `{HIV}`
- [ ] `\bibliographystyle{vancouver}` is used
- [ ] `\bibliography{references}` points to the correct file

## LaTeX Compilation

- [ ] Paper compiles without fatal errors
- [ ] No "Undefined reference" warnings
- [ ] No "Missing figure" warnings
- [ ] Page count is within 10 pages (excluding references and supplement)
- [ ] Running header shows correct short title and "Public Health" subject
- [ ] Footer shows page numbers in "X/Y" format
- [ ] All special characters are properly escaped: `\%`, `\$`, `\&`, `\#`, `\_`
- [ ] No raw `%`, `$`, `&`, `#` in text (will cause compilation errors or silent text disappearance)

## Turing Test (Does It Read Like a Human Wrote It?)

- [ ] No generic AI filler phrases:
  - "This is an important topic that deserves attention"
  - "In today's world..."
  - "It is worth noting that..."
  - "This study aims to shed light on..."
  - "Moving forward, it is crucial..."
- [ ] Specific domain terminology is used correctly throughout
- [ ] Paragraph transitions are logical and varied (not all "Furthermore," or "Additionally,")
- [ ] The argument has a clear narrative arc: context → gap → question → methods → findings → implications
- [ ] Numbers feel realistic: proportions are between 0-100%, sample sizes are plausible, CIs are not absurdly wide or narrow
- [ ] The writing style is consistent throughout (no sudden shifts in formality or vocabulary)
- [ ] Hedging is appropriate: strong claims for strong evidence, tentative language for weaker evidence
- [ ] The paper sounds like it was written by a public health researcher, not a language model

---

## Quick-Fix Priorities

If time is short, prioritize fixing these (most likely to be noticed by graders):

1. **Numbers mismatch** between Abstract and Results (instant credibility loss)
2. **Missing `\cite` keys** causing LaTeX errors (paper won't compile)
3. **Missing figure files** causing blank spaces (looks broken)
4. **Generic AI language** in Discussion (fails Turing test)
5. **Wrong statistical method** for the data structure (scientific rigor issue)
