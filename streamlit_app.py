from __future__ import annotations

from io import BytesIO
from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Know Envi • Student Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

REQUIRED_COLUMNS = {
    "student_name": ["student_name", "name", "student"],
    "student_id": ["student_id", "reg_no", "register_no", "roll_no", "admission_no"],
    "attendance_pct": ["attendance_pct", "attendance", "attendance_percentage"],
    "average_score": ["average_score", "score", "marks", "percentage", "total50", "total_50"],
    "department": ["department", "dept", "course"],
    "semester": ["semester", "sem", "year"],
    "subject": ["subject", "paper", "course_name"],
    "month_name": ["month_name", "month"],
}


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
        [data-testid="stSidebar"] {background: #12182b;}
        [data-testid="stSidebar"] * {color: #f6f7fb;}
        .hero {
            padding: 1.25rem 1.35rem;
            border: 1px solid #e7e9f4;
            border-radius: 22px;
            background: linear-gradient(135deg, #ffffff 0%, #f4f6ff 100%);
            margin-bottom: 1rem;
        }
        .hero h1 {margin: 0; font-size: 2rem; color: #18223f;}
        .hero p {margin: .35rem 0 0; color: #6d7390;}
        .metric-card {
            padding: 1rem 1.05rem;
            border: 1px solid #e8eaf3;
            border-radius: 18px;
            background: white;
            min-height: 104px;
        }
        .metric-label {color: #8a90a8; font-size: .78rem;}
        .metric-value {color: #18223f; font-size: 1.55rem; font-weight: 800;}
        .risk-high {color: #b42318; font-weight: 700;}
        .risk-medium {color: #b54708; font-weight: 700;}
        .risk-low {color: #027a48; font-weight: 700;}
        .tiny {font-size: .78rem; color: #7f859e;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result.columns = (
        result.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^0-9a-zA-Z_]+", "", regex=True)
    )
    return result


def first_match(columns: list[str], aliases: list[str]) -> str | None:
    for name in aliases:
        if name in columns:
            return name
    return None


def standardize_frame(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df).dropna(how="all").reset_index(drop=True)
    columns = list(df.columns)
    rename: dict[str, str] = {}
    for canonical, aliases in REQUIRED_COLUMNS.items():
        match = first_match(columns, aliases)
        if match and match != canonical and canonical not in df.columns:
            rename[match] = canonical
    df = df.rename(columns=rename)

    if "student_name" not in df.columns:
        df["student_name"] = [f"Student {i + 1}" for i in range(len(df))]
    if "student_id" not in df.columns:
        df["student_id"] = [f"STU{i + 1:04d}" for i in range(len(df))]
    if "department" not in df.columns:
        df["department"] = "General"
    if "semester" not in df.columns:
        df["semester"] = 1
    if "subject" not in df.columns:
        df["subject"] = "Overall"
    if "month_name" not in df.columns:
        df["month_name"] = "Current"

    for col in ["attendance_pct", "average_score", "semester"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "attendance_pct" not in df.columns:
        df["attendance_pct"] = np.nan
    if "average_score" not in df.columns:
        df["average_score"] = np.nan

    df["student_name"] = df["student_name"].astype(str).str.strip()
    df["student_id"] = df["student_id"].astype(str).str.strip()
    df["department"] = df["department"].astype(str).str.strip()
    df["subject"] = df["subject"].astype(str).str.strip()
    return df


def load_upload(uploaded) -> pd.DataFrame:
    suffix = Path(uploaded.name).suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(uploaded)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(uploaded)
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        raw = uploaded.getvalue()
        tmp = Path("/tmp/know_envi_upload.sqlite")
        tmp.write_bytes(raw)
        with sqlite3.connect(tmp) as conn:
            tables = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn
            )
            if tables.empty:
                raise ValueError("No table found in the uploaded SQLite database.")
            return pd.read_sql_query(f'SELECT * FROM "{tables.iloc[0, 0]}"', conn)
    raise ValueError("Supported formats: CSV, XLSX/XLS, SQLite.")


@st.cache_data(show_spinner=False)
def demo_data(seed: int = 42, students: int = 420) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    departments = ["AIML", "CSE", "Data Science", "IT", "ECE"]
    subjects = {
        "AIML": ["Python", "Machine Learning", "Statistics", "NLP"],
        "CSE": ["Data Structures", "DBMS", "Networks", "Java"],
        "Data Science": ["Python", "Statistics", "Visualization", "ML"],
        "IT": ["Web Tech", "DBMS", "Cloud", "Java"],
        "ECE": ["Signals", "Digital Systems", "Python", "IoT"],
    }
    months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    rows: list[dict[str, object]] = []

    for i in range(students):
        sid = f"RCAS26{i + 1:04d}"
        dept = departments[i % len(departments)]
        sem = int(rng.integers(1, 7))
        ability = float(np.clip(rng.normal(68, 12), 32, 94))
        base_attendance = float(np.clip(rng.normal(84, 9), 45, 100))
        name = f"Student {i + 1:03d}"
        for month_index, month in enumerate(months):
            growth = month_index * rng.normal(0.8, 0.25)
            for subject in subjects[dept]:
                score = float(np.clip(ability + growth + rng.normal(0, 8), 20, 100))
                attendance = float(np.clip(base_attendance + rng.normal(0, 4), 35, 100))
                rows.append(
                    {
                        "student_id": sid,
                        "student_name": name,
                        "department": dept,
                        "semester": sem,
                        "subject": subject,
                        "month_name": month,
                        "attendance_pct": round(attendance, 1),
                        "average_score": round(score, 1),
                    }
                )
    return pd.DataFrame(rows)


def student_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["student_id", "student_name", "department", "semester"], as_index=False)
        .agg(
            average_score=("average_score", "mean"),
            attendance_pct=("attendance_pct", "mean"),
            records=("student_id", "size"),
        )
    )
    summary["average_score"] = summary["average_score"].round(1)
    summary["attendance_pct"] = summary["attendance_pct"].round(1)
    return apply_risk(summary)


def apply_risk(summary: pd.DataFrame) -> pd.DataFrame:
    df = summary.copy()
    score = df["average_score"].fillna(0)
    attendance = df["attendance_pct"].fillna(0)

    points = np.zeros(len(df), dtype=int)
    points += np.where(score < 50, 3, np.where(score < 60, 2, np.where(score < 70, 1, 0)))
    points += np.where(attendance < 65, 3, np.where(attendance < 75, 2, np.where(attendance < 85, 1, 0)))
    df["risk_points"] = points
    df["risk_level"] = np.select(
        [points >= 5, points >= 3],
        ["High", "Medium"],
        default="Low",
    )

    reasons = []
    for s, a in zip(score, attendance):
        parts = []
        if s < 60:
            parts.append("low academic score")
        elif s < 70:
            parts.append("score needs improvement")
        if a < 75:
            parts.append("low attendance")
        elif a < 85:
            parts.append("attendance watch")
        reasons.append(", ".join(parts) if parts else "on track")
    df["risk_reason"] = reasons
    return df.sort_values(["risk_points", "average_score"], ascending=[False, True])


def metric_card(label: str, value: str, note: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="tiny">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plot_monthly(df: pd.DataFrame) -> plt.Figure:
    order = list(dict.fromkeys(df["month_name"].astype(str).tolist()))
    monthly = df.groupby("month_name", as_index=False)["average_score"].mean()
    monthly["month_name"] = pd.Categorical(monthly["month_name"], categories=order, ordered=True)
    monthly = monthly.sort_values("month_name")
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.plot(monthly["month_name"].astype(str), monthly["average_score"], marker="o", linewidth=2.2)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Average score")
    ax.set_xlabel("")
    ax.grid(alpha=0.22)
    fig.tight_layout()
    return fig


def plot_subjects(df: pd.DataFrame) -> plt.Figure:
    subject = (
        df.groupby("subject", as_index=False)["average_score"]
        .mean()
        .sort_values("average_score")
        .tail(10)
    )
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.barh(subject["subject"], subject["average_score"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Average score")
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    return fig


def plot_attendance_vs_score(summary: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 3.2))
    ax.scatter(summary["attendance_pct"], summary["average_score"], alpha=0.55, s=28)
    ax.axvline(75, linestyle="--", linewidth=1)
    ax.axhline(60, linestyle="--", linewidth=1)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("Attendance %")
    ax.set_ylabel("Average score")
    ax.grid(alpha=0.18)
    fig.tight_layout()
    return fig


def data_quality(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in ["student_id", "student_name", "department", "semester", "average_score", "attendance_pct"]:
        if col in df.columns:
            missing = int(df[col].isna().sum())
            rows.append(
                {
                    "Field": col,
                    "Missing": missing,
                    "Complete %": round((1 - missing / max(len(df), 1)) * 100, 1),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    apply_theme()
    st.markdown(
        """
        <div class="hero">
          <h1>Know Envi • Student Intelligence</h1>
          <p>Free, local-first academic analytics with transparent risk alerts. No paid API, no cloud database, no hidden model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("## Know Envi 2.0")
        st.caption("Portfolio-ready student analytics")
        source = st.radio("Data source", ["Built-in demo", "Upload my data"], index=0)
        uploaded = None
        if source == "Upload my data":
            uploaded = st.file_uploader("CSV, Excel or SQLite", type=["csv", "xlsx", "xls", "db", "sqlite", "sqlite3"])
        st.divider()
        st.caption("Risk alerts are decision support only. They are based on visible attendance and score thresholds.")

    if source == "Upload my data":
        if uploaded is None:
            st.info("Upload a dataset to start. The app accepts common student-data column names and standardizes them automatically.")
            st.stop()
        try:
            frame = standardize_frame(load_upload(uploaded))
        except Exception as exc:
            st.error(f"Could not read the file: {exc}")
            st.stop()
    else:
        frame = standardize_frame(demo_data())

    if frame.empty:
        st.warning("The selected dataset contains no rows.")
        st.stop()

    left, right = st.columns(2)
    with left:
        departments = sorted(frame["department"].dropna().astype(str).unique().tolist())
        selected_depts = st.multiselect("Department", departments, default=departments)
    with right:
        semesters = sorted(frame["semester"].dropna().unique().tolist())
        selected_sems = st.multiselect("Semester", semesters, default=semesters)

    filtered = frame[
        frame["department"].astype(str).isin(selected_depts)
        & frame["semester"].isin(selected_sems)
    ].copy()

    if filtered.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    summary = student_summary(filtered)
    total_students = summary["student_id"].nunique()
    avg_score = summary["average_score"].mean()
    avg_attendance = summary["attendance_pct"].mean()
    high_risk = int((summary["risk_level"] == "High").sum())

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Students", f"{total_students:,}", f"{len(filtered):,} academic records")
    with m2:
        metric_card("Average score", f"{avg_score:.1f}%", "Across current filters")
    with m3:
        metric_card("Attendance", f"{avg_attendance:.1f}%", "Student average")
    with m4:
        metric_card("High-risk alerts", str(high_risk), "Transparent threshold engine")

    tab_overview, tab_risk, tab_student, tab_quality = st.tabs(
        ["Overview", "Risk Monitor", "Student Drill-down", "Data Quality"]
    )

    with tab_overview:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Performance trend")
            st.pyplot(plot_monthly(filtered), use_container_width=True)
        with c2:
            st.subheader("Subject performance")
            st.pyplot(plot_subjects(filtered), use_container_width=True)

        st.subheader("Attendance vs performance")
        st.pyplot(plot_attendance_vs_score(summary), use_container_width=True)

        dept_summary = (
            summary.groupby("department", as_index=False)
            .agg(
                Students=("student_id", "nunique"),
                Score=("average_score", "mean"),
                Attendance=("attendance_pct", "mean"),
                High_Risk=("risk_level", lambda s: int((s == "High").sum())),
            )
        )
        dept_summary["Score"] = dept_summary["Score"].round(1)
        dept_summary["Attendance"] = dept_summary["Attendance"].round(1)
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)

    with tab_risk:
        risk_filter = st.multiselect("Risk level", ["High", "Medium", "Low"], default=["High", "Medium"])
        risk_view = summary[summary["risk_level"].isin(risk_filter)].copy()
        st.dataframe(
            risk_view[
                [
                    "student_id",
                    "student_name",
                    "department",
                    "semester",
                    "average_score",
                    "attendance_pct",
                    "risk_level",
                    "risk_reason",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )
        csv = risk_view.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download risk report (.csv)",
            data=csv,
            file_name="know_envi_risk_report.csv",
            mime="text/csv",
        )

    with tab_student:
        names = summary.apply(lambda r: f"{r['student_name']} • {r['student_id']}", axis=1).tolist()
        selected = st.selectbox("Student", names)
        idx = names.index(selected)
        row = summary.iloc[idx]
        student_rows = filtered[filtered["student_id"] == row["student_id"]].copy()

        a, b, c, d = st.columns(4)
        a.metric("Score", f"{row['average_score']:.1f}%")
        b.metric("Attendance", f"{row['attendance_pct']:.1f}%")
        c.metric("Risk", row["risk_level"])
        d.metric("Records", int(row["records"]))
        st.caption(f"Risk reason: {row['risk_reason']}")

        subject_view = (
            student_rows.groupby("subject", as_index=False)
            .agg(Score=("average_score", "mean"), Attendance=("attendance_pct", "mean"))
        )
        subject_view["Score"] = subject_view["Score"].round(1)
        subject_view["Attendance"] = subject_view["Attendance"].round(1)
        st.dataframe(subject_view, use_container_width=True, hide_index=True)

    with tab_quality:
        st.subheader("Data quality check")
        st.dataframe(data_quality(filtered), use_container_width=True, hide_index=True)
        duplicate_rows = int(filtered.duplicated().sum())
        st.write(f"Duplicate rows: **{duplicate_rows}**")
        st.write(f"Columns detected: **{len(filtered.columns)}**")
        st.write(f"Rows analyzed: **{len(filtered):,}**")
        if source == "Upload my data":
            st.success("Your uploaded file is processed in the running app session. Know Envi does not require a paid external API.")

    st.divider()
    st.caption("Know Envi 2.0 • Python + Streamlit + Pandas + NumPy + Matplotlib • MIT-licensed portfolio project")


if __name__ == "__main__":
    main()
