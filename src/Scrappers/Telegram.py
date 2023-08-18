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
		"telegram": True,
		"replying_to": []
	}

	BASE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

	def __init__(self, acc: AccountWatchlist.Account):
		self.account = acc
		self.url = acc.account_url
		self.options = acc.json_options
		self.cache_list = []
		self.weboptions = webdriver.ChromeOptions()
		self.weboptions.add_argument('--disable-blink-features=AutomationControlled')
		self.weboptions.add_argument('--disable-popup-blocking')
		self.weboptions.add_argument('--start-maximized')
		self.weboptions.add_argument('--disable-extensions')
		self.weboptions.add_argument('--no-sandbox')
		self.weboptions.add_argument('--disable-dev-shm-usage')
		self.weboptions.add_argument('--headless')

	def scrape_images(self):
		wbd_profile = webdriver.Chrome(options=self.weboptions)
		stealth(wbd_profile,
				languages=["en-US", "en"],
				vendor="Google Inc.",
				platform="Win32",
				webgl_vendor="Intel Inc.",
				renderer="Intel Iris OpenGL Engine",
				fix_hairline=True,)
		wbd_profile.get(self.url)
		list_classes_profile = wbd_profile.find_elements(By.CLASS_NAME, 'tgme_widget_message')
		image_list = []
		for item in list_classes_profile:
			mis = item.find_element_by_class_name('tgme_widget_message_info')
			metadata = mis.find_element_by_class_name('tgme_widget_message_meta')
			date_post = metadata.find_element(By.CSS_SELECTOR,'a').find_element(By.CSS_SELECTOR, 'time').get_attribute('datetime')
			image = item.find_element_by_class_name('tgme_widget_message_photo_wrap').value_of_css_property("background-image")
			image_list.append((datetime.strptime(date_post[:-6], self.BASE_TIME_FORMAT), image[5:-2]))
		self.cache_list = sorted(image_list, key=lambda x: x[0])
		wbd_profile.close()

	def download_files(self):
		c = 0
		for image_date, image_url in self.cache_list:
			if self.options['last_downloaded'] is None \
					or image_date > datetime.strptime(self.options['last_downloaded'], self.BASE_TIME_FORMAT):
				request = get(image_url, allow_redirects=True)
				image_name = f"{image_date.strftime(self.BASE_TIME_FORMAT)}_{c}{image_url[-4:]}"
				with open('/home/giulliano/Documentos/Projetos/carlinhos-bot/downloads/' + image_name, 'wb+') as img:
					img.write(request.content)
				self.options['last_downloaded'] = image_date.strftime(self.BASE_TIME_FORMAT)
				c += 1
		self.account.json_options = self.options





