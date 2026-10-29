# 🧪 Validation Playground

An interactive demo for the AI Engineering post
**"Your Model Scored 97%, Then Failed on Real Data: How to Build and Test It the Right Way"**
(K-fold cross validation, explained simply).

By **Nagaraju Poralla**, AI Engineering series · [aiengineer.help](https://aiengineer.help)

![Single split vs K-fold](screenshots/02b-single-vs-kfold-charts.png)

## What you can do

| Section | The one idea |
|---|---|
| **1. One split vs K-fold** | One train/test split is luck. Press **Reshuffle** (or drag the seed) and watch the score jump. A chart shows the score on 20 different seeds. Next to it, K-fold gives one bar per fold plus the mean and std. A **Stratified** toggle keeps the class mix in every fold. |
| **2. Leakage** | A switch compares scaling **before the split** (leaks) with scaling **inside a Pipeline** (correct). It shows both scores and the difference, and explains why. A bonus demo on pure noise shows a leak that fakes 80%+ accuracy. |
| **3. Small data or large data?** | Enter a row count and class balance. The advisor recommends **K-fold**, **stratified K-fold**, **LOOCV** or a **hold-out split**, explains why, and gives code to copy. |
| **4. Your setup as code** | The exact scikit-learn code for the settings you picked. |

**Data:** breast cancer, wine, iris, a synthetic imbalanced set (5% positive), or **upload your own CSV** and choose the target column (classification only; text columns are one-hot encoded, missing values are filled inside the pipeline).
**Models:** Logistic Regression, Random Forest, Decision Tree. **k:** 3 to 10. **Score:** accuracy, balanced accuracy, or macro F1.

### An honest note on scaling leakage
Scaling before the split leaks only a little. On the breast cancer data the gap is 0.000 to about 0.007 depending on dataset and folds, and tree models (Decision Tree, Random Forest) do not care about feature scale at all. The playground shows the true number and does not exaggerate it. Steps that use the **labels** (like selecting the best features) can leak a lot, which is why the noise demo is included.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501.

## Test it

```bash
python test_app.py     # runs the app headlessly for every dataset, model, score, stratified on/off, leak switch, k and reshuffle
```

Screenshots (optional, needs Playwright and Chrome): `python take_screenshots.py http://localhost:8501`

## Deploy on Render (free)

This repo includes a `render.yaml`. Create a **Web Service** from the repo with:

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
- Env var: `PYTHON_VERSION=3.12.8`

The free plan sleeps after inactivity, so the first load can take about a minute.

## Files

- `app.py`: the Streamlit app (layout and charts)
- `validation_lib.py`: data loading, models, experiments and the advisor (plain scikit-learn)
- `sample_data/customer_churn_sample.csv`: a small CSV to try the upload (target: `churned`)
- `.streamlit/config.toml`: the white and pastel theme

## License

MIT, see [LICENSE](LICENSE).
