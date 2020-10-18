from pages import LoginPage, KeypadPage, BasePage

from selenium import webdriver
import os

class Properties:
    agency = ''
    account = ''
    password = ''

    @classmethod
    def from_env(cls):
        obj = cls()
        obj.agency = os.environ['agency']
        obj.account = os.environ['account']
        obj.password = os.environ['password']
        return obj


def main():
    init()
    props = Properties.from_env()
    LoginPage().login(props.agency, props.account)
    KeypadPage().enter_password(props.password)
    

def init():
    driver = webdriver.Chrome()
    BasePage.set_driver(driver)

if __name__ == '__main__':
    main()
