from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_registry import async_entries_for_config_entry
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCHEMA = vol.Schema({
    vol.Required("Magnitude Threshold", default=4): cv.positive_int,
    vol.Required("Polling Interval (Minutes)", default=5): cv.positive_int,
})

@config_entries.HANDLERS.register(DOMAIN)
class JmaEarthquakeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """JMA Earthquake config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 0

    async def async_step_user(self, info):
        if info is not None:
            pass  # TODO: process info
        schema = SCHEMA
        return self.async_show_form(step_id='user', data_schema=schema)
