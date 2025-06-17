
# 📊 Logistic Regression Fairness Analysis of LLM Predictions

This repository contains a Jupyter notebook (`Logistic_Regression.ipynb`) that reproduces the logistic regression models presented in the paper:

**_Auditing Fairness in LLM-Generated Survey Responses_** ([arXiv:2501.15351](https://arxiv.org/abs/2501.15351))  
Andrés Abeliuk, Vanessa Gaete, Naim Bro – 2025

---

## 📁 Contents

- **`Logistic_Regression.ipynb`**: Performs fairness-aware logistic regressions using socio-demographic variables to explain prediction accuracy of LLMs simulating survey responses.
- Models are estimated for:
  - 🇨🇱 **Chile**: Includes Models 1–4 (Table 2 in the paper)
  - 🇺🇸 **United States**: Includes Models 1–3 (Table 3 in the paper)

---


## 📈 Description of Models

The notebook estimates the following:

### Chile
- **Model 1**: Main effects only
- **Model 2**: Adds `sexo × religion`
- **Model 3**: Adds `Education × iden_pol_2`
- **Model 4**: Adds `religion × iden_pol_2`

### United States
- **Model 1**: Main effects only
- **Model 2**: Adds `sexo × iden_pol_2`
- **Model 3**: Adds `race × sexo`

---

