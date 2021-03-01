import pandas as pd
import numpy as np

class NFL_Model():
    def __init__(self, year, week, weighting_full, weighting_bye):
        self.year = year
        self.week = week
        self.weighting_full = weighting_full
        self.weighting_bye = weighting_bye
        
    def get_dvoa(self, csvs=None):
        if self.week != 0:
            if not csvs:
                dvoa = pd.read_html("https://www.footballoutsiders.com/stats/nfl/team-efficiency/2020")[0]
            else:
                dvoa = pd.read_csv("C:/Users/agad4/OneDrive/Documents/python_work/baseball/mysite/nfl/static/nfl/2020 Team DVOA Ratings Overall.csv")
            dvoa_proj = pd.read_html("https://www.footballoutsiders.com/dvoa-ratings/2020/2020-dvoa-projections")[0]

            def dvoa_cleanup(seaworth, proj):
                if proj:
                    seaworth.columns = seaworth.loc[0, :]
                    seaworth.drop(0, inplace=True)
                seaworth.replace(regex='%', value='', inplace=True)
                for i in range(0, len(seaworth.columns)):
                    try:
                        seaworth.iloc[:, i] = seaworth.iloc[:, i].astype(float)
                    except:
                        continue
                if (not proj) & (self.weighting_full != 1):
                    seaworth.rename(columns={'Total DVOA': 'dvoa',
                                             'DAVE': 'dave',
                                             'Offense DVOA': 'dvoa_o',
                                             'Defense DVOA': 'dvoa_d',
                                             'Special Teams DVOA': 'dvoa_st',
                                             'Team': 'team'}, inplace=True)    
                    pcts = ['dvoa', 'dave', 'dvoa_o', 'dvoa_d', 'dvoa_st']
                elif (not proj) & (self.weighting_full == 1):
                    seaworth.rename(columns={'Total DVOA': 'dvoa',
                                             'Weighted DVOA': 'dave',
                                             'Offense DVOA': 'dvoa_o',
                                             'Defense DVOA': 'dvoa_d',
                                             'Special Teams DVOA': 'dvoa_st',
                                             'Team': 'team'}, inplace=True)
                    pcts = ['dvoa', 'dave', 'dvoa_o', 'dvoa_d', 'dvoa_st']
                else:
                    seaworth.rename(columns={'TOTAL  DVOA': 'dvoa',
                                         'OFF.  DVOA': 'dvoa_o',
                                         'DEF.  DVOA': 'dvoa_d',
                                         'S.T.  DVOA': 'dvoa_st',
                                         'TEAM': 'team'}, inplace=True)    
                    pcts = ['dvoa', 'dvoa_o', 'dvoa_d', 'dvoa_st']
                for i in pcts:
                    seaworth[i] = seaworth[i] / 100
                seaworth.sort_values('team', inplace=True)
                seaworth.reset_index(drop=True, inplace=True)
                return seaworth
            
            dvoa = dvoa_cleanup(dvoa, proj=False)
            dvoa_proj = dvoa_cleanup(dvoa_proj, proj=True)
            
            records = dvoa['W-L'].str.split('-')
            games = []
            for i in records:
                total = 0
                for x in i:
                    total += int(x)
                games.append(total)
            dvoa['games'] = games
            
            dvoa['dave_o'] = np.where(dvoa['games'] == self.week, 
                                      (self.weighting_full * dvoa['dvoa_o']) + ((1-self.weighting_full) * dvoa_proj['dvoa_o']),
                                      (self.weighting_bye * dvoa['dvoa_o']) + ((1-self.weighting_bye) * dvoa_proj['dvoa_o']))
            dvoa['dave_d'] = np.where(dvoa['games'] == self.week,
                                      (self.weighting_full * dvoa['dvoa_d']) + ((1-self.weighting_full) * dvoa_proj['dvoa_d']),
                                      (self.weighting_bye * dvoa['dvoa_d']) + ((1-self.weighting_bye) * dvoa_proj['dvoa_d']))
            dvoa['dave_st'] = np.where(dvoa['games'] == self.week,
                                       (self.weighting_full * dvoa['dvoa_st']) + ((1-self.weighting_full) * dvoa_proj['dvoa_st']),
                                       (self.weighting_bye * dvoa['dvoa_st']) + ((1-self.weighting_bye) * dvoa_proj['dvoa_st']))
            
            return dvoa

        else:
            dvoa = pd.read_html("https://www.footballoutsiders.com/dvoa-ratings/2020/2020-dvoa-projections")[0]
            dvoa.columns = dvoa.loc[0, :]
            dvoa.drop(0, inplace=True)
            dvoa.replace(regex='%', value='', inplace=True)
            for i in range(0, len(dvoa.columns)):
                try:
                    dvoa.iloc[:, i] = dvoa.iloc[:, i].astype(float)
                except:
                    continue
            dvoa.rename(columns={'TOTAL  DVOA': 'dvoa',
                                 'OFF.  DVOA': 'dvoa_o',
                                 'DEF.  DVOA': 'dvoa_d',
                                 'S.T.  DVOA': 'dvoa_st',
                                 'TEAM': 'team'}, inplace=True)    
            pcts = ['dvoa', 'dvoa_o', 'dvoa_d', 'dvoa_st']
            for i in pcts:
                dvoa[i] = dvoa[i] / 100
            dvoa.sort_values('team', inplace=True)
            dvoa.reset_index(drop=True, inplace=True)
        
        return dvoa
    
    def get_pfr(self):
        pfr_urls = {2020: "http://pfref.com/pi/share/RxYj9", 2019: "http://pfref.com/pi/share/1cnN2", 
                    2018: "http://pfref.com/pi/share/oXSmR", 2017: "http://pfref.com/pi/share/vALS1", 
                    2016: "http://pfref.com/pi/share/Q7eFC"}
        lg_ppp = {2020: [], 2019: [],2018: [],2017: [],2016: []}
        lg_ypp = {2020: [], 2019: [],2018: [],2017: [],2016: []}
        lg_ypt = {2020: [], 2019: [],2018: [],2017: [],2016: []}
        for i in range(2016, 2021):
            pfr = pd.read_html(pfr_urls[i])[0]
            pfr.drop([32, 33, 34], axis=0, inplace=True)
            
            pts = pfr[('Unnamed: 3_level_0', 'PF')]
            yds = pfr[('Unnamed: 4_level_0', 'Yds')]
            ply = pfr[('Tot Yds & TO', 'Ply')]
            
            lg_ppp[i].append(pts.sum() / ply.sum())
            lg_ypp[i].append(yds.sum() / ply.sum())
            lg_ypt[i].append(yds.sum() / pts.sum())
        
        weighted_ppp = ((((sum(lg_ppp[2019])*1.75) + (sum(lg_ppp[2018])*1.5) + (sum(lg_ppp[2017])*0.5) + (sum(lg_ppp[2016])*0.25)) / 4) * (1-self.weighting_full)) + (sum(lg_ppp[2020]) * self.weighting_full)
        weighted_ypp = ((((sum(lg_ypp[2019])*1.75) + (sum(lg_ypp[2018])*1.5) + (sum(lg_ypp[2017])*0.5) + (sum(lg_ypp[2016])*0.25)) / 4) * (1-self.weighting_full)) + (sum(lg_ypp[2020]) * self.weighting_full)
        weighted_ypt = ((((sum(lg_ypt[2019])*1.75) + (sum(lg_ypt[2018])*1.5) + (sum(lg_ypt[2017])*0.5) + (sum(lg_ypt[2016])*0.25)) / 4) * (1-self.weighting_full)) + (sum(lg_ypt[2020]) * self.weighting_full)
        
        return {'ppp': weighted_ppp, 'ypp': weighted_ypp, 'ypt': weighted_ypt}

    def get_pace(self, csvs=None):
        pace20 = {2020: pd.DataFrame(), 2019: pd.DataFrame(), 2018: pd.DataFrame(), 2017: pd.DataFrame(), 2016: pd.DataFrame()}
        team_change = {'SD': 'LAC', 'STL': 'LAR', 'OAK': 'LV'}
        for i in range(2016, 2021):
            if not csvs:
                pace = pd.read_html(f"https://www.footballoutsiders.com/stats/nfl/pace-stats/{i}")[0]
            else:
                pace = pd.read_csv(f"C:/Users/agad4/OneDrive/Documents/python_work/baseball/mysite/nfl/static/nfl/{i} NFL Pace_Time Stats.csv")
            pace.query("Team != 'Avg'", inplace=True)
            pace.query("Team != 'NFL'", inplace=True)
            teams = []
            for x in pace['Team']:
                try:
                    teams.append(team_change[x])
                except:
                    teams.append(x)
            pace['Team'] = teams
            pace.sort_values('Team', inplace=True)
            
            pace.rename(columns={'Sec/Play(situationneutral)': 'spp'}, inplace=True)
        
            pace = pace[['Team', 'spp']]
            pace.reset_index(drop=True, inplace=True)
            pace['mpp'] = pace['spp'] / 60
            pace['plpg'] = 30 / pace['mpp']
            
            pace20[i] = pace20[i].append(pace)
        
        pacenew = pd.DataFrame({'team': pace20[2020]['Team'], 
                                     'pace': ((((pace20[2019]['plpg']*2) + (pace20[2018]['plpg']*1.25) + (pace20[2017]['plpg']*0.5) + (pace20[2016]['plpg']*0.25)) / 4) * (1-self.weighting_full)) + (pace20[2020]['plpg']*self.weighting_full)})
        pace20_d = ((((pace20[2019]['plpg'].mean()*2) + (pace20[2018]['plpg'].mean()*1.25) + (pace20[2017]['plpg'].mean()*0.5) + (pace20[2016]['plpg'].mean()*0.25)) / 4) * (1-self.weighting_full)) + (pace20[2020]['plpg'].mean()*self.weighting_full)            
                
        return [pacenew, pace20_d]
  
    def get_hfa(self):
        schedule = pd.read_csv(r"C:\Users\agad4\OneDrive\Documents\python_work\baseball\mysite\nfl\static\nfl\nfl_schedules.csv") \
            .query("(game_type == 'REG') & (location != 'Neutral')")
        schedule['away_team'] = np.where(schedule['away_team'] == 'SD', 'LAC',
                                         np.where(schedule['away_team'] == 'OAK', 'LV',
                                                  np.where(schedule['away_team'] == 'LA', 'LAR',
                                                           schedule['away_team'])))
        schedule['home_team'] = np.where(schedule['home_team'] == 'SD', 'LAC',
                                         np.where(schedule['home_team'] == 'OAK', 'LV',
                                                  np.where(schedule['home_team'] == 'LA', 'LAR',
                                                           schedule['home_team'])))
                        
        away_games = schedule.groupby('away_team').agg({'game_id': pd.Series.nunique,
                                                        'home_result': 'sum'})
        away_games.reset_index(inplace=True)
        away_games['home_result'] = -1 * away_games['home_result']
        away_games.rename(columns={'game_id': 'away_games', 'home_result': 'away_result', 'away_team': 'team'}, inplace=True)
        home_games = schedule.groupby('home_team').agg({'game_id': pd.Series.nunique,
                                                        'home_result': 'sum'})
        home_games.reset_index(inplace=True)
        home_games.rename(columns={'game_id': 'home_games', 'home_team': 'team'}, inplace=True)
        all_games = home_games.merge(away_games)
        all_games['all_result'] = all_games['home_result'] + all_games['away_result']
        all_games['all_games'] = all_games['home_games'] + all_games['away_games']
        
        all_games['pdpg_all'] = all_games['all_result'] / all_games['all_games']
        home_games['pdpg_home'] = home_games['home_result'] / home_games['home_games']
        
        hfa = all_games[['team', 'pdpg_all']].merge(home_games[['team', 'pdpg_home']])
        hfa['hfa'] = hfa['pdpg_home'] - hfa['pdpg_all']
        
        return hfa

    def get_ratings(self, pace_csv=None, dvoa_csv=None):
        tempo = self.get_pace(csvs=pace_csv)
        dvoa = self.get_dvoa(csvs=dvoa_csv)
        hfa = self.get_hfa()
        lg_stats = self.get_pfr()
        
        offense = dvoa[['team', 'dave_o']]
        offense = offense.merge(tempo[0])
        offense['adj_ypp_o'] = (offense['dave_o'] * lg_stats['ypp']) + lg_stats['ypp']
        offense['adj_ppg_o'] = (offense['pace'] * offense['adj_ypp_o']) / lg_stats['ypt']
        
        defense = dvoa[['team', 'dave_d', 'dave_st']]
        defense['adj_ypp_d'] = (defense['dave_d'] * lg_stats['ypp']) + lg_stats['ypp']
        defense['adj_ppg_d'] = (tempo[1] * defense['adj_ypp_d']) / lg_stats['ypt']
        
        nfl_ratings = offense.merge(defense)
        nfl_ratings.loc[:, nfl_ratings.columns != 'team'] = nfl_ratings.loc[:, nfl_ratings.columns != 'team'].astype(float)
        avg_ppg = nfl_ratings[['adj_ppg_o', 'adj_ppg_d']].mean().mean()
        nfl_ratings['adj_ppg_st'] = nfl_ratings['dave_st'] * avg_ppg
        nfl_ratings['overall'] = nfl_ratings['adj_ppg_o'] - nfl_ratings['adj_ppg_d'] + nfl_ratings['adj_ppg_st']
        nfl_ratings = nfl_ratings.merge(hfa.drop(['pdpg_all', 'pdpg_home'], axis=1))
        nfl_ratings['hfa'] = nfl_ratings['hfa'].astype(float)
        
        nfl_ratings['ovr_rank'] = nfl_ratings['overall'].rank(ascending=False)
        nfl_ratings['off_rank'] = nfl_ratings['adj_ppg_o'].rank(ascending=False)
        nfl_ratings['def_rank'] = nfl_ratings['adj_ppg_d'].rank()
        nfl_ratings['st_rank'] = nfl_ratings['adj_ppg_st'].rank(ascending=False)
        nfl_ratings['pac_rank'] = nfl_ratings['pace'].rank(ascending=False)
        nfl_ratings['hfa_rank'] = nfl_ratings['hfa'].rank(ascending=False)

        return nfl_ratings