# from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Counter
from enum import IntEnum
import re

# Using IntEnum instead of Enum allows us to sort dice by type (ordered).
# Con = Consequences.
ConType = IntEnum('ConType', 'Health Time')
StatsType = IntEnum('StatsType', 'Strength Agility Magic Health')
DieType = IntEnum('DieType', 'Strength Agility Magic Heroic Any')

class HeroStats(Counter):
  '''A Counter of Strength, Agility, Magic, and Health.'''
  def __init__(self, strength=0, agility=0, magic=0, health=0):
    super(HeroStats, self).__init__({
      StatsType.Strength: strength, StatsType.Agility: agility,
      StatsType.Magic: magic, StatsType.Health:health})

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

# An individual box in the challenge set.
class ChallengeBox(object):
  def __init__(self, die_type, requirement, consequences=Consequences(),
               is_wide=False, is_armor=False):
    self._die_type = die_type
    self._requirement = requirement
    self._consequences = consequences
    self._is_wide = is_wide
    self._is_armor = is_armor

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
                        

  @staticmethod
  def Peril(die_type, requirement, consequences):
    return ChallengeBox(die_type, requirement, consequences, is_wide=True)

# The group of challenge boxes to be completed.
class ChallengeBoxes(object):
  def __init__(self, boxes=[]):
    self._boxes = boxes

  @staticmethod
  def Parse(boxes_description):
    boxes = []
    for box_description in boxes_description.split(','):
      boxes.append(ChallengeBox.Parse(box_description))
    return ChallengeBoxes(boxes)

class Hero(object):
  _stats = Counter()
  _items = []
  def __init__(self, strength, agility, magic, health):
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

  @staticmethod
  def Archer(): return Hero(strength=2, agility=3, magic=2, health=5)
  @staticmethod
  def Mage(): return Hero(strength=1, agility=2, magic=4, health=5)
  @staticmethod
  def Paladin(): return Hero(strength=3, agility=1, magic=3, health=5)
  @staticmethod
  def Rogue(): return Hero(strength=1, agility=4, magic=2, health=5)
  @staticmethod
  def Warrior(): return Hero(strength=4, agility=2, magic=1, health=6)
  # TODO: Add 2player versions of heroes.

class Encounter(object):
  def __init__(self, experience, item_stats):
    self._experience = experience
    self._item_stats = item_stats
    # TODO: Add Skills
  def AsExperience(self): return self_.experience
  def AsItemStats(self): return self._item_stats
  # TODO: Add skills
  # Times that encounter special abilities might be applied:
  # - Before combat (Ice Elemental's Frost)
  # - After the roll (Glooping Ooze's Split)
  # - During combat (Bandit's Dodge, Shadow's Fade)
  # - After the dice are placed (Beetle's Survivor)

class CombatEncounter(Encounter):
  def __init__(self, challenge, experience, item_stats):
    # TODO: Add monster special abilities
    self._challenge = challenge
    super(CombatEncounter, self).__init__(experience, item_stats)

  @staticmethod
  def Skeleton(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return CombatEncounter(
      ChallengeBoxes.Parse('m2a,m4a,s3t,s5ht,a5ht,s6t'), 2, stats)

class PerilEncounter(Encounter):
  def __init__(self, paid_challenge, free_challenge, swap_cost,
               experience, item_stats):
    self._paid_challenge = paid_challenge
    self._free_challenge = free_challenge
    self._swap_cost = swap_cost
    super(PerilEncounter, self).__init__(experience, item_stats)

  @staticmethod
  def RunePuzzle(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return PerilEncounter(
      ChallengeBox.Peril(DieType.Magic, 6, Consequences(1, 3)),
      ChallengeBox.Peril(DieType.Strength, 11, Consequences(3, 2)),
      Consequences(time=2), 2, stats)

class EncounterDeck(object):
  _encounters = [PerilEncounter.RunePuzzle(),
                 PerilEncounter.RunePuzzle(variant=True),
                 CombatEncounter.Skeleton(),
                 CombatEncounter.Skeleton(variant=True)]
  
