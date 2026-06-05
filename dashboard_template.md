# Student Dashboard Template Map

This layout follows the supplied UI style, but the food-related section is removed and replaced with a school and college student analytics section.
It is intended for a Streamlit implementation, not Flask or custom HTML/CSS.
The dashboard can switch between the synthetic school and college datasets.

## Sidebar

Keep the same vertical shell and icon style.

Use these items:
- Dashboard
- Students
- Teachers
- Event
- Finance
- Performance
- User
- Chat
- Latest Activity

Remove:
- Food

## Top Summary Cards

Keep the four-card row, but rename the metrics for student use:
- Students
- Teachers
- Events
- Performance

If you want stronger academic framing, the last card can also be:
- Attendance
- Exams
- Results
- Risk Alerts

## Main Dashboard Panels

Keep the same overall placement:
- large analytics chart on the left
- calendar or academic schedule panel below or beside it
- finance or fee tracking panel as-is if the system tracks tuition or payments
- right rail for recent students, messages, and alerts

Recommended student replacements for chart titles:
- `School Performance` -> `Student Performance`
- `School Calendar` -> `Academic Calendar`
- `School Finance` -> `Fee / Payment Summary` if the data exists

## Detail Pages

Keep the same style for:
- Students
- Teachers
- Add New Student
- Add New Teacher
- Student Details
- Teacher Details
- Events

## Data Sections to Connect Later

- registration number
- admission number
- student name
- guardian name
- father name
- mother name
- blood group
- email
- address
- city
- state
- pincode
- mock interview score
- mock GD score
- video resume score
- total out of 30
- total out of 50
- attendance percentage
- fee status

## Visualization Requirement

Use `matplotlib` for the plots that are generated from the notebook or analysis layer.

Recommended plots:
- line chart for trends
- bar chart for subject or category comparisons
- heatmap for correlation or class-level patterns
- scatter plot for relationships
- box plot for outliers

## Dummy Workbook Mapped Fields

The current dummy workbook at `E:\br\Downloads\AIML.xlsx` maps to:
- `Reg. No` -> `reg_no`
- `Name` -> `name`
- `Mock Interview` -> `mock_interview`
- `Mock GD` -> `mock_gd`
- `Video Resume` -> `video_resume`
- `Total (30)` -> `total_30`
- `Total(50)` -> `total50`

## Synthetic Dataset Specification

### School Mode

- 500 unique students
- `reg_no` format like `III45`
- admission number, guardian, parent, address, and attendance fields included
- 6 subjects
- 10 academic months
- 5 internal exams out of 50
- 3 main exams out of 100
- daily test out of 10
- weekly test out of 25

### College Mode

- 3000 unique students
- `reg_no` format like `RCAS24BAM018`
- department acts like the class group
- admission number, guardian, parent, address, and attendance fields included
- 3 to 6 subjects depending on semester
- 10 academic months
- 2 internal exams, each out of 100
- no external/main exam layer
- unique Indian-style phone numbers that do not start with 0

## College Context

- Department examples:
  - `Artificial Intelligence and Machine Learning`
  - `Computer Science and Engineering`
  - `Data Science`
  - `Information Technology`
  - `Electronics and Communication Engineering`
  - `Mathematics`
  - `Physics`
  - `Chemistry`
- Semester-based subject load
- 10-month academic year
