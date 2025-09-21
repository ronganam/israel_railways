# israel_railways_api.py
import aiohttp
import asyncio
import datetime
import json

class IsraelRailwaysAPI:
    def __init__(self, station_a, station_b):
        self.station_a = station_a
        self.station_b = station_b
        self.base_url = "https://rail-api.rail.co.il/rjpa/api/v1/timetable/searchTrain"
    
    async def get_next_train(self):
        date_now = datetime.datetime.now()
        date_str = date_now.strftime('%Y-%m-%d')
        hour_str = date_now.strftime('%H:%M')
        
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '5e64d66cf03f4547bcac5de2de06b566',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.rail.co.il',
            'Referer': 'https://www.rail.co.il/'
        }
        
        # Create the JSON payload based on the new API format
        payload = {
            "methodName": "searchTrainLuzForDateTime",
            "fromStation": int(self.station_a),
            "toStation": int(self.station_b),
            "date": date_str,
            "hour": hour_str,
            "systemType": "2",
            "scheduleType": "ByDeparture",
            "languageId": "Hebrew",
            "requestLocation": '{"latitude":"0.0","longitude":"0.0"}',
            "requestIP": "176.228.67.5",
            "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0",
            "screenResolution": '{"height":1169,"width":1800}',
            "searchFromFavorites": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=headers,
                data=json.dumps(payload)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    travels = data['result']['travels']
                    for travel in travels:
                        departure_time = datetime.datetime.fromisoformat(travel['departureTime'])
                        if departure_time >= date_now:
                            return travel['trains'][0]
        return None
    
    async def get_station_name(self):
        station_a, station_b = "", ""
        url = "https://rail-api.rail.co.il/common/api/v1/stations?languageId=Hebrew&systemType=2"
        headers = {'Ocp-Apim-Subscription-Key': '5e64d66cf03f4547bcac5de2de06b566'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    for station in data["result"]:
                        if station["stationId"] == int(self.station_a):
                            station_a = station["stationName"]
                        if station["stationId"] == int(self.station_b):
                            station_b = station["stationName"]
                        if station_a!="" and station_b!="":
                            break
        return station_a, station_b
