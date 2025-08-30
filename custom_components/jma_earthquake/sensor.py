from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import logging

import requests
import xml.etree.ElementTree as ET
import datetime
import re

from datetime import timedelta

_LOGGER = logging.getLogger(__name__)

# XML feed URL
FEED_URL = 'https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml'

ATOM = '{http://www.w3.org/2005/Atom}'
SEISMOLOGY1 = '{http://xml.kishou.go.jp/jmaxml1/body/seismology1/}'
ELEMENTBASIS1 = '{http://xml.kishou.go.jp/jmaxml1/elementBasis1/}'
EARTHQUAKETITLE = '震源・震度に関する情報'
MAGNITUDE_THRESHOLD = 3.0

SCAN_INTERVAL = timedelta(seconds=300)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
#    config = hass.data[DOMAIN][config_entry.entry_id]
#    session = async_get_clientsession(hass)
    """Set up the sensor platform."""
    add_entities([JmaEarthquake(hass,config)],True)

async def setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    add_entities([JmaEarthquake(hass,config)],update_before_add=True)
    
def fetch_latest_jma_report():
    res = requests.get(FEED_URL)
    res.raise_for_status()
    rt = ET.fromstring(res.content)
    for entry in rt:
        if( entry.tag == f'{ATOM}entry' ):
            title = entry.find(f'{ATOM}title').text
            if( title == EARTHQUAKETITLE ):
                link = entry.find(f'{ATOM}id').text
                eq = requests.get(link)
                eq.raise_for_status()
                ert = ET.fromstring(eq.content)

                body = ert.find(f'{SEISMOLOGY1}Body')
                quake = body.find(f'{SEISMOLOGY1}Earthquake')
                magstr = quake.find(f'{ELEMENTBASIS1}Magnitude').text
                magnitude = float(magstr)

                if( magnitude >= MAGNITUDE_THRESHOLD ):
                    time = quake.find(f'{SEISMOLOGY1}OriginTime').text
                    dt = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')
                    th = dt.strftime( '%H' )
                    tm = dt.strftime( '%M' )

                    hypo = quake.find(f'{SEISMOLOGY1}Hypocenter')
                    area = hypo.find(f'{SEISMOLOGY1}Area')
                    areastr = area.find(f'{SEISMOLOGY1}Name').text
                    hypocenter = area.find(f'{ELEMENTBASIS1}Coordinate').text
                    # hypocenter is a text looking like '+29.3+129.4+0/' or '+29.3+129.4-20000/'
                    hcl = re.findall(r'([+-]\d{2,8}.\d{1,2})', hypocenter)
                    latitude = float(hcl[0])
                    longitude = float(hcl[1])
                    if len(hcl) > 2:
                        depthstr = hcl[2]
                        depth = abs(int(int(depthstr)/1000)) # convgert to kilo-meter
                    else:
                        depth = None

                    if depth == 0:
                        output = f'{th}時{tm}分頃、{areastr}のごく浅いところでマグニチュード{magstr}の地震がありました'
                    elif depth == None:
                        output = f'{th}時{tm}分頃、{areastr}でマグニチュード{magstr}の地震がありました。深さは不明です'
                    else:
                        output = f'{th}時{tm}分頃、{areastr}の深さ{depth}キロでマグニチュード{magstr}の地震がありました'
                    results = {
                        'text': output,
                        'latitude': latitude,
                        'longitude': longitude,
                        'depth': depth,
                        'magnitude': magnitude,
                        'magstr': magstr,
                        'area': areastr,
                        'time': dt }

                    return results
    return None

class JmaEarthquake(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = 'Latest Earthquake' # name of entity
    _attr_has_entity_name = True

    def __init__(self, hass, config):
        """Initialize the sensor."""
        self._hass = hass
        self._hass.custom_attributes = {}
        
    def update(self) -> None:
        results = fetch_latest_jma_report()
        if results != None:
            self._attr_native_value = results.pop('text')
            self._attr_available = True
            self._hass.custom_attributes = results

    @property
    def extra_state_attributes(self):
        return self._hass.custom_attributes
         
class JmaCoordinator(DataUpdateCoordinator):
    """JMA Earthquake coordinator."""

    def __init__(self, hass, config_entry, my_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name='JMA Earthquake',
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=300),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.my_api = my_api
        self._device: MyDevice | None = None

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        self._device = await self.my_api.get_device()


    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # Grab active context variables to limit data required to be fetched from API
        # Note: using context is not required if there is no need or ability to limit
        # data retrieved from API.
        listening_idx = set(self.async_contexts())
        return await self.my_api.fetch_data(listening_idx)


class JmaEntity(CoordinatorEntity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
      should_poll
      async_update
      async_added_to_hass
      available
    """

    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
