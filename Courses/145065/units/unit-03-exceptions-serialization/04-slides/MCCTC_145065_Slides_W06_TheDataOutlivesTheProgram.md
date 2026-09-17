# The Data Outlives the Program
---
## Slide 1: The save that ate the last good copy
- The program saves at shutdown
- The power strip goes off mid-save
- Next morning the file will not load
- The last good copy was that file
Speaker notes: A program saves when it closes. Somebody switches off the power strip while it is still writing. In the morning the file will not load, and the only good copy was the file that was being overwritten. Today is about making sure that can never happen.
Image: A power strip switch being flipped, with a half-written file icon.
---
## Slide 2: open with w empties the file first
```python
def save(document, path):
    with open(path, "w", encoding="utf-8") as handle:   # the old file is empty from here
        json.dump(document, handle, indent=2)
```
```
first save: 103 bytes, loads: 2
second save failed: Object of type set is not JSON serializable
file now holds 80 characters: '",\n      "load_kg": '
JSONDecodeError: Expecting value: line 6 column 18 (char 80)
```
Speaker notes: Open with w empties the file the moment it opens. Then json dump writes in pieces. When the set could not be written, the file held eighty characters of the new text and none of the old. The first save is gone, and what is left will not load.
Image: None. This slide is code.
---
## Slide 3: The safe save, four steps
- 1. Build the whole text in memory
- 2. Copy the current file to .bak
- 3. Write a .tmp file, flush, fsync
- 4. os.replace() the .tmp over the file
Speaker notes: Four steps. Build everything in memory, so a model error touches nothing. Copy the old file to a backup. Write the new text somewhere else and make the disk hold it. Then swap it in with one atomic replace. A crash at any point leaves the old file or the new one, never half of each.
Image: A four-step flowchart with a crash icon between each step and a whole file below each.
---
## Slide 4: The safe save in code
```python
def save(document, path):
    path = Path(path)
    text = json.dumps(document, indent=2) + "\n"          # 1. build it all in memory
    temp = path.with_name(path.name + ".tmp")
    try:
        if path.exists():
            shutil.copy2(path, path.with_name(path.name + ".bak"))   # 2. keep the old one
        with open(temp, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)                              # 3. write somewhere else
            handle.flush()
            os.fsync(handle.fileno())                       #    and make the disk hold it
        os.replace(temp, path)                              # 4. swap, in one step
    except OSError:
        temp.unlink(missing_ok=True)
        raise
```
Speaker notes: Here are the four steps with their numbers in the comments. Flush hands the text to the operating system, and fsync asks it to put the bytes on the disk now. Replace is the operating system call that swaps the files in one step.
Image: None. This slide is code.
---
## Slide 5: The same failure, handled
```
third save failed: Object of type set is not JSON serializable
['line3.json', 'line3.json.bak']
file:   {'version': 2, 'load_kg': 950}
backup: {'version': 2, 'load_kg': 640}
```
Speaker notes: The third save failed in step one, in memory, before any file was opened. The folder has the second save and a backup of the first, both loadable, and no leftover temp file.
Image: None. This slide is code.
---
## Slide 6: Restore only what loads
- Load the backup fully first
- Then copy it into place
- A bad backup is refused
- The last good file stays untouched
Speaker notes: Restoring means copying the backup over the file. If the backup is damaged and you copy first, both copies are now damaged. So load and check the backup first. If it fails, stop, and the current file stays exactly as it was.
Image: A backup file passing through a checkpoint before reaching the main file.
---
## Slide 7: Old files, new program
```
{"kind": "press", "tag": "L3-PRS-01", "name": "Press 1", "rated_kw": 15, "locked_out_by": null}
version 1 unchanged: True
```
Speaker notes: Version one called the rating power kW and never recorded lockouts. The migration renames the field and fills lockouts with null. The old document is unchanged. That null means unknown, not unlocked, so a person must walk the line before trusting it.
Image: None. This slide is code.
---
## Slide 8: A backup taken after the damage
- The file was damaged at 6 a.m.
- The backup job runs at midnight
- The stick now holds the damage too
- Keep dated copies, check before rotating
Speaker notes: A backup is only as good as the moment it was taken. A nightly job that copies a damaged file replaces the good copy with a bad one. Keep more than one dated copy, and check a file loads before it replaces an older backup. Friday's problem drop is built on this.
Image: A USB stick with a launch red warning icon.
---
## Slide 9: Write the recovery plan first
- What exactly is lost
- Who notices, and how
- The steps, in order
- What a person must check by hand
- When the plan was last tested
Speaker notes: A disaster recovery plan is written before the disaster. It forces the questions nobody asks until it is too late. A backup nobody has ever restored is a hope, not a plan, so the plan says how you test it.
Image: A clipboard titled recovery plan with five checkboxes.
---
## Slide 10: What you are about to build
- Lab U03-02, Part 3
- save_line() with backup and atomic replace
- restore_backup() that checks first
- The version 1 migration
- Your project's RECOVERY_PLAN.md
Speaker notes: In the lab you write the four-step save, the checked restore, and the last line of the migration, then answer which migrated values a person must review. Seventeen of seventeen. Build 2 adds backup and restore to your own project and writes your recovery plan.
Image: A file, its backup, and a plan document side by side.
