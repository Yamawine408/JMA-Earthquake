from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class JmaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """JMA config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 0

    async def async_step_user(self, user_input: dict | None = None) -> FlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            # Validate the input using the schema
            try:
                # Replace with your actual schema
                schema = vol.Schema({
                    vol.Required("Magnitude Threshold"): vol.Coerce(int),
                    vol.Required("Polling Interval (Minutes)"): vol.Coerce(int)
                })
                user_input = schema(user_input)

                # If validation passes, proceed with the flow
                # For example, create a config entry
                return self.async_create_entry(title="JMA Earthquake", data=user_input)
            except vol.Invalid as error:
                # Handle validation errors
                errors["base"] = str(error)

        # If there are errors or it's the initial step, show the form
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
        
