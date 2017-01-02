from collections import Counter
from enum import IntEnum
import random

# Consequences
ConType = IntEnum('ConType', 'Health Time')
StatsType = IntEnum('StatsType', 'Strength Agility Magic Health')
DieType = IntEnum('DieType', 'Strength Agility Magic Heroic Any')

class Consequences(object):
  def __init__(self, health=0, time=0):
    self._health = health
    self._time = time
  def AsCounter(self):
    return Counter({ConType.Health: self._health, ConType.Time: self._time})
                   

class ChallengeBox(object):
  def __init__(self, die_type, requirement, consequences, is_wide, is_armor):
    self._die_type = die_type
    self._requirement = requirement
    self._consequences = consequences
    self._is_wide = is_wide
    self._is_armor = is_armor

class Rogue1Player(object):
  _stats = Counter({StatsType.Strength: 1,
                    StatsType.Agility: 4,
                    StatsType.Magic: 2,
                    StatsType.Health: 5})
  _items = []

  def AddItem(self, item): self._items.append(item)
  def GetDice(self):
    total_stats = self._stats
    for item in self._items:
      total_stats += item
    return Counter({DieType.Strength: total_stats[StatsType.Strength],
                    DieType.Agility: total_stats[StatsType.Agility],
                    DieType.Magic: total_stats[StatsType.Magic]})
  # TODO: Add skills


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
      result.append((die_type, random.randint(1, 6)))
  return sorted(result)
    

def main():
  character = Rogue1Player()
  print Roll(character.GetDice())
  print Roll(character.GetDice())
  print Roll(character.GetDice())
  character.AddItem(ArrowWall().AsItemStats())
  character.AddItem(ArrowWall().AsItemStats())
  character.AddItem(ArrowWall().AsItemStats())
  character.AddItem(ArrowWall().AsItemStats())
  print Roll(character.GetDice())
  

if __name__ == '__main__':
  main()
