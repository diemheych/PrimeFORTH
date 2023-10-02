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
# Additional Words
A number of additional words have been included in the FORTH implementation, for example, to provide access to Prime graphics capability.

The additional words are summarised below.

- acos: return arccosine of n (n)
- asin: return arcsine of n (n)
- atan: return the arctangent of n (n)
- circle: draw a circle (x y radius)
- cls: clears the text and graphics (GROB 0) screens
- col: set the current colour (n)
- cos: return the cosine of n (n)
- dump: dump contents of stack to terminal window
- fillrect: draw a filled rectangle (x y w h)
- getcol: return the current colour
- getpix: return pixel colour (x y)
- getpix2: return pixel colour (x y)
- getpix4: return pixel colour (x y)
- int: truncate number (eg floating point)
- key: wait for keyboard input
- lastkey: return last key pressed
- line: draw a line (x1 y1 x2 y2)
- list: display FORTH file
- load: load FORTH file
- pixon: turn on pixel (x y)
- pixon2: turn on scaled pixel (x y)
- pixon4: turn on scaled pixel (x y)
- random: return random number between 0 and n-1 (n)
- rect: draw a rectangle (x y w h)
- sin: return sine of n (n)
- sleep: sleep for n milliseconds (n)
- sqrt: return square root of n (n)
- tan: return tangent of n (n)
- ticks: return the HP Prime millisecond timer
- words: list all available words
- sleep: pause program for a number of milliseconds (n)

Graphics commands use Prime pixel co-ordinates where 0,0 is the top left of the screen.
Scaled pixel commands double or quadruple the pixel size and similarly scale x and y down by the same amount (for example, Snake game uses pixon4 and getpix4).
