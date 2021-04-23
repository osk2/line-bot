"""Config flow to configure Line-Bot component."""
from collections import OrderedDict
from typing import Optional
import voluptuous as vol

from homeassistant.config_entries import (
    CONN_CLASS_LOCAL_PUSH,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
    )
from homeassistant.const import CONF_NAME, CONF_CLIENT_ID, CONF_ACCESS_TOKEN
from homeassistant.core import callback
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, DEFAULT_NAME


class LineBotFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Line-Bot config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize flow."""
        self._client_id: Optional[str] = None
        self._token: Optional[str] = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self,
        user_input: Optional[ConfigType] = None,
        error: Optional[str] = None
    ):  # pylint: disable=arguments-differ
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self._set_user_input(user_input)
            self._name = user_input.get(CONF_NAME)
            self._abort_if_unique_id_configured(
                updates={CONF_NAME: self._name}
            )
            await self.async_set_unique_id(self._name)
            return self._async_get_entry()

        fields = OrderedDict()
        fields[vol.Optional(CONF_NAME,
                            default=self._name or DEFAULT_NAME)] = str
        fields[vol.Required(CONF_CLIENT_ID,
                            default=self._client_id or vol.UNDEFINED)] = str
        fields[vol.Required(CONF_ACCESS_TOKEN,
                            default=self._token or vol.UNDEFINED)] = str
        if self._name is None:
            self._name = DEFAULT_NAME
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(fields),
            errors={'base': error} if error else None
        )

    @property
    def _name(self):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        return self.context.get(CONF_NAME)

    @_name.setter
    def _name(self, value):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        self.context[CONF_NAME] = value
        self.context["title_placeholders"] = {"name": self._name}

    def _set_user_input(self, user_input):
        if user_input is None:
            return
        self._name = user_input.get(CONF_NAME, "")
        self._client_id = user_input.get(CONF_CLIENT_ID, "")
        self._token = user_input.get(CONF_ACCESS_TOKEN, "")

    @callback
    def _async_get_entry(self):
        return self.async_create_entry(
            title=self._name,
            data={
                CONF_NAME: self._name,
                CONF_CLIENT_ID: self._client_id,
                CONF_ACCESS_TOKEN: self._token,
            },
        )


class OptionsFlowHandler(OptionsFlow):
    # pylint: disable=too-few-public-methods
    """Handle options flow changes."""
    _name = None
    _client_id = None
    _token = None

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            self._name = user_input.get(CONF_NAME)
            self._client_id = user_input.get(CONF_CLIENT_ID)
            self._token = user_input.get(CONF_ACCESS_TOKEN)
            return self.async_create_entry(
                title='',
                data={
                    CONF_NAME: self._name,
                    CONF_CLIENT_ID: self._client_id,
                    CONF_ACCESS_TOKEN: self._token,
                },
            )
        self._name = self.config_entry.options.get(CONF_NAME, '')
        self._token = self.config_entry.options.get(CONF_ACCESS_TOKEN, '')
        self._client_id = self.config_entry.options.get(CONF_CLIENT_ID, '')

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=self._name): str,
                    vol.Required(CONF_CLIENT_ID, default=self._client_id): str,
                    vol.Required(CONF_ACCESS_TOKEN, default=self._token): str
                }
            ),
        )