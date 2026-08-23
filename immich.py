#!/usr/bin/env python3

import xbmcgui
import xbmcplugin
import xbmcaddon
from lib.immich_api import Immich_API

addon = xbmcaddon.Addon()

IMMICH = Immich_API(
	addon.getSettingString("immich_url"),
	addon.getSettingString("api_key"),
	favonly = addon.getSettingBool("fav_only")
	)

#--------------------------------------------------------------------
def KodiContent(HANDLE, assets, t="timeline"):

    items = []
    
    orig = addon.getSettingBool("orig")
    
    for asset in assets:
        item = xbmcgui.ListItem(asset.originalFileName)

        item.setArt({"thumb": IMMICH.getAssetUrl(asset.id, size="thumbnail")})
        item.setProperty("MimeType", asset.originalMimeType)
        item.setDateTime(asset.fileCreatedAt.strftime("%Y-%m-%dT%H:%M:%SZ"))

        # item.setLabel(asset.exifInfo.description) # Titel überschreben
        item.setLabel2(asset.exifInfo.description)

            
        if asset.type == "VIDEO":
            tag = item.getVideoInfoTag()
            
            tag.setTitle(asset.originalFileName)
            
            if asset.exifInfo.description:
                tag.setPlot(asset.exifInfo.description)

            if asset.exifInfo.rating:
                tag.setUserRating(asset.exifInfo.rating)
            
            item.setInfo(
                type='video', 
                infoLabels={
                    'userrating': asset.exifInfo.rating,
                    }
	        )

        elif asset.type == "IMAGE":
#            tag = item.getPictureInfoTag()
            
            item.setInfo(
                type='pictures', 
                infoLabels={
                    'title': asset.exifInfo.description,
                    'userrating': asset.exifInfo.rating,
#                    **asset.exifInfo.to_kodi_info()
                    }
	        )


        if orig:
            AssetSize = "original"
        else:
            if asset.type == "VIDEO":
                AssetSize = "video"
            else:
                AssetSize = "preview"
        
        
        # RaspberryPI workarounds:       
        if asset.type == "IMAGE" and AssetSize == "original" and asset.originalMimeType == "image/heic":
                AssetSize = "fullsize"

        if asset.type == "VIDEO" and AssetSize == "original" and asset.originalMimeType == "video/webm":
                AssetSize = "video"            
            
        items.append((
            IMMICH.getAssetUrl(asset.id, size=AssetSize), 
            item,
            False))


    xbmcplugin.setContent(HANDLE, "images")
    xbmcplugin.addDirectoryItems(HANDLE, items, len(items))
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_USER_RATING)
    if t == "album":
        xbmcplugin.addSortMethod(HANDLE, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)
