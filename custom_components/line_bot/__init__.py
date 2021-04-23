"""The Line Bot component."""
import asyncio

import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_NAME, CONF_CLIENT_ID, CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DOMAINS, LINE_BOT


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
    """ Update Optioins if available """
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Handle removal of an entry."""

    for i in hass.data[DOMAIN][LINE_BOT]:
        if i[CONF_NAME] == entry.options[CONF_NAME]:
            hass.data[DOMAIN][LINE_BOT].remove(i)


async def async_setup(hass: HomeAssistant, hass_config: dict):
    """Set up the Line Bot component."""
    # pylint: disable=unused-argument
    hass.data.setdefault(DOMAIN, {})
    config = hass_config.get(DOMAIN, {})
    if not config:
        return True

    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_IMPORT},
            data=config,
        )
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Configure LINE Bot."""

    # migrate data (also after first setup) to options
    if entry.data:
        hass.config_entries.async_update_entry(entry, data={},
                                               options=entry.data)

    config = {CONF_NAME: entry.options[CONF_NAME],
              CONF_CLIENT_ID: entry.options[CONF_CLIENT_ID],
              CONF_ACCESS_TOKEN: entry.options[CONF_ACCESS_TOKEN]}

    if LINE_BOT not in hass.data[DOMAIN]:
        hass.data[DOMAIN][LINE_BOT] = []
    hass.data[DOMAIN][LINE_BOT].append(config)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
     # pylint: disable=unused-argument
    return True
