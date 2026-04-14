from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"


class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

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
            description=(
                "Denna integration används för att ladda ner filerna för energisystemet första gången.\n\n"
                "Efter installation följer du instruktionerna via GitHub.\n"
                "När systemet är igång kan du ta bort denna integration.\n\n"
                "Systemet uppdateras därefter via energisystemet Hemvy."
            ),
            data_schema=vol.Schema({})
        )
