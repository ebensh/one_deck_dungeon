from pprint import pprint
from random import randint, shuffle

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

def TestARound():
  hero = Hero.Warrior()
  deck = GetEncounterCards()
  shuffle(deck)
  encounter = deck.pop()
  print hero, encounter
  rolled_dice = Roll(hero.GetDiceCounts())
  pprint(rolled_dice)
  

def main():
  #TestPrintHeroesItemsAndRolls()
  #TestPrintTheDeck()
  TestARound()

  # Ideas to continue on:
  # - Pretend we have no skills, forget the rewards, just fix a character
  #   at a set of stats / dice, and see how many monsters they could defeat.
  #   In order to do this, we need a function that can figure out:
  #     For a given set of rolled dice, can we beat this monster?
  #     How much damage do we take?
  #     Over a thousand trials, will we win without taking any damage?
  #       Min damage, max damage? Maybe not the best measure. Mean/median?
  #     Note: for Perils we need to consider each option
  #   Sort encounters in term of mean damage, how many could we get through
  #     if we assume we get super lucky in ordering?
  #   I'm picturing something like a zip of the Encounter deck and the mean
  #     damage for each one, sorted by the mean damage ascending.
  #   Then we can see based on purely base stats which character will get
  #     farthest. As we add skills, there's a max of 7, one per encounter,
  #     even if we permute them all that's a max of 5040 orderings, each has
  #     a limited effect (which dice can be used/effected), if we simplify
  #     a lot of the skills we might be able to get a "fitness" function
  #     for how good a character is at getting through a floor. This would
  #     be great for identifying things like: skill synergies with classes,
  #     or number of encounters we expect to do well in.
  

if __name__ == '__main__':
  main()
