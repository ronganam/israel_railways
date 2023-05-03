import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from datetime import timedelta,datetime
from .israel_railways_api import IsraelRailwaysAPI

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    station_a = config_entry.data.get("station_a")
    station_b = config_entry.data.get("station_b")
    api_to = IsraelRailwaysAPI(station_a, station_b)
    api_from = IsraelRailwaysAPI(station_b, station_a)
    async_add_entities([IsraelRailwaysSensor(api_to, station_a, station_b)], True)
    async_add_entities([IsraelRailwaysSensor(api_from, station_b, station_a)], True)

class IsraelRailwaysSensor(Entity):
    def __init__(self, api, station_a, station_b):
        self.api = api
        self.station_a = station_a
        self.station_b = station_b
        self._entity_id = f"train_{self.station_a}_{self.station_b}"
        self._state = None
        self.station_a_name = None
        self.station_b_name = None
        self._attributes = {}

    @property
    def name(self):
        return f"Israel Railways Next Train from {self.station_a} to {self.station_b}"

    @property
    def unique_id(self):
        return self._entity_id

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the entity."""
        return self._attributes

    @property
    def extra_state_attributes(self):
        """Return other details about the sensor state."""
        return self._attributes

    async def async_update(self, now=None):
        try:
            next_train = await self.api.get_next_train()
            _LOGGER.debug("next_train: %s", next_train)
            if next_train:
                self._state = datetime.fromisoformat(next_train['departureTime']).strftime("%H:%M")
                attrs = {}
                attrs["trainNumber"] = next_train['trainNumber']
                attrs["originName"] = self.station_a_name
                attrs["destName"] = self.station_b_name
                attrs["departureTime"] = datetime.fromisoformat(next_train['departureTime']).strftime("%H:%M")
                attrs["arrivalTime"] = datetime.fromisoformat(next_train['arrivalTime']).strftime("%H:%M")
                attrs["remainTime"] = (datetime(1, 1, 1) + (datetime.fromisoformat(next_train['departureTime']) - datetime.now())).strftime("%H:%M")
                attrs["originPlatform"] = next_train['originPlatform']
                attrs["destPlatform"] = next_train['destPlatform']
                attrs["crowded"] = next_train['crowded']
                if "trainPosition" in next_train and next_train["trainPosition"] != None:
                    if "calcDiffMinutes" in next_train["trainPosition"]:
                        attrs["calcDiffMinutes"] = next_train['trainPosition']['calcDiffMinutes']
                else:
                    attrs["calcDiffMinutes"] = None
                self._attributes = attrs
                self.async_schedule_update_ha_state(True)
        except Exception as e:
            _LOGGER.error("Error updating IsraelRailwaysSensor: %s", e)

    async def async_added_to_hass(self):
        # First update station names before setting up the interval
        self.station_a_name, self.station_b_name = await self.api.get_station_name()
        
        await self.async_update()  # First update before setting up the interval
        async_track_time_interval(
            self.hass,
            self.async_update,
            timedelta(minutes=1)  # Update every minute.
        )
