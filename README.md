# exapunks

A library for manipulating exapunks savefiles and redshift projects.

Main features:
 - Read and parse a .solution file
 - Edit and access all fields
 - Save a solution into a .solution file readable by the game

## DISCLAIMER:

Back up all files you manipulate with this software. I take no responsibility for any damage caused by the usage of this software.

## Usage

Example: Reading and saving a .solution file with an edited name:

```python
from exapunks.solution import Solution

sol = Solution.from_file("file.solution")

sol.solution_name = "New and cool name"

sol.to_file("newfile.solution")
```

## Installation

idk how python works