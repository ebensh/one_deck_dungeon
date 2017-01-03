from pprint import pprint
from random import randint, shuffle

from encounters import *
from odd_types import *
from odd_utils import *

  # TODO: Create accessors to all "private" members accessed.
def main():
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
    challenge_boxes = deepcopy(encounter._challenge)
    print challenge_boxes

    rolled_dice = GroupedRoll(hero.GetDiceCounts())  # Sorts and Groups
    print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)

    # TODO: Don't brute force, replace with smarts! :)
    # Extract the type of the box.
    box_types = [box._die_type for box in challenge_boxes]

    # For each die in the flattened dice, create a list of all the challenge
    # boxes it's eligible for.

    for die_type, die_values in rolled_dice:




if __name__ == '__main__':
  main()
