import csv
import sys
#from pprint import pprint
#from random import seed, shuffle

from encounters import *
from odd_types import *
from odd_utils import *

def IsDieEligibleForBox(die_type, die_value, box):
  types_match = (die_type == box._die_type or
                 die_type == DieType.Black or
                 box._die_type == DieType.Any)
  value_sufficient = (die_value >= box._requirement or box._is_wide)
  return types_match and value_sufficient

def GetDieToBoxPossibilities(rolled_dice, challenge_boxes):
  die_to_eligible_boxes = []
  for (die_type, die_value) in rolled_dice:      
    die_to_eligible_boxes.append(
      [box_ix for box_ix, box in enumerate(challenge_boxes)
       if IsDieEligibleForBox(die_type, die_value, box)])
  return die_to_eligible_boxes

def GetConsequences(rolled_dice, challenge_boxes, assignments):
  # Figure out how much (numerically) we have assigned to each challenge box.
  box_sums = [0] * len(challenge_boxes)
  for die_ix, box_ix in enumerate(assignments):
    if box_ix is None: continue
    box_sums[box_ix] += rolled_dice[die_ix][1]

  # Figure out which boxes are numerically satisfied.
  are_boxes_satisfied = [box_sum >= box._requirement
                         for (box, box_sum) in zip(challenge_boxes, box_sums)]
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

def GetAverageConsequences(dice_counts, challenge_boxes):
  average_consequences = Consequences()
  NUM_TRIALS = 1000
  for trial in xrange(1, NUM_TRIALS + 1):
    rolled_dice = Roll(dice_counts)
    # Sort the rolled dice by type and value ascending.
    rolled_dice.sort(key=lambda kv: (kv[0].value, kv[1]))
    # Rolled dice arrangement is now fixed so that we can rely on indicies.
    #print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)
    
    die_to_eligible_boxes = GetDieToBoxPossibilities(rolled_dice,
                                                     challenge_boxes)
    
    # Create a list of all the possible assignments and their consequences.
    possible_assignments = []
    for assignments in GenerateAssignments(
        die_to_eligible_boxes, map(lambda box: box._is_wide, challenge_boxes)):
      consequences = GetConsequences(rolled_dice, challenge_boxes, assignments)
      possible_assignments.append((assignments, consequences))
      
    # Sort the possible moves using a cost function.
    possible_assignments.sort(key=lambda move_and_consequences: \
                              ConsequencesToCost(move_and_consequences[1]))

    # Record this trial's best move's consequences and cost
    best_move, consequences = possible_assignments[-1]
    average_consequences += consequences

    # After all the trials are done, output an average cost.
    #print "Average consequences of encounter:"
    #for key, value in average_consequences.iteritems():
    #  print key, float(value) / NUM_TRIALS
  for key in average_consequences:
    average_consequences[key] = float(average_consequences[key]) / NUM_TRIALS
  return average_consequences
  

# TODO: Create accessors to all "private" members accessed.
def main():
  heroes = [Hero.Archer(), Hero.Mage(), Hero.Paladin(), Hero.Rogue(),
            Hero.Warrior()]
  encounters = GetEncounterCards()

  with sys.stdout as csvfile:
    fieldnames = ['encounter', 'experience']
    for hero in heroes:
      fieldnames.append(hero._name + '_health_dmg')
      fieldnames.append(hero._name + '_time_dmg')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for encounter_ix, encounter in enumerate(encounters):
      for hero_ix, hero in enumerate(heroes):
        
        # TODO: Replace private member access with accessors
        consequences = None
        if type(encounter) is CombatEncounter:
          consequences = GetAverageConsequences(
            hero.GetDiceCounts(), encounter._challenge)
          writer.writerow({'encounter': encounter._name,
                           'experience': encounter.AsExperience(),
                           hero._name + '_health_dmg': consequences[ConType.Health],
                           hero._name + '_time_dmg': consequences[ConType.Time]})
        elif type(encounter) is PerilEncounter:
          free_consequences = GetAverageConsequences(
            hero.GetDiceCounts(), encounter._free_challenge)
          paid_consequences = GetAverageConsequences(
          hero.GetDiceCounts(), encounter._paid_challenge) + encounter._swap_cost
          writer.writerow({'encounter': encounter._name + '_free',
                           'experience': encounter.AsExperience(),
                           hero._name + '_health_dmg': free_consequences[ConType.Health],
                           hero._name + '_time_dmg': free_consequences[ConType.Time]})
          writer.writerow({'encounter': encounter._name + '_paid',
                           'experience': encounter.AsExperience(),
                           hero._name + '_health_dmg': paid_consequences[ConType.Health],
                           hero._name + '_time_dmg': paid_consequences[ConType.Time]})                            
    
if __name__ == '__main__':
  main()
