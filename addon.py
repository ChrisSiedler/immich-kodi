import socket

import sys
import datetime
from urllib.parse import parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin

from album import list_albums, list_favorites, album
from timeline import list_timeline, time
from utils import get_url, set_locale

from immich import IMMICH

DEBUG = False
if DEBUG:
    import debug

URL = sys.argv[0]
HANDLE = int(sys.argv[1])
addon = xbmcaddon.Addon()

if __name__ == '__main__':
    set_locale()
    params = dict(parse_qsl(sys.argv[2][1:]))

    try:
        IMMICH.get_version()
    except Exception as e:
        raise Exception('Can\'t connect to Immich')

    if not params.get('action'):
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action='timeline'),
                                    xbmcgui.ListItem(addon.getLocalizedString(30002)), True)

#       xbmcplugin.addDirectoryItem(HANDLE, get_url(action='timeline', video='1'),
#                                    xbmcgui.ListItem(addon.getLocalizedString(30015)), True)
        xbmcplugin.addDirectoryItem(HANDLE, get_url(action='albums'),
                                    xbmcgui.ListItem(addon.getLocalizedString(30003)), True)

        xbmcplugin.addDirectoryItem(HANDLE, get_url(action='favorites'),
                                    xbmcgui.ListItem(addon.getLocalizedString(30004)), True)
        xbmcplugin.endOfDirectory(HANDLE)
        
    elif params['action'] == 'settings':
        addon.openSettings()
    elif params['action'] == 'timeline':
        list_timeline()
    elif params['action'] == 'albums':
        list_albums()
    elif params['action'] == 'album':
        album(params['id'])
    elif params['action'] == 'time':
        time(params['id'])
    elif params['action'] == 'favorites':
        list_favorites()
        
if DEBUG:
    import pydevd

    pydevd.stoptrace()
