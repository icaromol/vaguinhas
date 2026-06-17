'''
Author:     Sai Vignesh Golla
LinkedIn:   https://www.linkedin.com/in/saivigneshgolla/

Copyright (C) 2024 Sai Vignesh Golla

License:    GNU Affero General Public License
            https://www.gnu.org/licenses/agpl-3.0.en.html

GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Support me: https://github.com/sponsors/GodsScion

version:    26.01.20.5.08
'''

import sys
import os
from modules.helpers import get_default_temp_profile, make_directories, critical_error_log, print_lg
from config.settings import run_in_background, disable_extensions, file_name, failed_file_name, logs_folder_path, generated_resume_path
from config.questions import default_resume_path

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import SessionNotCreatedException

BROWSER = os.environ.get("VAGUINHAS_BROWSER", "firefox").lower()


def createChromeSession(isRetry: bool = False):
    make_directories([file_name, failed_file_name, logs_folder_path+"/screenshots", default_resume_path, generated_resume_path+"/temp"])

    if BROWSER == "chrome":
        return _open_chrome(isRetry)
    else:
        return _open_firefox(isRetry)


def _open_firefox(isRetry: bool = False):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager

    options = FirefoxOptions()
    if run_in_background:
        options.add_argument("--headless")
    if disable_extensions:
        options.set_preference("extensions.enabled", False)

    options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

    if not isRetry:
        profile_dir = r"C:\Users\icaro\AppData\Roaming\Mozilla\Firefox\Profiles\81fsqb6w.default-release"
        if os.path.exists(profile_dir):
            options.add_argument("-profile")
            options.add_argument(profile_dir)
            print_lg(f"[DEBUG] Perfil Firefox carregado: {profile_dir}")
        else:
            print_lg(f"[DEBUG] PERFIL NAO ENCONTRADO: {profile_dir}")
    else:
        print_lg("[DEBUG] Abrindo Firefox sem perfil (retry)...")

    print_lg("[DEBUG] Iniciando GeckoDriver...")
    service = FirefoxService(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    print_lg(f"[DEBUG] Firefox aberto. URL: {driver.current_url}")
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    return options, driver, actions, wait


def _open_chrome(isRetry: bool = False):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    options = ChromeOptions()
    if run_in_background:
        options.add_argument("--headless=new")
    if disable_extensions:
        options.add_argument("--disable-extensions")

    if not isRetry:
        profile_path = str(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data"))
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--profile-directory=Default")
        print_lg(f"[DEBUG] Perfil Chrome carregado: {profile_path}")
    else:
        print_lg("[DEBUG] Abrindo Chrome sem perfil (retry)...")

    print_lg("[DEBUG] Iniciando ChromeDriver...")
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    print_lg(f"[DEBUG] Chrome aberto. URL: {driver.current_url}")
    driver.maximize_window()
    wait = WebDriverWait(driver, 5)
    actions = ActionChains(driver)
    return options, driver, actions, wait


try:
    options, driver, actions, wait = None, None, None, None
    print_lg(f"[DEBUG] Usando navegador: {BROWSER}")
    options, driver, actions, wait = createChromeSession()
except SessionNotCreatedException as e:
    critical_error_log(f"Falha ao criar sessão {BROWSER}, tentando sem perfil", e)
    options, driver, actions, wait = createChromeSession(True)
except Exception as e:
    if BROWSER == "chrome":
        msg = 'Erro ao abrir Chrome. Verifique se o Chrome está instalado.'
    else:
        msg = 'Erro ao abrir Firefox. Verifique se o Firefox está instalado em C:\\Program Files\\Mozilla Firefox\\'
    print_lg(msg)
    critical_error_log(f"Erro ao abrir {BROWSER}", e)
    import pymsgbox
    pymsgbox.alert(msg, f"Erro ao abrir {BROWSER}")
    try: driver.quit()
    except: exit()
