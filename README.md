# Championship_Odds
Probability of winning World Series based on regular season record (current 6-team format vs possible 8-team format)

# Inspiration
This small project arose from a question in the interview process with an MLB team: If MLB instituted an 8-team postseason format (a la 2020), how should organizations adjust their team-building philosophy? Here was my response, limited to 300 words:

If MLB expanded the playoffs to eight teams in each league, organizations should place less emphasis on maximizing peak team quality, and more emphasis on minimizing the frequency of uncompetitive seasons. The plot to the right (odds_by_format.png) displays championship odds for teams of varying quality under the current and proposed formats.

The lack of byes eliminates much of the advantage of a great regular season record, as home field is a fairly small factor in five and seven game series. Only the three game series, presumably still played entirely at one venue, still fairly reward a better record.

Let’s say you are the owner of a team projected to win 89 games. A 4-WAR player is set to depart in free agency, but you can give him a qualifying offer of $20M, bringing up your team’s projection to 93 wins. Under the current format, this improves your championship odds from 2.5% to 6.8%, but under the new format, they change from 2.4% to just 4.4%. For the decision to be fiscally “correct”, the value of a World Series championship4 would have to be about $500M under the current format, and at least $1B under the new format. 

Or, put another way, maintaining an 84 win team for just five seasons would yield the same championship odds as a single 93 win season; currently that would take nearly nineteen years.

All that is to say that in this scenario, teams should prioritize consistently clearing the .500 threshold, and only pursue greatness when it does not come at the expense of future mediocrity.

# Methodology
Instead of using large-scale simulations, I endeavored to come up with a purely formulaic method to answer this question. Fortunately for me, most of the hard work has already been done: John A. Richards of SABR developed a formula that strongly estimates a team's odds of beating a .500 team based on their record, Bill James introduced a formula which gives the probability of one team beating another based on their respective qualities, and Vivienne Pelletier developed an equation that gives the probability of one team beating another in a series of N games based on single game win probability. I simply combined these equations, along with postseason odds, bye odds (where applicable) and rough estimates of opponent quality for each round of the playoffs.

# Future developments
I believe that the largest flaw in this methodology is the lack of consideration for home field advantage in the DS, LCS, and WS. Home field advantage is far more important in the Wild Card Series because all three games are played at one venue, and it is likewise far easier to model, as it is the first round and so opponent quality is easy to guess. For the later rounds, home field advantage shifts throughout the series, and so Pelletier's equation (which assumes static win probabilities) does not hold. Further, it is much more difficult to determine the probability of the team in quetion actually having home field advantage, as that depends on the results of other series.

It would certainly not be impossible, nor in fact all that difficult, to account for this, but it would take more time than I am currently willing to commit to this project, and so it will be left here as a reminder for me if I ever have need to revisit it, or if someone else would like to carry on my work.
