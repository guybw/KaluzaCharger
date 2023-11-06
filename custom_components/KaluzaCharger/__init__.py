from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from .api import KaluzaAPI  # Your custom API class
from .const import DOMAIN  # Define your domain as a string constant in a const.py file

async def async_setup(hass: HomeAssistantType, config: dict):
    """Set up the Kaluza component."""
    # This method must return True if the setup was successful.
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Kaluza from a config entry."""
    # Initialize your API or connection to the device
    kaluza_api = KaluzaAPI(
        entry.data["email"],  # Assume the email is part of the entry data
        entry.data["password"],  # Assume the password is part of the entry data
        hass
    )

    # Create a new instance of your API client
    hass.data[DOMAIN] = {
        "api": kaluza_api
    }

    # Set up the sensor platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # If you have other platforms like switch, light, etc., set them up here:
    # hass.async_create_task(
    #     hass.config_entries.async_forward_entry_setup(entry, "switch")
    # )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    # If you have other platforms, unload them here as well

    # Remove the API instance from hass.data if all platforms were successfully unloaded
    if unload_ok:
        hass.data.pop(DOMAIN)

    return unload_ok
