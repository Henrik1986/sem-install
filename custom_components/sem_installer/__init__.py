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
    """Installer runs once per config entry."""

    # ✔ kör bara en gång
    if entry.data.get("installed"):
        _LOGGER.info("SEM Installer: already installed – skipping")
        return True

    base = hass.config.path()

    tmp_zip = os.path.join(base, "sem_tmp.zip")
    tmp_dir = os.path.join(base, "sem_tmp")

    # 🧪 TESTLÄGE (ingen HA-inläsning)
    target_root = hass.config.path("_sem_installer_test")
    target = os.path.join(target_root, "sem")

    try:
        _LOGGER.info("SEM Installer: starting installation (TEST MODE)")

        # 1. skapa testmapp
        os.makedirs(target_root, exist_ok=True)

        # 2. ladda ner zip
        async with aiohttp.ClientSession() as session:
            async with session.get(ZIP_URL) as resp:
                if resp.status != 200:
                    raise Exception(f"Download failed: HTTP {resp.status}")

                data = await resp.read()
                with open(tmp_zip, "wb") as f:
                    f.write(data)

        # 3. packa upp
        shutil.rmtree(tmp_dir, ignore_errors=True)

        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmp_dir)

        source = os.path.join(tmp_dir, "huawei-energy-managment-main/sem")

        if not os.path.exists(source):
            raise Exception("SEM folder not found in repository zip")

        # 4. rensa tidigare test
        shutil.rmtree(target_root, ignore_errors=True)
        os.makedirs(target_root, exist_ok=True)

        # 5. kopiera endast sem
        shutil.copytree(source, target)

        # 6. städa temporära filer
        os.remove(tmp_zip)
        shutil.rmtree(tmp_dir, ignore_errors=True)

        # 7. markera installerad
        hass.config_entries.async_update_entry(
            entry,
            data={**entry.data, "installed": True},
        )

        _LOGGER.info("SEM Installer: installation complete (TEST MODE)")

    except Exception:
        _LOGGER.exception("SEM Installer failed")
        raise

    return True
