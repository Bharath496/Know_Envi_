---
title: Know Envi Student Intelligence
emoji: 📊
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Know Envi 2.0

**Know Envi** is a free, local-first student performance and academic-risk analytics dashboard built with Python and Streamlit.

The project is designed as a portfolio-grade education analytics system that can run without a paid API, cloud database, or proprietary AI service.

## Highlights

- Built-in demo dataset so the app works immediately
- Upload support for CSV, Excel, and SQLite
- Automatic normalization of common student-data column names
- Department and semester filters
- Academic KPI cards
- Monthly performance trends
- Subject-wise performance analysis
- Attendance vs. score visualization
- Student-level drill-down
- Transparent High / Medium / Low risk alerts
- Human-readable reasons for every risk flag
- Downloadable CSV risk reports
- Data-quality checks for missing and duplicate records
- Responsive Streamlit interface
- Docker-ready deployment

## Risk logic

Know Envi deliberately uses an explainable rule-based risk engine rather than pretending a black-box model is automatically better.

Risk is based on two visible signals:

- academic score
- attendance

The dashboard exposes the reason for every alert, making the output suitable for review by teachers, mentors, or administrators.

The alerts are **decision support**, not an automatic academic judgment.

## Supported inputs

The app accepts:

- `.csv`
- `.xlsx` / `.xls`
- `.db` / `.sqlite` / `.sqlite3`

If an uploaded dataset uses common alternatives such as `name`, `marks`, `attendance`, `dept`, or `sem`, the app attempts to standardize them automatically.

## Run locally

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run streamlit_app.py
```

## Free deployment

The repository includes a Dockerfile configured for port `7860`, which makes it suitable for a free Hugging Face Space using the Docker SDK.

No paid database or paid LLM API is required.

## Repository structure

```text
Know_Envi_/
├── streamlit_app.py
├── src/
│   └── student_dashboard_analysis.py
├── scripts/
│   └── generate_student_dataset.py
├── dashboard_template.md
├── requirements.txt
├── Dockerfile
└── LICENSE
```

The legacy analysis and synthetic-data utilities are retained for experimentation, while the main app is now self-contained and can run immediately with its own demo data.

## Tech stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- SQLite / CSV / Excel support
- Docker

## Portfolio summary

> Built a local-first student intelligence dashboard with academic KPIs, attendance-performance analysis, student drill-downs, explainable risk alerts, data-quality checks, file ingestion, and downloadable reports.

## License

MIT
