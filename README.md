TableBuilder for Python
=======================
[![Build Status](https://travis-ci.org/vedosis/tablebuilder-python.svg?branch=master)](https://travis-ci.org/vedosis/tablebuilder-python)
[![codecov](https://codecov.io/gh/vedosis/tablebuilder-python/branch/master/graph/badge.svg)](https://codecov.io/gh/vedosis/tablebuilder-python)

A spiritual API port of Symfony's Console Helper Class [Table](http://symfony.com/doc/current/components/console/helpers/table.html) 
for [click](http://click.pocoo.org). There are a few augmentations and improvements but it sticks 
to the concept of building simplistic APIs with advanced options.

Building a Basic Table
----------------------
All column widths default to "exact width". Iterating over the rows to identify the widest entry.
```python
from tablebuilder import Table

table = Table()
table.headers = ['ISBN', 'Title', 'Author']
table.rows = [
    ['99921-58-10-7', 'Divine Comedy', 'Dante Alighieri'],
    ['9971-5-0210-0', 'A Tale of Two Cities', 'Charles Dickens']
]
table.render()
```
```
+===============+======================+=================+
| ISBN          | Title                | Author          |
+===============+======================+=================+
| 99921-58-10-7 | Divine Comedy        | Dante Alighieri |
| 9971-5-0210-0 | A Tale of Two Cities | Charles Dickens |
+===============+======================+=================+
```
Column Widths
-------------
Column widths can be modified by
```python
table.column_widths = [0, None, None]
table.column_widths[1] = 35
table.render()
```
```
+===============+=====================================+========================+
| ISBN          | Title                               | Author                 |
+===============+=====================================+========================+
| 99921-58-10-7 | Divine Comedy                       | Dante Alighieri        |
| 9971-5-0210-0 | A Tale of Two Cities                | Charles Dickens        |
+===============+=====================================+========================+
```
|Value|Intention|
|---:|:---|
|`None`|All columns that are marked this way are scaled to the best fit. The remaining console width (as understood by `click.get_terminal_size()`) is split evenly.|
|`0`|Exact fit
|`int`|Columns will be padded to this width (includes padding) or truncated to this width|
|`float`|Columns will be a percentage of the remaining space from strictly set column widths. i.e. `40.5 = 45.0%`, `0.5 = 1/2%`|

Styling
-------
### Table Separator
```python
table.rows.append(TableSeparator())
table.rows.append(['80-902734-1-6', 'And Then There Were None Is A Really Long Title', 'Agatha Christie'])
table.rows.append(['960-425-059-0', 'The Lord of the Rings', 'J. R. R. Tolkien'])
table.render()
```
```
+===============+===========================+========================+
| ISBN          | Title                     | Author                 |
+===============+===========================+========================+
| 99921-58-10-7 | Divine Comedy             | Dante Alighieri        |
| 9971-5-0210-0 | A Tale of Two Cities      | Charles Dickens        |
+===============+===========================+========================+
| 80-902734-1-6 | And Then There Were None  | Agatha Christie        |
|               | Is A Really Long Title    |                        |
| 960-425-059-0 | The Lord of the Rings     | J. R. R. Tolkien       |
+===============+===========================+========================+
```
### Padding and Border Characters
```python
table.padding = 2
table.padding_char = "."
table.borders.horizontal_char = u'\u2501'
table.borders.vertical_char = u'\u2503'
table.borders.crossing_char = u'\u254B'
table.render()
```
```
╋━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━╋
┃..ISBN...........┃..Title......................┃..Author..................┃
╋━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━╋
┃..99921-58-10-7..┃..Divine Comedy..............┃..Dante Alighieri.........┃
┃..9971-5-0210-0..┃..A Tale of Two Cities.......┃..Charles Dickens.........┃
╋━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━╋
┃..80-902734-1-6..┃..And Then There Were None...┃..Agatha Christie.........┃
┃.................┃..Is A Really Long Title.....┃..........................┃
┃..960-425-059-0..┃..The Lord of the Rings......┃..J. R. R. Tolkien........┃
╋━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━╋
```

Limitations and Roadmap
-----------------------
#### Generators
Current logic requires all data to be converted to a list for width
comparisons and justifications. This will be fixed in the future to require
fixed widths for data from a generator but also allow for use of generators
#### Terminal Width
`click.get_terminal_width` is good. Really good, but not perfect. Because
that is the primary mechanism for determining column width, some variation
occur and a 80x24 grid is assumed.
#### Colors
`click.style` is not support because it adds extra characters to the string
and messes with the widths. I'll fix that but it's a current limitation.
#### Generic Styles
Support for a standard set of styles ("Condensed", "Borderless", "Default",
 etc.) is on the Road Map.
#### Intelligent Column Reduction
Right now the process for reducing the column widths (if the columns are 
wider than the display width) is to reduce the `None` columns, then all
columns with `0`'s for width and then `float` columns. Finally there's 
a general reduction on all widths. It'd be nice if there could be a more
intelligent breaking up of the columns to give the nicest display to the
user.
#### Other stuff
checkout `tests/cli.py`. This is the file that is determining my Behaviorial
Expectations. Feel free to write a new request there and I'll try and figure
it out.