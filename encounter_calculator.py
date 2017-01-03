from pprint import pprint
from random import randint, shuffle

from encounters import *
from odd_types import *
from odd_utils import *

def main():
  hero = Hero.Warrior()
  encounter = PerilEncounter.RunePuzzle()
  print hero, encounter
  rolled_dice = Roll(hero.GetDiceCounts())
  print rolled_dice

if __name__ == '__main__':
  main()
