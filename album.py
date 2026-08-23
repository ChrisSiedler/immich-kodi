
import sys
import xbmcgui
import xbmcplugin

from immich import IMMICH, KodiContent
HANDLE = int(sys.argv[1])

from utils import (
    get_url
)

def list_albums():
    albums = IMMICH.getAllAlbums()
    
    items = []
    for album in albums:
        if album.assetCount == 0:   # skip empty albums
            continue
            
        item = xbmcgui.ListItem(album.albumName)
        
        if album.albumThumbnailAssetId:
            item.setArt({"thumb": IMMICH.getThumbUrl(album.albumThumbnailAssetId)})

        if album.startDate:
            item.setDateTime(album.startDate.strftime("%Y-%m-%dT%H:%M:%SZ"))

        if album.description: 
            item.setInfo(
                type='video', 
                infoLabels={
                    'title': album.albumName,
                    'plot':  album.description
                    }
	        )
            
        items.append((
            get_url(action="album", id=album.id), 
            item,
            True))
            

    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_LABEL)

    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))      
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
     
#--------------------------------------       
def list_favorites():

    favorites = IMMICH.getFavoriteAssets()
    KodiContent(HANDLE, favorites["assets"], "album")    
   
         
#--------------------------------------       
def album(id):
    album = IMMICH.get_album(id)
    KodiContent(HANDLE, album["assets"], "album")    

    
