# take input as current state of stealwords game, as:
#
# player-owned words
# center letters
# other stored data relating to these, such as:
# word extensions (computed from edges to some depth)
#
# and one additional move that is used to update state:
# which can be one letter flip in center, or
# one steal which combines some player words and letters.
#
# update should account for all new state properties
#
# new move is either a letter flip or a steal.
# in case of letter flip, the new state only has to
# update letters in the center
# in case of steal, the new state updates for fewer 
# letters in center, fewer player owned words, (when
# either of those happens) and new player owned word.
# word extensions can also be updated.


