from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


SEED = 42
random.seed(SEED)
np.random.seed(SEED)

ACADEMIC_MONTHS = [
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
]

INDIAN_CITIES = [
    ("Chennai", "Tamil Nadu", "600001"),
    ("Coimbatore", "Tamil Nadu", "641001"),
    ("Madurai", "Tamil Nadu", "625001"),
    ("Salem", "Tamil Nadu", "636001"),
    ("Tirunelveli", "Tamil Nadu", "627001"),
    ("Trichy", "Tamil Nadu", "620001"),
    ("Erode", "Tamil Nadu", "638001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("Mysuru", "Karnataka", "570001"),
    ("Hyderabad", "Telangana", "500001"),
    ("Kochi", "Kerala", "682001"),
    ("Mumbai", "Maharashtra", "400001"),
    ("Pune", "Maharashtra", "411001"),
    ("Vellore", "Tamil Nadu", "632001"),
    ("Thanjavur", "Tamil Nadu", "613001"),
]

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

SCHOOL_SUBJECTS = [
    "Tamil",
    "English",
    "Mathematics",
    "Science",
    "Social Science",
    "Computer Science",
]

COLLEGE_SUBJECTS: dict[int, list[str]] = {
    1: ["Communicative English", "Mathematics I", "Programming Fundamentals"],
    2: ["Mathematics II", "C Programming", "Digital Logic"],
    3: ["Data Structures", "Object Oriented Programming", "Statistics", "Database Fundamentals"],
    4: ["Python Programming", "Computer Organization", "Operating Systems", "Discrete Mathematics"],
    5: ["Machine Learning Basics", "Software Engineering", "Probability & Statistics", "Web Technologies", "Data Visualization"],
    6: ["Artificial Intelligence", "Deep Learning", "Big Data Analytics", "Cloud Computing", "Natural Language Processing"],
    7: ["MLOps", "Advanced Machine Learning", "Research Methods", "Mobile Computing", "Project Work", "Seminar"],
    8: ["Capstone Project", "Model Deployment", "Optimization Techniques", "AI Ethics", "Internship", "Industry Project"],
}

FIRST_NAMES = [
    "Aarav",
    "Aadhya",
    "Aanya",
    "Abhinav",
    "Aditya",
    "Akash",
    "Akhil",
    "Aman",
    "Amit",
    "Ananya",
    "Aniket",
    "Arjun",
    "Arya",
    "Dev",
    "Dhruv",
    "Divya",
    "Gauri",
    "Hari",
    "Harsh",
    "Isha",
    "Ishaan",
    "Kabir",
    "Karthik",
    "Kavya",
    "Krishna",
    "Meera",
    "Mohan",
    "Nandini",
    "Neha",
    "Nikhil",
    "Pooja",
    "Pranav",
    "Priya",
    "Rahul",
    "Riya",
    "Rohan",
    "Sahana",
    "Sakshi",
    "Sanjay",
    "Sanjana",
    "Shreya",
    "Siddharth",
    "Sneha",
    "Suresh",
    "Tanvi",
    "Varun",
    "Vidya",
    "Vikram",
    "Yash",
    "Zoya",
]

MIDDLE_NAMES = [
    "Kumar",
    "Kumari",
    "Singh",
    "Sivam",
    "Shiv",
    "Kiran",
    "Karthik",
    "Anand",
    "Babu",
    "Prasad",
    "Ravi",
    "Sai",
    "Sri",
    "Vijay",
    "Mohan",
    "Devi",
]

LAST_NAMES = [
    "R",
    "S",
    "K",
    "P",
    "M",
    "B",
    "V",
    "N",
    "T",
    "H",
    "G",
    "A",
    "D",
    "I",
    "J",
    "Khan",
    "Patel",
    "Sharma",
    "Verma",
    "Gupta",
    "Singh",
    "Reddy",
    "Nair",
    "Iyer",
    "Das",
    "Mishra",
    "Joshi",
    "Bhat",
    "Mehta",
    "Malik",
]

ROMAN_MAP = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
}

COLLEGE_SHORT = "RCAS"
COLLEGE_YEAR = "24"
ACADEMIC_YEAR = "2025-2026"

COLLEGE_DEPARTMENTS: list[tuple[str, str]] = [
    ("Artificial Intelligence and Machine Learning", "BAM"),
    ("Computer Science and Engineering", "CSE"),
    ("Data Science", "DSC"),
    ("Information Technology", "IT"),
    ("Electronics and Communication Engineering", "ECE"),
    ("Mathematics", "MAT"),
    ("Physics", "PHY"),
    ("Chemistry", "CHE"),
]

HOUSE_NAMES = ["Red", "Blue", "Green", "Yellow"]
EMAIL_DOMAINS = ["mail.com", "gmail.com", "college.edu.in", "school.edu.in"]


@dataclass(frozen=True)
class SchoolProfile:
    student_id: str
    admission_no: str
    reg_no: str
    student_name: str
    phone_number: str
    gender: str
    guardian_name: str
    father_name: str
    mother_name: str
    blood_group: str
    email: str
    address: str
    city: str
    state: str
    pincode: str
    house: str
    admission_year: int
    standard: int
    standard_roman: str
    section: str
    date_of_birth: str


@dataclass(frozen=True)
class CollegeProfile:
    student_id: str
    admission_no: str
    reg_no: str
    student_name: str
    phone_number: str
    gender: str
    guardian_name: str
    father_name: str
    mother_name: str
    blood_group: str
    email: str
    address: str
    city: str
    state: str
    pincode: str
    department: str
    department_code: str
    semester: int
    section: str
    admission_year: int
    date_of_birth: str


def bounded_int(value: float, lower: int, upper: int) -> int:
    return int(np.clip(np.rint(value), lower, upper))


def build_unique_names(count: int) -> list[str]:
    pool: set[str] = set()
    names: list[str] = []

    candidates: list[str] = []
    for first in FIRST_NAMES:
        for middle in MIDDLE_NAMES:
            for last in LAST_NAMES:
                candidates.append(f"{first} {middle} {last}")
                candidates.append(f"{first} {last}")
                candidates.append(f"{first} {middle}")

    random.shuffle(candidates)

    for name in candidates:
        normalized = " ".join(name.split())
        if normalized not in pool:
            pool.add(normalized)
            names.append(normalized)
        if len(names) == count:
            return names

    suffix = 1
    while len(names) < count:
        base = candidates[len(names) % len(candidates)]
        candidate = f"{base} {suffix}"
        if candidate not in pool:
            pool.add(candidate)
            names.append(candidate)
        suffix += 1

    return names


def make_school_student_id(index: int) -> str:
    return f"SCH{index:04d}"


def make_college_student_id(index: int) -> str:
    return f"COL{index:05d}"


def make_college_reg_no(index: int, department_code: str) -> str:
    serial = f"{index:03d}" if index < 1000 else f"{index:04d}"
    return f"{COLLEGE_SHORT}{COLLEGE_YEAR}{department_code}{serial}"


def make_school_reg_no(standard: int, roll_no: int) -> str:
    return f"{ROMAN_MAP[standard]}{roll_no}"


def make_admission_no(prefix: str, year: int, index: int) -> str:
    return f"{prefix}{year}{index:04d}"


def make_email(name: str, index: int, school: bool) -> str:
    handle = "".join(ch.lower() for ch in name if ch.isalnum() or ch == " ").replace(" ", ".")
    domain = EMAIL_DOMAINS[index % len(EMAIL_DOMAINS)] if school else EMAIL_DOMAINS[(index + 1) % len(EMAIL_DOMAINS)]
    return f"{handle}{index % 97 + 3}@{domain}"


def address_for(index: int, city: str, state: str, pincode: str) -> str:
    street_no = 10 + (index % 80)
    lane = ["Main Road", "Lake View", "Temple Street", "Market Road", "MG Road"][index % 5]
    return f"{street_no}, {lane}, {city}, {state} - {pincode}"


def build_school_profiles(count: int = 500) -> list[SchoolProfile]:
    names = build_unique_names(count)
    phones = random.sample(range(6000000000, 10000000000), count)
    genders = np.random.choice(["Female", "Male"], size=count, p=[0.48, 0.52])
    standards = np.repeat(np.arange(1, 13), math.ceil(count / 12))[:count]
    np.random.shuffle(standards)
    sections = np.random.choice(["A", "B", "C", "D"], size=count)
    city_rows = (INDIAN_CITIES * math.ceil(count / len(INDIAN_CITIES)))[:count]
    np.random.shuffle(city_rows)

    roll_counters = {standard: 0 for standard in range(1, 13)}
    profiles: list[SchoolProfile] = []

    for idx in range(count):
        standard = int(standards[idx])
        roll_counters[standard] += 1
        roll_no = roll_counters[standard]
        city, state, pincode = city_rows[idx]
        admission_year = random.randint(2018, 2025)
        year = random.randint(2010, 2016)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        student_name = names[idx]
        profiles.append(
            SchoolProfile(
                student_id=make_school_student_id(idx + 1),
                admission_no=make_admission_no("SCHADM", admission_year, idx + 1),
                reg_no=make_school_reg_no(standard, roll_no),
                student_name=student_name,
                phone_number=str(phones[idx]),
                gender=str(genders[idx]),
                guardian_name=random.choice([f"Mr. {student_name.split()[0]}", f"Mrs. {student_name.split()[0]}", f"{student_name.split()[0]} Family"]),
                father_name=random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
                mother_name=random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
                blood_group=random.choice(BLOOD_GROUPS),
                email=make_email(student_name, idx + 1, school=True),
                address=address_for(idx + 1, city, state, pincode),
                city=city,
                state=state,
                pincode=pincode,
                house=random.choice(HOUSE_NAMES),
                admission_year=admission_year,
                standard=standard,
                standard_roman=ROMAN_MAP[standard],
                section=str(sections[idx]),
                date_of_birth=f"{year:04d}-{month:02d}-{day:02d}",
            )
        )

    return profiles


def build_college_profiles(count: int = 3000) -> list[CollegeProfile]:
    names = build_unique_names(count)
    phones = random.sample(range(6000000000, 10000000000), count)
    genders = np.random.choice(["Female", "Male"], size=count, p=[0.49, 0.51])
    semesters = np.repeat(np.arange(1, 9), math.ceil(count / 8))[:count]
    np.random.shuffle(semesters)
    sections = np.random.choice(["A", "B", "C", "D"], size=count)
    department_names = np.repeat([name for name, _ in COLLEGE_DEPARTMENTS], math.ceil(count / len(COLLEGE_DEPARTMENTS)))[:count]
    np.random.shuffle(department_names)
    department_codes = {name: code for name, code in COLLEGE_DEPARTMENTS}
    department_counters = {name: 0 for name, _ in COLLEGE_DEPARTMENTS}
    city_rows = (INDIAN_CITIES * math.ceil(count / len(INDIAN_CITIES)))[:count]
    np.random.shuffle(city_rows)

    profiles: list[CollegeProfile] = []
    for idx in range(count):
        department = str(department_names[idx])
        department_counters[department] += 1
        department_code = department_codes[department]
        city, state, pincode = city_rows[idx]
        admission_year = random.randint(2021, 2025)
        year = random.randint(2004, 2008)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        student_name = names[idx]
        profiles.append(
            CollegeProfile(
                student_id=make_college_student_id(idx + 1),
                admission_no=make_admission_no("COLADM", admission_year, idx + 1),
                reg_no=make_college_reg_no(department_counters[department], department_code),
                student_name=student_name,
                phone_number=str(phones[idx]),
                gender=str(genders[idx]),
                guardian_name=random.choice([f"Mr. {student_name.split()[0]}", f"Mrs. {student_name.split()[0]}", f"{student_name.split()[0]} Family"]),
                father_name=random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
                mother_name=random.choice(FIRST_NAMES) + " " + random.choice(LAST_NAMES),
                blood_group=random.choice(BLOOD_GROUPS),
                email=make_email(student_name, idx + 1, school=False),
                address=address_for(idx + 1, city, state, pincode),
                city=city,
                state=state,
                pincode=pincode,
                department=department,
                department_code=department_code,
                semester=int(semesters[idx]),
                section=str(sections[idx]),
                admission_year=admission_year,
                date_of_birth=f"{year:04d}-{month:02d}-{day:02d}",
            )
        )
    return profiles


def school_subjects() -> list[str]:
    return SCHOOL_SUBJECTS


def college_subjects(semester: int) -> list[str]:
    if semester <= 2:
        return COLLEGE_SUBJECTS[semester]
    if semester <= 4:
        return COLLEGE_SUBJECTS[semester]
    if semester <= 6:
        return COLLEGE_SUBJECTS[semester]
    return COLLEGE_SUBJECTS[semester]


def school_subject_bias(subject: str) -> float:
    return {
        "Tamil": 0.03,
        "English": 0.05,
        "Mathematics": -0.05,
        "Science": -0.01,
        "Social Science": 0.01,
        "Computer Science": 0.04,
    }.get(subject, 0.0)


def college_subject_bias(subject: str) -> float:
    return {
        "Communicative English": 0.04,
        "Mathematics I": -0.03,
        "Mathematics II": -0.03,
        "Programming Fundamentals": 0.02,
        "C Programming": 0.01,
        "Digital Logic": -0.01,
        "Data Structures": -0.02,
        "Object Oriented Programming": 0.00,
        "Statistics": -0.01,
        "Database Fundamentals": 0.02,
        "Python Programming": 0.03,
        "Computer Organization": -0.02,
        "Operating Systems": -0.02,
        "Discrete Mathematics": -0.03,
        "Machine Learning Basics": 0.02,
        "Software Engineering": 0.01,
        "Probability & Statistics": -0.01,
        "Web Technologies": 0.03,
        "Data Visualization": 0.04,
        "Artificial Intelligence": 0.03,
        "Deep Learning": 0.04,
        "Big Data Analytics": 0.02,
        "Cloud Computing": 0.01,
        "Natural Language Processing": 0.03,
        "MLOps": 0.02,
        "Advanced Machine Learning": 0.04,
        "Research Methods": 0.01,
        "Mobile Computing": 0.00,
        "Project Work": 0.05,
        "Seminar": 0.02,
        "Capstone Project": 0.06,
        "Model Deployment": 0.04,
        "Optimization Techniques": -0.01,
        "AI Ethics": 0.03,
        "Internship": 0.05,
        "Industry Project": 0.05,
    }.get(subject, 0.0)


def college_department_bias(department: str) -> float:
    return {
        "Artificial Intelligence and Machine Learning": 0.03,
        "Computer Science and Engineering": 0.02,
        "Data Science": 0.04,
        "Information Technology": 0.01,
        "Electronics and Communication Engineering": -0.01,
        "Mathematics": -0.03,
        "Physics": -0.02,
        "Chemistry": -0.02,
    }.get(department, 0.0)


def build_school_records(profiles: list[SchoolProfile]) -> pd.DataFrame:
    month_bias = np.linspace(-0.08, 0.12, len(ACADEMIC_MONTHS))
    standard_bias = {
        1: -0.08,
        2: -0.07,
        3: -0.06,
        4: -0.05,
        5: -0.04,
        6: -0.02,
        7: -0.01,
        8: 0.00,
        9: 0.01,
        10: 0.02,
        11: 0.03,
        12: 0.04,
    }

    rows: list[dict[str, object]] = []
    record_id = 1

    for profile in profiles:
        base_ability = float(np.clip(np.random.normal(0.60, 0.14), 0.12, 0.95))
        std_bias = standard_bias[profile.standard]

        for month_no, month_name in enumerate(ACADEMIC_MONTHS, start=1):
            progress = month_bias[month_no - 1]

            for subject in school_subjects():
                skill = base_ability + std_bias + progress + school_subject_bias(subject) + np.random.normal(0, 0.05)
                skill = float(np.clip(skill, 0.05, 0.98))

                internal_scores = [
                    bounded_int(1 + skill * 49 + np.random.normal(0, 2.2), 1, 50)
                    for _ in range(5)
                ]
                main_scores = [
                    bounded_int(1 + skill * 99 + np.random.normal(0, 4.2), 1, 100)
                    for _ in range(3)
                ]
                daily_test = bounded_int(1 + skill * 9 + np.random.normal(0, 0.8), 1, 10)
                weekly_test = bounded_int(1 + skill * 24 + np.random.normal(0, 1.6), 1, 25)

                internal_avg = round(float(np.mean(internal_scores)), 2)
                main_avg = round(float(np.mean(main_scores)), 2)
                daily_pct = round(daily_test * 10.0, 2)
                weekly_pct = round(weekly_test * 4.0, 2)
                average_score = round(
                    0.25 * (internal_avg * 2.0)
                    + 0.45 * main_avg
                    + 0.10 * daily_pct
                    + 0.20 * weekly_pct,
                    2,
                )
                average_score = float(np.clip(average_score, 0, 100))
                attendance_pct = round(float(np.clip(58 + skill * 38 + np.random.normal(0, 4.0), 30, 100)), 2)
                grade = (
                    "A"
                    if average_score >= 85
                    else "B"
                    if average_score >= 70
                    else "C"
                    if average_score >= 55
                    else "D"
                    if average_score >= 40
                    else "E"
                )

                rows.append(
                    {
                        "record_id": f"SR{record_id:07d}",
                        "institution_type": "School",
                        "student_id": profile.student_id,
                        "admission_no": profile.admission_no,
                        "reg_no": profile.reg_no,
                        "student_name": profile.student_name,
                        "phone_number": profile.phone_number,
                        "gender": profile.gender,
                        "guardian_name": profile.guardian_name,
                        "father_name": profile.father_name,
                        "mother_name": profile.mother_name,
                        "blood_group": profile.blood_group,
                        "email": profile.email,
                        "address": profile.address,
                        "city": profile.city,
                        "state": profile.state,
                        "pincode": profile.pincode,
                        "house": profile.house,
                        "admission_year": profile.admission_year,
                        "standard": profile.standard,
                        "standard_roman": profile.standard_roman,
                        "section": profile.section,
                        "date_of_birth": profile.date_of_birth,
                        "academic_year": ACADEMIC_YEAR,
                        "month_no": month_no,
                        "month_name": month_name,
                        "subject": subject,
                        "internal_exam_1": internal_scores[0],
                        "internal_exam_2": internal_scores[1],
                        "internal_exam_3": internal_scores[2],
                        "internal_exam_4": internal_scores[3],
                        "internal_exam_5": internal_scores[4],
                        "main_exam_1": main_scores[0],
                        "main_exam_2": main_scores[1],
                        "main_exam_3": main_scores[2],
                        "daily_test": daily_test,
                        "weekly_test": weekly_test,
                        "attendance_pct": attendance_pct,
                        "average_score": average_score,
                        "grade": grade,
                        "result": "Pass" if average_score >= 50 else "Fail",
                    }
                )
                record_id += 1

    return pd.DataFrame(rows)


def build_college_records(profiles: list[CollegeProfile]) -> pd.DataFrame:
    semester_bias = {
        1: -0.04,
        2: -0.03,
        3: -0.02,
        4: 0.00,
        5: 0.02,
        6: 0.03,
        7: 0.05,
        8: 0.06,
    }
    month_bias = np.linspace(-0.06, 0.10, len(ACADEMIC_MONTHS))

    rows: list[dict[str, object]] = []
    record_id = 1

    for profile in profiles:
        base_ability = float(np.clip(np.random.normal(0.64, 0.13), 0.18, 0.95))
        dept_bias = college_department_bias(profile.department)
        sem_bias = semester_bias[profile.semester]

        for month_no, month_name in enumerate(ACADEMIC_MONTHS, start=1):
            progress = month_bias[month_no - 1]
            for subject in college_subjects(profile.semester):
                aptitude = base_ability + dept_bias + sem_bias + progress + college_subject_bias(subject) + np.random.normal(0, 0.05)
                aptitude = float(np.clip(aptitude, 0.05, 0.98))

                internal_1 = bounded_int(1 + aptitude * 99 + np.random.normal(0, 5.0), 1, 100)
                internal_2 = bounded_int(1 + aptitude * 99 + np.random.normal(0, 5.0), 1, 100)
                average_score = round((internal_1 + internal_2) / 2.0, 2)
                attendance_pct = round(float(np.clip(62 + aptitude * 32 + np.random.normal(0, 4.0), 35, 100)), 2)
                grade = (
                    "A"
                    if average_score >= 85
                    else "B"
                    if average_score >= 70
                    else "C"
                    if average_score >= 55
                    else "D"
                    if average_score >= 40
                    else "E"
                )

                rows.append(
                    {
                        "record_id": f"CR{record_id:07d}",
                        "institution_type": "College",
                        "student_id": profile.student_id,
                        "admission_no": profile.admission_no,
                        "reg_no": profile.reg_no,
                        "student_name": profile.student_name,
                        "phone_number": profile.phone_number,
                        "gender": profile.gender,
                        "guardian_name": profile.guardian_name,
                        "father_name": profile.father_name,
                        "mother_name": profile.mother_name,
                        "blood_group": profile.blood_group,
                        "email": profile.email,
                        "address": profile.address,
                        "city": profile.city,
                        "state": profile.state,
                        "pincode": profile.pincode,
                        "department": profile.department,
                        "department_code": profile.department_code,
                        "semester": profile.semester,
                        "section": profile.section,
                        "admission_year": profile.admission_year,
                        "date_of_birth": profile.date_of_birth,
                        "academic_year": ACADEMIC_YEAR,
                        "month_no": month_no,
                        "month_name": month_name,
                        "subject": subject,
                        "internal_exam_1": internal_1,
                        "internal_exam_2": internal_2,
                        "attendance_pct": attendance_pct,
                        "average_score": average_score,
                        "grade": grade,
                        "result": "Pass" if average_score >= 50 else "Fail",
                    }
                )
                record_id += 1

    return pd.DataFrame(rows)


def build_student_master_school(profiles: list[SchoolProfile]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "institution_type": "School",
                "student_id": profile.student_id,
                "admission_no": profile.admission_no,
                "reg_no": profile.reg_no,
                "student_name": profile.student_name,
                "phone_number": profile.phone_number,
                "gender": profile.gender,
                "guardian_name": profile.guardian_name,
                "father_name": profile.father_name,
                "mother_name": profile.mother_name,
                "blood_group": profile.blood_group,
                "email": profile.email,
                "address": profile.address,
                "city": profile.city,
                "state": profile.state,
                "pincode": profile.pincode,
                "house": profile.house,
                "admission_year": profile.admission_year,
                "standard": profile.standard,
                "standard_roman": profile.standard_roman,
                "section": profile.section,
                "date_of_birth": profile.date_of_birth,
            }
            for profile in profiles
        ]
    )


def build_student_master_college(profiles: list[CollegeProfile]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "institution_type": "College",
                "student_id": profile.student_id,
                "admission_no": profile.admission_no,
                "reg_no": profile.reg_no,
                "student_name": profile.student_name,
                "phone_number": profile.phone_number,
                "gender": profile.gender,
                "guardian_name": profile.guardian_name,
                "father_name": profile.father_name,
                "mother_name": profile.mother_name,
                "blood_group": profile.blood_group,
                "email": profile.email,
                "address": profile.address,
                "city": profile.city,
                "state": profile.state,
                "pincode": profile.pincode,
                "department": profile.department,
                "department_code": profile.department_code,
                "semester": profile.semester,
                "section": profile.section,
                "admission_year": profile.admission_year,
                "date_of_birth": profile.date_of_birth,
            }
            for profile in profiles
        ]
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    school_profiles = build_school_profiles(500)
    college_profiles = build_college_profiles(3000)

    school_master = build_student_master_school(school_profiles)
    school_records = build_school_records(school_profiles)
    college_master = build_student_master_college(college_profiles)
    college_records = build_college_records(college_profiles)

    school_master.to_csv(data_dir / "school_student_master.csv", index=False)
    school_records.to_csv(data_dir / "school_academic_records.csv", index=False)
    college_master.to_csv(data_dir / "college_student_master.csv", index=False)
    college_records.to_csv(data_dir / "college_academic_records.csv", index=False)

    print(f"Created {len(school_master)} school students")
    print(f"Created {len(school_records)} school academic records")
    print(f"Created {len(college_master)} college students")
    print(f"Created {len(college_records)} college academic records")
    print(f"Saved to: {data_dir}")


if __name__ == "__main__":
    main()
