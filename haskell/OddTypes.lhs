Useful for Lens syntax: https://wiki.haskell.org/LensBeginnersCheatsheet

> {-# LANGUAGE TemplateHaskell #-}

> module OddTypes where

> import Control.Applicative ((<$>), (<*>))
> import Control.Lens
> import Control.Monad (when)

> import System.Random (randomRs, newStdGen)

> data DieColor = Black | Cyan | Magenta | Yellow deriving (Enum, Eq, Ord, Show)
> data Die = Die { _color :: DieColor
>                , _value :: Int
>                } deriving (Eq, Ord, Show)
> makeLenses ''Die

> data AbilityStats = AbilityStats { _strength :: Int
>      	      	      		   , _agility :: Int
>		   		   , _magic :: Int
>		   		   , _health :: Int
>                                  } deriving (Eq, Ord, Show)
> makeLenses ''AbilityStats

TODO: Add items, which are just [AbilityStats]
TODO: Add skills
TODO: Add experience
TODO: Add more heroes.

> data Hero = Hero { _stats :: AbilityStats } deriving (Show)
> makeLenses ''Hero
> basicHero = Hero { _stats = AbilityStats{_strength=1, _agility=1, _magic=1, _health=3} }
> archerHero = Hero { _stats = AbilityStats{_strength=2, _agility=3, _magic=2, _health=5} }

> data Consequences = Consequences { _healthDmg :: Int
>      		      		   , _timeDmg :: Int } deriving (Show)
> makeLenses ''Consequences

> data ChallengeBox = ChallengeBox { _dieColor :: DieColor
>      		      		   , _requirement :: Int
>                     		   , _isWide :: Bool
>				   , _isArmor :: Bool
> 				   , _consequence :: Consequences
>				   } deriving (Show)
> makeLenses ''ChallengeBox

> isValidAssignment :: ChallengeBox -> Die -> Bool
> isValidAssignment box die = box^.dieColor == die^.color &&
> 		     	      box^.requirement <= die^.value

> randomDieValues :: IO [Int]
> randomDieValues = randomRs (1, 6) <$> newStdGen

