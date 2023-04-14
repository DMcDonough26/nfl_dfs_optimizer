
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import timeit
import numpy as np
from pulp import *


scoring_dict = {}
scoring_dict['passing_yards_score'] = 0.04
scoring_dict['passing_TD_score'] = 4
scoring_dict['passing_interception_score'] = -1
scoring_dict['rushing_yards_score'] = 0.1
scoring_dict['rushing_TD_score'] = 6
scoring_dict['offense_fumble_score'] = -1
scoring_dict['receptions_score'] = 1
scoring_dict['receiving_yards_score'] = 0.1
scoring_dict['receiving_TD_score'] = 6
scoring_dict['sack_score'] = 1
scoring_dict['defense_interception_score'] = 2
scoring_dict['defense_fumble_score'] = 2
scoring_dict['defense_TD_score'] = 6
scoring_dict['safety_score'] = 2
scoring_dict['points_against_score'] = -2/7


def scrape_qb(week,range_val=45):
    url = 'https://www.fantasypros.com/nfl/projections/qb.php?week='+str(week)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    team = []
    attempts = []
    completions = []
    yards = []
    touchdowns = []
    interceptions = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []

    for i in range(week,range_val):
        name = len(str(soup.findAll('td')[4+11*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+11*i].findAll('a')[0]).split('>')[1][0:name-3])
        team.append(str(soup.findAll('td')[4+11*i]).split('a> ')[1].split(' <')[0])
        attempts.append(float(str(soup.findAll('td')[5+11*i]).split('>')[1].split('<')[0]))
        completions.append(float((str(soup.findAll('td')[6+11*i]).split('>')[1].split('<')[0])))
        yards.append(float(str(soup.findAll('td')[7+11*i]).split('>')[1].split('<')[0].split(',')[0]))
        touchdowns.append(float((str(soup.findAll('td')[8+11*i]).split('>')[1].split('<')[0])))
        interceptions.append(float((str(soup.findAll('td')[9+11*i]).split('>')[1].split('<')[0])))
        rush_attempts.append(float((str(soup.findAll('td')[10+11*i]).split('>')[1].split('<')[0])))
        rush_yards.append(float((str(soup.findAll('td')[11+11*i]).split('>')[1].split('<')[0])))
        rush_tds.append(float((str(soup.findAll('td')[12+11*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[13+11*i]).split('>')[1].split('<')[0])))

    qb_projections = pd.DataFrame({'player_stat':player_stat,'team':team,'attempts':attempts,'completions':completions,
                                   'yards':yards,'touchdowns':touchdowns,'interceptions':interceptions,
                                   'rush_attempts':rush_attempts,'rush_yards':rush_yards,'rush_tds':rush_tds,'fumbles':fumbles})

    return qb_projections


def scrape_rb(week,range_val=85):
    url = 'https://www.fantasypros.com/nfl/projections/rb.php?week='+str(week)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    team = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    receptions = []
    receive_yards = []
    receive_tds = []
    fumbles = []
    for i in range(range_val):
        name = len(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1][0:name-3])
        team.append(str(soup.findAll('td')[4+9*i]).split('a> ')[1].split(' <')[0])
        rush_attempts.append(float((str(soup.findAll('td')[5+9*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]) < 6:
            rush_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0])))
        else:
            rush_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]).split(',')[0]+(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]).split(',')[1]))
        rush_tds.append(float((str(soup.findAll('td')[7+9*i]).split('>')[1].split('<')[0])))
        receptions.append(float((str(soup.findAll('td')[8+9*i]).split('>')[1].split('<')[0])))
        receive_yards.append(float((str(soup.findAll('td')[9+9*i]).split('>')[1].split('<')[0])))
        receive_tds.append(float((str(soup.findAll('td')[10+9*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[11+9*i]).split('>')[1].split('<')[0])))

    rb_projections = pd.DataFrame({'player_stat':player_stat,'team':team,'rush_attempts':rush_attempts,
                                   'rush_yards':rush_yards,'rush_tds':rush_tds,'receptions':receptions,
                                   'receive_yards':receive_yards,'receive_tds':receive_tds,'fumbles':fumbles})

    return rb_projections


def scrape_wr(week,range_val=120):
    url = 'https://www.fantasypros.com/nfl/projections/wr.php?week='+str(week)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    team = []
    receptions = []
    receive_yards = []
    receive_tds = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []
    for i in range(range_val):
        name = len(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[4+9*i].findAll('a')[0]).split('>')[1][0:name-3])
        team.append(str(soup.findAll('td')[4+9*i]).split('a> ')[1].split(' <')[0])
        receptions.append(float((str(soup.findAll('td')[5+9*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0]) < 6:
            receive_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0])))
        else:
            receive_yards.append(float((str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0].split(',')[0]+str(soup.findAll('td')[6+9*i]).split('>')[1].split('<')[0].split(',')[1])))
        receive_tds.append(float((str(soup.findAll('td')[7+9*i]).split('>')[1].split('<')[0])))
        rush_attempts.append(float((str(soup.findAll('td')[8+9*i]).split('>')[1].split('<')[0])))
        rush_yards.append(float((str(soup.findAll('td')[9+9*i]).split('>')[1].split('<')[0])))
        rush_tds.append(float((str(soup.findAll('td')[10+9*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[11+9*i]).split('>')[1].split('<')[0])))

    wr_projections = pd.DataFrame({'player_stat':player_stat,'team':team,'receptions':receptions,
                                   'receive_yards':receive_yards,'receive_tds':receive_tds,'rush_attempts':rush_attempts,
                                   'rush_yards':rush_yards,'rush_tds':rush_tds,'fumbles':fumbles})

    return wr_projections


def scrape_te(week,range_val=70):
    url = 'https://www.fantasypros.com/nfl/projections/te.php?week='+str(week)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    player_stat = []
    team = []
    receptions = []
    receive_yards = []
    receive_tds = []
    rush_attempts = []
    rush_yards = []
    rush_tds = []
    fumbles = []
    for i in range(range_val):
        name = len(str(soup.findAll('td')[3+6*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[3+6*i].findAll('a')[0]).split('>')[1][0:name-3])
        team.append(str(soup.findAll('td')[3+6*i]).split('a> ')[1].split(' <')[0])
        receptions.append(float((str(soup.findAll('td')[4+6*i]).split('>')[1].split('<')[0])))
        if len(str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0]) < 6:
            receive_yards.append(float((str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0])))
        else:
            receive_yards.append(float(str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0].split(',')[0]+str(soup.findAll('td')[5+6*i]).split('>')[1].split('<')[0].split(',')[1]))
        receive_tds.append(float((str(soup.findAll('td')[6+6*i]).split('>')[1].split('<')[0])))
        fumbles.append(float((str(soup.findAll('td')[7+6*i]).split('>')[1].split('<')[0])))

    te_projections = pd.DataFrame({'player_stat':player_stat,'team':team,'receptions':receptions,'receive_yards':receive_yards,
                                   'receive_tds':receive_tds,'fumbles':fumbles})

    return te_projections


def scrape_dst(week,range_val=26):
    url = 'https://www.fantasypros.com/nfl/projections/dst.php?week='+str(week)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    player_stat = []
    sack = []
    interception = []
    fumble_recovered = []
    touchdowns = []
    safety = []
    points_against = []
    yards_against = []

    for i in range(range_val):
        name = len(str(soup.findAll('td')[0+10*i].findAll('a')[0]).split('>')[1])
        player_stat.append(str(soup.findAll('td')[0+10*i].findAll('a')[0]).split('>')[1][0:name-3])
        sack.append(float((str(soup.findAll('td')[1+10*i]).split('>')[1].split('<')[0])))
        interception.append(float((str(soup.findAll('td')[2+10*i]).split('>')[1].split('<')[0])))
        fumble_recovered.append(float((str(soup.findAll('td')[3+10*i]).split('>')[1].split('<')[0])))
        touchdowns.append(float((str(soup.findAll('td')[5+10*i]).split('>')[1].split('<')[0])))
        safety.append(float((str(soup.findAll('td')[6+10*i]).split('>')[1].split('<')[0])))
        points_against.append(float((str(soup.findAll('td')[7+10*i]).split('>')[1].split('<')[0])))
        yards_against.append((str(soup.findAll('td')[8+10*i]).split('>')[1].split('<')[0]))

    dst_projections = pd.DataFrame({'player_stat':player_stat,'sack':sack,'interception':interception,
                                   'fumble_recovered':fumble_recovered,'touchdowns':touchdowns,
                                   'safety':safety,'points_against':points_against,'yards_against':yards_against})

    return dst_projections


def clean_dst(dst_projections):
    name_dict = {'San Francisco 49ers':'49ers',
    'New Orleans Saints':'Saints',
    'Tennessee Titans':'Titans',
    'Denver Broncos':'Broncos',
    'Indianapolis Colts':'Colts',
    'Baltimore Ravens':'Ravens',
    'Cincinnati Bengals':'Bengals',
    'Cleveland Browns':'Browns',
    'New York Jets':'Jets',
    'Pittsburgh Steelers':'Steelers',
    'Los Angeles Chargers':'Chargers',
    'Philadelphia Eagles':'Eagles',
    'Green Bay Packers':'Packers',
    'Los Angeles Rams':'Rams',
    'Miami Dolphins':'Dolphins',
    'Kansas City Chiefs':'Chiefs',
    'Carolina Panthers':'Panthers',
    'Tampa Bay Buccaneers':'Buccaneers',
    'New York Giants':'Giants',
    'Washington Commanders':'Commanders',
    'New England Patriots':'Patriots',
    'Seattle Seahawks':'Seahawks',
    'Buffalo Bills':'Bills',
    'Jacksonville Jaguars':'Jaguars',
    'Chicago Bears':'Bears',
    'Houston Texans':'Texans',
    'Detroit Lions':'Lions',
    'Atlanta Falcons':'Falcons',
    'Las Vegas Raiders':'Raiders',
    'Dallas Cowboys':'Cowboys',
    'Arizona Cardinals':'Cardinals',
    'Minnesota Vikings':'Vikings'}

    abrv_dict = {'49ers':'SF',
    'Saints':'NO',
    'Titans':'TEN',
    'Broncos':'DEN',
    'Colts':'IND',
    'Ravens':'BAL',
    'Bengals':'CIN',
    'Browns':'CLE',
    'Jets':'NYJ',
    'Steelers':'PIT',
    'Chargers':'LAC',
    'Eagles':'PHI',
    'Packers':'GB',
    'Rams':'LAR',
    'Dolphins':'MIA',
    'Chiefs':'KC',
    'Panthers':'CAR',
    'Buccaneers':'TB',
    'Giants':'NYG',
    'Commanders':'WAS',
    'Patriots':'NE',
    'Seahawks':'SEA',
    'Bills':'BUF',
    'Jaguars':'JAC',
    'Bears':'CHI',
    'Texans':'HOU',
    'Lions':'DET',
    'Falcons':'ATL',
    'Raiders':'LV',
    'Cowboys':'DAL',
    'Cardinals':'ARI',
    'Vikings':'MIN'}

    dst_projections['player_stat'] = [name_dict[x] for x in dst_projections['player_stat']]
    dst_projections['team'] = [abrv_dict[x] for x in dst_projections['player_stat']]

    return dst_projections


def combine_projections(qb_projections,rb_projections,wr_projections,te_projections,dst_projections):
    all_projections = pd.concat([qb_projections[['player_stat','team','points']],rb_projections[['player_stat','team','points']],
                             wr_projections[['player_stat','team','points']], te_projections[['player_stat','team','points']],
                             dst_projections[['player_stat','team','points']]])

    all_projections.sort_values(by='points',ascending=False,inplace=True)

    return all_projections


def clean_name(x):
    if x['Position'] == 'DST':
        return x['Name'].split(' ')[0]
    else:
        return x['Name']

def get_salaries():
    df_raw = pd.read_csv('DKSalaries.csv')
    df_raw['Name'] = df_raw.apply(clean_name,axis=1)

    return df_raw


def check_players(x, position, droplist, df_raw):
    print("In projections, but not in salaries: ")
    temp = x[x['team'].apply(lambda x: True if x not in droplist else False)]
    for index, player in enumerate(temp['player_stat']):
        if player not in df_raw['Name'].unique():
            print(index,' ',player)
    test_df = df_raw[df_raw['Position']==position].merge(x,how='left',left_on='Name',right_on='player_stat')
    missing_df = test_df[(test_df['player_stat'].isna())]
    if len(missing_df) > 0:
        print('\nIn salaries, but not in projections:')
        return missing_df.head(20)
