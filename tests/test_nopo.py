import time

from selenium.webdriver.common.keys import Keys

from src.nopo import El, Els, By, Pg


class GitHubPage(Pg):

    textbox = El(By.XPATH, '//input[@aria-label="Search GitHub"]')
    main_page = El(By.TAG_NAME, 'main')
    user_a = El(By.XPATH, '//a[@class="mr-1"]')
    name = El(By.XPATH, '//span[@itemprop="name"]')

    def search_user(self, name):
        self.textbox.send_keys(name+"1212", clear=True)
        self.textbox.send_keys(name, clear=True)
        self.textbox.send_keys(Keys.ENTER)
        time.sleep(5)
        mid_el = self.main_page / El(By.XPATH, './/nav[1]')
        mid_el_id = id(mid_el)
        mid_el /= El(By.TAG_NAME, 'a')
        assert id(mid_el) == mid_el_id
        lis = Els(el=mid_el)
        lis[-1].click()
        self.user_a.click()
        assert self.name.value == 'Ding Junyao'


class W3SchoolsSelect(El):
    pass


class W3SchoolsPage(Pg):

    iframe = El(By.ID, 'iframeResult')
    selection = W3SchoolsSelect(By.TAG_NAME, 'select')

    @property
    def selections(self):
        return self.selection.options

    def select(self, selection):
        return self.selection.select_by_visible_text(selection)


def test_nopo(selenium):
    selenium.maximize_window()
    selenium.get('https://github.com/')
    gh_page = GitHubPage(selenium)
    gh_page.search_user('DingJunyao')
    selenium.get('https://www.w3school.com.cn/tiy/t.asp?f=eg_html_elements_select')
    w3_page = W3SchoolsPage(selenium)
    w3_page.iframe.switch_in()
    assert [a.text for a in w3_page.selections] == ['Volvo', 'Saab', 'Fiat', 'Audi']
    w3_page.select('Fiat')
