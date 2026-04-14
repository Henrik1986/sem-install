from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

DOMAIN = "sem_installer"

class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            return self.async_create_entry(title="SEM Installer", data={})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "text": "Klicka install för att köra installation"
            }
        )

    @callback
    def async_get_options_flow(self, entry):
        return SemOptionsFlow(entry)


class SemOptionsFlow(config_entries.OptionsFlow):

    def __init__(self, entry):
        self.entry = entry

    async def async_step_init(self, user_input=None):

        if user_input is not None:
            # kör din install-service
            await self.hass.services.async_call(
                "sem_installer",
                "install",
            )
            return self.async_create_entry(title="", data={})

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
            description_placeholders={
                "text": "Klicka för att installera"
            }
        )
