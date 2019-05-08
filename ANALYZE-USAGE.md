The 'analyze.py' is a Python program to analyze the CSV file containing
the result of the Google Form of the MPI International Survey.

- Build
Run the shell script 'build.sh' to create 'analyze.py'

- Analysis

usage: analyze.py <OPTIONS> <CSV_FILE> [<CSV_FILE> ...]  
       - `-h` show this help message and exit  
       - `-t` draw a time-series graph  
       - `-e` show events in the time-series graph  
       - `-s <Q> ...` draw a simple analysis graph of the specified
       question. Or 'all' to draw graphs on all questions  
       - `-c <Q0>,<Q1> ...` draw a cross-tab analysis graph on the
       pair of specified questions. Or, 'all' to draw graphs on all
       possible combinations  
       - `-m <N>` threshold of number of answers to be a major region  
       - `-f <FORMAT>` if specified, 'eps', 'pdf', or 'png', create
       file(s) in the specified format instead of showing graph(s)  
       - `-o <OUTDIR>` if specified, the output file(s) are created
       under the specified directory  

- Authors
  - Atsushi Hori (Riekn-CSS)  
  - George Bosilca (UTK)  

-Date
2019, April

Beware:
- all countries name will be stripped of all accents

