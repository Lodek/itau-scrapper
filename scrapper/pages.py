from selenium import webdriver

class BasePage:
    """
    Base abstraction for a page
    """
    url = ''
    driver = None

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
        button = next(filter(lambda button: n in button.text, button))
        return button

    def enter_password(self, password):
        for digit in password:
            key = self.get_key(password)
            key.click()
        self.login_button.click()
