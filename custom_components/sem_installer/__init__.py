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

    if entry.data.get("installed"):
        _LOGGER.info("SEM already installed – skipping")
        return True

    base = hass.config.path()

    tmp_zip = os.path.join(base, "sem_tmp.zip")
    tmp_dir = os.path.join(base, "sem_tmp")

    packages_dir = hass.config.path("packages")
    os.makedirs(packages_dir, exist_ok=True)

    target = os.path.join(packages_dir, "sem")

    try:
        _LOGGER.info("SEM Installer: downloading package")

        async with aiohttp.ClientSession() as session:
            async with session.get(ZIP_URL) as resp:
                if resp.status != 200:
                    raise Exception(f"Download failed: {resp.status}")

                data = await resp.read()
                with open(tmp_zip, "wb") as f:
                    f.write(data)

        shutil.rmtree(tmp_dir, ignore_errors=True)

        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmp_dir)

        source = os.path.join(tmp_dir, "huawei-energy-managment-main/sem")

        if not os.path.exists(source):
            raise Exception("Source folder missing in zip")

        if os.path.exists(target):
            shutil.rmtree(target)

        shutil.copytree(source, target)

        os.remove(tmp_zip)
        shutil.rmtree(tmp_dir, ignore_errors=True)

        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, "installed": True},
        )

        _LOGGER.info("SEM Installer: installation complete")

    except Exception:
        _LOGGER.exception("SEM Installer failed")
        raise

    return True
