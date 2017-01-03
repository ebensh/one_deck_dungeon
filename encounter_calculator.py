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
  challenge_boxes = encounter._challenge
  print challenge_boxes

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

  NUM_TRIALS = 1
  for trial in xrange(1, NUM_TRIALS + 1):
    rolled_dice = Roll(hero.GetDiceCounts())
    rolled_dice.sort(key=lambda kv: (kv[0].value, kv[1]))
    print "Trial #{0}: Rolled {1}".format(trial, rolled_dice)
    

if __name__ == '__main__':
  main()
