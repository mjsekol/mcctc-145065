# Three Interfaces, Three Versions
---
## Slide 1: "It's one line in the file"
- The shift lead wants a warning at 225 C
- Maintenance says it is one line
- Every panel reads that file
- Nobody's compiler reads it
Speaker notes: The shift lead wants a yellow warning when the oven passes 225, before the 230 alarm. Maintenance says no problem, it is one line in the limits file. Here is the thing. Every panel on the floor reads that file, and no compiler anywhere checks it. So what does that one line actually do?
Image: A thresholds file on a clipboard with one line circled in launch red.
---
## Slide 2: Your panel has more than one interface
- The reading contract with the Pi
- The thresholds file and its schema_version
- The words on the screen
- The command line, and the release itself
Speaker notes: An interface is anything outside your code that depends on it staying the same. Your panel has five. The reply format from the Pi. The limits file, which has its own format version. The words operators were trained on. The command line in the shortcut. And the release number. Before any change, ask which one it touches.
Image: A panel in the middle with five labeled arrows to the Pi, a file, an operator, a shortcut, and a version tag.
---
## Slide 3: A baseline is the version everyone agreed on
```
git tag -a v1.0.0 -m "Baseline: the version the shift lead is trained on"
git push origin v1.0.0
```
Speaker notes: Today you set your baseline. It is the version the shift lead is trained on tomorrow, and every later change is measured against it. An annotated tag records who tagged it and when. Remember from 145060: git push alone does not send tags. Push the tag by name.
Image: None. This slide is code.
---
## Slide 4: The new key, on a 1.0.0 panel
```
File: cr-a-extra-key.json
LOADED   3 sensors, stale after 5 s
         oven-temp        Limits 190.0 to 230.0 C
Ignored by a 1.0.0 panel: warn_high (oven-temp)
```
Speaker notes: This is the real result from the lab's probe, shortened to the oven line. The old panel starts normally. It shows no warning. It says nothing. Its loader asks for the keys it knows and never looks at the rest. The last line is the probe talking. The panel itself would stay silent.
Image: None. This slide is code.
---
## Slide 5: The same key, with schema_version 2
```
File: cr-b-schema-2.json
REFUSED  schema_version is 2; this panel reads version 1.
```
Speaker notes: Same change, but the file now says it is format version 2. The old panel refuses to start, with a sentence. That is less convenient and much safer. Nobody believes in a warning on a panel that cannot show one. The cost goes in the plan: update every panel before the new file goes out.
Image: None. This slide is code.
---
## Slide 6: The wrong way: a new positional parameter
```
Program.cs(2,17): error CS7036: There is no argument given that corresponds to the required parameter 'WarnHigh' of 'Limit.Limit(string, double?, double?, double?)'
```
Speaker notes: In C#, adding the warning as a fourth positional parameter of the record breaks every existing call. Inside one program that is the kind wrong. The compiler's list of errors is your impact analysis. An init property instead keeps every old call compiling. The dangerous changes are the ones no compiler sees.
Image: None. This slide is code.
---
## Slide 7: The change nobody catches
- Rename the oven's high key in the file
- The 1.0.0 panel loads it without complaint
- The oven tile says Low limit 190.0 C
- A hot oven never alarms again
Speaker notes: In the lab you will find this one yourself. A tidy rename of one key, on the oven only. The panel starts. The limits line quietly loses its high limit. From then on, an overheating oven shows NORMAL. No error anywhere. This is the design that works today, and it is the one that hurts someone.
Image: An oven tile showing NORMAL with a thermometer beside it reading far too high.
---
## Slide 8: Why it is tempting
- Files do not feel like interfaces
- The compiler taught you to trust silence
- One program, but several version numbers
Speaker notes: A settings file feels like data, not like an interface, but it has more readers than most classes. In C#, no errors usually means no problem, so silence feels safe. And it is tempting to think a project has one version, when its file format has a version of its own.
Image: A quiet control room with a single unnoticed warning light.
---
## Slide 9: Classify, predict, then change
- Which interface does it touch?
- Predict the impact before any edit
- Compatible or breaking, for each reader
- Version numbers follow the answer
Speaker notes: Here is the habit. First, name the interface. Second, write your prediction and commit it before you touch anything. Third, decide for each reader whether the change is compatible or breaking. Only then pick the version numbers, one for the program and, if the file format changed, one for the file.
Image: Four numbered steps in a row, navy boxes.
---
## Slide 10: What you are about to build
- Build 1: Lab U09-02, predict then measure five files
- Build 2: tag v1.0.0 and write your change log
- Your change impact note, with your five interfaces
- Tomorrow, the shift lead trains on this baseline
Speaker notes: In Build 1 you predict what a 1.0.0 panel does with five limits files, commit the predictions, then run the probe and find out. In Build 2 you tag your baseline, start your change log, and write the first part of your change impact note: your baseline and your interfaces. Tomorrow, the shift lead trains on exactly this version.
Image: A Git tag labeled v1.0.0 beside an open change log.
