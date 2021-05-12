"""
Example configuration.yaml entry:

notify:
  - name: line_bot
    platform: line_bot
    client_id: 'YOUR_CLIENT_ID'
    access_token: 'YOUR_ACCESS_TOKEN'

"""

import json
import logging
import requests
import voluptuous as vol

from aiohttp.hdrs import AUTHORIZATION
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME, CONF_ACCESS_TOKEN, CONF_CLIENT_ID
from homeassistant.components.notify import (
    ATTR_DATA, PLATFORM_SCHEMA, BaseNotificationService)

from .const import DOMAIN, LINE_BOT, BASE_URL_PUSH, BASE_URL_MULTICAST, BASE_URL_BROADCAST

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
    vol.Required(CONF_CLIENT_ID): cv.string,
    vol.Required(CONF_NAME): cv.string,
})

def get_service(hass, config, discovery_info=None):
    """Get the LINE Bot notification service."""
    # pylint: disable=unused-argument
    line_bot = {}
    if (config.get(CONF_NAME) and
        config.get(CONF_CLIENT_ID) and
        config.get(CONF_ACCESS_TOKEN)):
        line_bot[CONF_NAME] = config[CONF_NAME]
        line_bot[CONF_CLIENT_ID] = config[CONF_CLIENT_ID]
        line_bot[CONF_ACCESS_TOKEN] = config[CONF_ACCESS_TOKEN]

    return LineNotificationService(line_bot, hass)


class LineNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, line_bot, hass):
        """Initialize the service."""
        self._hass = hass
        self._line_bot = line_bot

    def send_message(self, message, **kwargs):
        """Send some message."""
        name = None
        if kwargs.get("data"):
            name = kwargs["data"].get("profile", self._line_bot[CONF_NAME])
        client_id = self._line_bot[CONF_CLIENT_ID]
        access_token = self._line_bot[CONF_ACCESS_TOKEN]

        if DOMAIN in self._hass.data and LINE_BOT in self._hass.data[DOMAIN]:
            for i in self._hass.data[DOMAIN][LINE_BOT]:
                if i[CONF_NAME] == name:
                    client_id = i[CONF_CLIENT_ID]
                    access_token = i[CONF_ACCESS_TOKEN]
                    break
        if client_id is None or access_token is None:
            _LOGGER.error("Missing client_id or access_token to send message")
            return

        headers = {AUTHORIZATION: "Bearer " + access_token,
                   'Content-type': 'application/json'}
        try:
            payload = json.loads(message.encode('utf-8'))
        except ValueError:
            _LOGGER.warning("The message is not for json format!")
            payload = {"messages" : [{"type": "text", "text": message}]}
        if "messages" not in payload:
            data = {}
            data["messages"] = [payload]
            payload = data
        to = client_id
        url = BASE_URL_PUSH
        if kwargs.get("data"):
            data = kwargs["data"].get('to')
            if data:
                url = BASE_URL_MULTICAST
                to = []
                for i in data.split(','):
                    to.append(i)
        payload['to'] = to
        payload = json.dumps(payload)

        ret = requests.Session().post(url, headers=headers, data=payload)
        if ret.status_code != 200:
            _LOGGER.error(ret.text)
