from selenium import webdriver
import time

class BasePage:
    """
    Base abstraction for a page
    """
    url = ''
    driver = None

    @classmethod
    def set_driver(cls, driver):
        """Set drivers for class and configures implict wait"""
        cls.driver = driver
        driver.implicitly_wait(30)

    @staticmethod
    def _by_id_factory(id):
        return lambda self: self.driver.find_element_by_id(id)

    def navigate(self):
        self.driver.get(self.url)


class LoginPage(BasePage):
    url = 'https://itau.com.br'

    agency_field = property(BasePage._by_id_factory('agencia'))
    account_field = property(BasePage._by_id_factory('conta'))
    login_button = property(BasePage._by_id_factory('btnLoginSubmit'))

    def login(self, agency, account):
        self.navigate()
        self.agency_field.send_keys(agency)
        self.account_field.send_keys(account)
        self.login_button.click()


class KeypadPage(BasePage):

    login_button = property(BasePage._by_id_factory('acessar'))

    @property
    def keypad_buttons(self):
        return self.driver.find_elements_by_class_name('campoTeclado')

    def get_key(self, n):
        """Return keypad button that contains the given digit"""
        buttons = self.keypad_buttons
        button = next(filter(lambda button: n in button.text, buttons))
        return button

    def enter_password(self, password):
        for digit in password:
            key = self.get_key(digit)
            key.click()
        self.login_button.click()
