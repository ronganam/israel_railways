from homeassistant import config_entries
import voluptuous as vol

DOMAIN = "israel_railways"

class IsraelRailwaysConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="Israel Railways", data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("station_a", default="9000"): str,
                    vol.Required("station_b", default="3700"): str,
                }
            ),
            errors=errors,
        )
