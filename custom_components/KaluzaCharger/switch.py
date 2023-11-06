import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Kaluza switches from a config entry."""
    kaluza_api = hass.data[DOMAIN]['api']
    coordinator = hass.data[DOMAIN]['coordinator']

    # Assuming you have some method to determine if Solar Match and Boost can be controlled
    # This could be based on features exposed by the devices or user preferences
    # For this example, we'll create two switches for each feature

    async_add_entities([
        KaluzaSwitch(kaluza_api, coordinator, entry, "Solar Match", "solar_match"),
        KaluzaSwitch(kaluza_api, coordinator, entry, "Boost", "boost")
    ])

class KaluzaSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Kaluza switch."""

    def __init__(self, api, coordinator, entry, name, switch_type):
        """Initialize the switch."""
        super().__init__(coordinator)
        self.api = api
        self.entry = entry
        self._name = name
        self._switch_type = switch_type
        self._is_on = False

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{self.entry.title} {self._name}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self.entry.entry_id}_{self._switch_type}"

    @property
    def is_on(self):
        """Return the status of the switch."""
        # Here we need to return the current state of the switch
        # You should replace this with the actual state checking
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        # Implement the actual logic to turn on the feature
        # This should call your API and update the switch's state
        if self._switch_type == "solar_match":
            await self.api.enable_solar_match()  # Replace with actual API call
        elif self._switch_type == "boost":
            await self.api.enable_boost()  # Replace with actual API call
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        # Implement the actual logic to turn off the feature
        # This should call your API and update the switch's state
        if self._switch_type == "solar_match":
            await self.api.disable_solar_match()  # Replace with actual API call
        elif self._switch_type == "boost":
            await self.api.disable_boost()  # Replace with actual API call
        self._is_on = False
        self.async_write_ha_state()

    async def async_update(self):
        """Fetch new state data for this switch."""
        # This method should fetch the current state of the switch
        # For this example, we're toggling the state, but in reality,
        # you would query your API for the current state
        self._is_on = not self._is_on
