# A Transaction Makes Many Writes One Change
---
## Slide 1: The upload that half worked
- You upload 40 photos to a shared album
- The Wi-Fi drops at photo 23
- Which 22 made it
- Do you upload all 40 again
Speaker notes: You have lived this one. An upload dies partway, and now you have to figure out which files went through. Upload everything again and you get duplicates. Skip it and you are missing some. Purchasing is about to send the tool crib a spreadsheet of 40 tools, and your import has the same problem unless we fix it today.
Image: A photo album grid with 22 filled squares and 18 empty ones, a broken Wi-Fi icon, launch red.
---
## Slide 2: All of them, or none of them
- A transaction groups writes
- Every write succeeds: commit, and they are permanent
- Any write fails: roll back, and nothing changed
- The table is exactly as it was
Speaker notes: This is today's idea. A transaction turns many writes into one change. Either the whole file goes in, or none of it does. If none of it does, you fix the file and run it again with nothing to clean up.
Image: A single switch with two positions labeled commit and rollback, navy and launch blue.
---
## Slide 3: The transaction block
```python
@contextmanager
def transaction(conn):
    """Commit if the block finishes. Roll back if anything in it raises."""
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
```
Speaker notes: This is the lab's transaction function, and it is short. Your with block runs at the yield. If it finishes, commit. If anything raises, roll back, then raise again so the caller still sees the error. A rollback that swallowed the error would be a second bug.
Image: None. This slide is code.
---
## Slide 4: One bad row in four
```python
ROWS = [("Assist gas pressure drops", 35), ("Roller 14 bearing noise", 0),
        ("Downtime typed wrong", 5000), ("Muting lamp out", 20)]

try:
    with transaction(conn):
        for title, minutes in ROWS:
            conn.execute("INSERT INTO issues (title, downtime_minutes) VALUES (?, ?)",
                         (title, minutes))
except sqlite3.IntegrityError as error:
    print("Import refused:", error)
print("rows in the table:", conn.execute("SELECT COUNT(*) FROM issues").fetchone()[0])
```
```
Import refused: CHECK constraint failed: downtime_minutes BETWEEN 0 AND 1440
rows in the table: 0
```
Speaker notes: The table has a CHECK rule, downtime from 0 to 1440, the minutes in one day. Row three says 5000. The first two inserts worked, then row three broke the rule, and the rollback undid the first two as well. Zero rows. That is the whole point.
Image: None. This slide is code.
---
## Slide 5: Move the commit into the loop
```python
try:
    for title, minutes in ROWS:
        conn.execute("INSERT INTO issues (title, downtime_minutes) VALUES (?, ?)",
                     (title, minutes))
        conn.commit()
except sqlite3.IntegrityError as error:
    print("Import refused:", error)
```
```
Import refused: CHECK constraint failed: downtime_minutes BETWEEN 0 AND 1440
rows in the table: 2
```
Speaker notes: Here is the wrong way. Commit after every row, which feels careful. Same error message, word for word. But two rows are in the table. The message says refused, so whoever reads it thinks nothing went in. Fix the bad row, run it again, and the first two are in twice. How would anyone know which rows came from which run?
Image: None. This slide is code.
---
## Slide 6: Count what changed
- UPDATE and DELETE report cursor.rowcount
- An id that does not exist changes 0 rows
- Zero rows raises no error
- Your function returns False, your route answers 404
Speaker notes: Updates and deletes are quiet. If you update issue 999 and there is no issue 999, nothing happens and nothing complains. The only signal is rowcount. The lab's delete function returns whether rowcount is one, and the route turns False into a 404.
Image: A counter display reading 0 next to an UPDATE statement card, navy.
---
## Slide 7: Delete asks first
- GET shows an are-you-sure page and changes nothing
- Only a POST with the token deletes
- Links get followed by preloaders, crawlers, and bookmarks
- Gloved hands hit the wrong button
Speaker notes: A delete link is a trap. A browser that preloads pages can follow it. So can a crawler, or a curious person. The CSRF check does not help, because it only runs on POST. So GET shows a confirmation page, and only the form on that page deletes. On a shop floor, confirmation before a destructive action is the rule.
Image: A confirmation dialog with a large Keep button and a red Delete permanently button, sized for gloves.
---
## Slide 8: An import checks every row first
- Read the whole file with utf-8-sig
- Check each row with the form's rules
- Collect every problem with its line number
- Any problem: import nothing, print them all
- Clean file: one transaction
Speaker notes: Open the lab's import_csv.py and look at read_rows. It checks everything before it writes anything. It lists every problem, not only the first, so the person fixing the spreadsheet fixes them all at once. Line numbers start at two, because line one is the header. And utf-8-sig removes the invisible marker some spreadsheet programs put at the start of a file.
Image: A spreadsheet with two rows highlighted in launch red and line numbers in the margin.
---
## Slide 9: What you are about to build
- Lab U05-01, Part 3: steps 18 through 25
- Write update_issue and delete_issue
- Write import_issues: all rows or none
- The bad CSV imports nothing and names four lines
- Target: 56 of 56, due end of block
Speaker notes: Part 3 finishes the lab. update_issue stamps closed_at once and returns whether a row changed. delete_issue removes the issue and its notes, and the docstring asks which file makes that happen. import_issues writes every row or none. Run both import commands on the good file and the bad file. Lab U05-01 is due at the end of today's block. In Build 2 you give your tool crib full CRUD and a CSV import.
Image: A terminal showing 56 of 56 self-checks passed, navy background, launch blue text.
