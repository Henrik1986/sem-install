from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "sem_installer"


class SemInstallerFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):

        if user_input is not None:
            try:
                await self.hass.services.async_call(
                    DOMAIN,
                    "install"
                )
            except Exception as e:
                raise Exception(f"Install failed: {e}")

            return self.async_create_entry(
                title="SEM Installer",
                data={"installed": True}
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({})
        )
