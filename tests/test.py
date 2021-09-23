import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nopo import El, Els


class GitHubPage:

    def __init__(self, drv):
        self.driver = drv

    textbox = El(By.XPATH, '//input[@aria-label="Search GitHub"]')
    main_page = El(By.TAG_NAME, 'main')
    user_a = El(By.XPATH, '//a[@class="mr-1"]')
    name = El(By.XPATH, '//span[@itemprop="name"]')

    def search_user(self, name):
        self.textbox.send_keys(name+"1212", clear=True)
        self.textbox.send_keys(name, clear=True)
        self.textbox.send_keys(Keys.ENTER)
        time.sleep(5)
        lis = Els(el=(self.main_page / El(By.XPATH, './/nav[1]') / El(By.TAG_NAME, 'a')))
        lis[-1].click()
        self.user_a.click()
        assert self.name.value == 'Ding Junyao'


class W3SchoolsPage:

    def __init__(self, drv):
        self.driver = drv

    iframe = El(By.ID, 'iframeResult')
    selection = El(By.TAG_NAME, 'select')

    @property
    def selections(self):
        return self.selection.options

    def select(self, selection):
        return self.selection.select_by_visible_text(selection)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://github.com/')
    gh_page = GitHubPage(driver)
    gh_page.search_user('DingJunyao')
    driver.get('https://www.w3school.com.cn/tiy/t.asp?f=eg_html_elements_select')
    w3_page = W3SchoolsPage(driver)
    w3_page.iframe.switch_in()
    assert [a.text for a in w3_page.selections] == ['Volvo', 'Saab', 'Fiat', 'Audi']
    w3_page.select('Fiat')
    driver.quit()
