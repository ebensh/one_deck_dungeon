> import OddTypes

> testDice :: [Die]
> testDice = zipWith Die dieColors dieValues
>   where dieColors = [Cyan, Cyan, Cyan, Yellow, Yellow, Magenta]
>         dieValues = [1, 3, 6, 2, 5, 4]

> testChallenge :: [ChallengeBox]
> testChallenge = [ChallengeBox Cyan 2 False False (Consequences 1 1),
> 		   ChallengeBox Cyan 4 False False (Consequences 1 1),
> 		   ChallengeBox Yellow 4 False False (Consequences 1 1),
> 		   ChallengeBox Magenta 6 False False (Consequences 1 1)]

> main = do
>   let dieColors = [Cyan, Cyan, Cyan, Yellow, Yellow, Magenta]
>   dieValues <- fmap (take (length dieColors)) randomDieValues
>   let dice = zipWith Die dieColors dieValues
>   mapM_ (putStrLn . show) dice

