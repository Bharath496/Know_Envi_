from __future__ import annotations

import calendar
import hashlib
import random
from textwrap import dedent
from datetime import date, datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

from src.student_dashboard_analysis import coerce_numeric_frame, load_table, normalize_columns


st.set_page_config(page_title="Know Envi Student Dashboard", layout="wide", initial_sidebar_state="expanded")
sns.set_theme(style="whitegrid")


DATASET_MAP = {
    "School": {
        "master": Path("data/school_student_master.csv"),
        "records": Path("data/school_academic_records.csv"),
    },
    "College": {
        "master": Path("data/college_student_master.csv"),
        "records": Path("data/college_academic_records.csv"),
    },
}

SCHOOL_COLORS = ["#ff7b54", "#ffd166", "#5b5bd6", "#4cc9f0", "#f94144", "#90be6d"]
COLLEGE_COLORS = ["#5b5bd6", "#ff7b54", "#ffd166", "#4cc9f0", "#f94144", "#8e7dff"]

AUTH_CREDENTIALS = {
    "teacher": {"password": "teacher123", "role": "Teacher"},
    "student": {"password": "student123", "role": "Student"},
}

COLLEGE_DEPARTMENTS = [
    ("Artificial Intelligence and Machine Learning", "BAM"),
    ("Computer Science and Engineering", "CSE"),
    ("Data Science", "DSC"),
    ("Information Technology", "IT"),
    ("Electronics and Communication Engineering", "ECE"),
    ("Mathematics", "MAT"),
    ("Physics", "PHY"),
    ("Chemistry", "CHE"),
]

SCHOOL_TEACHERS = [
    ("Dimitres Viga", "Mathematics"),
    ("Tom Housenburg", "Science"),
    ("Dana Benevista", "Art"),
    ("Salvadore Morbeau", "Biology"),
    ("Maria Historia", "History"),
    ("Jack Sally", "Physics"),
    ("Lula Beatrice", "Computer Science"),
    ("Nella Vita", "English"),
    ("Nadia Laravela", "Programming"),
    ("Dakota Farral", "Science"),
    ("Miranda Adila", "Social Science"),
    ("Indiana Barker", "Biology"),
]

COLLEGE_TEACHERS = [
    ("Dimitres Viga", "Mathematics"),
    ("Tom Housenburg", "Machine Learning"),
    ("Dana Benevista", "AI Fundamentals"),
    ("Salvadore Morbeau", "Data Science"),
    ("Maria Historia", "Research Methods"),
    ("Jack Sally", "Python Programming"),
    ("Lula Beatrice", "Database Systems"),
    ("Nella Vita", "Operating Systems"),
    ("Nadia Laravela", "Programming"),
    ("Dakota Farral", "Cloud Computing"),
    ("Miranda Adila", "Deep Learning"),
    ("Indiana Barker", "NLP"),
]

CITY_POOL = [
    "Coimbatore",
    "Madurai",
    "Chennai",
    "Salem",
    "Tirunelveli",
    "Bengaluru",
    "Mysuru",
    "Hyderabad",
    "Trichy",
    "Erode",
    "Thanjavur",
    "Vellore",
    "Kochi",
    "Mumbai",
    "Pune",
]

PARENT_POOL = [
    "Ravi Kumar",
    "Suresh Babu",
    "Mohan Raj",
    "Vijay Kumar",
    "Anand Kumar",
    "Shankar",
    "Prakash",
    "Karthik",
    "Murugan",
    "Bala",
    "Mani",
    "Selvam",
    "Ramesh",
    "Srinivasan",
    "Gopal",
]

MESSAGES = [
    "Please review the latest assessment update.",
    "Attendance report has been published.",
    "Project submission deadline is tomorrow.",
    "New lab schedule is available.",
    "Parent meeting is scheduled for Friday.",
    "Fee reminder has been generated.",
]


def apply_css() -> None:
    st.markdown(
        """
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stAppViewContainer"] {background: #f4f5ff;}
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #5b47c4 0%, #5143b7 100%);
        }
        [data-testid="stSidebar"] * {color: white;}
        [data-testid="stSidebar"] .stRadio label {padding: 0.28rem 0.1rem;}
        .block-container {padding-top: 1rem; padding-bottom: 1rem;}
        .brand {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin: 0.3rem 0 1.1rem 0;
            font-size: 1.45rem;
            font-weight: 800;
        }
        .brand-badge {
            width: 1.65rem;
            height: 1.65rem;
            border-radius: 0.55rem;
            background: #ff8a65;
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1rem;
        }
        .sidebar-note {
            margin-top: 1.5rem;
            font-size: 0.72rem;
            line-height: 1.4;
            opacity: 0.9;
        }
        .page-title {
            margin: 0;
            font-size: 2rem;
            line-height: 1;
            font-weight: 800;
            color: #223061;
        }
        .page-subtitle {
            margin-top: 0.2rem;
            color: #7b7f9f;
            font-size: 0.95rem;
        }
        .top-user {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            justify-content: flex-end;
        }
        .chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 2rem;
            height: 2rem;
            border-radius: 999px;
            background: #ffffff;
            box-shadow: 0 6px 20px rgba(48, 57, 125, 0.09);
            color: #6e6ef0;
            font-weight: 700;
        }
        .metric-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1rem 1.05rem;
            box-shadow: 0 10px 30px rgba(44, 44, 114, 0.06);
            display: flex;
            align-items: center;
            gap: 0.8rem;
            min-height: 4.2rem;
        }
        .metric-label {
            color: #a1a4c2;
            font-size: 0.78rem;
            margin-bottom: 0.15rem;
        }
        .metric-value {
            color: #223061;
            font-size: 1.45rem;
            font-weight: 800;
            line-height: 1;
        }
        .soft-card-title {
            font-weight: 800;
            color: #26335f;
            margin: 0 0 0.75rem 0;
            font-size: 1rem;
        }
        .soft-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 10px 30px rgba(44, 44, 114, 0.06);
        }
        .right-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1rem 0.95rem 1.1rem 0.95rem;
            box-shadow: 0 10px 30px rgba(44, 44, 114, 0.06);
            margin-bottom: 0.9rem;
        }
        .list-item {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.46rem 0;
            border-bottom: 1px solid #f0f1fb;
        }
        .list-item:last-child { border-bottom: none; }
        .list-name { font-weight: 700; color: #26335f; font-size: 0.86rem; line-height: 1.05; }
        .list-meta { color: #a1a4c2; font-size: 0.74rem; }
        .list-time { color: #a1a4c2; font-size: 0.72rem; }
        .avatar {
            width: 2.2rem;
            height: 2.2rem;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.78rem;
            box-shadow: 0 8px 18px rgba(25, 25, 85, 0.14);
            flex-shrink: 0;
        }
        .mini-avatar {
            width: 1.9rem;
            height: 1.9rem;
            border-radius: 999px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 0.7rem;
            box-shadow: 0 8px 18px rgba(25, 25, 85, 0.14);
            flex-shrink: 0;
        }
        .teacher-card {
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(44, 44, 114, 0.06);
            padding: 1rem;
            text-align: center;
            min-height: 11rem;
        }
        .teacher-name { font-weight: 800; color: #26335f; margin-top: 0.7rem; margin-bottom: 0.1rem; }
        .teacher-subject { color: #a1a4c2; font-size: 0.82rem; margin-bottom: 0.6rem; }
        .pill {
            display: inline-flex;
            align-items: center;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            color: white;
            font-weight: 700;
            font-size: 0.72rem;
        }
        .calendar-wrap, .page-box {
            background: #ffffff;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(44, 44, 114, 0.06);
            padding: 1rem;
        }
        .calendar-head {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            margin-bottom: 0.5rem;
            color: #a1a4c2;
            font-size: 0.72rem;
            text-align: center;
        }
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.45rem;
        }
        .day {
            min-height: 3.1rem;
            border-radius: 10px;
            border: 1px solid #e5e7fa;
            color: #2a3562;
            font-weight: 700;
            font-size: 0.82rem;
            padding: 0.35rem 0.45rem;
            position: relative;
        }
        .day.empty {
            background: #f8f9ff;
            color: #d5d8ed;
        }
        .day.active {
            background: #5b47c4;
            color: white;
            border-color: #5b47c4;
        }
        .day.hot {
            background: linear-gradient(180deg, #ff9a7a, #ff7b54);
            color: white;
            border-color: #ff7b54;
        }
        .day.badge::after {
            content: '';
            width: 0.45rem;
            height: 0.45rem;
            border-radius: 999px;
            background: #ffb703;
            position: absolute;
            right: 0.4rem;
            bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def stable_int(key: str, modulo: int) -> int:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % modulo


def normalize_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    cleaned = coerce_numeric_frame(normalize_columns(df))
    cleaned = cleaned.dropna(how="all").reset_index(drop=True)
    cleaned = cleaned.loc[:, ~cleaned.columns.str.startswith("unnamed")]
    return cleaned


def initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    if not parts:
        return "S"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def pick(pool: list[str], key: str) -> str:
    return pool[stable_int(key, len(pool))]


def load_datasets(mode: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    paths = DATASET_MAP[mode]
    return normalize_frame(load_table(paths["master"])), normalize_frame(load_table(paths["records"]))


def enrich_students(mode: str, master: pd.DataFrame) -> pd.DataFrame:
    df = master.copy()
    if df.empty:
        return df

    if mode == "School":
        roman_map = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}
        if "standard_roman" not in df.columns and "standard" in df.columns:
            df["standard_roman"] = df["standard"].map(roman_map).astype(str)
        df["type_label"] = df.apply(lambda r: f"{r.get('standard_roman', '')} {r.get('section', '')}".strip(), axis=1)
        df["group_label"] = df["type_label"]
    else:
        if "department" not in df.columns:
            df["department"] = COLLEGE_DEPARTMENTS[0][0]
        dept_codes = {name: code for name, code in COLLEGE_DEPARTMENTS}
        if "department_code" not in df.columns:
            df["department_code"] = df["department"].map(dept_codes).fillna("GEN")
        df["type_label"] = df["department"].astype(str)
        df["group_label"] = df.apply(lambda r: f"Sem {int(r.get('semester', 1))} {r.get('section', '')}".strip(), axis=1)

    df["city"] = df["student_id"].apply(lambda sid: pick(CITY_POOL, sid))
    df["parent_name"] = df["student_name"].apply(lambda name: pick(PARENT_POOL, name))
    df["email"] = df["student_name"].str.lower().str.replace(" ", ".", regex=False) + "@mail.com"
    df["avatar_bg"] = df["student_id"].apply(lambda sid: pick(SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS, sid))
    df["avatar"] = df["student_name"].apply(initials)
    df["fee_due"] = df["student_id"].apply(lambda sid: (45000 if mode == "School" else 60000) + stable_int(sid, 45000))
    return df


def score_column(df: pd.DataFrame) -> str | None:
    for candidate in ["average_score", "overall_score", "total50", "total_50"]:
        if candidate in df.columns:
            return candidate
    return None


def monthly_summary(records: pd.DataFrame, score_col: str) -> pd.DataFrame:
    monthly = records.groupby(["month_no", "month_name"], as_index=False)[score_col].mean().sort_values("month_no")
    if monthly.empty:
        return monthly
    monthly["benchmark"] = (monthly[score_col] * 0.9 + np.linspace(5, -2, len(monthly))).clip(0, 100)
    return monthly


def build_teacher_df(mode: str) -> pd.DataFrame:
    roster = SCHOOL_TEACHERS if mode == "School" else COLLEGE_TEACHERS
    rows = []
    colors = SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS
    for idx, (name, subject) in enumerate(roster):
        rows.append(
            {
                "name": name,
                "subject": subject,
                "avatar": initials(name),
                "avatar_bg": colors[idx % len(colors)],
                "email": name.lower().replace(" ", ".") + "@mail.com",
                "phone": f"+91 {random.randint(600, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            }
        )
    return pd.DataFrame(rows)


def build_schedule(mode: str, teachers: pd.DataFrame) -> pd.DataFrame:
    titles = ["Basic Algorithm", "Basic Art", "HTML & CSS Class", "Simple Past Tense"] if mode == "School" else ["Project Review", "Machine Learning Lab", "Database Systems", "NLP Seminar"]
    classes = ["VII-B", "VII-A", "IX", "VII-C"] if mode == "School" else [dept for dept, _ in COLLEGE_DEPARTMENTS[:4]]
    today = datetime.today()
    colors = SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS
    rows = []
    for i, title in enumerate(titles):
        dt = today.replace(day=min(today.day, 28)) + pd.Timedelta(days=i * 2)
        rows.append(
            {
                "title": title,
                "class": classes[i],
                "date": dt.strftime("%d %B %Y"),
                "time": f"{9 + i:02d}:00 - {10 + i:02d}:00 AM",
                "teacher": teachers.iloc[i % len(teachers)]["name"],
                "color": colors[i % len(colors)],
            }
        )
    return pd.DataFrame(rows)


def build_recent_students(perf_students: pd.DataFrame, score_col: str | None) -> pd.DataFrame:
    ordered = perf_students.sort_values(score_col, ascending=False) if score_col and score_col in perf_students.columns else perf_students.copy()
    return ordered.head(5).copy()


def build_messages(recent_students: pd.DataFrame, teachers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i in range(min(4, len(recent_students))):
        student = recent_students.iloc[i]
        teacher = teachers.iloc[i % len(teachers)]
        rows.append(
            {
                "name": student["student_name"],
                "snippet": f"{teacher['name']}: {MESSAGES[i % len(MESSAGES)]}",
                "time": f"{12 + i:02d}:{45 if i % 2 else 15:02d} PM",
                "avatar": student["avatar"],
                "bg": student["avatar_bg"],
            }
        )
    return pd.DataFrame(rows)


def build_fee_table(students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, row in students.head(12).iterrows():
        status = "Complete" if i % 3 == 0 else "Pending" if i % 3 == 1 else "Canceled"
        rows.append(
            {
                "name": row["student_name"],
                "reg_no": row["reg_no"],
                "class_display": row["type_label"],
                "fee": row["fee_due"],
                "status": status,
                "avatar": row["avatar"],
                "bg": row["avatar_bg"],
            }
        )
    return pd.DataFrame(rows)


def build_activity_log(students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for i, row in students.head(6).iterrows():
        rows.append(
            {
                "name": row["student_name"],
                "message": f"{row['type_label']} updated at {9 + i}:00 AM",
                "time": f"{9 + i}:00 AM",
                "avatar": row["avatar"],
                "bg": row["avatar_bg"],
            }
        )
    return pd.DataFrame(rows)


def topbar(title: str) -> None:
    left, center, right = st.columns([1.5, 1.2, 1.1], vertical_alignment="center")
    with left:
        st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
    with center:
        st.text_input("Search", placeholder="Search here...", label_visibility="collapsed")
    with right:
        st.markdown(
            """
            <div class='top-user'>
              <span class='chip'>!</span>
              <span class='chip'>⚙</span>
              <div style='text-align:right; line-height:1.05;'>
                <div style='font-weight:700; color:#4b5476; font-size:0.78rem;'>Nabila A.</div>
                <div style='color:#7b7f9f; font-size:0.72rem;'>Admin</div>
              </div>
              <div class='avatar' style='background:#7c4dff;'>NA</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def metric_card(label: str, value: str, icon: str, bg: str) -> None:
    st.markdown(
        f"""
        <div class='metric-card'>
          <div class='avatar' style='background:{bg}; width:2.45rem; height:2.45rem; font-size:1rem;'>{icon}</div>
          <div>
            <div class='metric-label'>{label}</div>
            <div class='metric-value'>{value}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_row(mode: str, students: pd.DataFrame, teachers: pd.DataFrame, schedule: pd.DataFrame, fee_table: pd.DataFrame) -> None:
    total_due = int(fee_table["fee"].sum()) if not fee_table.empty else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Students", f"{len(students):,}", "A", (SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS)[2])
    with c2:
        metric_card("Teachers", f"{len(teachers):,}", "T", (SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS)[0])
    with c3:
        metric_card("Events", f"{len(schedule):,}", "E", (SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS)[1])
    with c4:
        metric_card("Fees", f"{total_due//1000}k", "₹", (SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS)[3])


def plot_performance_chart(mode: str, monthly: pd.DataFrame, score_col: str) -> None:
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(monthly["month_name"], monthly[score_col], color="#ff7b54", linewidth=2.2, marker="o", markersize=5)
    ax.plot(monthly["month_name"], monthly["benchmark"], color="#ffbf3f", linewidth=2.2, marker="o", markersize=4)
    ax.fill_between(range(len(monthly)), monthly[score_col].values, alpha=0.12, color="#ff7b54")
    ax.set_title(f"{mode} Performance", loc="left", fontsize=11, fontweight="bold", color="#2a3562")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylabel("Score")
    ax.set_xlabel("")
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig, clear_figure=True)


def plot_finance_chart(fee_table: pd.DataFrame) -> None:
    weekly = pd.DataFrame(
        {
            "day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "This Week": [95, 62, 38, 52, 31, 78, 64],
            "Last Week": [72, 48, 34, 41, 27, 68, 55],
        }
    )
    x = np.arange(len(weekly["day"]))
    width = 0.36
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.bar(x - width / 2, weekly["This Week"], width, color="#ff7b54")
    ax.bar(x + width / 2, weekly["Last Week"], width, color="#ffd166")
    ax.set_xticks(x, weekly["day"])
    ax.set_ylim(0, 100)
    ax.grid(axis="y", alpha=0.25)
    ax.set_title("Finance", loc="left", fontsize=11, fontweight="bold", color="#2a3562")
    ax.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig, clear_figure=True)


def render_calendar_card() -> None:
    today = date.today()
    year = today.year
    month = today.month
    month_name = calendar.month_name[month]
    weeks = calendar.monthcalendar(year, month)
    highlight_days = {today.day, min(today.day + 2, 28), min(today.day + 6, 28)}
    weekday_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    head = "".join(f"<div style='text-align:center; font-weight:700;' class='list-meta'>{d}</div>" for d in weekday_names)
    grid = f"<div class='calendar-head'>{head}</div><div class='calendar-grid'>"
    for week in weeks:
        for day in week:
            if day == 0:
                grid += "<div class='day empty'> </div>"
            elif day == today.day:
                grid += f"<div class='day active'>{day}</div>"
            elif day in highlight_days:
                grid += f"<div class='day hot badge'>{day}</div>"
            else:
                grid += f"<div class='day'>{day}</div>"
    grid += "</div>"
    st.markdown(
        f"""
        <div class='calendar-wrap'>
          <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;'>
            <div class='soft-card-title' style='margin:0;'>School Calendar</div>
            <div class='list-meta'>{month_name} {year}</div>
          </div>
          {grid}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recent_students(recent_students: pd.DataFrame) -> None:
    items = ""
    for _, row in recent_students.iterrows():
        items += f"""
<div class='list-item'>
  <div class='mini-avatar' style='background:{row['avatar_bg']}'>{row['avatar']}</div>
  <div style='flex:1; min-width:0;'>
    <div class='list-name'>{row['student_name']}</div>
    <div class='list-meta'>{row['type_label']}</div>
  </div>
  <div class='chip' style='width:1.6rem; height:1.6rem; font-size:0.7rem;'>?</div>
</div>
"""
    st.markdown(
        dedent(f"""
<div class='right-card'>
  <div class='soft-card-title'>Recent Students</div>
  <div class='subtle' style='margin-top:-0.35rem; margin-bottom:0.7rem;'>You have {len(recent_students)} students</div>
  {items}
  <div style='margin-top:0.7rem;'>
    <button style='width:100%; border:none; background:#ebe9ff; color:#5847c4; padding:0.6rem 0.8rem; border-radius:999px; font-weight:700;'>View More</button>
  </div>
</div>
"""),
        unsafe_allow_html=True,
    )
def render_messages(messages: pd.DataFrame) -> None:
    items = ""
    for _, row in messages.iterrows():
        items += f"""
<div class='list-item'>
  <div class='mini-avatar' style='background:{row['bg']}'>{row['avatar']}</div>
  <div style='flex:1; min-width:0;'>
    <div class='list-name'>{row['name']}</div>
    <div class='list-meta'>{row['snippet']}</div>
  </div>
  <div class='list-time'>{row['time']}</div>
</div>
"""
    st.markdown(
        dedent(f"""
<div class='right-card'>
  <div class='soft-card-title'>Messages</div>
  {items}
  <div style='margin-top:0.7rem;'>
    <button style='width:100%; border:none; background:#ebe9ff; color:#5847c4; padding:0.6rem 0.8rem; border-radius:999px; font-weight:700;'>View More</button>
  </div>
</div>
"""),
        unsafe_allow_html=True,
    )
def render_upcoming_cards(mode: str, schedule: pd.DataFrame) -> None:
    title = "Current Courses" if mode == "College" else "Current Activities"
    items = ""
    colors = SCHOOL_COLORS if mode == "School" else COLLEGE_COLORS
    for i, (_, row) in enumerate(schedule.iterrows()):
        items += f"""
<div style='display:flex; gap:0.75rem; align-items:center; background:#fff; border-radius:14px; padding:0.65rem; box-shadow:0 10px 30px rgba(44,44,114,0.06); margin-bottom:0.75rem; border-left:6px solid {row['color']};'>
  <div class='avatar' style='background:{colors[i % len(colors)]}; width:2.45rem; height:2.45rem; font-size:0.82rem;'>{initials(row['title'])[:2]}</div>
  <div style='min-width:0;'>
    <div class='list-name'>{row['title']}</div>
    <div class='list-meta'>{row['class']}</div>
    <div class='list-meta'>{row['date']} ? {row['time']}</div>
  </div>
</div>
"""
    st.markdown(
        dedent(f"""
<div class='right-card'>
  <div class='soft-card-title'>{title}</div>
  {items}
  <div style='margin-top:0.7rem;'>
    <button style='width:100%; border:none; background:#ebe9ff; color:#5847c4; padding:0.6rem 0.8rem; border-radius:999px; font-weight:700;'>View More</button>
  </div>
</div>
"""),
        unsafe_allow_html=True,
    )
def render_fee_table(fee_table: pd.DataFrame, mode: str) -> None:
    st.markdown("<div class='soft-card-title'>Fee Status</div>", unsafe_allow_html=True)
    class_label = "Class" if mode == "School" else "Department"
    display = fee_table.rename(
        columns={
            "name": "Student",
            "reg_no": "ID",
            "class_display": class_label,
            "fee": "Fee Due",
            "status": "Status",
        }
    )[["Student", "ID", class_label, "Fee Due", "Status"]]
    st.dataframe(display, use_container_width=True, hide_index=True, height=300)


def is_teacher_user() -> bool:
    return st.session_state.get("auth_role") == "Teacher" and bool(st.session_state.get("auth_ok"))


def sidebar_login() -> None:
    st.markdown("<div class='soft-card-title'>Login</div>", unsafe_allow_html=True)
    username = st.text_input("Username", key="login_username", placeholder="teacher or student")
    password = st.text_input("Password", key="login_password", type="password", placeholder="Enter password")
    role = st.radio("Role", ["Teacher", "Student"], horizontal=True, key="login_role")
    login_col, logout_col = st.columns(2)
    with login_col:
        if st.button("Login", use_container_width=True):
            record = AUTH_CREDENTIALS.get(username.strip().lower())
            if record and record["password"] == password and record["role"] == role:
                st.session_state["auth_ok"] = True
                st.session_state["auth_role"] = role
                st.success(f"Logged in as {role}.")
            else:
                st.session_state["auth_ok"] = False
                st.session_state["auth_role"] = "Guest"
                st.error("Invalid credentials.")
    with logout_col:
        if st.button("Logout", use_container_width=True):
            st.session_state["auth_ok"] = False
            st.session_state["auth_role"] = "Guest"
            st.info("Logged out.")
    current = st.session_state.get("auth_role", "Guest")
    st.caption(f"Current role: {current}")


def dashboard_page(mode: str, students: pd.DataFrame, records: pd.DataFrame, score_col: str) -> None:
    teachers = build_teacher_df(mode)
    schedule = build_schedule(mode, teachers)
    fee_table = build_fee_table(students)
    perf_students = students.copy()
    if score_col in records.columns:
        perf_students = perf_students.merge(records.groupby("student_id", as_index=False)[score_col].mean(), on="student_id", how="left")
    recent_students = build_recent_students(perf_students, score_col)
    messages = build_messages(recent_students, teachers)
    monthly = monthly_summary(records, score_col)

    topbar("Dashboard")
    render_metric_row(mode, students, teachers, schedule, fee_table)
    st.write("")

    left, right = st.columns([2.7, 1.2], gap="large")
    with left:
        st.markdown(f"<div class='soft-card-title'>{mode} Performance</div>", unsafe_allow_html=True)
        plot_performance_chart(mode, monthly, score_col)
        st.write("")
        c1, c2 = st.columns([1, 1], gap="large")
        with c1:
            render_calendar_card()
        with c2:
            st.markdown(f"<div class='soft-card-title'>{mode} Finance</div>", unsafe_allow_html=True)
            plot_finance_chart(fee_table)
    with right:
        render_recent_students(recent_students)
        render_messages(messages)
        render_upcoming_cards(mode, schedule)


def students_page(mode: str, students: pd.DataFrame) -> None:
    topbar("Students")
    c1, c2 = st.columns([1.4, 0.7], gap="large")
    with c1:
        st.text_input("Search students", placeholder="Search here...", label_visibility="collapsed")
    with c2:
        sort = st.selectbox("", ["Newest", "Oldest", "Name"], label_visibility="collapsed")

    student_rows = students.sort_values("student_id", ascending=(sort == "Oldest"))
    if sort == "Name":
        student_rows = student_rows.sort_values("student_name")

    if mode == "School":
        table = student_rows[["student_name", "reg_no", "admission_no", "date_of_birth", "parent_name", "city", "phone_number", "blood_group", "email", "type_label"]].rename(
            columns={
                "student_name": "Name",
                "reg_no": "ID",
                "admission_no": "Admission No",
                "date_of_birth": "Date",
                "parent_name": "Parent Name",
                "city": "City",
                "phone_number": "Contact",
                "blood_group": "Blood Group",
                "email": "Email",
                "type_label": "Class",
            }
        )
    else:
        table = student_rows[["student_name", "reg_no", "admission_no", "date_of_birth", "parent_name", "city", "phone_number", "blood_group", "email", "type_label", "semester"]].rename(
            columns={
                "student_name": "Name",
                "reg_no": "ID",
                "admission_no": "Admission No",
                "date_of_birth": "Date",
                "parent_name": "Parent Name",
                "city": "City",
                "phone_number": "Contact",
                "blood_group": "Blood Group",
                "email": "Email",
                "type_label": "Department",
                "semester": "Semester",
            }
        )
        table["Semester"] = table["Semester"].apply(lambda value: f"Sem {int(value)}")
    st.markdown("<div class='soft-card-title'>Student Records</div>", unsafe_allow_html=True)
    st.dataframe(table.head(30), use_container_width=True, hide_index=True, height=520)


def add_student_page() -> None:
    topbar("Add New Student")
    with st.form("student_form"):
        st.markdown("<div class='soft-card-title'>Student Details</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([0.8, 1.4, 1.4], gap="large")
        with c1:
            st.file_uploader("Photo", label_visibility="visible")
            st.text_input("Photo Link", placeholder="Drag and drop or click here to select file")
        with c2:
            st.text_input("First Name", placeholder="Samantha")
            st.date_input("Date & Place of Birth", value=date(2007, 2, 24))
            st.text_input("Email", placeholder="william@gmail.com")
            st.text_area("Address", placeholder="Enter address here")
        with c3:
            st.text_input("Last Name", placeholder="William")
            st.text_input("Parent Name", placeholder="Mona William")
            st.text_input("Phone", placeholder="+1234567890")
            st.text_input("City", placeholder="Jakarta")

        st.write("")
        st.markdown("<div class='soft-card-title'>Parent Details</div>", unsafe_allow_html=True)
        p1, p2 = st.columns(2, gap="large")
        with p1:
            st.text_input("Parent First Name", placeholder="Mona")
            st.text_input("Parent Email", placeholder="parent@mail.com")
            st.text_area("Parent Address", placeholder="Parent address")
        with p2:
            st.text_input("Parent Last Name", placeholder="William")
            st.text_input("Parent Phone", placeholder="+1234567890")
            st.radio("Payments", ["Cash", "Debit"], horizontal=True)
        if st.form_submit_button("Submit"):
            st.success("Student form submitted.")


def teachers_page(mode: str) -> None:
    topbar("Teachers")
    teachers = build_teacher_df(mode)
    students, _records = load_datasets(mode)
    students = enrich_students(mode, students)
    fee_table = build_fee_table(students)
    c1, c2 = st.columns([1.4, 0.7], gap="large")
    with c1:
        st.text_input("Search teachers", placeholder="Search here...", label_visibility="collapsed")
    with c2:
        st.selectbox("", ["Newest", "Name"], label_visibility="collapsed")

    for row_idx in range(0, len(teachers), 4):
        cols = st.columns(4, gap="large")
        for i, (_, teacher) in enumerate(teachers.iloc[row_idx : row_idx + 4].iterrows()):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class='teacher-card'>
                      <div class='avatar' style='background:{teacher['avatar_bg']}; width:4.2rem; height:4.2rem; font-size:1.25rem; margin:0 auto;'>{teacher['avatar']}</div>
                      <div class='teacher-name'>{teacher['name']}</div>
                      <div class='teacher-subject'>{teacher['subject']}</div>
                      <div style='display:flex; justify-content:center; gap:0.45rem;'>
                        <div class='chip' style='width:1.8rem; height:1.8rem; font-size:0.7rem;'>TEL</div>
                        <div class='chip' style='width:1.8rem; height:1.8rem; font-size:0.7rem;'>MAIL</div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    if is_teacher_user():
        st.write("")
        st.markdown("<div class='soft-card-title'>Fee Status</div>", unsafe_allow_html=True)
        render_fee_table(fee_table.head(12), mode)
    else:
        st.info("Fee structure is visible to teachers only. Log in as a teacher to view it.")


def teacher_details_page(mode: str) -> None:
    topbar("Teacher Details")
    teachers = build_teacher_df(mode)
    teacher = teachers.iloc[4]
    schedule = build_schedule(mode, teachers)
    left, right = st.columns([2.2, 1], gap="large")
    with left:
        st.markdown(
            f"""
            <div style='background:#ffffff; border-radius:16px; box-shadow:0 10px 30px rgba(44,44,114,0.06); overflow:hidden;'>
              <div style='background:#5b47c4; height:5rem; position:relative;'>
                <div class='avatar' style='background:#2f2f88; width:5.1rem; height:5.1rem; font-size:1.15rem; position:absolute; left:1rem; top:1.2rem; border:4px solid white;'>{teacher['avatar']}</div>
              </div>
              <div style='padding:4.5rem 1rem 1rem 1rem;'>
                <div class='page-title' style='font-size:1.55rem; margin-bottom:0.15rem;'>{teacher['name']}</div>
                <div class='page-subtitle'>{teacher['subject']} Teacher</div>
                <div style='display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0;'>
                  <div class='pill' style='background:#ff7b54;'>Jakarta, Indonesia</div>
                  <div class='pill' style='background:#ff8a65;'>{teacher['phone']}</div>
                  <div class='pill' style='background:#ffb703;'>{teacher['email']}</div>
                </div>
                <div class='soft-card-title'>About:</div>
                <div class='list-meta'>Experienced educator focused on classroom engagement, student support, and practical assessments.</div>
                <div class='soft-card-title' style='margin-top:1rem;'>Education:</div>
                <ul class='list-meta'>
                  <li>Know Envi University</li>
                  <li>Master of Education</li>
                </ul>
                <div class='soft-card-title' style='margin-top:1rem;'>Expertise:</div>
                <div class='list-meta'>{teacher['subject']}, classroom mentoring, student assessment, analytics</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='right-card'><div class='soft-card-title'>Schedule Details</div><div class='list-meta'>Thursday, 10th April, 2021</div></div>", unsafe_allow_html=True)
        for _, item in schedule.iterrows():
            st.markdown(
                f"""
                <div class='right-card' style='border-left:6px solid {item['color']};'>
                  <div class='list-name'>{item['title']}</div>
                  <div class='list-meta'>{item['class']}</div>
                  <div class='list-meta' style='margin-top:0.35rem;'>{item['date']}</div>
                  <div class='list-meta'>{item['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def student_details_page(mode: str, students: pd.DataFrame, records: pd.DataFrame) -> None:
    topbar("Student Details")
    selected = st.selectbox("Student", students["student_name"].tolist(), label_visibility="collapsed")
    row = students.loc[students["student_name"] == selected].iloc[0]
    student_records = records.loc[records["student_id"] == row["student_id"]].copy()
    avg_attendance = float(student_records["attendance_pct"].mean()) if "attendance_pct" in student_records.columns and not student_records.empty else None
    student_score_col = score_column(student_records)
    avg_score = float(student_records[student_score_col].mean()) if student_score_col and not student_records.empty else None
    avg_score_text = f"{avg_score:.2f}" if avg_score is not None else "N/A"
    avg_attendance_text = f"{avg_attendance:.2f}%" if avg_attendance is not None else "N/A"
    schedule = build_schedule(mode, build_teacher_df(mode))
    left, right = st.columns([2.2, 1], gap="large")
    with left:
        st.markdown(
            f"""
            <div style='background:#ffffff; border-radius:16px; box-shadow:0 10px 30px rgba(44,44,114,0.06); overflow:hidden;'>
              <div style='background:#5b47c4; height:5rem; position:relative;'>
                <div style='width:4.5rem; height:4.5rem; border-radius:999px; background:{row['avatar_bg']}; color:white; display:flex; align-items:center; justify-content:center; font-size:1.05rem; font-weight:800; position:absolute; left:1rem; top:1.1rem; border:4px solid white;'>{row['avatar']}</div>
                <div style='position:absolute; right:1.15rem; top:1.5rem; color:white; opacity:0.85;'>...</div>
              </div>
              <div style='padding:4.2rem 1rem 1rem 1rem;'>
                <div class='page-title' style='font-size:1.45rem; margin-bottom:0.15rem;'>{row['student_name']}</div>
                <div class='page-subtitle'>{row['type_label']}</div>
                <div style='display:flex; gap:1rem; flex-wrap:wrap; margin:1rem 0;'>
                  <div class='pill' style='background:#ff7b54;'>Parent: {row['parent_name']}</div>
                  <div class='pill' style='background:#ff8a65;'>City: {row['city']}</div>
                  <div class='pill' style='background:#ffb703;'>Phone: {row['phone_number']}</div>
                  <div class='pill' style='background:#5b5bd6;'>Mail: {row['email']}</div>
                </div>
                <div style='display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:0.6rem; margin-bottom:0.8rem;'>
                  <div class='list-item' style='margin:0;'><div><div class='list-name'>Admission No</div><div class='list-meta'>{row.get('admission_no', row['student_id'])}</div></div></div>
                  <div class='list-item' style='margin:0;'><div><div class='list-name'>Blood Group</div><div class='list-meta'>{row.get('blood_group', 'N/A')}</div></div></div>
                  <div class='list-item' style='margin:0;'><div><div class='list-name'>Guardian</div><div class='list-meta'>{row.get('guardian_name', 'N/A')}</div></div></div>
                  <div class='list-item' style='margin:0;'><div><div class='list-name'>Admission Year</div><div class='list-meta'>{row.get('admission_year', 'N/A')}</div></div></div>
                </div>
                <div class='soft-card-title'>Address:</div>
                <div class='list-meta'>{row.get('address', 'N/A')}</div>
                <div class='soft-card-title'>About:</div>
                <div class='list-meta'>A student profile card showing basic identity, contact, and academic grouping information.</div>
                <div class='soft-card-title' style='margin-top:1rem;'>Education:</div>
                <ul class='list-meta'>
                  <li>{row.get('department', 'School Curriculum')}</li>
                  <li>{row['group_label']}</li>
                </ul>
                <div class='soft-card-title' style='margin-top:1rem;'>Academic Snapshot:</div>
                <ul class='list-meta'>
                  <li>Average score: {avg_score_text}</li>
                  <li>Attendance: {avg_attendance_text}</li>
                </ul>
                <div class='soft-card-title' style='margin-top:1rem;'>Expertise:</div>
                <div class='list-meta'>Assignments, assessments, attendance review, and academic progress tracking.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='right-card'><div class='soft-card-title'>Schedule Details</div><div class='list-meta'>Thursday, 10th April, 2021</div></div>", unsafe_allow_html=True)
        for _, item in schedule.iterrows():
            st.markdown(
                f"""
                <div class='right-card' style='border-left:6px solid {item['color']};'>
                  <div class='list-name'>{item['title']}</div>
                  <div class='list-meta'>{item['class']}</div>
                  <div class='list-meta' style='margin-top:0.35rem;'>{item['date']}</div>
                  <div class='list-meta'>{item['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def event_page(mode: str) -> None:
    topbar("Events")
    teachers = build_teacher_df(mode)
    schedule = build_schedule(mode, teachers)
    left, right = st.columns([2.2, 1], gap="large")
    with left:
        st.markdown(
            """
            <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:0.8rem;'>
              <div class='soft-card-title' style='margin:0;'>Calendar</div>
              <div style='display:flex; gap:0.5rem;'>
                <div class='pill' style='background:#ffffff; color:#5b47c4; border:1px solid #cfcdf5;'>January</div>
                <div class='pill' style='background:#ffffff; color:#5b47c4; border:1px solid #cfcdf5;'>2021</div>
                <div class='pill' style='background:#5b47c4;'>+ New Student</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_calendar_card()
    with right:
        st.markdown("<div class='right-card'><div class='soft-card-title'>Schedule Details</div><div class='list-meta'>Thursday, 10th April, 2021</div></div>", unsafe_allow_html=True)
        for _, item in schedule.iterrows():
            st.markdown(
                f"""
                <div class='right-card' style='border-left:6px solid {item['color']};'>
                  <div class='list-name'>{item['title']}</div>
                  <div class='list-meta'>{item['class']}</div>
                  <div class='list-meta' style='margin-top:0.35rem;'>{item['date']}</div>
                  <div class='list-meta'>{item['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def finance_page(mode: str, students: pd.DataFrame) -> None:
    topbar("Finance")
    fee_table = build_fee_table(students)
    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        st.markdown("<div class='soft-card-title'>Fee Summary</div>", unsafe_allow_html=True)
        plot_finance_chart(fee_table)
    with c2:
        if is_teacher_user():
            render_fee_table(fee_table, mode)
        else:
            st.info("Fee structure is visible to teachers only. Log in as a teacher to view it.")


def simple_list_page(title: str, mode: str, students: pd.DataFrame) -> None:
    topbar(title)
    st.markdown("<div class='soft-card-title'>Activity Feed</div>", unsafe_allow_html=True)
    if title == "User":
        for _, row in students.head(8).iterrows():
            st.markdown(
                f"""
                <div class='list-item'>
                  <div class='mini-avatar' style='background:{row['avatar_bg']}'>{row['avatar']}</div>
                  <div style='flex:1'>
                    <div class='list-name'>{row['student_name']}</div>
                    <div class='list-meta'>{row['reg_no']} · {row['type_label']}</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif title == "Chat":
        teachers = build_teacher_df(mode)
        msgs = build_messages(build_recent_students(students, None), teachers)
        render_messages(msgs)
    else:
        for _, row in build_activity_log(students).iterrows():
            st.markdown(
                f"""
                <div class='list-item'>
                  <div class='mini-avatar' style='background:{row['bg']}'>{row['avatar']}</div>
                  <div style='flex:1'>
                    <div class='list-name'>{row['name']}</div>
                    <div class='list-meta'>{row['message']}</div>
                  </div>
                  <div class='list-time'>{row['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def sidebar(default_mode: str) -> tuple[str, str]:
    with st.sidebar:
        st.markdown(
            """
            <div class='brand'>
              <span class='brand-badge'>K</span>
              <span>Know Envi</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if "auth_ok" not in st.session_state:
            st.session_state["auth_ok"] = False
        if "auth_role" not in st.session_state:
            st.session_state["auth_role"] = "Guest"
        sidebar_login()
        st.markdown("<hr style='border:0; border-top:1px solid rgba(255,255,255,0.2); margin:1rem 0;'>", unsafe_allow_html=True)
        institution = st.radio("Institution", ["School", "College"], index=0 if default_mode == "School" else 1)
        page = st.radio(
            "Menu",
            [
                "Dashboard",
                "Students",
                "Teachers",
                "Event",
                "Finance",
                "User",
                "Chat",
                "Latest Activity",
                "Add New Student",
                "Add New Teacher",
                "Student Details",
                "Teacher Details",
            ],
            index=0,
        )
        st.markdown(
            """
            <div class='sidebar-note'>
              Know Envi - Student Analytics Dashboard<br/>
              Made with by Peterdraw
            </div>
            """,
            unsafe_allow_html=True,
        )
        return institution, page


def add_teacher_page() -> None:
    topbar("Add New Teacher")
    st.markdown("<div class='soft-card-title'>Personal Details</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.text_input("First Name", placeholder="Maria")
        st.text_input("Email", placeholder="hitoria@gmail.com")
        st.text_area("Address", placeholder="Lorem ipsum dolor sit amet")
        st.date_input("Date of Birth", value=date(1997, 2, 24))
    with c2:
        st.text_input("Last Name", placeholder="Historia")
        st.text_input("Phone", placeholder="+1234567890")
        st.file_uploader("Photo", label_visibility="visible")
        st.text_input("Place of Birth", placeholder="Jakarta, Indonesia")

    st.write("")
    st.markdown("<div class='soft-card-title'>Education</div>", unsafe_allow_html=True)
    e1, e2 = st.columns(2, gap="large")
    with e1:
        st.text_input("University", placeholder="Know Envi University")
        st.text_input("Start Date", placeholder="September 2013")
    with e2:
        st.text_input("Degree", placeholder="History Major")
        st.text_input("End Date", placeholder="September 2017")


def main() -> None:
    apply_css()
    institution, page = sidebar("School")
    master, records = load_datasets(institution)
    students = enrich_students(institution, master)
    score_col = score_column(records) or "average_score"

    if page == "Dashboard":
        dashboard_page(institution, students, records, score_col)
    elif page == "Students":
        students_page(institution, students)
    elif page == "Teachers":
        teachers_page(institution)
    elif page == "Event":
        event_page(institution)
    elif page == "Finance":
        finance_page(institution, students)
    elif page == "User":
        simple_list_page("User", institution, students)
    elif page == "Chat":
        simple_list_page("Chat", institution, students)
    elif page == "Latest Activity":
        simple_list_page("Latest Activity", institution, students)
    elif page == "Add New Student":
        add_student_page()
    elif page == "Add New Teacher":
        add_teacher_page()
    elif page == "Student Details":
        student_details_page(institution, students, records)
    elif page == "Teacher Details":
        teacher_details_page(institution)


if __name__ == "__main__":
    main()
