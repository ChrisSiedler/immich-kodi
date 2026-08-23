#!/usr/bin/env python3

import requests
import logging
import sys
from lib.models import Album, ItemAsset, TimelineBucket

class Immich_API():
    def __init__(self, RAW_SERVER_URL, APIKey, favonly=False):
        self.url    = RAW_SERVER_URL
        self.APIKey = APIKey
        
        self.global_filter = {
            "visibility": "timeline",
            "withExif": True
            }

        if favonly:
            self.global_filter['isFavorite'] = True

    #---------------------------------------------------------
    @staticmethod
    def _user_agent():
        try:
            import xbmc
            return xbmc.getUserAgent()
        except ModuleNotFoundError:
            return "Immich-API 0.1"
            
    #---------------------------------------------------------
    def _api_call(self, action, path, payload=None):
        url = f"{self.url}/api/{path}"

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': self.APIKey,
            "User-agent": self._user_agent(),
            }

        resp = requests.request(action, url, headers=headers, json=payload)

        if resp.status_code == 403:
            print(resp.text)
            raise PermissionError

        elif resp.status_code == 401:
            print(resp.text)
            raise ConnectionError
#            return false

        elif resp.status_code != 200:
            print(resp.status_code, resp.text)
            raise ConnectionError
#            return false
            
        response = resp.json()
        return response

    #---------------------------------------------------------
    def get_version(self):
        return self._api_call("GET", "server/version")

    #---------------------------------------------------------
    def getAllAlbums(self):
        resp = self._api_call("GET", "albums")
        return [Album.from_api_response(d) for d in resp ]
        
    #---------------------------------------------------------
    def getTimeBuckets(self):
        resp = self._api_call("GET", "timeline/buckets")
        return [TimelineBucket.from_api_response(d) for d in resp ]

    #---------------------------------------------------------
    def getThumbUrl(self, uuid):
        return self.getAssetUrl(uuid, size="thumbnail")

    #---------------------------------------------------------
    def getAssetUrl(self, uuid, size="original"):
        if size=="original":
            return f"{self.url}/api/assets/{uuid}/original|x-api-key={self.APIKey}"
            
        elif size in ["original", "fullsize", "preview", "thumbnail"]:
            return f"{self.url}/api/assets/{uuid}/thumbnail?size={size}|x-api-key={self.APIKey}"

        elif size == "video": # Transcoded video
            return f"{self.url}/api/assets/{uuid}/video/playback|x-api-key={self.APIKey}"
        else:
            raise ValueError
            
    #---------------------------------------------------------
    def get_album(self, id):

        myfilter = self.global_filter.copy()
        myfilter.update({
           "albumIds": [id],
        })
           
        resp = self._api_call("POST", "search/metadata", myfilter)
            
        return {"assets": [ItemAsset.from_api_response(d) for d in resp["assets"]["items"]]}

    #---------------------------------------------------------
    def getTimeBucket(self, startdate, enddate):

        myfilter = self.global_filter.copy()
        myfilter.update({
            "takenAfter": startdate.isoformat(), 
            "takenBefore": enddate.isoformat()
        })
        
        resp = self._api_call("POST", "search/metadata", myfilter)
        
        return {"assets": [ItemAsset.from_api_response(d) for d in resp["assets"]["items"]]}
    #---------------------------------------------------------
    def getFavoriteAssets(self):

        myfilter = self.global_filter.copy()
        myfilter.update({
            "isFavorite": True
        })
        
        resp = self._api_call("POST", "search/metadata", myfilter)
        
        return {"assets": [ItemAsset.from_api_response(d) for d in resp["assets"]["items"]]}
        
    #---------------------------------------------------------
    def get_random_Asset(self, filter={"size": 1}):    
        # Just get one random picture

        myfilter = self.global_filter.copy()
        myfilter.update(filter)

        return self._api_call("POST", "search/random", myfilter)
        
    #---------------------------------------------------------
    def getAssetInfo(self, assetId):
	    return self._api_call("GET", f"assets/{assetId}")

    #---------------------------------------------------------
    def getParrentAlbums(self, assetId):
	    response = self._api_call("GET", f"albums?assetId={assetId}")
	    
	    blacklist = ['Bilderrahmen']
	    	    
	    return [x for x in response if x['albumName'] not in blacklist]
	    
            
# ======================================================================================
# ======================================================================================
    
