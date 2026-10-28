"""Build arcadia_employees.csv: one row per Arcadia Systems employee on the report date.

Arcadia Systems is fictional; all data is synthetic. Executive officers (department D-901)
are excluded, so the file holds 30,005 rows on Jun 30, 2026, the same headcount as every
Arcadia dashboard.

Run from the warehouse repository root:
    python3 build_arcadia_employees.py 2026-06-30 arcadia_employees.csv

Rules:
- A job record is current on the report date when it starts on or before it and ends on
  or after it (or has no end).
- Someone whose last day is the report date still counts on that date (month-end convention).
- Regular employees only; contingent workers live in a different system.
"""
import sys

import duckdb

as_of = sys.argv[1] if len(sys.argv) > 1 else "2026-06-30"
out = sys.argv[2] if len(sys.argv) > 2 else "arcadia_employees.csv"
raw = "data/raw/"
a = f"DATE '{as_of}'"

con = duckdb.connect()
con.sql(f"""
create table emp as
select j.worker_id                as employee_id,
       {a}                        as as_of_date,
       d.function                 as function_name,
       d.sub_function,
       d.department_name,
       l.region,
       l.country_name,
       l.office_name,
       jl.level_code              as job_level,
       case when j.job_level <= 2 then 'L1–L2 Associate'
            when j.job_level <= 4 then 'L3–L4 Senior'
            when j.job_level <= 6 then 'L5–L6 Manager'
            else 'L7+ Director' end as level_band,
       jp.career_track,
       jp.job_family,
       w.original_hire_date       as hire_date
from read_csv_auto('{raw}fact_job_history.csv') j
join read_csv_auto('{raw}dim_worker.csv')     w using (worker_id)
join read_csv_auto('{raw}dim_department.csv') d using (department_id)
join read_csv_auto('{raw}dim_location.csv')   l using (location_id)
join read_csv_auto('{raw}dim_job_level.csv')  jl on jl.job_level = j.job_level
join read_csv_auto('{raw}dim_job_profile.csv') jp on jp.job_profile_id = j.job_profile_id
where j.effective_start_date <= {a}
  and (j.effective_end_date is null or j.effective_end_date >= {a})
  and j.department_id <> 'D-901'
  and w.worker_type = 'Regular Employee'
  and (w.termination_date is null or w.termination_date >= {a})
order by function_name, department_name, region, country_name, office_name, employee_id
""")

rows, people = con.sql("select count(*), count(distinct employee_id) from emp").fetchall()[0]
assert rows == people, "one row per employee"
con.sql(f"copy emp to '{out}' (header, delimiter ',')")
print(f"{out}: {rows:,} employees on {as_of}")
