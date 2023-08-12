from selenium import webdriver
from selenium.webdriver.common.by import By
from requests import get
from urllib.request import urlretrieve
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from requests import get
from selenium_stealth import stealth
from datetime import datetime

from src.users_management.AccountWatchlist import AccountWatchlist
from typing import List


class TelegramScrapper:
	OPTIONS_SCHEME = {
		"last_downloaded": None,  # datetime
		'runned_at': None,
		"replying in channels": [1079145452970188832]
	}

	DEFAULT_FORMAT = 'jpg'

	def __init__(self, url: str, options: dict):
		self.url = url
		self.options = options
		self.weboptions = webdriver.ChromeOptions()
		self.weboptions.add_argument('--disable-blink-features=AutomationControlled')
		self.weboptions.add_argument('--disable-popup-blocking')
		self.weboptions.add_argument('--start-maximized')
		self.weboptions.add_argument('--disable-extensions')
		self.weboptions.add_argument('--no-sandbox')
		self.weboptions.add_argument('--disable-dev-shm-usage')
		self.weboptions.add_argument('--headless')


	def scrape_images(self, account: AccountWatchlist.Account) -> List[str]:
		wbd_profile = webdriver.Chrome(options=self.weboptions)
		stealth(wbd_profile,
				languages=["en-US", "en"],
				vendor="Google Inc.",
				platform="Win32",
				webgl_vendor="Intel Inc.",
				renderer="Intel Iris OpenGL Engine",
				fix_hairline=True,)
		waiter = WebDriverWait(wbd_profile, 10)
		wbd_profile.get(account.account_url)
		sleep(10)
		list_classes_profile = wbd_profile.find_elements(By.CLASS_NAME, 'tgme_widget_message')
		for item in list_classes_profile:
			mis = item.find_element_by_class_name('tgme_widget_message_info')
			metadata = mis.find_element_by_class_name('tgme_widget_message_meta')
			mm = metadata.find_element(By.CSS_SELECTOR,'a').find_element(By.CSS_SELECTOR, 'time')
			print(mm.get_attribute('datetime'))
			image = item.find_element_by_class_name('tgme_widget_message_photo_wrap')




