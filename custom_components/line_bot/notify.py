"""
Example configuration.yaml entry:

notify:
  - name: line_bot
    platform: line_bot
    client_id: 'YOUR_CLIENT_ID'
    access_token: 'YOUR_ACCESS_TOKEN'    

"""

import json
import requests
import logging
import voluptuous as vol

from aiohttp.hdrs import AUTHORIZATION
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_ACCESS_TOKEN, CONF_CLIENT_ID)
from homeassistant.components.notify import (
    ATTR_DATA, PLATFORM_SCHEMA, BaseNotificationService)

_LOGGER = logging.getLogger(__name__)

BASE_URL = 'https://api.line.me/v2/bot/message/push'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
    vol.Required(CONF_CLIENT_ID): cv.string,
})


def get_service(hass, config, discovery_info=None):
    """Get the Line notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    client_id = config.get(CONF_CLIENT_ID)
    return LineNotificationService(access_token, client_id)


class LineNotificationService(BaseNotificationService):
    """Implementation of a notification service for the Line Messaging service."""

    def __init__(self, access_token, client_id):
        """Initialize the service."""
        self.access_token = access_token
        self.client_id = client_id

    def send_message(self, message, **kwargs):
        """Send some message."""
        data = kwargs.get(ATTR_DATA, None)
        headers = {AUTHORIZATION: "Bearer " + self.access_token,
                   'Content-type': 'application/json'}

        payload = json.loads(message.encode('utf-8'))
        payload['to'] = self.client_id
        payload = json.dumps(payload)

        r = requests.Session().post(BASE_URL, headers=headers, data=payload)
        if r.status_code != 200:
            _LOGGER.error(r.text)
