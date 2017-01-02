from collections import Counter
from enum import IntEnum
from pprint import pprint
from random import randint

from odd_types import *


def Roll(dice):
  result = []
  for die_type, num_dice in dice.iteritems():
    for _ in xrange(num_dice + 1):
      result.append((die_type, randint(1, 6)))
  return sorted(result, key=lambda kv: (kv[0], -kv[1]))  # Asc type, Desc val

def TestPrintSomeThings():
  character = Rogue1()
  pprint(Roll(character.GetDice()))
  pprint(Roll(character.GetDice()))
  character = Warrior1()
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
