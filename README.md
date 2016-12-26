# Hack League – The connected future of Healthcare
## The challenge
This repo contains the winning solution to a Hack League code battle as developed at the event by Juul De Ruysscher and Dries Oeyen.
The original challenge instructions can be found here: http://hackleague.io/cb-iot-health/

## This solution
Our strategy when developing this solution was simple:

1. Use the visual UI component of Hack League's test server to identify patterns for each illness that we could easily test for.
2. Use the same visual UI to administer drugs to see which works best for each illness. In other words: find the best treatment for each illness by trial and error.
3. Putting the two together: write a test case that attempts to guess the illness of a patient based on the parameters, then apply the treatment we found worked best.

In step 1, we made conclusions like:

* Sepsis results in a sudden spike in temperature and heart rate, and a drop in blood pressure.
* Gastroenteritis results in a fever between 37 and 38°C in the first half of week 1, and a fever above 38°C in the second half.
* Intoxication results in an elevated heart rate in the second half of week 1.

We specifically focused on trying to draw a useful conclusion in week 1, because we noticed a steep drop in health if patients came back in the 2nd week.
Focusing on week 1 would have the most significant impact on our final score, so that's where we focused our time.

In step 2, we determined the best cure for each illness:

| Illness | Preferred treatment |
| --- | --- |
| Common cold | Wait |
| Pneunomia | Antiviral1 |
| Intoxication | Detoxifier |
| Gastroenteritis | Antibio1 |
| Sepsis | Antibio3 |
| Flu | Antiviral1 |

In step 3, we translated into code the test cases from step 1 and the preferred actions from step 2.
The resulting code can be found in the `turn(curstate)` function in `main.py`.

### Running the solution
The entire solution is included in `main.py`, you just need to `pip install requests` before running.
However, please note that it relies on a server that was hosted locally at the event. In case Hack League makes it available online later: you'll still need to change the `serverDomain` variable near the top of `main.py`.

## Future work
We think an ideal solution to this challenge would incorporate machine learning, but decided to do all of this manually due to the limited time constraint of the challenge.

With machine learning, you could simply automate the steps we took: have the algorithm figure out test cases of interest and the accompanying preferred treatment.
In fact, the way a machine learning algo would solve this problem is so similar to what we did by hand, Juul and I jokingly called our strategy "manual machine learning".
