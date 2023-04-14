
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import random
import timeit
import numpy as np
from pulp import *


def get_scoring_dict():
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

    return scoring_dict

def qb_scoring(x, scoring_dict):
    points = x['yards'] * scoring_dict['passing_yards_score'] + x['touchdowns'] * scoring_dict['passing_TD_score'] +\
        x['interceptions'] * scoring_dict['passing_interception_score'] +\
        x['rush_yards'] * scoring_dict['rushing_yards_score'] + x['rush_tds'] * scoring_dict['rushing_TD_score'] +\
        x['fumbles'] * scoring_dict['offense_fumble_score']

    if x['yards'] >= 300:
        points += 3

    if x['rush_yards'] >= 100:
        points += 3

    return points


def rb_scoring(x, scoring_dict):
    points = x['rush_yards'] * scoring_dict['rushing_yards_score'] + x['rush_tds'] * scoring_dict['rushing_TD_score'] +\
    x['receptions'] * scoring_dict['receptions_score'] + x['receive_yards'] * scoring_dict['receiving_yards_score'] +\
    x['receive_tds'] * scoring_dict['receiving_TD_score'] + x['fumbles'] * scoring_dict['offense_fumble_score']

    if x['rush_yards'] >= 100:
        points += 3

    if x['receive_yards'] >= 100:
        points += 3

    return points


def wr_scoring(x, scoring_dict):
    points = x['rush_yards'] * scoring_dict['rushing_yards_score'] + x['rush_tds'] * scoring_dict['rushing_TD_score'] +\
    x['receptions'] * scoring_dict['receptions_score'] + x['receive_yards'] * scoring_dict['receiving_yards_score'] +\
    x['receive_tds'] * scoring_dict['receiving_TD_score'] + x['fumbles'] * scoring_dict['offense_fumble_score']

    if x['rush_yards'] >= 100:
        points += 3

    if x['receive_yards'] >= 100:
        points += 3

    return points


def te_scoring(x, scoring_dict):
    points = x['receptions'] * scoring_dict['receptions_score'] +\
    x['receive_yards'] * scoring_dict['receiving_yards_score'] + x['receive_tds'] * scoring_dict['receiving_TD_score'] +\
    x['fumbles'] * scoring_dict['offense_fumble_score']

    if x['receive_yards'] >= 100:
        points += 3

    return points


def dst_scoring(x, scoring_dict):
    points = x['sack'] * scoring_dict['sack_score'] + x['interception'] * scoring_dict['defense_interception_score'] +\
    x['fumble_recovered'] * scoring_dict['defense_fumble_score'] + x['touchdowns'] * scoring_dict['defense_TD_score'] +\
    x['safety'] * scoring_dict['safety_score'] + x['points_against'] * scoring_dict['points_against_score'] + 7

    return points
