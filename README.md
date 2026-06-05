---
title: Know Envi Student Dashboard
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Know Envi Student Dashboard

This workspace contains a backend analysis layer and a Streamlit dashboard for both school and college student dashboards.

It is designed to support:
- synthetic academic dataset generation
- school and college student performance analysis
- `matplotlib`-based visualization
- CSV inputs generated from a reproducible script

## What is included

- `src/student_dashboard_analysis.py`: reusable loader and plotting helpers
- `dashboard_template.md`: layout notes based on the provided UI, with the food section removed
- `streamlit_app.py`: the Streamlit app entrypoint
- `scripts/generate_student_dataset.py`: creates both school and college datasets
- `requirements.txt`: Python dependencies for the analysis layer

## Supported inputs

- `.csv`
- `.xlsx` / `.xls`
- `.db` / `.sqlite` / `.sqlite3`

## Next step

Generate the dataset with:

```bash
python scripts/generate_student_dataset.py
```

This writes:
- `data/school_student_master.csv`
- `data/school_academic_records.csv`
- `data/college_student_master.csv`
- `data/college_academic_records.csv`

Run the dashboard with:

```bash
python -m streamlit run streamlit_app.py
```

## Hugging Face Spaces

This repo is also prepared for a free public Hugging Face Space using the Docker SDK.

Once pushed to a Space repository, the app will be available at a public `https://<space-name>.hf.space` URL while the Space exists.
Free Spaces can sleep when inactive, but the URL remains the same.

When you send the final database and UI build target, this starter can be connected to:
- dashboard cards
- filters
- chart sections
- table summaries
- model or rule-based risk scoring
