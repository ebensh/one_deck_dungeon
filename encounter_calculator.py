from copy import deepcopy
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint
from random import randint, seed, shuffle

from encounters import *
from odd_types import *
from odd_utils import *

def IsDieEligibleForBox(die_type, die_value, box):
  types_match = (die_type == box._die_type or
                 die_type == DieType.Black or
                 box._die_type == DieType.Any)
  value_sufficient = (die_value >= box._requirement or box._is_wide)
  return types_match and value_sufficient

# Generates lists that are each the same length as die_to_eligible_boxes (the
# number of rolled dice). The list contains the index of the box each die is
# assigned to, or None if the die was not assigned.
# is_box_wide is the length of the number of challenge boxes, and is populated
# with a True/False value representing whether that box is wide or not.
def GenerateAssignments(die_to_eligible_boxes, is_box_wide):
  if not die_to_eligible_boxes:
    yield []
  else:
    #possibilities = die_to_eligible_boxes[0]
    #if not possibilities: possibilities = [None]
    possibilities = [None] + die_to_eligible_boxes[0]
    for possibility in possibilities:
      remaining_dice = die_to_eligible_boxes[1:]
      if possibility and not is_box_wide[possibility]:
        # The box is small, so we need to filter it out from future assignment.
        remaining_dice = [[x for x in xs if x != possibility]
                          for xs in remaining_dice]
      for tail_assignment in GenerateAssignments(remaining_dice, is_box_wide):
        yield [possibility] + tail_assignment


# Assume all the dice are fixed (no skills will come into play).
# Try every legal assignment of dice, and take the minimum penalty.
#   We set the "cost" of a box to be 1.49*health + 1.0*time. This is
#   a simple way to say HH > HT > TT > H > T. We use 1.49 instead of
#   1.5 to handle cases like HHH (4.5) v HTTT (4.5) so that there's
#   a consistent ordering. The value is somewhat arbitrary as in the real
#   game this is situational.
def ConsequencesToCost(consequences):
  return -1.49 * consequences[ConType.Health] - consequences[ConType.Time]
      

# TODO: Create accessors to all "private" members accessed.
def main():
  seed(2)  # While debugging
  
  hero = Hero.Warrior()
  encounter = CombatEncounter.Skeleton()
  print hero, encounter
  challenge_boxes = encounter._challenge

  NUM_TRIALS = 1
  for trial in xrange(1, NUM_TRIALS + 1):
    rolled_dice = Roll(hero.GetDiceCounts())
    # Sort the rolled dice by type and value ascending.
    rolled_dice.sort(key=lambda kv: (kv[0].value, kv[1]))
    # Rolled dice arrangement is now fixed so that we can rely on indicies.
    print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)

    die_to_eligible_boxes = []
    for (die_type, die_value) in rolled_dice:      
      die_to_eligible_boxes.append(
        [box_ix for box_ix, box in enumerate(challenge_boxes)
         if IsDieEligibleForBox(die_type, die_value, box)])
    print rolled_dice
    print challenge_boxes
    print die_to_eligible_boxes

    possible_moves = []
    for assignments in GenerateAssignments(
        die_to_eligible_boxes, map(lambda box: box._is_wide, challenge_boxes)):
      box_sums = [0] * len(challenge_boxes)
      for die_ix, box_ix in enumerate(assignments):
        if box_ix is None: continue
        box_sums[box_ix] += rolled_dice[die_ix][1]

      are_boxes_satisfied = [box_sum >= box._requirement
                             for (box, box_sum) in zip(challenge_boxes, box_sums)]
      is_armor_satisfied = all([not box._is_armor or (box._is_armor and box_is_satisfied)
                                for (box, box_is_satisfied)
                                in zip(challenge_boxes, are_boxes_satisfied)])
      if not is_armor_satisfied:
        are_boxes_satisfied = [False] * len(are_boxes_satisfied)

      consequences = sum([box._consequences
                          for box, is_satisfied in zip(challenge_boxes, are_boxes_satisfied)
                          if not is_satisfied], Consequences())
      possible_moves.append((assignments, consequences))

    
    scored_moves = [(move, ConsequencesToCost(consequences))
                    for (move, consequences) in possible_moves]
    scored_moves.sort(key=lambda move_and_score: move_and_score[1])
    print "Worst 3 moves:"
    for move in scored_moves[:3]: print move
    print "Best 3 moves:"
    for move in scored_moves[-3:]: print move

    
if __name__ == '__main__':
  main()
