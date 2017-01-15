import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint
from random import randint, seed, shuffle

from encounters import *
from odd_types import *
from odd_utils import *

# TODO: Create accessors to all "private" members accessed.
def main():
  seed(2)  # While debugging
  
  hero = Hero.Warrior()
  encounter = CombatEncounter.Skeleton()
  print hero, encounter

  # Assume all the dice are fixed (no skills will come into play).
  # Try every legal assignment of dice, and take the minimum penalty.
  #   We set the "cost" of a box to be 1.49*health + 1.0*time. This is
  #   a simple way to say HH > HT > TT > H > T. We use 1.49 instead of
  #   1.5 to handle cases like HHH (4.5) v HTTT (4.5) so that there's
  #   a consistent ordering. The value is somewhat arbitrary as in the real
  #   game this is situational.
  def box_cost(box):
    return (1.49 * box._consequences[ConType.Health] +
            box._consequences[ConType.Time])
  def box_priority(box):
    return 1000 * box_.is_armor + box_cost(box)

  NUM_TRIALS = 1
  for trial in xrange(1, NUM_TRIALS + 1):
    rolled_dice = Roll(hero.GetDiceCounts())
    # Sort the rolled dice by type and value ascending.
    rolled_dice.sort(key=lambda kv: (kv[0].value, kv[1]))
    # Rolled dice arrangement is now fixed so that we can rely on indicies.
    print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)

    possible_placements = []
    for die_index, (die_type, die_value) in enumerate(rolled_dice):
      legal_placements = []
      for box_index, box in enumerate(challenge_boxes):
        #print die_type, die_value, box, box._die_type, die_value, box._requirement, die_type==box._die_type, die_value >= box._requirement, type(die_value), type(box._requirement)
        if (die_type == box._die_type or
            die_type == DieType.Black or
            box._die_type == DieType.Any) and die_value >= box._requirement:
          legal_placements.append(box_index)
      possible_placements.append(legal_placements)
    print rolled_dice
    print challenge_boxes
    print possible_placements


if __name__ == '__main__':
  main()
