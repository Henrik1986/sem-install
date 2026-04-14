import os
import shutil
import zipfile
import aiohttp
import logging

from homeassistant.core import HomeAssistant

DOMAIN = "sem_installer"
ZIP_URL = "https://github.com/Henrik1986/huawei-energy-managment/archive/refs/heads/main.zip"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry):
    """Installer runs once per entry."""

    # ✔ SKYDD: kör bara en gång
    if entry.data.get("installed"):
        _LOGGER.info("SEM already installed – skipping")
        return True

    base = hass.config.path()

    tmp_zip = os.path.join(base, "sem_tmp.zip")
    tmp_dir = os.path.join(base, "sem_tmp")

    target = os.path.join(base, "packages/sem")

    try:
        _LOGGER.info("SEM Installer: downloading package")

        async with aiohttp.ClientSession() as session:
            async with session.get(ZIP_URL) as resp:
                data = await resp.read()
                with open(tmp_zip, "wb") as f:
                    f.write(data)

        shutil.rmtree(tmp_dir, ignore_errors=True)

        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmp_dir)

        source = os.path.join(tmp_dir, "huawei-energy-managment-main/sem")

        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(source, target)

        os.remove(tmp_zip)
        shutil.rmtree(tmp_dir, ignore_errors=True)

        # ✔ markera som installerad
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, "installed": True},
        )

        _LOGGER.info("SEM Installer: installation complete")

    except Exception as e:
        _LOGGER.error("SEM Installer failed: %s", e)
        raise

    return True
