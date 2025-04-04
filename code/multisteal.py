# take in 2 or 3 words, plus single letters, on command line, 
# determine if they combine to make a multisteal, ie. combine 
# to form a new word.
# ex. python multisteal.py HAPPEN JOINT OVER U G N K
# should return list of steals, meaning all words formable
# using combinations of words and letters.

import sys

print("Argument List:", str(sys.argv))
args = len(sys.argv)

words = []
letters = []
for i in range(1, args) :
    if len(sys.argv[i]) > 1 :
        words.append(sys.argv[i])
    if len(sys.argv[i]) < 4 :
        letters.append(sys.argv[i])


print("words:")
print(words)
print("letters:")
print(letters)


