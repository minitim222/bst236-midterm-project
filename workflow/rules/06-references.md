# Rule 06: Reference Generation

## Purpose

Generate a realistic, topically relevant `references.bib` file with 25-35 BibTeX entries that compile cleanly with the Vancouver bibliography style.

---

## Reference Strategy

### Step 1: Use Web Search for Real References

Whenever possible, use web search to find REAL published papers. Search for:
- "[topic] JAMA" or "[topic] JAMA Network Open"
- "[exposure] [outcome] association" on Google Scholar
- "[statistical method name] econometrics" for methods references
- "[data source name] methodology" for data references

Extract from search results: full title, all authors, journal name, year, volume, issue, pages, DOI.

### Step 2: Fill Gaps with Plausible References

If web search is unavailable or too slow, generate plausible references that:
- Use realistic author names (2-4 authors typical)
- Use real journal names (see list below)
- Have plausible titles that match the topic
- Have realistic year, volume, issue, and page numbers
- Have DOI formats matching the journal: `10.1001/jamanetworkopen.2024.XXXXX`

---

## Reference Distribution (25-35 total)

Allocate references across these categories:

| Category | Count | Where cited |
|----------|-------|-------------|
| Historical/foundational context | 2-3 | Introduction paragraph 1 |
| Policy/intervention background | 4-6 | Introduction paragraph 2 |
| Prior studies on similar topics | 3-5 | Introduction paragraph 3 |
| Ethical/political debate | 2-3 | Introduction paragraph 4 |
| Data source documentation | 2-3 | Methods: Data |
| Statistical methods | 2-3 | Methods: Statistical Analysis |
| Comparison studies | 4-6 | Discussion |
| Limitation-related | 1-2 | Discussion: Limitations |
| Federal policy/legal | 2-3 | Introduction or Discussion |

---

## BibTeX Format

Every entry must follow this format exactly:

### Journal Article (most common)
```bibtex
@article{wang2024state,
  title={State {COVID-19} vaccine mandates and uptake among health care workers in the {US}},
  author={Wang, Yin and Stoecker, Charles and Callison, Kevin and Hernandez, Julie H},
  journal={JAMA Netw Open},
  volume={7},
  number={8},
  pages={e2426847},
  year={2024},
  doi={10.1001/jamanetworkopen.2024.26847}
}
```

### Book
```bibtex
@book{schama2023foreign,
  title={Foreign Bodies: Pandemics, Vaccines and the Health of Nations},
  author={Schama, Simon},
  publisher={Simon \& Schuster},
  year={2023}
}
```

### Government Report / Webpage
```bibtex
@misc{cms2021mandate,
  title={Biden-{Harris} Administration takes additional action to protect {America's} nursing home residents from {COVID-19}},
  author={{Centers for Medicare \& Medicaid Services}},
  year={2021},
  howpublished={News release},
  note={Accessed June 8, 2023. \url{https://www.cms.gov/newsroom/...}}
}
```

### Working Paper
```bibtex
@techreport{acton2022effect,
  title={The effect of vaccine mandates on disease spread: Evidence from college {COVID-19} mandates},
  author={Acton, Ralph K and Cao, Wenjia and Cook, Emily E and Imberman, Scott A and Lovenheim, Michael F},
  institution={National Bureau of Economic Research},
  type={Working Paper},
  number={30303},
  year={2022}
}
```

---

## BibTeX Key Naming Convention

Use `firstauthorlastname` + `year` + `firstkeyword`:
- `wang2024state`
- `mcgarry2022association`
- `sun2021estimating`
- `callaway2021difference`

This makes keys predictable and avoids collisions.

---

## Real Journal Names for BibTeX

Use these abbreviated journal names (Vancouver style):

| Full Name | BibTeX `journal` field |
|-----------|----------------------|
| JAMA | JAMA |
| JAMA Network Open | JAMA Netw Open |
| JAMA Health Forum | JAMA Health Forum |
| New England Journal of Medicine | N Engl J Med |
| The Lancet | Lancet |
| The Lancet Public Health | Lancet Public Health |
| American Journal of Public Health | Am J Public Health |
| Health Affairs | Health Aff (Millwood) |
| Nature | Nature |
| Nature Human Behaviour | Nat Hum Behav |
| Nature Communications | Nat Commun |
| BMJ | BMJ |
| Annals of Internal Medicine | Ann Intern Med |
| Vaccine | Vaccine |
| Vaccines | Vaccines (Basel) |
| Journal of Econometrics | J Econom |
| Journal of Medical Ethics | J Med Ethics |
| Morbidity and Mortality Weekly Report | MMWR Morb Mortal Wkly Rep |
| Preventive Medicine | Prev Med |
| Social Science & Medicine | Soc Sci Med |

---

## Citation Insertion in LaTeX

The template uses `natbib` with `super` option and `vancouver` style. Citations render as superscript numbers.

**How to cite:**
```latex
Prior work has examined this topic.\cite{wang2024state,mcgarry2022association}
```
This renders as: "Prior work has examined this topic.^{1,2}"

**For multiple citations:** `\cite{ref1,ref2,ref3}` — natbib auto-sorts and compresses (e.g., 1-3).

**For in-text author mentions:** Write the name in text and cite:
```latex
Sun and Abraham\cite{sun2021estimating} proposed a method that...
```

---

## Validation Checklist

Before finalizing `references.bib`:

1. Every `\cite{key}` in the paper has a matching entry in the `.bib` file
2. No `.bib` entry is unused (LaTeX will warn but not error)
3. No duplicate keys
4. All entries have at minimum: `title`, `author`, `year`
5. Journal articles have: `journal`, `volume`, `year`; ideally also `number`, `pages`, `doi`
6. Special characters in titles are protected with braces: `{COVID-19}`, `{US}`, `{HIV}`
7. Author names use the format: `Last, First` or `Last, First Middle`
8. Institutional authors use double braces: `author={{World Health Organization}}`
9. Ampersands are escaped: `Simon \& Schuster`
10. The file compiles without bibtex errors

---

## Common Mistakes to Avoid

1. Don't use `@article` for websites or reports — use `@misc` or `@techreport`
2. Don't forget to protect acronyms in titles with braces: `{COVID-19}`, `{US}`, `{HIV}`
3. Don't include URLs in `@article` entries — use DOI instead
4. Don't mix citation styles — use `\cite{}` everywhere (natbib handles formatting)
5. Don't have orphan citations — every cited work must appear in text AND in `.bib`
6. Don't use extremely long keys — keep them short and memorable
