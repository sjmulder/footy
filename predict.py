#!/usr/bin/python
# coding=utf-8

import math
import json

# Uncomment if you want to plot or pretty print some data
#import matplotlib.pyplot as pyplot
#import pprint

class MatchResult:
    WIN  = 1
    DRAW = 2

    def __init__(self, a_name, a_score, b_name, b_score):
        self.a_name  = a_name
        self.a_score = a_score
        self.b_name  = b_name
        self.b_score = b_score
        if self.a_score > self.b_score:
            self.result = MatchResult.WIN
            self.winner = a_name
        elif self.a_score < self.b_score:
            self.result = MatchResult.WIN
            self.winner = b_name
        else:
            self.result = MatchResult.DRAW
            self.winner = None

    def __repr__(self):
        return '{0} {1} - {2} {3}'.format(
            self.a_name, str(self.a_score),
            str(self.b_score), self.b_name)

class Stats:
    def __init__(self, num, wins, draws, score_mean):
        self.num    = num
        self.wins   = wins
        self.draws  = draws
        self.losses = num - wins - draws
        self.p_win  = (1. / 3.) if num == 0 else float(self.wins)  / num
        self.p_draw = (1. / 3.) if num == 0 else float(self.draws) / num
        self.p_loss = 1. - self.p_win - self.p_draw
        self.score_mean = score_mean

    def __repr__(self):
        return 'wins = {0}, draws = {1}, losses = {2}'.format(
            self.wins, self.draws, self.num - self.wins - self.draws);

def calc_stats(matches, team):
    filtered = [m for m in matches if m.a_name == team or m.b_name == team]
    wins = [m for m in filtered if m.winner == team]
    draws = [m for m in filtered if m.result == MatchResult.DRAW]
    scores = []
    scores.extend([m.a_score for m in filtered if m.a_name == team])
    scores.extend([m.b_score for m in filtered if m.b_name == team])
    num_scores = len(scores)
    score_mean = None if num_scores == 0 else scores[num_scores / 2]
    return Stats(len(filtered), len(wins), len(draws), score_mean)

class NaiveClassifier:
    """
    Implements a naive bayes classifier over wins/draws/losses,
    returning a 1 - 0, 0 - 0, or 0 - 1 result.
    """

    matches = []
    
    def predict(self, a_name, b_name):
        a = calc_stats(self.matches, a_name)
        b = calc_stats(self.matches, b_name)
        p_win_a = (a.p_win + b.p_loss) / 2.
        p_win_b = (a.p_loss + b.p_win) / 2.
        p_draw  = (a.p_draw + b.p_draw) / 2.
        max_p = max(p_win_a, p_win_b, p_draw)
        if (max_p == p_draw):
            return MatchResult(a_name, 0, b_name, 0)
        elif (max_p == p_win_a):
            return MatchResult(a_name, 1, b_name, 0)
        else:
            return MatchResult(a_name, 0, b_name, 1)

    def update(self, match):
        self.matches.append(match)

class MeanScore:
    """
    Simply returns the mean of the number of goals each team
    made in previous matches.
    """

    matches = []

    def predict(self, a_name, b_name):
        a = calc_stats(self.matches, a_name)
        b = calc_stats(self.matches, b_name)
        a_score = a.score_mean if a.score_mean != None else 0
        b_score = b.score_mean if b.score_mean != None else 0
        return MatchResult(a_name, a_score, b_name, b_score)

    def update(self, match):
        self.matches.append(match)

class LinearRegressionScore:
    """
    Implements the assumption the better the oponent, the fewer
    goals a team will make - where “better” means a higher avrage
    number of goals.

    More specifically, this will compute a function that calculates
    the number of goals a team will make given the opponent’s average 
    number of goals per match.
    """

    matches = []
    stats = {}

    def draw_prediction(self, history, w0, w1):
        xs = [x for x, _ in history]
        ys = [y for _, y in history]
        pyplot.plot(ys, xs, 'ro',
                    [w0 + w1 * x for x in range(int(max(xs) + 1))])
        pyplot.show()
        #pprint.pprint(history)
        #print 'y = {0} * x + {1}'.format(w1, w0);

    def predict_team(self, us, them):
        if len(matches) == 0 or not (them in self.stats):
            return 0
        history = []
        history.extend([(m.a_score, self.stats[m.b_name].score_mean)
                        for m in matches 
                         if m.a_name == us
                        and m.b_name in self.stats])
        history.extend([(m.b_score, self.stats[m.a_name].score_mean)
                        for m in matches 
                         if m.b_name == us 
                        and m.a_name in self.stats])
        n = float(len(history))
        if n == 0:
            return 0
        sum_x  = sum([x for x, _ in history])
        sum_y  = sum([y for _, y in history])
        sum_xy = sum([x * y for x, y in history])
        sum_xx = sum([x * x for x, _ in history])
        d = (n * sum_xx - sum_x ** 2)
        if d == 0:
            return self.stats[us].score_mean
        w1 = (n * sum_xy - sum_x * sum_y) / d
        w0 = (sum_y - w1 * sum_x) / n
        #self.draw_prediction(history, w0, w1)
        return int(round(w0 + w1 * self.stats[them].score_mean))

    def predict(self, a_name, b_name):
        return MatchResult(a_name, self.predict_team(a_name, b_name),
                           b_name, self.predict_team(b_name, a_name))

    def update(self, match):
        self.matches.append(match)
        teams = set([m.a_name for m in self.matches] +
                    [m.b_name for m in self.matches])
        self.stats = { t : calc_stats(self.matches, t) for t in teams }

data = open('match_results.json', 'r').read()
data_json = json.loads(data)

matches = [MatchResult(x['a_name'], x['a_score'], x['b_name'], x['b_score']) 
           for x in data_json]

algorithms = [NaiveClassifier(), MeanScore(), LinearRegressionScore()]
predictions = { a.__class__.__name__ : [] for a in algorithms }

for match in matches:
    for algo in algorithms:
        algo_name = algo.__class__.__name__
        prediction = algo.predict(match.a_name, match.b_name)
        predictions[algo_name].append(prediction)
        algo.update(match)
        print '{0} ({1})'.format(prediction, algo_name)
    print match
    print

# Calculate and print the normal distribution of the deviation from 
# the actual match results for every algorithm
d = float(len(matches))
best_score = None
best_algo  = None
for algo in algorithms:
    algo_name = algo.__class__.__name__
    zipped = zip(predictions[algo_name], matches)
    loss   = [p.a_score - m.a_score for p, m in zipped] + \
             [p.b_score - m.b_score for p, m in zipped]
    mu     = sum(loss) / d
    sigma  = math.sqrt(sum([l ** 2 for l in loss]) / d)
    score  = abs(mu) + sigma
    print 'score: %1.2f (% 1.2f ± %1.2f0 for %s' % (score, mu, sigma, algo_name)
    if best_score == None or best_score > score:
        best_score = score
        best_algo  = algo

print
print 'NEW PREDICTIONS by ' + best_algo.__class__.__name__

# Simply pop future games in here and out comes a prediction
future_matches = [
    ('Vitesse', 'Heracles Almelo'),
    ('RKC Waalwijk', 'De Graafschap'),
    ('Excelsior', 'Roda JC Kerkrade'),
    ('VVV-Venlo', 'NEC'),
    ('ADO Den Haag', 'Ajax'),
    ('PSV', 'sc Heerenveen'),
    ('FC Utrecht', 'FC Groningen'),
    ('FC Twente', 'Feyenoord'),
    ('AZ', 'NAC Breda')
]

teams = set([m.a_name for m in matches] +
            [m.b_name for m in matches])
fm_teams = set([a for a, _ in future_matches] +
               [b for _, b in future_matches])

missing_teams = [t for t in fm_teams if not (t in teams)]
for team in missing_teams:
    print 'Warning! Unknown team ' + team

print

name_w = max([len(t) for t in teams])
for a, b in future_matches:
    print ' ' * (name_w - len(a)) + repr(best_algo.predict(a, b))
