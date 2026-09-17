# A Release You Can Install
---
## Slide 1: Friday, the panel PC, and a USB drive
- The shift lead wants the new build today
- You copy the program to a USB drive
- You double-click it beside the oven
- Nothing happens. No window, no message.
Speaker notes: Picture this. It is Friday. The panel PC beside the oven needs your new build. You copy the program onto a USB drive, walk it over, and double-click it. Nothing happens. No window. No error. Nothing at all. By the end of today you will know exactly why, and your implementation plan will say what to do about it.
Image: A USB drive beside a dark touch screen on a shop-floor post.
---
## Slide 2: Your panel has never been released
- It runs with dotnet run, from source
- That needs the SDK, your folder, and you
- A release runs without any of those
Speaker notes: Everything you have done with the panel so far used dotnet run. That works because your PC has the SDK, your source code, and you sitting in front of it. The panel PC has none of those. A release is what runs when you are not there.
Image: Two columns: a developer laptop with source files, and a bare panel PC with only a program folder.
---
## Slide 3: A release has three parts
- A built program folder, from dotnet publish
- One version number, written once
- Written steps anyone can follow and check
Speaker notes: Three parts, and you need all three. A built folder, not source. One version number, written in one place and shown on the screen. And an implementation plan, which you met in 145060, where every step says what you should see. Miss any one, and nobody can say what is installed.
Image: Three stacked blocks labeled folder, version, plan, in navy.
---
## Slide 4: The version lives in one place
```xml
<PropertyGroup>
  <OutputType>WinExe</OutputType>
  <TargetFramework>net8.0-windows</TargetFramework>
  <UseWPF>true</UseWPF>
  <Version>1.0.0</Version>
</PropertyGroup>
```
Speaker notes: This is the only place the version is written. The build stamps it into the program file. Your header reads it back. Your change log and your plan must agree with it, and ShipCheck will check that they do.
Image: None. This slide is code.
---
## Slide 5: The program reads its own stamp
```csharp
string? stamp = typeof(Program).Assembly
    .GetCustomAttribute<AssemblyInformationalVersionAttribute>()?
    .InformationalVersion;

Console.WriteLine($"Stamped: {stamp}");
Console.WriteLine($"Shown:   {Shown(stamp)}");
```
Speaker notes: One line of reflection reads the version the build stamped in. With version 1.0.1 in the project file, this printed Stamped 1.0.1. Inside a Git repository the SDK can add a plus sign and the commit id, so the panel shows only the part before the plus.
Image: None. This slide is code.
---
## Slide 6: Build the release folder
```
dotnet publish Line3.Hmi.Panel -c Release -o ..\release\Line3Panel-1.0.1
```
Speaker notes: Publish builds the program and gathers everything it needs into one folder. On the build PC that folder held nine files: the exe, two dlls, their pdb files, two json files that describe the program, and the two thresholds files. Every one of them is part of the release. The release folder is build output, so it goes in your gitignore.
Image: None. This slide is code.
---
## Slide 7: Check the stamp before you carry it
```
(Get-Item .\Line3.Hmi.Panel.exe).VersionInfo.ProductVersion

1.0.1+557a56c22322f8a1709ad88c85e68b3a93d9e874
```
Speaker notes: This PowerShell line reads the stamp from the program file itself. On the build PC it printed 1.0.1, a plus sign, and the commit id. Your commit id will differ. The part before the plus must match your project file. This is the first verification step in your plan.
Image: None. This slide is code.
---
## Slide 8: The wrong way: copy only the exe
```
The application to execute does not exist: '...\Line3.Hmi.Panel.dll'.
```
Speaker notes: Here is why nothing happened on Friday. The exe is only a launcher. Your code is in the dll beside it. Double-clicked, it shows nothing at all. Started from a terminal, it prints this line and exits with code 0x8000809A. Copy the whole folder, every time, and put this row in your contingency table.
Image: None. This slide is code.
---
## Slide 9: Why the wrong way is tempting
- The exe looks like the program
- dotnet run hides every file it needs
- "It runs" starts to mean "it ships"
Speaker notes: On your own PC, double-clicking the exe in bin works, because every file it needs is sitting next to it. dotnet run hides the build completely. So it is natural to think the exe is the program. On a different machine, that belief costs you a Friday.
Image: A bin folder with one file highlighted and the rest faded out.
---
## Slide 10: What you are about to build
- Build 1: ShipCheck Part 1, one version everywhere
- Build 2: version on your header, a real release folder
- Then: your implementation plan, with real output
- Rollback: keep the previous folder
Speaker notes: In Build 1 you write the part of ShipCheck that checks your project, your change log, and your plan agree on one version. In Build 2 you put the version on your own header, publish a real release folder, read its stamp, start it from that folder, and write your implementation plan with the output you actually saw. Keep every release folder. The previous one is your rollback.
Image: A terminal with a version stamp beside an open implementation plan.
