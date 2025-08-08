import logging
import voluptuous as vol

from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_registry import async_entries_for_config_entry
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONF_MAGNITUDE = "magnitude_threshold"
CONF_INTERVAL = "polling_interval"

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_MAGNITUDE, default=4): cv.positive_int,
    vol.Required(CONF_INTERVAL, default=5): cv.positive_int,
})

class JmaEarthquakeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for JMA Earthquake integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # 入力を保存して完了
            return self.async_create_entry(
                title="JMA Earthquake",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
