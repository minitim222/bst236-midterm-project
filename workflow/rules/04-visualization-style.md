# Rule 04: Visualization Style Guide

## Purpose

Generate publication-quality figures that match the JAMA Network Open aesthetic. All figures must look professional enough to pass visual inspection as a real journal article.

---

## Matplotlib Global Configuration

Place this block at the top of every analysis script, before any plotting calls:

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

JAMA_CRIMSON = '#AF1E37'
JAMA_DARK = '#333333'
JAMA_GRAY = '#666666'
JAMA_LIGHT = '#C8C8C8'
JAMA_GOLD = '#C39B32'

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
```

---

## Color Palette

| Use | Color | Hex |
|-----|-------|-----|
| Primary series / main emphasis | JAMA Crimson | `#AF1E37` |
| Secondary series | Dark Gray | `#333333` |
| Tertiary series | Medium Gray | `#666666` |
| Reference lines / gridlines | Light Gray | `#C8C8C8` |
| Accent (sparingly) | JAMA Gold | `#C39B32` |

For two-outcome plots (like the sample paper), use crimson for outcome 1 and dark gray for outcome 2.

---

## Figure Types and Specifications

### Event Study / Coefficient Plot

This is the most common figure type for policy evaluation studies. It plots regression coefficients over time relative to a treatment event.

```python
def plot_event_study(event_times, coefficients, ci_lower, ci_upper,
                     label='', color=JAMA_CRIMSON, ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 5))

    ax.axhline(y=0, color=JAMA_LIGHT, linewidth=0.8, linestyle='-', zorder=1)
    ax.axvline(x=-0.5, color=JAMA_GRAY, linewidth=0.8, linestyle='--', zorder=1)

    ax.errorbar(event_times, coefficients,
                yerr=[np.array(coefficients) - np.array(ci_lower),
                      np.array(ci_upper) - np.array(coefficients)],
                fmt='o-', color=color, capsize=3, capthick=1,
                markersize=6, linewidth=1.5, label=label, zorder=3)

    ax.set_xlabel('Time from mandate announcement, wk')
    ax.set_ylabel('Change, percentage points')
    ax.legend(loc='lower right')

    return ax
```

**Requirements:**
- Horizontal reference line at y = 0 (light gray, solid)
- Vertical dashed line at event time 0 (or between -1 and 0, at x = -0.5)
- Filled circles connected by lines for point estimates
- Error bars with caps for 95% CIs
- X-axis: relative time units (weeks, months, quarters)
- Y-axis: "Change, percentage points" or "Change in proportion"
- Symmetric y-axis range (e.g., -15 to 15) so zero line is centered
- Pre-treatment coefficients should hover near zero (validates parallel trends)

**For two-outcome plots (preferred: use multi-panel, NOT overlay):**

Overlaying two outcomes on one plot makes it harder to read. Use a 2-panel layout instead:

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 9), sharex=True)

plot_event_study(times, coefs1, ci_lo1, ci_hi1,
                 label='Ever vaccinated', color=JAMA_CRIMSON, ax=ax1)
ax1.set_title('A', loc='left', fontsize=12, fontweight='bold')
ax1.set_ylabel('Change, percentage points')
ax1.text(0.98, 0.95, 'Ever vaccinated', transform=ax1.transAxes,
         ha='right', va='top', fontsize=9, color=JAMA_GRAY)

plot_event_study(times, coefs2, ci_lo2, ci_hi2,
                 label='Primary series completed', color=JAMA_DARK, ax=ax2)
ax2.set_title('B', loc='left', fontsize=12, fontweight='bold')
ax2.set_ylabel('Change, percentage points')
ax2.text(0.98, 0.95, 'Primary series completed', transform=ax2.transAxes,
         ha='right', va='top', fontsize=9, color=JAMA_GRAY)

plt.tight_layout()
fig.savefig('figures/figure1.pdf')
```

**Only overlay on one plot if the two outcomes have very similar scales and the CI bars do not overlap visually.** If in doubt, use panels.

### Stratified Event Study (Multi-Panel)

For subgroup analyses, use a 2-row, 1-column layout:

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 9), sharex=True)

# Panel A: Subgroup 1
plot_event_study(times, coefs_a, ci_lo_a, ci_hi_a, ax=ax1)
ax1.set_title('A. States with test-out option', loc='left', fontsize=11)

# Panel B: Subgroup 2
plot_event_study(times, coefs_b, ci_lo_b, ci_hi_b, ax=ax2)
ax2.set_title('B. States with no test-out option', loc='left', fontsize=11)

plt.tight_layout()
fig.savefig('figures/figure2.pdf')
```

**Panel labeling:** Use "A" and "B" (bold) at the top-left of each panel.

### Bar Chart (Descriptive)

For comparing values across categories:

```python
fig, ax = plt.subplots(figsize=(7, 5))
categories = ['Category A', 'Category B', 'Category C']
values = [45.2, 32.1, 22.7]

bars = ax.barh(categories, values, color=JAMA_CRIMSON, height=0.6, edgecolor='white')

for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', va='center', fontsize=9)

ax.set_xlabel('Percentage')
ax.invert_yaxis()
fig.savefig('figures/descriptive.pdf')
```

### Line Chart (Time Trends)

For showing trends over time:

```python
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(dates, treatment_trend, '-o', color=JAMA_CRIMSON,
        label='Treatment group', markersize=5)
ax.plot(dates, control_trend, '-s', color=JAMA_DARK,
        label='Control group', markersize=5)

ax.axvline(x=intervention_date, color=JAMA_GRAY, linestyle='--', linewidth=0.8)
ax.set_xlabel('Date')
ax.set_ylabel('Outcome measure')
ax.legend()
fig.savefig('figures/trends.pdf')
```

### Forest Plot (Multiple Effect Estimates)

For displaying multiple coefficient estimates side by side:

```python
fig, ax = plt.subplots(figsize=(7, 4))
labels = ['Full sample', 'Test-out states', 'No test-out states', 'Age 25-49', 'Age 50-64']
estimates = [3.46, 2.82, 3.77, 5.97, -1.78]
ci_lo = [0.29, -5.57, 0.82, 2.37, -5.62]
ci_hi = [6.63, 11.22, 6.71, 9.57, 2.06]

y_pos = range(len(labels))
ax.errorbar(estimates, y_pos, xerr=[np.array(estimates)-np.array(ci_lo),
            np.array(ci_hi)-np.array(estimates)],
            fmt='o', color=JAMA_CRIMSON, capsize=4, markersize=7)
ax.axvline(x=0, color=JAMA_LIGHT, linewidth=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.set_xlabel('Change, percentage points (95% CI)')
ax.invert_yaxis()
fig.savefig('figures/forest.pdf')
```

---

## Saving Figures

Always save in both formats:

```python
fig.savefig('figures/figure1.pdf', dpi=300, bbox_inches='tight')
fig.savefig('figures/figure1.png', dpi=300, bbox_inches='tight')
plt.close(fig)
```

- PDF for LaTeX inclusion (vector, crisp at any size)
- PNG as backup
- Always call `plt.close(fig)` after saving to free memory

---

## LaTeX Figure Inclusion

In the paper, reference figures like this:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{figure1.pdf}
\caption{Event Study of the Association Between State COVID-19 Vaccine Mandates
and Uptake Among Health Care Workers in the Full Sample}
\label{fig:main_results}
\end{figure}
```

**Caption requirements:**
- Start with figure type: "Event Study of..." or "Bar Chart Showing..." or "Trends in..."
- Be specific about what is shown and the sample
- Add a note below the caption (in smaller font) explaining the methodology, similar to the sample paper

---

## Annotation Best Practices

- Always add "Pre-mandate" and "Post-mandate" text labels on event study plots, positioned on each side of the vertical dashed line
- For trend plots, add a text annotation near the vertical line: "Mandate announcements begin"
- For forest plots, add the numeric estimate and CI as right-aligned text next to each point:
  ```python
  ax.text(x_right, y_pos, f'{est:.1f} [{lo:.1f}, {hi:.1f}]', va='center', fontsize=8)
  ```
- Symmetrize y-axis on event study plots so the zero line is centered:
  ```python
  ymax = max(abs(ax.get_ylim()[0]), abs(ax.get_ylim()[1]))
  ax.set_ylim(-ymax * 1.1, ymax * 1.1)
  ```

---

## Common Mistakes to Avoid

1. Don't use default matplotlib colors (blue/orange) — always set JAMA palette
2. Don't include background gridlines (or make them very faint horizontal only)
3. Don't use titles on figures — the caption serves as the title
4. Don't forget to close figures with `plt.close()` to avoid memory issues
5. Don't use PNG for LaTeX — use PDF for sharp rendering
6. Don't make figures too small — full-width (7 inches) is standard for JAMA
7. Don't include a legend if there's only one series
8. Don't overlay two outcomes on one plot if CI bars would overlap — use multi-panel instead
9. Don't use `prefix='race'` in `get_dummies` and then select `c.startswith('race_')` without excluding the original string column (e.g., `race_cat`)
