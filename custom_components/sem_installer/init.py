import os
import shutil
import zipfile
import aiohttp

from homeassistant.core import HomeAssistant

DOMAIN = "sem_installer"

ZIP_URL = "https://github.com/Henrik1986/huawei-energy-managment/archive/refs/heads/main.zip"


async def async_setup_entry(hass: HomeAssistant, entry):
    """Körs när integrationen läggs till via UI."""

    async def install(call):

        base = hass.config.path()

        tmp_zip = os.path.join(base, "sem_tmp.zip")
        tmp_dir = os.path.join(base, "sem_tmp")

        target = os.path.join(base, "_sem_installer_test")

        # 1. ladda ner zip
        async with aiohttp.ClientSession() as session:
            async with session.get(ZIP_URL) as resp:
                data = await resp.read()
                with open(tmp_zip, "wb") as f:
                    f.write(data)

        # 2. packa upp
        shutil.rmtree(tmp_dir, ignore_errors=True)
        with zipfile.ZipFile(tmp_zip, "r") as z:
            z.extractall(tmp_dir)

        # 3. kopiera sem-mappen
        source = os.path.join(tmp_dir, "huawei-energy-managment-main/sem")

        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(source, target)

        # 4. städa
        os.remove(tmp_zip)
        shutil.rmtree(tmp_dir, ignore_errors=True)

    hass.services.async_register(DOMAIN, "install", install)

    return True
