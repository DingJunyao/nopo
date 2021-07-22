from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nopo import El, Els


class GitHubPage:

    def __init__(self, drv):
        self.driver = drv

    textbox = El(By.XPATH, '//input[@aria-label="Search GitHub"]')
    main_page = El(By.TAG_NAME, 'main')
    user_a = El(By.CLASS_NAME, 'mr-1')
    name = El(By.XPATH, '//span[@itemprop="name"]')

    def search_user(self, name):
        self.textbox.send_keys(name, clear=True)
        self.textbox.send_keys(Keys.ENTER)
        lis = Els(el=(self.main_page / El(By.XPATH, './/nav[1]') / El(By.TAG_NAME, 'a')))
        lis[-1].click()
        self.user_a.click()
        assert self.name.value == 'Ding Junyao'


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://github.com/')
    gh_page = GitHubPage(driver)
    gh_page.search_user('DingJunyao')
    driver.quit()
