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
  character = Hero.Rogue()
  pprint(Roll(character.GetDiceCounts()))
  pprint(Roll(character.GetDiceCounts()))
  character = Hero.Warrior()
  pprint(Roll(character.GetDiceCounts()))
  pprint(Roll(character.GetDiceCounts()))

  pprint(character.GetDiceCounts())
  character.AddItem(PerilEncounter.RunePuzzle().AsItemStats())
  pprint(character.GetDiceCounts())
  character.AddItem(PerilEncounter.RunePuzzle(variant=True).AsItemStats())
  pprint(character.GetDiceCounts())
  character.AddItem(CombatEncounter.Skeleton().AsItemStats())
  pprint(character.GetDiceCounts())
  character.AddItem(CombatEncounter.Skeleton(variant=True).AsItemStats())
  pprint(character.GetDiceCounts())

  pprint(Roll(character.GetDiceCounts()))
  pprint(Roll(character.GetDiceCounts()))

def main():
  TestPrintSomeThings()

if __name__ == '__main__':
  main()
