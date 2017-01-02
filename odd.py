from collections import Counter
from enum import IntEnum
from pprint import pprint
from random import randint

from encounters import *
from odd_types import *

def Roll(dice):
  result = []
  for die_type, num_dice in dice.iteritems():
    for _ in xrange(num_dice + 1):
      result.append((die_type, randint(1, 6)))
  return sorted(result, key=lambda kv: (kv[0], -kv[1]))  # Asc type, Desc val

def TestPrintHeroesItemsAndRolls():
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

def TestPrintTheDeck():
  deck = GetEncounterCards()
  for card in deck:
    pprint(str(card))

def main():
  #TestPrintHeroesItemsAndRolls()
  TestPrintTheDeck()

if __name__ == '__main__':
  main()
