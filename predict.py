import matplotlib.pyplot as pyplot
import json
import pprint

class MatchInfo:
    TEAM_HOME = 1
    TEAM_AWAY = 2

    def __init__(self, data, team):
        if team == self.TEAM_HOME:
            us, them = 'a', 'b'
            self.is_home = True
        elif team == self.TEAM_AWAY:
            us, them = 'b', 'a'
            self.is_home = False
        else:
            raise 'Invalid value for team'
        self.team       = data[us + '_name']
        self.team_score = data[us + '_score']
        self.opponent       = data[them + '_name']
        self.opponent_score = data[them + '_score']
        self.is_win  = self.team_score > self.opponent_score
        self.is_draw = self.team_score == self.opponent_score
        self.is_loss = self.team_score < self.opponent_score
        self.points  = 3 if self.is_win else 1 if self.is_draw else 0
        
    def __repr__(self):
        return self.team + ' ' + str(self.team_score) + ' - ' \
             + str(self.opponent_score) + ' ' + self.opponent

data = open('match_results.json', 'r').read()
results = json.loads(data);

matches = []
matches.extend([MatchInfo(x, MatchInfo.TEAM_HOME) for x in results])
matches.extend([MatchInfo(x, MatchInfo.TEAM_AWAY) for x in results])

teams = set([m.team for m in matches])
team_matches = {t : [m for m in matches if m.team == t] for t in teams}

