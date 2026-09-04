
# Berlin Urban Deprivation Analysis
### A Cross-City Comparison with London Using Machine Learning and SHAP Explainability

**Author:** Mithun Surriya KS
**Date:** August 2026
**Tools:** Python · Pandas · Scikit-learn · SHAP · Matplotlib
**Data Source:** Monitoring Soziale Stadtentwicklung (MSS) 2023, Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen Berlin

---

## 1. Introduction

Cities like London and Berlin are among the wealthiest in the world — yet within each city, the gap between the most and least deprived neighbourhoods is dramatic. This project investigates the structure of social deprivation across Berlin's 143 planning districts (Bezirksregionen), using the same machine learning methodology applied in a previous study of London's 32 boroughs.

The core research question is: **what drives deprivation most in Berlin, and does it differ from London?**

In the London study, SHAP explainability analysis identified employment deprivation as the dominant driver of overall deprivation. This analysis tests whether the same pattern holds in Berlin, or whether a different indicator takes precedence — and what that difference means in practice.

---

## 2. Data

The dataset used is the **Monitoring Soziale Stadtentwicklung (MSS) 2023** — Berlin's official social development monitoring report, published by the Senate Department for Urban Development. It covers 143 planning districts across the city and includes data collected between 31.12.2020 and 31.12.2022.

**Indicators used:**

| Column | Description |
|---|---|
| unemployment_pct | % of residents claiming unemployment benefits (SGB II) |
| single_parent_pct | % of children living in single-parent households |
| welfare_pct | % of residents receiving welfare (SGB II and XII) |
| child_poverty_pct | % of children under 15 living in welfare-dependent households |

These four indicators were selected as they directly parallel the deprivation dimensions used in London's Index of Multiple Deprivation (IMD), enabling a fair cross-city comparison.

---

## 3. Data Preprocessing

The raw Excel file contained several formatting challenges typical of government-published data:

- **Header rows:** The first 11 rows contained title text, column descriptions, and city-wide averages (mean and standard deviation rows) rather than district-level data. These were skipped on import using `skiprows=11`.
- **Column renaming:** All column headers were in German (e.g. "S1: Anteil Arbeitslose") and renamed to descriptive English equivalents for clarity and reproducibility.
- **Summary rows:** Three rows at the bottom of the file contained city-wide totals (Berlin overall, mean across 143 districts, standard deviation) rather than individual district data. These were identified by their missing district_id values and removed using `dropna(subset=['district_id'])`.
- **Index reset:** After dropping rows, the dataframe index was reset to ensure clean sequential numbering.

**Final dataset:** 143 rows × 11 columns, with zero missing values across all indicator columns.

---

## 4. Exploratory Analysis

### 4.1 Summary Statistics

| Indicator | Mean | Min | Max |
|---|---|---|---|
| unemployment_pct | 4.47% | 0.82% | 14.07% |
| single_parent_pct | 26.71% | 15.76% | 43.31% |
| welfare_pct | 10.64% | 1.82% | 33.29% |
| child_poverty_pct | 23.11% | 3.03% | 65.62% |

The range between the least and most deprived districts is striking — unemployment varies by a factor of 17x, and child poverty by over 20x, within a single city.

### 4.2 Correlation Analysis

| Pair | Correlation |
|---|---|
| welfare_pct vs child_poverty_pct | 0.98 |
| unemployment_pct vs welfare_pct | 0.97 |
| unemployment_pct vs child_poverty_pct | 0.96 |
| unemployment_pct vs single_parent_pct | 0.53 |

Unemployment, welfare dependency, and child poverty are almost perfectly correlated (0.96–0.98), indicating they move as a single block across districts. Single-parent household rates show a moderate but weaker relationship (0.53), suggesting it reflects a partly independent dimension of deprivation.

### 4.3 Most and Least Deprived Districts

An overall deprivation score was calculated by standardising all four indicators (using z-score normalisation) and averaging them into a single composite score per district.

**Top 5 most deprived:**

| District | Deprivation Score |
|---|---|
| Köllnische Heide | 2.92 |
| MV Nord | 1.77 |
| Heerstraße | 1.68 |
| Osloer Straße | 1.67 |
| Rollbergesiedlung | 1.66 |

**Top 5 least deprived:**

| District | Deprivation Score |
|---|---|
| Mahlsdorf | -1.61 |
| Gatow/Kladow | -1.57 |
| Nord 1 - Frohnau/Hermsdorf | -1.52 |
| Müggelheim | -1.51 |
| Schmöckwitz | -1.40 |

The total gap between the most and least deprived districts spans approximately 4.5 standard deviations — a level of within-city inequality comparable to that observed in London.

A notable geographic pattern emerges: the most deprived districts are concentrated in former East Berlin and inner West Berlin areas with high immigrant populations, while the least deprived are predominantly in the outer West Berlin suburbs. This suggests that the socioeconomic legacy of German reunification (1990) remains visible in Berlin's deprivation data over 35 years later.

---

## 5. Machine Learning Model

### 5.1 Approach

A **Random Forest Regressor** was trained to predict each district's composite deprivation score from the four indicator columns. The same methodology was used in the London study, enabling direct comparison of feature importance findings.

- **Features (X):** unemployment_pct, single_parent_pct, welfare_pct, child_poverty_pct
- **Target (y):** composite deprivation score
- **Train/test split:** 80% training, 20% test
- **Model:** RandomForestRegressor, 100 trees, random_state=42

### 5.2 Model Performance

**R² Score: 0.97**

The model explains 97% of the variance in deprivation scores across Berlin's districts — indicating a strong and consistent relationship between the four indicators and overall deprivation. This is comparable to the R² of 0.897 achieved in the London study.

---

## 6. SHAP Explainability Analysis

SHAP (SHapley Additive exPlanations) was used to determine which indicator contributed most to the model's predictions across all 143 districts. SHAP measures the average impact of each feature on the model's output — a more rigorous measure of importance than simple correlation.

**Results:**

| Rank | Indicator | Mean SHAP Value |
|---|---|---|
| 1 | child_poverty_pct | 0.4398 |
| 2 | unemployment_pct | 0.2295 |
| 3 | welfare_pct | 0.1047 |
| 4 | single_parent_pct | 0.0817 |

**Child poverty is the dominant driver of overall deprivation in Berlin**, with a SHAP importance of 0.44 — nearly twice that of unemployment (0.23).

---

## 7. Cross-City Comparison: Berlin vs London

| | London | Berlin |
|---|---|---|
| Primary driver | Employment deprivation | Child poverty |
| Secondary driver | Income deprivation | Unemployment |
| Model R² | 0.897 | 0.97 |
| Most deprived area | Hackney | Köllnische Heide |
| Least deprived area | Richmond upon Thames | Mahlsdorf |
| Within-city gap | ~4 standard deviations | ~4.5 standard deviations |

Both cities show extreme within-city inequality of a similar magnitude. However, the structural driver differs: London's deprivation is primarily a **labour market problem** (employment deprivation ranks first), while Berlin's is primarily a **generational poverty problem** (child poverty ranks first).

This distinction has direct policy implications. A London policymaker should prioritise employment and job access programmes in deprived boroughs. A Berlin policymaker should prioritise family support, child welfare, and early years investment — because children are entering poverty even in districts where adult unemployment rates are relatively moderate.

---

## 8. Limitations

- **Causality:** SHAP values identify strong associations between indicators and deprivation scores, not causal relationships. Child poverty being the strongest predictor does not necessarily mean it causes deprivation — both may reflect a shared underlying condition.
- **Composite score:** The deprivation score was constructed from the same four indicators used as features, which introduces circularity. Future work could use an externally validated deprivation index as the target variable.
- **Data scope:** The MSS 2023 covers 143 planning districts. A finer-grained neighbourhood-level analysis may reveal additional patterns not visible at this resolution.
- **Single time point:** This analysis uses a snapshot of 2022 data. A longitudinal analysis using multiple MSS editions (available from 2000 onwards) could reveal whether Berlin's deprivation structure is stable or changing over time.

---

## 9. Conclusions

This analysis provides evidence that within-city inequality in Berlin is both extreme and structurally distinct from London. While both cities show a gap of approximately 4–4.5 standard deviations between their most and least deprived areas, the primary driver differs: child poverty in Berlin versus employment in London.

The persistence of a geographic East/West deprivation divide in Berlin — over three decades after reunification — suggests that historical structural factors continue to shape social outcomes at the neighbourhood level, independent of more recent economic conditions.

Future work will extend this comparison to a third European city, and explore whether a model trained on London data generalises to Berlin's deprivation structure — directly testing the transferability of city-specific AI systems across different urban contexts.

---

## 10. Files in This Repository

- `berlin_deprivation_analysis.ipynb` — full analysis notebook
- `1sdi_mss2023.xlsx` — raw data (MSS 2023, Berlin Senate)
- `berlin_shap.png` — SHAP feature importance chart
- `README.md` — this report

---

*This project is part of an ongoing cross-city deprivation research series. The London analysis is available at: [London Urban Inequality Analyser](https://londoninequalitydashboard-r8w46bkkvvt6xmeyxbu7ku.streamlit.app)*
