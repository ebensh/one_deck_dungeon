from odd_types import *

class Encounter(object):
  def __init__(self, name, experience, item_stats):
    self._name = name
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
  def FireElemental(variant=False):
    stats = HeroStats.MagicHealth() if variant else HeroStats.AgilityHealth()
    return CombatEncounter('FireElemental',
      ChallengeBoxes.Parse('m3t,a3t,m6ht,m11whht,a6ht'), 4, stats)

  @staticmethod
  def Skeleton(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return CombatEncounter('Skeleton',
      ChallengeBoxes.Parse('m2a,m4a,s3t,s5ht,a5ht,s6t'), 2, stats)

  

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
  def PitOfSpikes(variant=False):
    stats = HeroStats.Magic() if variant else HeroStats.Strength()
    return PerilEncounter('PitOfSpikes',
      ChallengeBox.Parse('s8whhtt'), ChallengeBox.Parse('a14whhhtt'),
      Consequences(time=3), 3, stats)

  @staticmethod
  def RunePuzzle(variant=False):
    stats = HeroStats.Agility() if variant else HeroStats.Strength()
    return PerilEncounter('RunePuzzle',
      ChallengeBox.Parse('m6whttt'), ChallengeBox.Parse('s11whhhtt'),
      Consequences(time=2), 2, stats)
  

def GetEncounterCards():
  encounter_factories = [CombatEncounter.FireElemental,
                         CombatEncounter.Skeleton,
                         PerilEncounter.RunePuzzle,
                         PerilEncounter.PitOfSpikes]
  cards = []
  for encounter_factory in encounter_factories:
    cards.append(encounter_factory(False))
    cards.append(encounter_factory(True))
  return cards
