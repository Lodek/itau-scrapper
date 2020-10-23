from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def convert_to_select(element_getter):
    """Decorator that receives a getter function for an element and return
    element cast as an HTML select element"""
    def caster():
        return Select(element_getter())


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
    """Page with account information fields"""
    url = 'https://itau.com.br'

    agency_field = property(BasePage._by_id_factory('agencia'))
    account_field = property(BasePage._by_id_factory('conta'))
    login_button = property(BasePage._by_id_factory('btnLoginSubmit'))

    def login(self, agency, account):
        """Nagivate to page, add info and click login"""
        self.navigate()
        self.agency_field.send_keys(agency)
        self.account_field.send_keys(account)
        self.login_button.click()


class KeypadPage(BasePage):
    """
    Page which contains keypad to input password
    """

    login_button = property(BasePage._by_id_factory('acessar'))


    #i'm dumb, should've done all this through JS... Should've just set the elements text
    @property
    def keypad_buttons(self):
        """Return all buttons in virtual keypad"""
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


class HomePage(BasePage):

    @property
    def popup_map(self):
        return self.driver.find_element_by_name('mapa_lightbox_banner_02')

    transactions_button = property(BasePage._by_id_factory('VerExtrato'))

    def dismiss_popup(self):
        map = self.popup_map
        if map:
            js = 'popFechar("02")'
            self.driver.execute_script(js)
        return self

    def view_transactions(self):
        self.transactions_button.click()
        return self


class TransactionModel:
    
    def __init__(self, date, transaction, value):
        self.date = date
        self.transaction = transaction
        self.value = value


class TransactionPage(BasePage):
    """
    Page with the SAUCE. Contains transactions, values and their dates.
    """

    @property
    def transactions(self):
        return self.driver.find_elements_by_class_name('extrato-tabela-pf')

    @property
    def filter_button(self):
        return self.driver.find_element_by_class_name('month-picker__button')

    period_select = property(convert_to_select(BasePage._by_id_factory('select-192')))
    month_picker = property(BasePage._by_id_factory('monthPickerBtn363'))
    date_input = property(BasePage._by_id_factory('inputDate363'))


    def period_by_month(self):
        self.period_select.select_by_value('mesCompleto')

    def filter_by_date(self, date):
        """
        Perform flow of filtering by month/year. Expect date object
        """
        self.period_select.select_by_value('mesCompleto')
        self.month_picker.click()
        date_text = f'{date.month:02}{date.year:04}'
        self.date_input.send_keys(date_text)
        self.filter_button.click()
        return self


#TODO Run stuffs
