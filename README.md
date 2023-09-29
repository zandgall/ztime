# ztime Application
Allows me to keep track of my day-to-day life, measuring and visualizing the amount of time I spend on different activities.

## ztime.py
A CLI application that allows quick command-line modification of time data. Also includes a visual output to an image file, which can be looked at to see a visual representation of the timeframe of data selected.
### COMMANDS:
| command | arguments | output | aliases |
| draw | begin[^1], end[^1][^2], width[^2] | Creates an image of time entries from the beginning time, to the end time (if not present, uses current time). The image will have a width of 3600, if width arg is not present. | &nbsp; |
| enter | type[^3], begin[^1], end[^1][^2] | Adds a time entry, with the name being (type), spanning from beginning to end, or the current time, if end isn't present. The command will then print the ID of the time entry created, which can be used to modify or remove this entry. | add |
| type | type[^3], color | Adds (type) to the type palette, assigning it the color given. Color should be a hex color string, with the '#' included. This color is used when drawing an image with the draw command. | &nbsp; |
| remove | id[^4] | Removes the entry with the ID provided | &nbsp; |
| modify | id[^4], type[^3], begin[^1], end[^1] | Modifies the entry with the ID provided, changing its type, begin, and end as given. | edit |
| list | start[^4], end[^4] | Lists all time entries with an ID between (start) and (end) inclusive. | &nbsp; |
| start | type[^3], start[^1][^2] | Marks the given type as 'running,' with the stop command, gives you the ability to mark the beginning and end of an activity in real time. If the (start) argument is present, uses that as the beginning time instead of the time the command was entered. | begin |
| stop | type[^3], end[^1][^2] | Stops a running type. Adds it as a time entry. If (end) argument is present, uses that as the end time instead of the time the command was run. | end |
| running | &nbsp; | Lists currently running types. | &nbsp; |

## ztime-cpp
A GUI application that allows the easy viewing of time entries. Letting you zoom in and out while retaining legibility, allowing you to thoroughly explore the data.
------
Soon I expect to integrate the ability to modify the time entries in the GUI program. Along with adding different ways to filter and view the data, including measuring tools.
