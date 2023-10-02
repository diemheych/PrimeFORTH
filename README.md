# PrimeFORTH
A simple version of FORTH written in Python for the HP Prime calculator.

Features include:
- graphics
- floating point support
- ability to load FORTH files
  
Example FORTH files included for N-Queens and a simple graphical game, Snake.

See a demonstration at: https://www.youtube.com/watch?v=ILMbia3-VZo
# Installation
Use the HP Connectivity Kit to transfer FORTH.hpprgm to a virtual or physical HP Prime calculator.

Note: the HP Prime must be running firmware that supports Python (actually MicroPython).
# Source
FORTH.py includes the source code and the PPL wrapper for execution on the HP Prime. The source can be loaded into the HP Connectivity Kit, modified if required, and dragged onto a virtual or physical HP Prime calculator.
# Examples
To use the example FORTH files (or your own FORTH in a text file with .fth extension), add the files to the Python environment of the HP Prime calculator. In the HP Connectivity Kit, browse to the appropriate calculator, Application Library, Python and Files to see the files already loaded into Python. Right click on Files and select Add File and browse to the text file with .fth extension. Click save and the FORTH file can now be accessed from Prime FORTH with 'list' to view the contents or 'load' to load the file.
