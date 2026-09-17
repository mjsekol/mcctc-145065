# Implementation plan · <panel name> <version>

**Reader:** whoever builds, installs, updates, or rolls back the panel. Write for a classmate who has
never seen your project and has thirty minutes.

*Delete every line in italics before you submit.*

---

## 1. What is being installed

| Item | Value |
|---|---|
| Program | *the .exe name* |
| Version | *the version in your WPF .csproj* |
| Source | *this ship folder, at the commit tagged v<version>* |
| Replaces | *the previous version and its tag* |
| Kind of build | *framework-dependent `dotnet publish`* |

## 2. Where it goes

| Machine | What runs there | Folder |
|---|---|---|
| *panel PC* | *your panel* | *the folder, one per version* |
| *sensor computer, or the simulator on the lab PC* | *the sensor service* | |

*Say which previous release folder is kept for rollback.*

## 3. Before you start

- [ ] *every check, each with the command that proves it*

## 4. Steps

*Numbered. One action each. After each: "You should see ..." with the real output you saw.*

**Step 1.** *Run the tests.* You should see ...

**Step 2.** *Build the release folder with `dotnet publish`.* You should see ...

**Step 3.** *Read the version stamp:*

```
(Get-Item .\<your program>.exe).VersionInfo.ProductVersion
```

You should see ... *(paste what it printed on your machine)*

**Step 4.** *Copy the whole folder.* ...

**Step 5.** *Stop the old version.* ...

**Step 6.** *Start the new version.* You should see ...

## 5. Settings (data dictionary)

**Command line**

| Option | Type | Default | What it controls |
|---|---|---|---|
| | | | |

**Your settings file**

| Field | Type | Shipped value | What it controls |
|---|---|---|---|
| | | | |

**Version.** *Where it is written. One place.*

## 6. How to verify it worked

| # | Check | Expected |
|---|---|---|
| V1 | *read the version on screen* | |
| V2 | | |
| V3 | *a failure state, safely* | |

*Say who is allowed to cause the failure state, and that it changes no machine.*

## 7. If it goes wrong (contingency plan)

| You see | Cause | Do this |
|---|---|---|
| *nothing happens at start-up* | | |
| *a "cannot start" box* | | |
| | | |

**Rollback to <previous version>.**

1. *numbered steps, ending with reading the old version on screen*

## 8. Known limits

- *what this release does not do, on purpose, and why*
