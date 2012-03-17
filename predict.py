import matplotlib.pyplot as pyplot
import json
import pprint

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
    def __init__(self, num, wins, draws):
        self.num    = num
        self.wins   = wins
        self.draws  = draws
        self.losses = num - wins - draws
        self.p_win  = (1. / 3.) if num == 0 else float(self.wins)  / num
        self.p_draw = (1. / 3.) if num == 0 else float(self.draws) / num
        self.p_loss = 1. - self.p_win - self.p_draw

    def __repr__(self):
        return 'wins = {0}, draws = {1}, losses = {2}'.format(
            self.wins, self.draws, self.num - self.wins - self.draws);

def calc_stats(matches, team):
    filtered = [m for m in matches if m.a_name == team or m.b_name == team]
    wins  = [m for m in filtered if m.winner == team]
    draws = [m for m in filtered if m.result == MatchResult.DRAW]
    stats = Stats(len(filtered), len(wins), len(draws))
    return stats

class NaiveClassifier:
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

data = open('match_results.json', 'r').read()
data_json = json.loads(data)

matches = [MatchResult(x['a_name'], x['a_score'], x['b_name'], x['b_score']) 
           for x in data_json]

algorithms = [NaiveClassifier()]

for match in matches:
    for algo in algorithms:
        prediction = algo.predict(match.a_name, match.b_name)
        algo.update(match)
        print '{0} ({1})'.format(prediction, algo.__class__.__name__)
    print match
    print
