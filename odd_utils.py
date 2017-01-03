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

def GroupedRoll(dice):
  rolls = SortedRoll(dice)
  # We don't use a defaultdict here because we don't want the client of the
  # utils to create entries unknowingly on failed lookup.
  result = {}
  for die_type, value in rolls:
    if die_type not in result:
      result[die_type] = []
    result[die_type].append(value)
  return result
