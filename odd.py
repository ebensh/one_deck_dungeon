from enum import Enum

DieType = Enum('DieType', 'Strength Agility Magic Heroic Any')

class Consequences(object):
  self.health = 0
  self.time = 0
  def __init__(self, health=0, time=0): self.health = health; self.time = time

class ChallengeBox(object):
  self._die_type = DieType.Any
  self._requirement = 0
  self._consequneces = Consequences()
  self._is_wide = False
  self._is_armor = False

  def __init__(self, die_type, requirement, consequences, is_wide, is_armor):
    self._die_type = die_type
    self._requirement = requirement
    self._consequences = consequences
    self._is_wide = is_wide
    self._is_armor = is_armor


class Rogue1Player(object):
  self._dice = {DiceType.Strength: 1,
                DiceType.Agility: 4,
                DiceType.Magic: 2,
                DiceType.Heroic: 0}
  self._health = 5
  # TODO: Add skills


# Encounter - Peril
class ArrowWall(object):
  self.primary_option = ChallengeBox(DieType.Agility, 11,
                                     Consequences(health=3, time=2),
                                     is_wide=True, is_armor=False)
  self.secondary_option = ChallengeBox(DieType.Magic, 6,
                                       Consequences(health=2, time=3),
                                       is_wide=True, is_armor=False)
  self.secondary_cost = Consequences(time=1)
  self.as_experience = 2
  self.as_item =
  # TODO: add skills

def main():
  print "Hello, world! :)"

if __name__ == '__main__':
  main()
