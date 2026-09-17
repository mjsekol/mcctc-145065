# A Report Calculates; It Never Stores
---
## Slide 1: Your paycheck says 1 hour
- You worked 1 hour and 15 minutes
- The schedule app says you worked 1 hour
- Nobody typed it wrong
- The arithmetic was wrong
Speaker notes: Picture this with a part-time job. You worked seventy-five minutes and the app pays you for sixty. Nobody made a typing mistake. The app divided minutes by sixty the wrong way. Today we build reports that get that right, and we prove it.
Image: A pay stub with 1.00 hours circled in launch red and a clock showing 1:15.
---
## Slide 2: Calculate every time, store nothing
- A calculated field comes from the rows
- It is computed each time the report runs
- So it can never disagree with the rows
- A stored total drifts the first time someone forgets
Speaker notes: This is today's idea. A number on a report is not stored anywhere. It is calculated from the rows when the report runs. Delete a row, and the report is right the next time it loads, with no extra code. A stored total is right only until someone edits a record and forgets to update it.
Image: A report table with arrows pointing back to many small row cards beneath it, launch blue.
---
## Slide 3: The downtime report
```sql
SELECT e.code,
       COUNT(i.id)                                              AS issues,
       SUM(CASE WHEN i.status <> 'closed' THEN 1 ELSE 0 END)     AS open_issues,
       COALESCE(SUM(i.downtime_minutes), 0)                     AS minutes,
       ROUND(COALESCE(SUM(i.downtime_minutes), 0) / 60.0, 2)    AS hours
FROM equipment AS e
LEFT JOIN issues AS i ON i.equipment_id = e.id
GROUP BY e.id, e.code
ORDER BY minutes DESC, e.code
```
Speaker notes: One row per machine, from GROUP BY. LEFT JOIN keeps a machine that has no issues. COUNT of i dot id counts issues. The SUM of CASE counts only the open ones. COALESCE turns nothing into zero. Dividing by sixty point zero keeps the fraction.
Image: None. This slide is code.
---
## Slide 4: Read every column
```
machine  issues  open  minutes  hours
CV-01         1     1       90    1.5
OV-01         2     1       75   1.25
LC-02         0     0        0    0.0
PB-02         1     1        0    0.0
```
Speaker notes: Check OV-01 by hand. Two issues, sixty and fifteen minutes. Seventy-five minutes. Seventy-five over sixty is one point two five. The report agrees. LC-02 is an invented laser with no issues, and it still has a row because of the LEFT JOIN. Every report you write gets checked against a hand calculation like this one.
Image: None. This slide is code.
---
## Slide 5: Change one number
```sql
       ROUND(COALESCE(SUM(i.downtime_minutes), 0) / 60, 2)      AS hours
```
```
machine  issues  open  minutes  hours
CV-01         1     1       90    1.0
OV-01         2     1       75    1.0
LC-02         0     0        0    0.0
PB-02         1     1        0    0.0
```
Speaker notes: I changed sixty point zero to sixty. No error. Ninety minutes is now one hour. Seventy-five minutes is one hour. SQLite divided an integer by an integer and threw away the fraction. Who would plan a shift around this number? A supervisor would, and never know why the conveyor schedule is off by half an hour.
Image: None. This slide is code.
---
## Slide 6: SQL and Python disagree
```
SQL    75 / 60, 75 / 60.0, 75 % 60: (1, 1.25, 15)
Python 75 / 60, 75 // 60, 75 % 60:  (1.25, 1, 15)
SQL    ROUND(1.25, 1): 1.3
Python round(1.25, 1): 1.2
SQL    ROUND(2.5), Python round(2.5): 3.0 2
```
Speaker notes: This is real output from one small script. In SQLite, slash between two integers throws away the fraction. In Python three, slash keeps it, and double slash throws it away. Rounding differs too. SQLite rounds an exact half away from zero. Python rounds it to the even neighbor. That is why the lab's report shows OV-01 as one point three hours. If your report and your hand math differ by a tenth, check this first.
Image: None. This slide is code.
---
## Slide 7: The COUNT(*) trap
- A LEFT JOIN gives an empty machine one row
- COUNT(*) counts that row: 1 issue
- COUNT(i.id) skips the empty value: 0 issues
- Always test a row with nothing to count
Speaker notes: Change COUNT of i dot id to COUNT star, and LC-02 claims one issue. It has none. The LEFT JOIN made one row for it with empty issue columns, and COUNT star counted the row. The bug hides on every machine that has issues, so a test needs a machine with none.
Image: A table row for LC-02 with a count of 1 crossed out and 0 written beside it.
---
## Slide 8: Why not store the total
- Faster: read one value per tool
- But every insert, edit, and delete must update it
- One missed update, and the report lies
- At tool crib size, calculating takes milliseconds
Speaker notes: Someone will ask why we do not keep a total column. It is a real technique for very large tables, with a plan to keep it true. For a tool crib, the calculation is fast, and it cannot drift. Ask the question every time: what updates this number when a checkout is voided?
Image: A balance scale with speed on one side and correctness on the other, navy.
---
## Slide 9: What you are about to build
- Lab U05-02, Part 1: steps 1 through 6
- Write report_by_equipment and report_totals
- Labor hours come through a subquery
- The report shows 3.8 hours for all of Line 3
- Target: 92 of 101 self-checks pass
Speaker notes: Lab U05-02 is Ship It. Part 1 is the report. Every machine appears, including one with no issues, and every number is calculated. Read the handout before you join work notes, because joining them straight into the grouped query counts downtime more than once. The tests compare every cell with a table worked out by hand. In Build 2 you write your tool crib's report and its CSV export.
Image: A report page with a totals row reading 3.8 hours, navy header, launch blue accents.
