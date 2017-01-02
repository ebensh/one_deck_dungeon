# from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Counter
from enum import IntEnum

# Using IntEnum instead of Enum allows us to sort dice by type (ordered).
# Con = Consequences.
ConType = IntEnum('ConType', 'Health Time')
StatsType = IntEnum('StatsType', 'Strength Agility Magic Health')
DieType = IntEnum('DieType', 'Strength Agility Magic Heroic Any')

class Consequences(Counter):
  '''A Counter of Health and Time.'''
  def __init__(self, health=0, time=0):
    super(Consequences, self).__init__(ConType.Health=health, ConType.Time=time)

class ChallengeBox(object):
  def __init__(self, die_type, requirement, consequences=Consequences(),
               is_wide=False, is_armor=False):
    self._die_type = die_type
    self._requirement = requirement
    self._consequences = consequences
    self._is_wide = is_wide
    self._is_armor = is_armor


class Hero(object):
  _stats = Counter()
  _items = []
  def AddItem(self, item): self_.items.append(item)
  def GetDiceCounts(self):
    total_stats = self._stats
    for item in self._items:
      total_stats += item
    return Counter({DieType.Strength: total_stats[StatsType.Strength],
                    DieType.Agility: total_stats[StatsType.Agility],
                    DieType.Magic: total_stats[StatsType.Magic]})

class Archer(Hero):
  _stats = Counter({StatsType.Strength: 2, StatsType.Agility: 3,
                    StatsType.Magic: 2, StatsType.Health: 5})
class Mage1(Hero):
  _stats = Counter({StatsType.Strength: 1, StatsType.Agility: 2,
                    StatsType.Magic: 4, StatsType.Health: 5})
class Paladin1(Hero):
  _stats = Counter({StatsType.Strength: 3, StatsType.Agility: 1,
                    StatsType.Magic: 3, StatsType.Health: 5})
class Rogue1(Hero):
  _stats = Counter({StatsType.Strength: 1, StatsType.Agility: 4,
                    StatsType.Magic: 2, StatsType.Health: 5})
class Warrior1(Hero):
  _stats = Counter({StatsType.Strength: 4, StatsType.Agility: 2,
                    StatsType.Magic: 1, StatsType.Health: 6})
# TODO: Add 2player versions of heroes.

class Encounter(object):
  def AsExperience(self): return 0
  def AsItemStats(self): return Counter()
