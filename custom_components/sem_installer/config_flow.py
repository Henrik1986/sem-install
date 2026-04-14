from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"


class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow för SEM installer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Första steget i installationen."""

        # När användaren klickar "Install"
        if user_input is not None:

            # Kör din install-service
            await self.hass.services.async_call(
                "sem_installer",
                "install"
            )

            # Skapa integration (utan data)
            return self.async_create_entry(
                title="SEM Installer",
                data={}
            )

        # UI som visas innan installation
        return self.async_show_form(
            step_id="user",
            title="SEM Installer",
            description=(
                "Denna integration används för att ladda ner filerna för energisystemet första gången.\n\n"
                "Efter installation följer du instruktionerna via GitHub.\n"
                "När systemet är igång kan du ta bort denna integration.\n\n"
                "Systemet uppdateras därefter via energisystemet Hemvy."
            ),
            data_schema=vol.Schema({})
        )
