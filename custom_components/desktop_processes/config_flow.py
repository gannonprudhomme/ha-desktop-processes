"""Config flow for Desktop Processes integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

import socketio
from .const import DOMAIN
from .desktop import Desktop

_LOGGER = logging.getLogger(__name__)

class PlaceholderHub:
    """Placeholder class to make tests pass.

    TODO Remove this placeholder class and replace with things from your PyPI package.
    """

    def __init__(self, host):
        """Initialize."""
        self.host = host

    async def authenticate(self, username, password) -> bool:
        """Test if we can authenticate with the host."""
        return True


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Desktop Processes."""

    VERSION = 1
    # TODO pick one of the available connection classes in homeassistant/config_entries.py
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        data_schema = vol.Schema({
            vol.Required("url", default="http://localhost:3001/"): str
        })

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=data_schema
            )

        # Verify that we can connect to this URL? Or nah?
        if "url" not in user_input:
            # raise some error?
            pass

        url = user_input.get("url")

        sio = socketio.AsyncClient()

        try:
            await sio.connect(url)
            await sio.disconnect()
            return self.async_create_entry(title=f"DP: {url}", data={"url": url})
        except socketio.exceptions.ConnectionError as err:
            print(err)
            errors = { "base": "auth_error" }
            return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
        except Exception as e:
            print(e)

# Really the only error we need
class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
