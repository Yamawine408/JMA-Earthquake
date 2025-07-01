
DOMAIN = "jma"

async def async_setup(hass, config):
    hass.states.async_set("jma.earthquake", None)
    return True
