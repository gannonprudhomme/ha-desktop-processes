""" The Desktop Processes integration. """
import logging
import asyncio
from datetime import timedelta
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.helpers.entity_component import EntityComponent
import socketio
from .desktop import Desktop, Process

from .const import DOMAIN, IGNORE, PRIORITY, ATTR_CONFIG

_LOGGER = logging.getLogger(__name__)

SCANNING_INTERVAL = 5

desktops = []


@callback
async def _set_process_volume(call: ServiceCall):
    """ Handle the call """
    pid = call.data.get("pid")
    volume = call.data.get("volume")

    if pid is None or volume is None:
        raise Exception("pid is none!")
        return

    # We're assuming there's only 1 desktop at the moment
    desktop = desktops[0]
    await desktop.set_volume(pid, volume)

@asyncio.coroutine
async def async_setup(hass: HomeAssistant, config: dict):
    """ Set up the Desktop Processes component. """
    # Setup data so we can pass the config data to async_setup_entry
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][ATTR_CONFIG] = config.get(DOMAIN)

    hass.services.async_register(DOMAIN, "set_process_volume", _set_process_volume)

    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """ Setup from config entry """
    config_data = hass.data[DOMAIN].get(ATTR_CONFIG)

    ignore_list = []
    if config_data and IGNORE in config_data:
        # Setup priorities and ignore_list
        ignore_list = config_data.get(IGNORE)

    priorities = dict()
    if config_data and PRIORITY in config_data:
        priority_settings = config_data.get(PRIORITY)
        priorities = {
            setting["name"]: setting.get("priority") for setting in priority_settings
        }

    scan_interval = SCANNING_INTERVAL

    if config_data and CONF_SCAN_INTERVAL in config_data:
        scan_interval = config_data.get(CONF_SCAN_INTERVAL) or SCANNING_INTERVAL

    url = entry.data.get("url")

    desktop = Desktop(url, priorities, ignore_list)
    await desktop.connect()

    desktops.append(desktop)

    component = EntityComponent(
        None, DOMAIN, hass, timedelta(seconds=scan_interval)
    )

    # Store the component so we can remove the Entity in async_unload_entry
    hass.data[DOMAIN]["component"] = component

    await component.async_add_entities([desktop])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Handle removal of entry """
    # Get the according component so we can get the entities it contains
    component = hass.data[DOMAIN]["component"]

    # Must convert it to a list, otherwise we'll get a "dict size changed during iteration"
    entities = list(component.entities)

    # There will only be one, but iterate anyways
    for entity in entities:
        await component.async_remove_entity(entity.entity_id)

    return True
