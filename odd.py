from collections import Counter
from enum import IntEnum
from pprint import pprint
from random import randint

import odd_types

# Encounter - Peril
class ArrowWall(object):
  first_option = ChallengeBox(DieType.Agility, 11,
                              Consequences(health=3, time=2),
                              is_wide=True, is_armor=False)
  second_option = ChallengeBox(DieType.Magic, 6,
                               Consequences(health=2, time=3),
                               is_wide=True, is_armor=False)
  second_cost = Consequences(time=1)
  def AsExperience(self): return 2
  def AsItemStats(self): return Counter({StatsType.Magic: 1})
  # TODO: add skills and potions

def Roll(dice):
  result = []
  for die_type, num_dice in dice.iteritems():
    for _ in xrange(num_dice + 1):
      result.append((die_type, randint(1, 6)))
  return sorted(result, key=lambda kv: (kv[0], -kv[1]))  # Asc type, Desc val

def TestPrintSomeThings():
  character = Rogue1Player()
  pprint(Roll(character.GetDice()))
  pprint(Roll(character.GetDice()))
  character.AddItem(ArrowWall().AsItemStats())
  character.AddItem(ArrowWall().AsItemStats())
  pprint(Roll(character.GetDice()))
  pprint(vars(ArrowWall().first_option))

def main():
  TestPrintSomeThings()

if __name__ == '__main__':
  main()
