# NFL-Betting

## What is it?
NFL Betting algorithm used to project point spreads for upcoming NFL games.

## How Does it Work?
Using [DVOA](https://help.footballoutsiders.com/hc/en-us/articles/360045226591-DVOA-The-Short-Version), pace data, and basic statistics (like yards per play and points scored), team offense, defense and special teams ratings are estimated. The ratings are in the format of Points per Game For (offense), Points per Game Against (defense), and Points per Game Added (special teams). An overall team rating is produced by subtracting defense from offense and adding special teams (offense - defense + special teams).

The following chart is a rough estimate of good/bad ratings:

| Rating | What it Means |
|:------:|:-------------:|
| >8     | Excellent     |
| 5 to 8 | Great         |
| 3 to 5    | Good          |
| 1 to 3    | Above Average |
| -1 to 1 | Average |
|-3 to -1 | Below Average |
| -5 to -3 | Bad |
| <-5 | Awful |

Once the overall team ratings are estimated, team home field advantage ratings need to be calculated. The formula used is average point differential per game at home over the past 5 years - average point differential per game in all games over the past 5 years. Most home field advantage ratings range from -1 (bad) to 3.5 (good).

Now that we have overall team ratings and home field advantage ratings, we can project spreads for upcoming games. In sports betting, negative spreads imply a team is favored to win, therefore we calculate the spread for the home team in a given game by: away team overall rating - home team overall rating - home field advantage.

Since 2018, this algorithm has produced a 54.60% winning percentage against the spread with a win-loss record of 380-316.

## Django Web App
Want to see the NFL Betting Algorithm in action? Go to https://www.gadsportsdata.com/nfl/game/ to try it out now!
