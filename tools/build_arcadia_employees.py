"""Build the Arcadia How-To CSVs from the warehouse's raw tables.

Arcadia Systems is fictional; all data is synthetic. Executive officers (department D-901)
are excluded, so every file holds 30,005 employees on Jun 30, 2026, the same headcount as
every Arcadia dashboard.

Run from the warehouse repository root:
    python3 build_arcadia_employees.py 2026-06-30 arcadia_employees.csv
        How-To #1: one row per employee on the report date.
    python3 build_arcadia_employees.py --monthly 2026-06-30 arcadia_monthly_headcount.csv
        How-To #2: employee counts by month-end x department x office x level band, for the
        61 month-ends ending on the report date (five years plus the opening month). The
        start is counted back from the report date, so no year is hard-coded.

Rules:
- A job record is current on a date when it starts on or before it and ends on or after
  it (or has no end).
- Someone whose last day is the date still counts on that date (month-end convention).
- Regular employees only; contingent workers live in a different system.
- Shared columns keep the same names in both files. In the monthly file, as_of_date is
  the month-end each row counts, and employees is the count.
"""
import sys

import duckdb

args = sys.argv[1:]
monthly = "--monthly" in args
args = [x for x in args if x != "--monthly"]
as_of = args[0] if len(args) > 0 else "2026-06-30"
out = args[1] if len(args) > 1 else ("arcadia_monthly_headcount.csv" if monthly else "arcadia_employees.csv")
raw = "data/raw/"
MONTHS = 61

con = duckdb.connect()
con.sql(f"""
create table dates as
select last_day(DATE '{as_of}' - to_months(i))::date as as_of_date
from range({MONTHS if monthly else 1}) t(i)
""")

level_band = """case when j.job_level <= 2 then 'L1–L2 Associate'
            when j.job_level <= 4 then 'L3–L4 Senior'
            when j.job_level <= 6 then 'L5–L6 Manager'
            else 'L7+ Director' end"""

current = f"""
from dates m
join read_csv_auto('{raw}fact_job_history.csv') j
  on j.effective_start_date <= m.as_of_date
 and (j.effective_end_date is null or j.effective_end_date >= m.as_of_date)
join read_csv_auto('{raw}dim_worker.csv')     w using (worker_id)
join read_csv_auto('{raw}dim_department.csv') d using (department_id)
join read_csv_auto('{raw}dim_location.csv')   l using (location_id)
where j.department_id <> 'D-901'
  and w.worker_type = 'Regular Employee'
  and (w.termination_date is null or w.termination_date >= m.as_of_date)
"""

if monthly:
    con.sql(f"""
    create table out as
    select m.as_of_date, d.function as function_name, d.sub_function, d.department_name,
           l.region, l.country_name, l.office_name, {level_band} as level_band,
           count(*) as employees
    {current}
    group by all
    order by as_of_date, function_name, department_name, region, country_name, office_name, level_band
    """)
    rows, months, last = con.sql(
        "select count(*), count(distinct as_of_date), "
        "sum(employees) filter (where as_of_date = (select max(as_of_date) from out)) from out"
    ).fetchall()[0]
    con.sql(f"copy out to '{out}' (header, delimiter ',')")
    print(f"{out}: {rows:,} rows, {months} month-ends, {last:,} employees on {as_of}")
else:
    con.sql(f"""
    create table out as
    select j.worker_id as employee_id, m.as_of_date, d.function as function_name, d.sub_function,
           d.department_name, l.region, l.country_name, l.office_name,
           jl.level_code as job_level, {level_band} as level_band,
           jp.career_track, jp.job_family, w.original_hire_date as hire_date
    {current.replace("where", f"join read_csv_auto('{raw}dim_job_level.csv') jl on jl.job_level = j.job_level join read_csv_auto('{raw}dim_job_profile.csv') jp on jp.job_profile_id = j.job_profile_id where", 1)}
    order by function_name, department_name, region, country_name, office_name, employee_id
    """)
    rows, people = con.sql("select count(*), count(distinct employee_id) from out").fetchall()[0]
    assert rows == people, "one row per employee"
    con.sql(f"copy out to '{out}' (header, delimiter ',')")
    print(f"{out}: {rows:,} employees on {as_of}")
