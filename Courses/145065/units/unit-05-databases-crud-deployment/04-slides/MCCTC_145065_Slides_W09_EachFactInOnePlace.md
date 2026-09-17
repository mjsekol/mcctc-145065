# Each Fact Lives in One Place
---
## Slide 1: Your contact shows two names
- A friend changed their name in one group chat
- The other chat still shows the old one
- Which name is right
- Your Unit 4 file has the same problem
Speaker notes: You have seen this. Someone changes their display name, and one app shows the new name while another shows the old one. Now you have two answers and no way to know which is true. A JSON file that copies a machine's name onto every issue has exactly that problem. Today we fix it for good.
Image: Two phone screens side by side showing the same friend under two different names, navy frame.
---
## Slide 2: One big table, one partial rename
```python
conn.execute("CREATE TABLE log (issue TEXT, machine_code TEXT, machine_name TEXT)")
conn.executemany("INSERT INTO log VALUES (?, ?, ?)", [
    ("Zone 2 heater slow", "OV-01", "Powder Coat Cure Oven"),
    ("Exhaust fan belt squeal", "OV-01", "Powder Coat Cure Oven"),
])
conn.execute("UPDATE log SET machine_name = 'Cure Oven 1' WHERE issue = 'Zone 2 heater slow'")
for row in conn.execute("SELECT DISTINCT machine_code, machine_name FROM log"):
    print(row)
```
Speaker notes: Riverside Fabrication is our invented shop. Here is the spreadsheet way. One table, the machine's name on every row. Someone renames the oven, but only on the row they were looking at. Predict what the last query prints.
Image: None. This slide is code.
---
## Slide 3: One machine, two names
```
('OV-01', 'Cure Oven 1')
('OV-01', 'Powder Coat Cure Oven')
```
Speaker notes: One machine code, two names. The table disagrees with itself, and no query can tell you which name is true. The problem is not the update. The problem is that the name was stored twice in the first place.
Image: None. This slide is code.
---
## Slide 4: Each fact lives in one place
- A machine's name lives only in equipment
- An issue stores the machine's key, not its name
- Primary key: the id that identifies a row
- Foreign key: a column holding another table's key
- Rename once, and every issue shows it
Speaker notes: This is normalization. Each fact has one home. The issue points at its machine by key. When you read, a join puts the name back next to the issue. When you rename, you change one row, and every issue shows the new name, because no issue ever had a copy.
Image: Two tables, equipment and issues, with an arrow from issues.equipment_id to equipment.id, launch blue.
---
## Slide 5: The normalized version
```python
conn.execute("PRAGMA foreign_keys = ON")    # SQLite ignores foreign keys without this
conn.executescript(SCHEMA)
conn.execute("INSERT INTO equipment (code, name) VALUES ('OV-01', 'Powder Coat Cure Oven')")
conn.execute("INSERT INTO issues (equipment_id, title) VALUES (1, 'Zone 2 heater slow')")
conn.execute("INSERT INTO issues (equipment_id, title) VALUES (1, 'Exhaust fan belt squeal')")
conn.execute("UPDATE equipment SET name = 'Cure Oven 1' WHERE code = 'OV-01'")
# ... join and print, then try an issue for machine 99
```
```
('Zone 2 heater slow', 'OV-01', 'Cure Oven 1')
('Exhaust fan belt squeal', 'OV-01', 'Cure Oven 1')
Refused: FOREIGN KEY constraint failed
issues stored: 2
```
Speaker notes: The schema has equipment with a unique code, and issues with equipment_id declared as a reference. One update, both issues show the new name. Then we try to log an issue for machine 99, which does not exist, and the database refuses. The full file is in today's notes.
Image: None. This slide is code.
---
## Slide 6: Constraints refuse bad rows
- NOT NULL refuses an empty value
- UNIQUE refuses a second badge T-1041
- CHECK refuses a row that breaks your rule
- REFERENCES refuses a key pointing at nothing
- Your form can be skipped. The database cannot.
Speaker notes: Why put a rule in the database when your form already checks it? Because a bug, a script, or a teammate's new route can skip your form. The database checks every write, no matter where it came from. Week 8's lockout rule gets enforced a second time here, on purpose.
Image: A gate with four locks labeled with the four constraint names, navy and launch red.
---
## Slide 7: Delete one line
```python
# conn.execute("PRAGMA foreign_keys = ON")    <- deleted
```
```
('Zone 2 heater slow', 'OV-01', 'Cure Oven 1')
('Exhaust fan belt squeal', 'OV-01', 'Cure Oven 1')
issues stored: 3
```
Speaker notes: Now I delete the PRAGMA line and run it again. Look for the Refused line. It is gone. Issues stored is three. The issue for machine 99 went in. Where is issue three's machine? Nowhere. The join hides it, because a join only shows issues whose machine exists. That row is an orphan, and SQLite said nothing. Every new SQLite connection starts with foreign keys off, which is why the lab's connect function turns them on every time.
Image: None. This slide is code.
---
## Slide 8: A table without personal data cannot leak it
- Technicians: a badge and a display name
- No address, phone, birth date, or email
- The app never needs them
- So the app never stores them
Speaker notes: Record confidentiality is a design decision, and it is competency one point four point three. Say this sentence with me: a table that does not hold personal data cannot leak it. No bug and no stolen laptop can expose a column that does not exist. The lab's starter has a column that fails this test. You will find it.
Image: A simple table card with two columns filled and three crossed-out columns labeled address, phone, email.
---
## Slide 9: Before your first database file
```
# Databases are data, not code. Never commit them.
*.db
*.sqlite3
instance/
.env
```
Speaker notes: Two minutes, right now, before Build 1. Add these four lines to the gitignore of the repository you work in. Then after the database exists, run git status and make sure instance slash line3 dot db is not listed. A committed database stays in the history forever, every record in it, even after you delete it in the next commit.
Image: None. This slide is code.
---
## Slide 10: What you are about to build
- Lab U05-01, Part 1: steps 1 through 9
- Declare the foreign keys and the CHECK rules
- Turn on foreign keys in connect
- Decide what the technicians table should not hold
- Target: 33 of 56 self-checks pass
Speaker notes: Lab U05-01 is Line 3 Gets a Database. The starter schema works and is wrong in several ways. Part 1 fixes them: declare the relationships, add the rules, turn on enforcement, and make the privacy decision and write down why. Run the self-check often. When every Part 1 line says PASS, you are at 33 of 56, and git status must not list your database. In Build 2 you design your tool crib schema and ER diagram.
Image: An ER diagram with four boxes, technicians, equipment, issues, work_notes, connected by one-to-many lines.
