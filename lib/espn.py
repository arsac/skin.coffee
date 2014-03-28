#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2012-2013 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import xbmc
import xbmcaddon
import json
import urllib2
from datetime import datetime, timedelta
import time
import logging

from common import log

ESPN_URL = 'http://scores.espn.go.com/aggregator/cached/tea/feed'
ESPN_SPORTS = [
    {
        'sport' : 'nba',
        'league' : 'nba'
    },
    {
        'sport' : 'ncb',
        'league' : 'ncb'
    },
    {
        'sport' : 'soccer',
        'league' : 'soccer23'
    }
]
ESPN_TZ = "America/New_York"
INTERVAL = 60

def _unicode( text, encoding="utf-8" ):
    try: text = unicode( text, encoding )
    except: pass
    return text

def isActiveTeam(sport,league,game):
    for k in ESPN_SPORTS:
        if k["sport"] == sport and k["league"] == league:
            if "team" in k.keys():
                _team = k.get("team")
                if _team == game.get("home").get("id") or _team == game.get("away").get("id"):
                    return True
                else:
                    return False
            else:
                return True
    return False

def isActiveLeague(sport,league):
    for k in ESPN_SPORTS:
        if k["sport"] == sport and k["league"] == league:
            return True
    return False

def isValidGame(game):
    return True
    now = datetime.now()
    _date = datetime.strptime("%s" % game.get("date"),"%Y%m%d%H%M%S") - timedelta(hours=3)
    if now.strftime("%Y%m%d") != _date.strftime("%Y%m%d") or (game.get("status") == "F" and now - _date > 3000) :
        return False
        
    return True

def formatGame(game):
    now = datetime.now()
    _d = {
        "gameId" : game.get("gameId"),
        "tv" : game.get("tv")
    }
    _date = datetime.strptime("%s" % game.get("date"),"%Y%m%d%H%M%S") - timedelta(hours=3)
    
    #_d = game.get("date")
    #_date = datetime(_d[:4],_d[4:6],_d[6:8],_d[8:10],_d[10:12], _d[12:14]),)
    
    
    
    _d["date"] = _date
    _d["label"] = "%s AT %s" % (game.get("away").get("name"), game.get("home").get("name"))
    if now > _date:
        #if game.get("status") == "F":
            
        _d["label2"] = _unicode(game.get("statusText"))
    else:
        _d["label2"] = _date.strftime("%H:%M")
    return _d
    

class EspnScoreboard:
    def __init__(self):
        self._last_fetch = False
        self._last_snapshotId = False
        self.data = {}
        self.isReady = False
        
    
    
    def get_data(self):
        return self._fetch_scoreboard()
    
    def _fetch_scoreboard(self, force = False):
        now = time.time()
        
        if not xbmc.abortRequested and ( not self._last_fetch or now > self._last_fetch + INTERVAL):
            log("Fetching data from ESPN")
            self._last_fetch = now
            #result = json.load(urllib2.urlopen(ESPN_URL))
            result = json.load(open("%s/test.json" % os.path.dirname(os.path.realpath(__file__))))
            
            snapshotId = result.get("snapshotId")
            
            if self._last_snapshotId == snapshotId:
                log("Snapshot Id is the same, no new data")
                return False
            
            log("New Snapshot Id, building data")
            
            self._last_snapshotId = snapshotId         
            data = {}
            if "sports" in result.keys():
                result = result.get("sports")
                for k in result:
                    if "sport" in k.keys() and "leagues" in k.keys():
                        _sport = k["sport"]
                        for l in k["leagues"]:
                            if "league" in l.keys() and isActiveLeague(_sport,l["league"]):
                                games = []
                                for g in l.get("games"):
                                    if isActiveTeam(_sport,l["league"],g) and isValidGame(g):
                                        games.append(formatGame(g))
                                data[l["league"]] = games
                                
            self.data = data
            return self.data
        
        return False
