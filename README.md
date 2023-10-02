# ztime Application

Allows me to keep track of my day-to-day life, measuring and visualizing the amount of time I spend on different activities.

## ztime.py

A CLI application that allows quick command-line modification of time data. Also includes a visual output to an image file, which can be looked at to see a visual representation of the timeframe of data selected.

### COMMANDS:

| command | arguments | output | aliases |
| --- | --- | --- | --- |
| draw | begin time[^1], end time, width* filters...* | Creates an image of time entries from the beginning time, to the end time (if not present, uses current time). The image will have a width of 3600, if width arg is not present. If there are any filters, (which includes if argument 3 is not a number), only tags included in the filters list will be drawn.| &nbsp; |
| enter | type[^2], begin time, end time* | Adds a time entry, with the name being (type), spanning from beginning to end, or the current time, if end isn't present. The command will then print the ID of the time entry created, which can be used to modify or remove this entry. | add |
| type | type, color[^3] | Adds (type) to the type palette, assigning it the color given. Color should be a hex color string, with the '#' included. This color is used when drawing an image with the draw command. | &nbsp; |
| remove | id[^4] | Removes the entry with the ID provided | &nbsp; |
| modify | id, type, begin, end | Modifies the entry with the ID provided, changing its type, begin time, and end time as given. | edit |
| list | start, end, filter* | Lists all time entries with an ID between (start) and (end) inclusive. If filter is present, only lists entries with the same name as (filter). | &nbsp; |
| start | type, start* | Marks the given type as 'running,' with the stop command, gives you the ability to mark the beginning and end of an activity in real time. If the (start) argument is present, uses that as the beginning time instead of the time the command was entered. | begin |
| stop | type, end* | Stops a running type. Adds it as a time entry. If (end) argument is present, uses that as the end time instead of the time the command was run. | end |
| running | &nbsp; | Lists currently running types. | &nbsp; |

*\*optional*
[^1]: This argument is a time. It will be parsed from a human readable format. The user can enter "8am" or "9/26/2023 16:45" if they choose.
[^2]: This argument is a type. Simply the name of an activity for whatever time entry you are starting, stopping, adding, or modifying.
[^3]: Colors are hex strings. In the form "#rrggbb" where rr (reg), gg (green), and bb (blue), are given in hexadecimal.
[^4]: This argument is an ID. IDs are given when a time entry is created. However you can also use the (list) command in order to see time entries and their IDs.

## ztime-cpp:

A GUI application that allows the easy viewing of time entries. Letting you zoom in and out while retaining legibility, allowing you to thoroughly explore the data.

------
Soon I expect to integrate the ability to modify the time entries in the GUI program. Along with adding different ways to filter and view the data, including measuring tools.
