from pages.base_page import BasePage
from utils.data_reader import DataReader
import logging

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    def __init__(self, page, data_reader: DataReader):
        super().__init__(page)
        self.data_reader = data_reader

    def login(self):
        url = self.data_reader.get_value("url")
        username = self.data_reader.get_value("username")
        password = self.data_reader.get_value("password")

        self.open_url(url)
        self.fill_text('input[name="username"]', username)
        self.fill_text('input[name="password"]', password)
        self.click_element("//button[@id='login']")
        logger.info("Completed login")

    def login_without_url(self):
        username = self.data_reader.get_value("username")
        password = self.data_reader.get_value("password")
        self.fill_text('input[name="username"]', username)
        self.fill_text('input[name="password"]', password)
        self.click_element("//button[@id='login']")
        logger.info("Completed login without loading URL")