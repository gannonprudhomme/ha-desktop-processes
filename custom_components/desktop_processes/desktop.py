import os
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
import socketio
from socketio.exceptions import ConnectionError

from .const import DOMAIN

ICON_PATH = "../../www/icons/"

_LOGGER = logging.getLogger(__name__)

@dataclass
class Process:
    """ Data describing a process """

    name: str
    volume: int
    icon: str


class Desktop(Entity):
    """Representation of a Desktop entity, which allows you access to a variety of
    resources on the Desktop
    """

    def __init__(self, url: str, priorities: Dict[str, int], ignore_list: List[str]):
        """ Initialize the Desktop """

        self.sio = socketio.AsyncClient()
        self._state = "disconnected"
        self.url = url
        self.processes = []
        self.priorities = priorities
        self.ignore_list = ignore_list

        # self.socket.send()

    async def connect(self):
        @self.sio.event
        async def connect():
            _LOGGER.info(f"Connected to {self.url}")

        @self.sio.event
        async def disconnect():
            _LOGGER.info(f"Disconnected from {self.url}")

        _LOGGER.info(f"Attempting to connect to {self.url}")
        try:
            await self.sio.connect(self.url)
            _LOGGER.info("Connected to server at URL %s", self.url)
        except ConnectionError as err:
            _LOGGER.error("Cannot connect to server at URL %s", self.url)

    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, self.unique_id),
            },
            "name": "Some desktop name",  # self.name
        }

    @property
    def name(self):
        """ Return the name of the Desktop. """
        # Where do we get this from?
        return "Desktop-1"

    @property
    def state(self):
        """ Return the state of the Desktop. """
        return str(self._state)

    @property
    def state_attributes(self):
        """Return the state attributes"""
        result = {
            "processes": self.processes,
        }
        return result

    @property
    def unique_id(self):
        return f"desktop_process-{self.url}"

    async def async_update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """

        def get_volume_icon(name: str):
            """Wrapper function that allows us to pass the name to the async function
            that will actually handle the returned data from the socket
            """

            async def write_data_to_file(data):
                """ Actually writes the bytes data to the file """
                dir = os.path.dirname(__file__)
                # TODO: Define this elsewhere (and validate the path?)
                # Also make the folder if it doesn't exist
                path = os.path.join(dir, "..", "..", "www", "icons")
                if not os.path.exists(path):
                    Path(path).mkdir(parents=True, exist_ok=True)

                filename = os.path.join(path, f"{name}.png")

                with open(filename, "wb+") as f:
                    f.write(data)

            return write_data_to_file

        async def get_volumes(data):
            filtered = [proc for proc in data if proc["name"] not in self.ignore_list]
            with_priority = []
            for proc in filtered:
                priority = self.priorities.get(proc["name"], 0)
                proc["priority"] = priority
                with_priority.append(proc)

            self.processes = with_priority

            # Get the volume icon for each process
            for proc in self.processes:
                if not "name" in proc:  # Will this ever work???? Can we use .get()?
                    pass
                name = proc.get("name")
                await self.sio.emit("get_volume_icon", name, None, get_volume_icon(name))

        # Attempt to connect to the server if we aren't already connected
        if not self.sio.connected:
            await self.connect()

            # If it's not connected after this, don't continue
            if not self.sio.connected:
                # Potentially redundant, see disconnect handler
                self.processes = []
                self._state = "disconnected"
                return

        try:
            await self.sio.emit("get_volumes", "something", None, get_volumes)
            self._state = "connected"
        # This won't happen anymore b/c of the connected check, but leaving it here anyways
        except socketio.exceptions.BadNamespaceError as err:
            _LOGGER.error("Desktop Processes server is not active at URL %s", self.url)

            self.processes = []
            self._state = "disconnected"

    async def set_volume(self, pid: int, volume: int):
        if not self.sio.connected:
            print("Not connected!")
        # TODO: Probably need to validate pid and volume

        await self.sio.emit("set_volume_proc", {"pid": pid, "volume": volume})
