This project contains python scripts which do some of the following:

- convert files from Collins dictionary in dict/ into word files based on
length of word.  Each line in these files, such as 2sort.txt etc., gives
the alphabetized string and the word, separated by a comma.  These files
are useful for quick look-ups of words based on the alphabetized string.

- convert *sort.txt files into nodes, listing only the alphabetized string
with no duplicates for multiple words, into *nodes.txt files.

- generate *edges.txt with various scripts.  For example 2-3-edges.txt
contains all directed edges consisting of a 2-node and a 3-node where the
edge points to the 3-node and there must be at least one word that can
be formed by adding one letter to the 2-node.  Equivalently, the 2-node
letters are contained in (with multiplicities) the 3-node letters. The
information is summarized by one line per 2-node followed by ; and then
all additional letters that lead to a 3-node, as a comma-separated list.

One can generate paths from a 2-node to a 4-node by using all paths that
go from the 2-node to any 3-node (adding one letter of the two) and then
to the 4-node (adding the remaining letter).  But it also possible to
have the addition of 2 letters neither of which can be added to the
2-node to make a 3-node.  In this case we put an edge indicating this
information into 2-4-edges.txt.  Similarly, all files n-m-edges.txt with
m-n > 1 contain only such edges which can be realized by a path using
edges other nodes.  Call the number of letters to be added by an edge
the "weight" of that edge, which is m-n.  Then any edge in n-m-edges.txt
gives the unique path from n-node to m-node.

Note: code files have been put into code/ after initially running on
data files which have been put into nodes/ dict/ and edges/.  To rerun
those scripts would mean to change some lines to point at the correct 
directories or move data and scripts back into one directory.

The scripts edges2.py, edges3.py, edges4.py, were written to tackle the
cases with m-n=2,3, and 4, gradually leading up to edges5.py for m-n=5 
being general enough to tackle all higher cases.  These took time to run
from under 5 seconds up to about 5 minutes. In some cases the files have
no edges to report, specifically 2-11-edges.txt through 2-15-edges.txt.
2-10-edges.txt has only two edges in it.  3-15-edges.txt has only 3.






