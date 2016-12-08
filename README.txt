=================================
   WELCOME TO THE GAME OF LYNE
=================================

LYNE is a puzzle game. The rules are simple: draw a line of each color from the
start to the end.

This version of LYNE has two main components: the generator and the solver.

The game always starts off with a tutorial that explains the basic rules of
LYNE, following which the player may choose between the two options.

Press ESC to quit.

=============
  GENERATOR
=============
The generator randomly generates new levels every time a puzzle is completed.
Every level has a random level of difficulty, can take on different sizes
ranging from 3 by 3 to a formidable 6 by 7, and can have up to 6 colors. Once a
puzzle is completed, a new one seamlessly slides in from the right.

The generator also comes with a slider that reveals itself when the mouse is
moved to the right edge of the screen. As the slider is dragged down, the
solution to the puzzle progressively reveals itself. This is to help players
that get stuck on especially hard puzzles, or for players that simply want to
watch extremely hard puzzles be instantaneously solved before their very eyes.

(NB. While not explicitly indicated within the game, the generator can generate
levels at 2 different difficulties. Press '1' for easier levels, and '2' for
harder levels.)


==========
  SOLVER
==========
The solver takes in a level, as specified by the user in the file "solve.txt",
and searches for a solution. Once a solution has been found, the game then
generates the puzzle itself, along with a functioning slider that reveals the
solution.

Once the puzzle is completed, a new randomly generated level slides in from the
right.


================
  DEPENDENCIES
================
This version of LYNE runs on Python 3, and requires PyGame and NumPy to be
installed.

You can get PyGame at http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame and
NumPy at https://pypi.python.org/pypi/numpy. You may also install them using
'pip install'.

Please download the appropriate files depending on your version of Python and
whether it is a 32-bit or 64-bit version.

===========
  CREDITS
===========
Original concept by Thomas Bowker. http://www.lynegame.com/
Get the game on Steam: http://store.steampowered.com/app/266010/

Airplane Ding Sound from Soundbible.com.
http://soundbible.com/1424-Air-Plane-Ding.html
Free for use under CC Sampling Plus 1.0 License.

All other code & assets by Colin Gay.
