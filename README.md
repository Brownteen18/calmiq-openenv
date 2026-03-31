## Action Space
- meditate: improves mood, reduces stress, costs energy
- exercise: boosts mood, reduces stress, high energy cost
- sleep: restores energy
- talk: improves mood but reduces energy

## Observation Space
- mood (0–10)
- stress (0–10)
- energy (0–10)

## Reward Function
- rewards high mood
- penalizes stress
- includes step penalty and anti-optimization penalty