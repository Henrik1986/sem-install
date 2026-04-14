from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"


class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for SEM Installer."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Start step with install button."""

        if user_input is not None:

            # Kör installationen
            await self.hass.services.async_call(
                DOMAIN,
                "install"
            )

            # Skapa config entry (markera som installerad)
            return self.async_create_entry(
                title="SEM Installer",
                data={"installed": True}
            )

        # Enkel form (ingen title/description här!)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
