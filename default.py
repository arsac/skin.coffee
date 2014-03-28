#!/usr/bin/env python
# encoding: utf-8
"""
default.py

Created by Mailo Arsac on 2014-03-24.
Copyright (c) 2014 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import xbmc
import xbmcgui
import datetime
import lib.common
from lib.common import log
from lib.espn import EspnScoreboard
import json
import urllib2

### get addon info
__addon__        = lib.common.__addon__
__addonprofile__ = lib.common.__addonprofile__
__version__      = lib.common.__version__

WINDOW = xbmcgui.Window(10000)
ESPN_CONTROL_ID = 999999


import logging

def Log(obj):
    logging.error(obj)
        
class Main:
    def __init__(self):
        WINDOW.clearProperty('SkinCoffee_Running')
        
        WINDOW.setProperty('SkinCoffee_Running', 'true')
        self._home_espn_list_items = {}
        self.EspnScoreboard = EspnScoreboard()
        
        
        
        self._daemon()
    def _daemon(self):
        # deamon is meant to keep script running at all time
        count = 0
        home_update = False
        while (not xbmc.abortRequested) and WINDOW.getProperty('SkinCoffee_Running') == 'true':
            if count > 0:
                xbmc.sleep(500)
            count += 1
            if not xbmc.Player().isPlayingVideo():
                espn_data = self.EspnScoreboard.get_data()
                Log(type(espn_data))
                if type(espn_data) is not bool:
                    ctl = WINDOW.getControl(ESPN_CONTROL_ID)
                
                
                    ctl.reset()
                
                
                    for league in espn_data.keys():
                        games = espn_data[league]
                        for game in games:
                            _item = xbmcgui.ListItem(game.get("label"),game.get("label2"),"sports/leagues/%s.png" %  league)
                            tv = game.get("tv").lower()
                            _item.setProperty("tv","tv/%s.png" %  tv)
                        
                            #_item.setProperty("gameId",game.get("gameId"))
                            #self._widget_ids[game.get("gameId")] = _item.getId()
                            ctl.addItem(_item)
                        
                
        

if (__name__ == "__main__"):
    log('script version %s started' % __version__)
    Main()
    del Main
    log('script version %s stopped' % __version__)