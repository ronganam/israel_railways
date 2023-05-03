# israel_railways_api.py
import aiohttp
import asyncio
import datetime

class IsraelRailwaysAPI:
    def __init__(self, station_a, station_b):
        self.station_a = station_a
        self.station_b = station_b
        self.base_url = "https://israelrail.azurefd.net/rjpa-prod/api/v1/timetable/searchTrainLuzForDateTime"
    
    async def get_next_train(self):
        date_now = datetime.datetime.now()
        date_str = date_now.strftime('%Y-%m-%d')
        hour_str = date_now.strftime('%H:%M')
        headers = {'Ocp-Apim-Subscription-Key': '4b0d355121fe4e0bb3d86e902efe9f20'}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url,
                headers=headers,
                params={
                    "fromStation": self.station_a,
                    "toStation": self.station_b,
                    "date": date_str,
                    "hour": hour_str,
                    "scheduleType": 1,
                    "systemType": 2,
                    "languageId": "English",
                },
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
        url = "https://israelrail.azurefd.net/common/api/v1/stations?languageId=Hebrew&systemType=2"
        headers = {'Ocp-Apim-Subscription-Key': '4b0d355121fe4e0bb3d86e902efe9f20'}
        
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
