# from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Counter
from enum import Enum, IntEnum
import re

# Con = Consequences.
class ConType(Enum):
  Health = 'h'
  Time = 't'
  def __repr__(self): return self.value
class StatsType(Enum):
  Strength = 's'
  Agility = 'a'
  Magic = 'm'
  Health = 'h'
  def __repr__(self): return self.value
class DieType(Enum):
  Strength = 's'
  Agility = 'a'
  Magic = 'm'
  Black = 'b'  # Technically "Heroic", but distinguish from "Health"
  Any = 'x'
  def __repr__(self): return self.value

class HeroStats(Counter):
  '''A Counter of Strength, Agility, Magic, and Health.'''
  def __init__(self, strength=0, agility=0, magic=0, health=0):
    super(HeroStats, self).__init__({
      StatsType.Strength: strength, StatsType.Agility: agility,
      StatsType.Magic: magic, StatsType.Health:health})
  def __repr__(self):
    return '{{S:{0}, A:{1}, M:{2}, Hlth:{3}}}'.format(
      self[StatsType.Strength], self[StatsType.Agility],
      self[StatsType.Magic], self[StatsType.Health])

  @staticmethod
  def Strength(): return HeroStats(strength=1)
  @staticmethod
  def StrengthHealth(): return HeroStats(strength=1, health=1)
  @staticmethod
  def Agility(): return HeroStats(agility=1)
  @staticmethod
  def AgilityHealth(): return HeroStats(agility=1, health=1)
  @staticmethod
  def Magic(): return HeroStats(magic=1)
  @staticmethod
  def MagicHealth(): return HeroStats(magic=1, health=1)


class Consequences(Counter):
  '''A Counter of Health and Time.'''
  def __init__(self, health=0, time=0):
    super(Consequences, self).__init__({ConType.Health: health,
                                        ConType.Time: time})
  def __repr__(self):
    return 'h' * self[ConType.Health] + 't' * self[ConType.Time]

# An individual box in the challenge set.
class ChallengeBox(object):
  def __init__(self, die_type, requirement, consequences=Consequences(),
               is_wide=False, is_armor=False):
    self._die_type = die_type
    self._requirement = requirement
    self._consequences = consequences
    self._is_wide = is_wide
    self._is_armor = is_armor

  def __repr__(self):
    return ''.join([
      self._die_type.value,
      self._requirement,
      'w' if self._is_wide else '',
      'a' if self._is_armor else '',
      str(self._consequences)
    ])

  @staticmethod
  def Parse(description):
    m = re.match(r'([ams])(\d+)(w?)(a?)(h*)(t*)', description)
    die_type, requirement, wide, armor, health, time = m.groups(False)
    if not die_type: die_type = DieType.Any
    elif die_type == 'a': die_type = DieType.Agility
    elif die_type == 'm': die_type = DieType.Magic
    elif die_type == 's': die_type = DieType.Strength
    else: assert False  # Should not happen.
    requirement = requirement if requirement else 0
    wide = True if wide else False
    armor = True if armor else False
    health = len(health) if health else 0
    time = len(time) if time else 0
    return ChallengeBox(die_type, requirement, Consequences(health, time),
                        wide, armor)

# The group of challenge boxes to be completed.
class ChallengeBoxes(object):
  def __init__(self, boxes=[]):
    self._boxes = boxes

  def __repr__(self):
    return '[' + ', '.join(map(str, self._boxes)) + ']'

  @staticmethod
  def Parse(boxes_description):
    boxes = []
    for box_description in boxes_description.split(','):
      boxes.append(ChallengeBox.Parse(box_description))
    return ChallengeBoxes(boxes)

class Hero(object):
  _stats = Counter()
  _items = []
  def __init__(self, name, strength, agility, magic, health):
    self._name = name
    self._stats = Counter({StatsType.Strength: strength,
                           StatsType.Agility: agility,
                           StatsType.Magic: magic,
                           StatsType.Health: health})
  def AddItem(self, item): self._items.append(item)
  def GetDiceCounts(self):
    total_stats = self._stats
    for item in self._items:
      total_stats += item
    return Counter({DieType.Strength: total_stats[StatsType.Strength],
                    DieType.Agility: total_stats[StatsType.Agility],
                    DieType.Magic: total_stats[StatsType.Magic]})

  def __repr__(self):
    dice = self.GetDiceCounts()
    return '{0}Hero{{S:{1}, A:{2}, M:{3}}}'.format(
      self._name, dice[DieType.Strength], dice[DieType.Agility],
      dice[DieType.Magic])

  @staticmethod
  def Archer():
    return Hero('Archer', strength=2, agility=3, magic=2, health=5)
  @staticmethod
  def Mage():
    return Hero('Mage', strength=1, agility=2, magic=4, health=5)
  @staticmethod
  def Paladin():
    return Hero('Paladin', strength=3, agility=1, magic=3, health=5)
  @staticmethod
  def Rogue():
    return Hero('Rogue', strength=1, agility=4, magic=2, health=5)
  @staticmethod
  def Warrior():
    return Hero('Warrior', strength=4, agility=2, magic=1, health=6)
  # TODO: Add 2player versions of heroes.
