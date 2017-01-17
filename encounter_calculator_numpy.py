import cProfile
from collections import defaultdict
from copy import deepcopy
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pprint import pprint
from random import randint, seed, shuffle
import sys

from encounters import *
from odd_types import *
from odd_utils import *

def AssignmentAsStr(assignment, rolled_dice, challenge_boxes):
  # Get the list of dice that are unassigned.
  unassigned_dice = np.logical_not(assignment.any(axis=1)).nonzero()[0]
  # Get the box indicies that each die is assigned to.
  die_to_box_indicies = assignment.argmax(axis=1)
  # Flip the lookup for easier access.
  box_to_dice = defaultdict(list)
  for die_ix, box_ix in enumerate(die_to_box_indicies):
    if die_ix in unassigned_dice: continue
    box_to_dice[box_ix].append(rolled_dice[die_ix])
  return [(box, box_to_dice[box_ix])
          for (box_ix, box) in enumerate(challenge_boxes)]
    

def IsDieEligibleForBox(rolled_die, box):
  die_type, die_value = rolled_die
  types_match = (die_type == box._die_type or
                 die_type == DieType.Black or
                 box._die_type == DieType.Any)
  value_sufficient = (die_value >= box._requirement or box._is_wide)
  return types_match and value_sufficient

def GetDiceToBoxPossibilities(rolled_dice, challenge_boxes):
  die_to_eligible_boxes = []
  for rolled_die in rolled_dice:      
    die_to_eligible_boxes.append(
      [box_ix for box_ix, box in enumerate(challenge_boxes)
       if IsDieEligibleForBox(rolled_die, box)])
  return die_to_eligible_boxes

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

# Converts from a list of die -> box mapping to one-hot matrix rows.
def AssignmentListToAssignmentMatrix(assignment_list, num_boxes):
  assignment = np.zeros((len(assignment_list), num_boxes), dtype=bool)
  for die_ix, box_ix in enumerate(assignment_list):
    if box_ix:
      assignment[die_ix,box_ix] = True
  return assignment

def GetConsequences(challenge_boxes, box_requirements, box_sums):
  # Figure out which boxes are numerically satisfied.
  boxes_satisfied = box_sums >= box_requirements
  # Have we satisfied all the armor boxes?
  is_armor_satisfied = all(
    [not box._is_armor or (box._is_armor and box_is_satisfied)
     for (box, box_is_satisfied)
     in zip(challenge_boxes, are_boxes_satisfied)])
  
  # If we haven't satisfied any armor box, then no boxes are satisfied.
  if not is_armor_satisfied:
    are_boxes_satisfied = [False] * len(are_boxes_satisfied)

  return sum([box._consequences
              for box, is_satisfied in zip(challenge_boxes, are_boxes_satisfied)
              if not is_satisfied], Consequences())


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
  #hero = Hero.Warrior(); encounter = CombatEncounter.Skeleton()  # Armored
  hero = Hero.Mage(); encounter = CombatEncounter.FireElemental()  # Wide box
  print hero, encounter
  challenge_boxes = encounter._challenge

  seed(2)

  # Row vector of maximum number of dice that can be assigned to a box
  max_assignment = np.array([1 if not box._is_wide else 999
                             for box in challenge_boxes])
  # Row vector, scalar requirement of each box.
  box_requirements = np.array([box._requirement for box in challenge_boxes])
  # Row vector, boolean of whether the box is wide or not.
  boxes_wide = np.array([box._is_wide for box in challenge_boxes])
  # Row vector, boolean of whether the box is armored or not.
  boxes_armored = np.array([box._is_armor for box in challenge_boxes])
  # Row vectors, health and time damage per box.
  box_consequences_health = np.array([box._consequences[ConType.Health]
                                      for box in challenge_boxes])
  box_consequences_time = np.array([box._consequences[ConType.Time]
                                    for box in challenge_boxes])

  average_consequences = Consequences()
  NUM_TRIALS = 100
  for trial in xrange(1, NUM_TRIALS + 1):
    rolled_dice = Roll(hero.GetDiceCounts())
    # Sort the rolled dice by type and value ascending.
    rolled_dice.sort(key=lambda kv: (kv[0].value, kv[1]))
    # Rolled dice arrangement is now fixed so that we can rely on indicies.
    print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)

    # Repeated column vector of dice values (matrix)
    dice_values =  np.array([die_value for (die_type, die_value) in rolled_dice]).repeat(len(challenge_boxes)).reshape(len(rolled_dice), len(challenge_boxes))

    dice_to_eligible_boxes = GetDiceToBoxPossibilities(rolled_dice, challenge_boxes)
    possible_assignments = []
    for assignment_list in GenerateAssignments(dice_to_eligible_boxes, boxes_wide):
      assignment = AssignmentListToAssignmentMatrix(assignment_list, len(challenge_boxes))
      #enumerate(itertools.product(*dice_to_eligible_boxes)):
      assignment = np.vstack(assignment)  # Make it into a mask matrix
      if np.any(assignment.sum(axis=0) > max_assignment):
        continue  # Too many dice assigned to a box, invalid assignment
      
      box_sums = (assignment * dice_values).sum(axis=0)
      boxes_unsatisfied = box_sums < box_requirements
      if np.any(boxes_unsatisfied * boxes_armored):
        boxes_unsatisfied.fill(True)

      consequences = Consequences(health=np.sum(box_consequences_health * boxes_unsatisfied),
                                  time = np.sum(box_consequences_time * boxes_unsatisfied))
      #print assignment, AssignmentAsStr(assignment, rolled_dice, challenge_boxes), consequences
      possible_assignments.append((assignment, consequences))

    # Sort the possible moves using a cost function.
    possible_assignments.sort(key=lambda move_and_consequences: ConsequencesToCost(move_and_consequences[1]))

    #print "Worst 3 moves:"
    #for move,consequnces in possible_assignments[:3]: print AssignmentAsStr(move, rolled_dice, challenge_boxes)
    #print "Best 3 moves:"
    #for move,consequences in possible_assignments[-3:]: print AssignmentAsStr(move, rolled_dice, challenge_boxes)

    # Record this trial's best move's consequences and cost
    best_move, consequences = possible_assignments[-1]
    average_consequences += consequences

  # After all the trials are done, output an average cost.
  print "Average consequences of encounter:"
  for key, value in average_consequences.iteritems():
    print key, float(value) / NUM_TRIALS
    
if __name__ == '__main__':
  main()
