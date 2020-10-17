from pages import LoginPage, KeypadPage, BasePage
from selenium import webdriver

class Properties:
    agency = ''
    conta = ''
    password = ''

    @classmethod
    def from_env(cls):
        pass

def main():
    props = init()
    LoginPage().login()
    KeypadPage().enter_password()
    

def init():
    driver = webdriver.Chrome()
    BasePage.driver = driver
