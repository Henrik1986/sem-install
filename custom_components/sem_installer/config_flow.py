from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"


class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):

        # DETTA körs när användaren klickar "Submit"
        if user_input is not None:

            await self.hass.services.async_call(
                DOMAIN,
                "install"
            )

            return self.async_create_entry(
                title="SEM Installer",
                data={"installed": True}
            )

        # Detta är bara UI
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
