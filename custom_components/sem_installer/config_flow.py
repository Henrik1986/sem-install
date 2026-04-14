from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"

class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            # kör install direkt
            await self.hass.services.async_call(
                "sem_installer",
                "install"
            )

            return self.async_create_entry(
                title="SEM Installer",
                data={}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "text": "Klicka Install för att köra installationen"
            }
        )
