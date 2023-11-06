import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client

from .api import KaluzaAPI  # Make sure to implement this module based on your API interaction

DOMAIN = 'kaluza'

class KaluzaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        # Check if already configured
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            # Validate user input
            email = user_input.get('email')
            password = user_input.get('password')
            session = aiohttp_client.async_get_clientsession(self.hass)
            kaluza_api = KaluzaAPI(email, password, session)

            try:
                # Try to obtain a token from the Kaluza API
                token = await kaluza_api.async_get_access_token()
                if token:
                    return self.async_create_entry(title=email, data=user_input)
                else:
                    errors['base'] = 'auth'
            except Exception as e:
                # Handle exceptions from the KaluzaAPI class
                errors['base'] = 'exception'

        # Display the input form to the user
        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required('email'): str,
                vol.Required('password'): str,
            }),
            errors=errors
        )
