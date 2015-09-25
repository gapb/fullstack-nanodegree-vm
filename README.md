Project 2 Submission - Gilbert Podell-Blume
===========================================

This is an attempt at a minimal implementation of the project. To run it,
navigate to vagrant/tournament. First, run `psql` and use it to run the
`tournament.sql` file. It will create the tournament database, connect to it,
and then populate it with the required tables as well as a few indices that I
hope improve the performance of the queries used by the program. After exiting
`psql`, run `tournament_test.py` using python.

tournament.py contains the required functions to facilitate a tournament
program. Theoretically, the `swissPairings()` function doesn't permit rematches,
but I have not modified the test scripts to confirm. `swissParings()` is messy,
and can be cleaned up and streamlined. That is on my todo list.

tournament_test.py contains the testing script for tournament.py. It's unchanged
from the version provided.

tournament.sql creates the database and tables the program needs to function.

My todo list (also a feature wish list to me for me) includes, but is not
limited to:

- cleaning up the comments,
- using properly formatted git commit messages,
- cleaning up `swissPairings()`,
- confirming that the indices actually do their jobs,
- confirming that the duplicate pairing detection works,
- creating a more sophisticated scoring system, as is used in *Magic: the
Gathering* tournaments,
- creating a more thorough testing script that additionally covers extra
features,
- and creating an actual program to run a tournament out of.

This program was developed and tested under Python 2.7.10 using PyCharm, as well
as under the provided Vagrant virtual machine.

rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses
