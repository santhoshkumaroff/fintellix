# ML Basics – Quick Recap (JD mentions preparing data "for models"; freshers often get 2–3 of these)

### Q1. Supervised vs unsupervised vs reinforcement learning?
- **Supervised:** learn from labelled data. *Example:* predict loan default (label: defaulted yes/no).
- **Unsupervised:** find structure without labels. *Example:* cluster customers by transaction behaviour.
- **Reinforcement:** learn by reward. *Example:* RLHF in LLM alignment; a collections strategy that learns which reminder timing works best.

### Q2. Classification vs regression?
- **Classification** predicts a category. *Example:* complaint category, default yes/no.
- **Regression** predicts a number. *Example:* predict LGD % or next month's deposit balance.

### Q3. Overfitting vs underfitting? How do you fix overfitting?
**Answer:** Overfitting = great on training data, poor on new data (it memorised the noise). Underfitting = poor on both (too simple). Fix overfitting with more data, regularisation (L1/L2), simpler models, cross-validation, early stopping, dropout, or pruning trees.
- **Example 1:** A decision tree with 100% train accuracy and 70% test accuracy on default prediction is overfitting, so limit `max_depth`.
- **Example 2:** Linear regression for a clearly non-linear pattern underfits.

### Q4. Train / validation / test split, and cross-validation?
**Answer:** Train to fit, validation to tune, test for the final unbiased estimate. k-fold CV rotates the validation fold for a stable estimate.
- **Example:** 5-fold CV for a fraud model; time-based splits for anything time-dependent.

### Q5. Common algorithms (one line each)?
Logistic regression (baseline classifier, interpretable; widely used in credit scoring), decision tree, random forest, gradient boosting (XGBoost/LightGBM, strong on tabular data), k-means (clustering), KNN, SVM.
- **Example 1:** A credit scorecard → logistic regression, because regulators value interpretability.
- **Example 2:** Fraud detection on tabular features → LightGBM.

### Q6. Accuracy is 98% on a fraud model – is it good?
**Answer:** Not necessarily. If only 2% of transactions are fraud, predicting "not fraud" every time gives 98% accuracy. Use precision, recall, F1, PR-AUC, and handle the imbalance (class weights, resampling).
- **Example:** Recall on the fraud class is 30%, which is unacceptable despite 98% accuracy.

### Q7. Bias-variance trade-off?
**Answer:** High bias means the model is too simple (underfits). High variance means it's too sensitive to the training data (overfits). The goal is the balance that minimises test error.

### Q8. What is feature engineering? Banking examples?
**Answer:** Creating informative inputs from raw data. *Examples:* debt-to-income ratio, number of missed EMIs in the last 6 months, max DPD in the last 12 months, credit utilisation %, account age.

### Q9. Explainability – why does it matter in banking?
**Answer:** Regulators and customers need reasons for decisions (e.g. why a loan was rejected). Tools: feature importance, SHAP, LIME, and inherently interpretable models.
- **Example:** SHAP shows "high utilisation" and "2 recent missed EMIs" drove the rejection.

### Q10. Classical ML vs LLM – when to use which?
- **Structured numeric prediction** (default probability) → classical ML. It's cheaper, more accurate and explainable.
- **Unstructured text tasks** (summarise, extract, classify free text, answer questions) → LLM.
- **Example:** Predict NPA risk with LightGBM. Explain the risk drivers to a relationship manager in plain English with Claude.
