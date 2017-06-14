from copy import deepcopy
from random import randint

from odd_types import Die, DieType, Hero


class TestHero(Hero):
  def __init__(self):
    super(TestHero, self).__init__('Test', 1,1,1,3)

  # Skills: StrToAbi, StrToMag, AgiToStr, AgiToMag, MagToStr, MagToAgi (1 to 1)
  # And there is a 7th skill that combines two dice to make a Black 6.


class DiceField(object):
  '''Represents the dice in front of a player.

  This class should provide a minimal, complete interface for skills to use.'''
  # TODO(ebensh): Should skills be actors that the DiceField applies? Or should
  # skills use the DiceField interface to make decisions / apply transactions of
  # state? TRY BOTH! :) We can optimize later.
  def __init__(self):
    self._dice = []

  def AddDie(self, die): self._dice.append(die)
  def RemoveDie(self, to_remove):
    for ix, die in enumerate(self._dice):
      if die == to_remove:
        self._dice.remove(ix)
        return True
    return False

  def GetDice(self):
    return deepcopy(self._dice)  # Does Python have a copy-on-write?


def main():
  df = DiceField()
  df.AddDie(Die(DieType.Strength))
  df.AddDie(Die(DieType.Agility))
  df.AddDie(Die(DieType.Magic))
  df.AddDie(Die(DieType.Black))
  hero = TestHero()
  print hero
  

if __name__=='__main__': main()
