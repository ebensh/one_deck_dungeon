from random import randint

from odd_types import *

def Roll(dice):
  result = []
  for die_type, num_dice in dice.iteritems():
    result += [(die_type, randint(1, 6)) for _ in xrange(num_dice + 1)]
  return result

def SortedRoll(dice):
  rolls = Roll(dice)
  rolls.sort(key=lambda kv: (kv[0].value, -kv[1]))  # Asc type, Desc val
  return rolls
