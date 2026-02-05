---
title: Introduction to Shell Assessment Items
output: html_document
description: Ten MultipleChoiceChallenge items aligned to Chapters 1–5 of Introduction to Shell.
---

## Interfaces to an OS

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A teammate says, "I never use the command line because Finder already lets me manage files." You want to clarify what the shell and a graphical file explorer have in common.

How should you describe the relationship between a graphical file explorer and a command-line shell?

`@options1`
- The shell can run programs, but file explorers cannot run programs
- The file explorer is built on top of the shell and uses shell commands
- The shell is part of the OS, while the file explorer is not software
- [Both are interfaces that issue commands to the operating system]

---

## Absolute versus relative

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You’re writing setup instructions for a teammate and want to avoid ambiguity about file locations.

What is the main benefit of using an absolute path (like `/home/repl/data`) instead of a relative path (like `data`)?

`@options1`
- It automatically creates the directory if it does not exist
- It always refers to a location from the filesystem root
- [It does not depend on the current working directory]
- It guarantees faster file access than a relative path

---

## Working directory meaning

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
Two developers run the same command, `cat notes.txt`. One sees the file contents, and the other gets “No such file or directory.” Both are sure `notes.txt` exists somewhere on the machine.

What is the most likely reason for the difference?

`@options1`
- The file was deleted before the second user ran it
- The file is corrupted on one machine but not the other
- The `cat` command behaves differently on different shells
- [They ran the command from different working directories]

---

## Moving between folders

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You are in `/home/repl/projects/analysis` and need to switch to `/home/repl/projects/data` without typing the full path.

Which command accomplishes this?

`@options1`
- `cd ./data`
- [ `cd ../data` ]
- `cd ../../data`
- `cd ../dataset`

---

## Copy versus move

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter1
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to place `report.csv` into a `backup/` directory, but you must keep the original file in your current directory because another script still reads it from there.

Which command should you use?

`@options1`
- `mv report.csv backup/`
- [ `cp report.csv backup/` ]
- `rm report.csv backup/`
- `cat report.csv > backup/`

---

## Viewing file contents

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You quickly want to print the entire contents of `course.txt` to the terminal to confirm it looks correct.

Which command is designed for that?

`@options1`
- `pwd course.txt`
- `cd course.txt`
- [ `cat course.txt` ]
- `ls course.txt`

---

## Paging output safely

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter2
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
A log file is too long to view comfortably with `cat`, and you want to scroll through it one page at a time and quit when you are done.

Which tool is intended for this?

`@options1`
- `mv`
- `cp`
- [ `less` ]
- `mkdir`

---

## Filtering with pipes

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You need to count how many lines in `server.log` contain the word `error`, and you want to do it without creating intermediate files.

Which symbol connects the output of one command to the input of another?

`@options1`
- `>`
- `<`
- `&`
- [ `|` ]

---

## Redirecting output to a file

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter3
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You run `ls` and want to save the command’s output into a new file named `files.txt` (overwriting it if it already exists).

Which operator should you use?

`@options1`
- [ `>` ]
- `|`
- `&&`
- `;`

---

## Wildcards in filenames

```yaml
type: MultipleChoiceChallenge
key:
unit: introduction-to-shell
subskill: chapter4
initial_difficulty: 0
item_writer_id: '999999999'
```

`@assignment1`
You want to select all files in the current directory that end with `.csv` without listing each filename explicitly.

Which pattern should you use?

`@options1`
- `.csv`
- `csv*`
- [ `*.csv` ]
- `*csv.`
