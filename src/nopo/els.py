import time

from cssselect import GenericTranslator
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .el import El


class Els:
    """Like a list of El s, but with more function."""
    def __init__(
            self,
            by: str = None,
            selector_str: str = None,
            selectors: tuple[tuple[By, str]] = None,
            max_time: int = 10,
            driver: WebDriver = None,
            el=None
    ):
        """Init the El element.

        :param by: How to select the element.
        :param selector_str: Selector text of the element.
        :param selectors: Tuple for multiply selectors (By, selector_str).
                If it's defined, by and selector_str attribute will be dismissed.
        :param max_time: Max time for waiting. Defaults to 10 (s).
        :param driver: Define the driver of the element. Use for normal instance.
        :param el: Transfer El / Els instance to another Els instance. Use for specifying class type.
                If it's determined, by, selector_str, selectors attribute will be dismissed.
                If el.driver is not None, driver attribute will be dismissed.
        """
        self.max_time = max_time
        if el:
            self.selectors = el.selectors
            if el.driver:
                self.driver = el.driver
            elif driver:
                self.driver = driver
        else:
            if not selectors:
                self.selectors = ((by, selector_str),)
            else:
                self.selectors = selectors
            if driver:
                self.driver = driver

    def __get__(self, instance, owner):
        """To binding the driver from the instance above the element."""
        self.driver = instance.driver
        return self

    def __truediv__(self, other):
        """Use Els_1 / Els_2 for cascading selectors."""
        return Els(selectors=self.selectors + other.selectors, max_time=self.max_time, driver=self.driver)

    @staticmethod
    def single_selector_to_xpath(by: str, selector: str):
        """Returns single selector to xpath."""
        if by == By.XPATH or by == By.TAG_NAME:
            return selector
        elif by == By.ID:
            return f'*[@id="{selector}"]'
        elif by == By.CLASS_NAME:
            return f'*[contains(concat(" ",@class," "), " {selector} ")]'
        elif by == By.NAME:
            return f'*[@name="{selector}"]'
        elif by == By.CSS_SELECTOR:
            return GenericTranslator().css_to_xpath('selector')
        else:
            raise ValueError('Only support By.XPATH, By.TAG_NAME, By.ID, By.CLASS_NAME, By.NAME and By.CSS_SELECTOR')

    @property
    def selectors_xpath(self) -> str:
        """Returns selector to xpath."""
        xpath = ''
        for index, selector in enumerate(self.selectors):
            if index != 0:
                if selector[0] == By.XPATH:
                    xpath += '/' + self.single_selector_to_xpath(*selector)
                else:
                    xpath += '//' + self.single_selector_to_xpath(*selector)
            else:
                if selector[0] != By.XPATH:
                    xpath += '//'
                xpath += self.single_selector_to_xpath(*selector)
        return xpath

    def __len__(self):
        for _ in range(self.max_time * 4):
            if len(self.driver.find_elements(By.XPATH, self.selectors_xpath)) == 0:
                time.sleep(0.25)
        return len(self.driver.find_elements(By.XPATH, self.selectors_xpath))

    def __getitem__(self, item):
        length = self.__len__()
        if isinstance(item, slice):
            return [self.__getitem__(i) for i in range(length)[item]]
        elif isinstance(item, int):
            if item >= 0:
                xpath_index = item + 1
            else:
                xpath_index = length + item + 1
            if xpath_index > length or xpath_index <= 0:
                raise IndexError(f'index ({item}) out of range ({length})')
            return El(By.XPATH, f'({self.selectors_xpath})[{xpath_index}]', driver=self.driver, max_time=self.max_time)
        else:
            raise TypeError(f'item must be slice or int, not {type(item)}')

    def __iter__(self):
        self.__order = -1
        return self

    def __next__(self):
        self.__order += 1
        if self.__order >= self.__len__():
            raise StopIteration()
        return self.__getitem__(self.__order)
