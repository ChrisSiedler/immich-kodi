
import sys
import xbmcgui
import xbmcplugin
import datetime

from immich import IMMICH, KodiContent

from utils import (
    get_url,
    next_month
)

HANDLE = int(sys.argv[1])

#--------------------------------------       
def list_timeline():

    buckets = IMMICH.getTimeBuckets()
    

    items = []
    for bucket in buckets:
        if bucket.count == 0:   # skip empty albums
            continue


        startdate = datetime.datetime.strptime(bucket.timeBucket, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
        enddate = next_month(startdate)
            
        item = xbmcgui.ListItem(f"{startdate.strftime('%Y-%m-%d')} -- {enddate.strftime('%Y-%m-%d')}  ({bucket.count}) Items")

        items.append((
            get_url(action="time", id=bucket.timeBucket), 
            item,
            True))
    
    
#    for item, timeline in zip(items, res):
#        item[1].setDateTime(
#            last_day_of_month(datetime.fromisoformat(timeline.timeBucket)).strftime(
#                "%Y-%m-%dT00:00:00Z"
#            )
#        )

    xbmcplugin.setContent(HANDLE, "files")
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


#--------------------------------------
def time(id):
   
    startdate = datetime.datetime.strptime(id, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc)
    enddate = next_month(startdate)

    bucket = IMMICH.getTimeBucket(startdate, enddate)
    KodiContent(HANDLE, bucket["assets"])
