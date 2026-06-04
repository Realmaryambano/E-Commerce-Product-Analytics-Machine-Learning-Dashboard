# Ecommerce Data Toolkit

Purpose
-------

This project is a lightweight toolkit for collecting, cleaning, exploring, and modeling e-commerce product data. It is designed for data scientists and ML engineers who want a repeatable pipeline from web-scraped product listings to trained models and a small inference app. The repository focuses on reproducible data processing, clear experiment tracking, and modular scripts that are easy to adapt for new sources or prediction targets.

What it contains
-----------------

- Data ingestion: `scraper.py` — fetch product pages and store raw rows in `data/raw_products.csv`.
- Data cleaning: `clean.py` — canonicalise fields, remove duplicates, and produce `data/clean_products.csv`.
- Exploratory analysis: `eda.py` and `notebooks/` — visualisations and quick checks saved to `plots/`.
- Feature engineering: `features.py` — transform cleaned data into `data/features_ready.csv` for modeling.
- Model training: `train_models.py` — train and evaluate models; trained artifacts go to `models/`.
- Inference app: `app.py` — simple interface to load a model and predict (CLI or minimal HTTP endpoint).

Repository layout
-----------------

```
.
├─ app.py                 # small inference app
├─ clean.py               # data cleaning pipeline
├─ eda.py                 # exploratory analysis script
├─ features.py            # feature engineering pipeline
├─ scraper.py             # scraping script
├─ train_models.py        # model training and evaluation
├─ data/
│   ├─ raw_products.csv
│   ├─ clean_products.csv
│   └─ features_ready.csv
├─ models/                # trained model artifacts
├─ notebooks/             # notebooks used for EDA and experiments
└─ plots/                 # generated figures
```

Quick start
-----------

1. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

If `requirements.txt` is missing, install core packages:

```bash
pip install pandas scikit-learn requests beautifulsoup4 lxml matplotlib seaborn joblib
```

2. Run the full pipeline (recommended sequence):

```bash
python scraper.py          # collect raw data
python clean.py            # clean and normalise
python eda.py              # produce plots and quick checks
python features.py         # build features for modeling
python train_models.py     # train and save models to models/
python app.py              # run inference (follow app.py docs)
```

Detailed sections
-----------------

- Data sources: Configure `scraper.py` with target URLs or feeds. Output is appended to `data/raw_products.csv`.
- Cleaning rules: `clean.py` applies normalization (lowercasing, trimming), fills missing values for key columns, drops malformed rows, and deduplicates by product ID or normalized title.
- Feature engineering: `features.py` creates numeric/encoded features (price transforms, TF-IDF or text embeddings for descriptions, categorical encodings for brand/category, availability flags).
- Modeling: `train_models.py` trains one or more baseline models (e.g., RandomForest, LightGBM, or logistic regression), performs cross-validation, and writes performance logs and serialized models to `models/`.
- Inference: `app.py` loads a serialized model and exposes a simple interface for single-row or batch predictions. See inline docstring in `app.py` for usage examples.

Data schema (expected)
-----------------------

Raw rows should include at least:

- `product_id` (string) — unique identifier when available
- `title` (string)
- `description` (string)
- `price` (float or string to parse)
- `currency` (string)
- `brand` (string)
- `category` (string)
- `url` (string)

After cleaning, `data/clean_products.csv` contains canonicalised, typed columns. `data/features_ready.csv` contains feature columns with a target column (if supervised training is used).

Best practices and notes
------------------------

- Keep raw data immutable: never overwrite `raw_products.csv` — append new scrapes and create snapshots.
- Track experiments by naming model artifacts with timestamps or git commit hashes.
- Validate assumptions in `eda.py` before training to avoid garbage-in models.

Testing and CI
--------------

- Add unit tests for small, deterministic functions (parsers, normalisers) and integration tests for pipeline scripts.
- Add a `requirements-dev.txt` with testing tools (`pytest`, `black`, `ruff`) and configure a basic GitHub Actions workflow to run tests on PRs.


Contributing
------------

Contributions are welcome. Please open an issue to discuss changes before submitting a pull request. Follow these steps:

1. Fork the repo and create a feature branch.
2. Add tests for your changes when applicable.
3. Submit a PR with a clear description of the change and link to any artifacts or visualisations.



Contact
-------


If you want help extending this project (requirements file, Docker, CI), tell me which piece to add and I'll scaffold it.

You can also reach me at: maryambano.official@gmail.com

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.


