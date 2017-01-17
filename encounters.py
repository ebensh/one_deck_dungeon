from odd_types import *

def ParseChallengeBoxes(boxes_description):
  boxes = []
  for box_description in boxes_description.split(','):
    boxes.append(ChallengeBox.Parse(box_description))
  return boxes


class Encounter(object):
  def __init__(self, name, experience, item_stats):
    self._name = name
    self._experience = experience
    self._item_stats = item_stats
    # TODO: Add Skills
  def AsExperience(self): return self._experience
  def AsItemStats(self): return self._item_stats
  # TODO: Add skills
  # Times that encounter special abilities might be applied:
  # - Before combat (Ice Elemental's Frost)
  # - After the roll (Glooping Ooze's Split)
  # - During combat (Bandit's Dodge, Shadow's Fade)
  # - After the dice are placed (Beetle's Survivor)
  def __repr__(self):
    return '{{{0}: exp:{0}, item:{1}}}'.format(
      self._name, self._experience, self._item_stats)

class CombatEncounter(Encounter):
  def __init__(self, name, challenge, experience, item_stats):
    # TODO: Add monster special abilities
    self._challenge = challenge
    super(CombatEncounter, self).__init__(name, experience, item_stats)

  def __repr__(self):
    return 'Combat{{{0}: {1}, exp:{2}, item:{3}}}'.format(
      self._name, self._challenge, self._experience, self._item_stats)

  @staticmethod
  def Bandit(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Agility()
    return CombatEncounter('Bandit',
      ParseChallengeBoxes('a8whh,a3h,a4t,s5tt,s5ht'), 3, stats)
  
  @staticmethod
  def Beetle(variant=False):
    stats = HeroStats.Magic()  # Both variants
    return CombatEncounter('Beetle',
      ParseChallengeBoxes('a3a,a4a,s5a,m3a,a4tt,s6ht'), 2, stats)

  @staticmethod
  def FireElemental(variant=False):
    stats = HeroStats.MagicHealth() if variant else HeroStats.AgilityHealth()
    return CombatEncounter('FireElemental',
      ParseChallengeBoxes('m3t,a3t,m6ht,m11whht,a6ht'), 4, stats)

  @staticmethod
  def GloopingOoze(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.StrengthHealth()
    return CombatEncounter('GloopingOoze',
      ParseChallengeBoxes('m2a,m3a,s4ht,s4ht,m5tt,s6ht'), 3, stats)
  
  @staticmethod
  def Goblin(variant=False):
    # TODO: Replace the first box with its proper X! It depends on the number
    # of open doors. I've put 4 as a placeholder (assuming 1 door open).
    stats = HeroStats.Strength()  # Both variants
    return CombatEncounter('Goblin',
      ParseChallengeBoxes('s4a,s3h,a4t,a4ht,s5hh'), 2, stats)

  @staticmethod
  def IceElemental(variant=False):
    stats = HeroStats.AgilityHealth()  # Both variants
    return CombatEncounter('IceElemental',
      ParseChallengeBoxes('s11wa,s3t,m4hh,m5ht,m6ht'), 4, stats)

  @staticmethod
  def Ogre(variant=False):
    stats = HeroStats.MagicHealth() if variant else HeroStats.StrengthHealth()
    return CombatEncounter('Ogre',
      ParseChallengeBoxes('s6wh,a4t,s9whh,a5ht,s12whhh,a6ht'), 4, stats)
  
  @staticmethod
  def Phantom(variant=False):
    stats = HeroStats.AgilityHealth() if variant else HeroStats.StrengthHealth()
    return CombatEncounter('Phantom',
      ParseChallengeBoxes('s4a,a4a,a5hh,a6ht,s5ht,s6hh'), 4, stats)

  @staticmethod
  def PlagueRat(variant=False):
    stats = HeroStats.Agility()  # Both variants
    # TODO: Replace the first box with its proper X! It depends on the number
    # of open doors. I've put 4 as a placeholder (assuming 1 door open).
    return CombatEncounter('PlagueRat',
      ParseChallengeBoxes('a4wa,a3ht,s3t,s5ht,a5tt'), 2, stats)

  @staticmethod
  def Shadow(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.StrengthHealth()
    return CombatEncounter('Shadow',
      ParseChallengeBoxes('a10wa,s5ht,m3ht,m4ht,m5ht'), 3, stats)
  
  @staticmethod
  def Skeleton(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return CombatEncounter('Skeleton',
      ParseChallengeBoxes('m2a,m4a,s3t,s5ht,a5ht,s6t'), 2, stats)

  @staticmethod
  def Wraith(variant=False):
    stats = HeroStats.Strength()  # Both variants
    return CombatEncounter('Wraith',
      ParseChallengeBoxes('m9wa,s5a,s3tt,s5hh,m6ht'), 3, stats)

class PerilEncounter(Encounter):
  def __init__(self, name, paid_challenge, free_challenge, swap_cost,
               experience, item_stats):
    self._paid_challenge = paid_challenge
    self._free_challenge = free_challenge
    self._swap_cost = swap_cost
    super(PerilEncounter, self).__init__(name, experience, item_stats)

  def __repr__(self):
    return 'Peril{{{0}: {1}, {2}, swap:{3}, exp:{4}, item:{5}}}'.format(
      self._name, self._paid_challenge, self._free_challenge,
      self._swap_cost, self._experience, self._item_stats)  

  @staticmethod
  def ArrowWall(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Strength()
    return PerilEncounter('ArrowWall',
      ParseChallengeBoxes('m6whhttt'), ParseChallengeBoxes('a11whhhtt'),
      Consequences(time=1), 2, stats)

  @staticmethod
  def BearTraps(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Agility()
    return PerilEncounter('BearTraps',
      ParseChallengeBoxes('a6whht'), ParseChallengeBoxes('a11whhhtt'),
      Consequences(time=3), 2, stats)

  @staticmethod
  def Boulder(variant=False):
    stats = HeroStats.MagicHealth() if variant else HeroStats.StrengthHealth()
    return PerilEncounter('Boulder',
      ParseChallengeBoxes('m11whhhtt'), ParseChallengeBoxes('a14whhhht'),
      Consequences(time=3), 4, stats)

  @staticmethod
  def CaveIn(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Agility()
    return PerilEncounter('CaveIn',
      ParseChallengeBoxes('s6whttt'), ParseChallengeBoxes('a11whhtt'),
      Consequences(time=2), 2, stats)

  @staticmethod
  def FlameStatues(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Strength()
    return PerilEncounter('FlameStatues',
      ParseChallengeBoxes('m8whhttt'), ParseChallengeBoxes('a14whhht'),
      Consequences(time=3), 3, stats)
  
  @staticmethod
  def ForceWall(variant=False):
    stats = HeroStats.MagicHealth() if variant else HeroStats.StrengthHealth()
    return PerilEncounter('ForceWall',
      ParseChallengeBoxes('a11whhtttt'), ParseChallengeBoxes('m14whhhhtt'),
      Consequences(time=3), 4, stats)

  @staticmethod
  def LockedDoor(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Strength()
    return PerilEncounter('LockedDoor',
      ParseChallengeBoxes('a8whtttt'), ParseChallengeBoxes('s11whhtt'),
      Consequences(time=1), 2, stats)

  @staticmethod
  def PitOfSpikes(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Strength()
    return PerilEncounter('PitOfSpikes',
      ParseChallengeBoxes('s8whhtt'), ParseChallengeBoxes('a14whhhtt'),
      Consequences(time=3), 3, stats)

  @staticmethod
  def RunePuzzle(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return PerilEncounter('RunePuzzle',
      ParseChallengeBoxes('m6whttt'), ParseChallengeBoxes('s11whhhtt'),
      Consequences(time=2), 2, stats)

  @staticmethod
  def SpikedLog(variant=False):
    stats = HeroStats.Agility()  # Both variants
    return PerilEncounter('SpikedLog',
      ParseChallengeBoxes('s8whhht'), ParseChallengeBoxes('a14whhhtt'),
      Consequences(time=2), 3, stats)


def GetEncounterCards(with_variants=True):
  encounter_factories = [CombatEncounter.Bandit,
                         CombatEncounter.Beetle,
                         CombatEncounter.FireElemental,
                         CombatEncounter.GloopingOoze,
                         CombatEncounter.Goblin,
                         CombatEncounter.IceElemental,
                         CombatEncounter.Ogre,
                         CombatEncounter.Phantom,
                         CombatEncounter.PlagueRat,
                         CombatEncounter.Shadow,
                         CombatEncounter.Skeleton,
                         CombatEncounter.Wraith,
                         PerilEncounter.ArrowWall,
                         PerilEncounter.BearTraps,
                         PerilEncounter.Boulder,
                         PerilEncounter.CaveIn,
                         PerilEncounter.FlameStatues,
                         PerilEncounter.ForceWall,
                         PerilEncounter.LockedDoor,
                         PerilEncounter.RunePuzzle,
                         PerilEncounter.PitOfSpikes,
                         PerilEncounter.SpikedLog]
  cards = []
  for encounter_factory in encounter_factories:
    cards.append(encounter_factory(False))
    if with_variants:
      cards.append(encounter_factory(True))
  return cards
