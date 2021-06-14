import time
from typing import Tuple, Optional

from cssselect import GenericTranslator
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class El:
    """Element for each page. You can use El_1 / El_2 for multiply selectors."""

    def __init__(
            self,
            by: By = None,
            selector_str: str = None,
            selectors: Tuple[Tuple[By, str]] = None,
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
        :param el: Transfer El / Els instance to another El instance. Use for specifying class type.
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
        """Use El_1 / El_2 for cascading selectors."""
        return El(selectors=self.selectors + other.selectors, max_time=self.max_time, driver=self.driver)


    @staticmethod
    def single_selector_to_xpath(by: By, selector: str):
        """Return single selector to xpath."""
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
        """Return selector to xpath."""
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

    def wait_for_click(self):
        """Wait until the element is clickable."""
        wait = WebDriverWait(self.driver, self.max_time)
        wait.until(ec.element_to_be_clickable(self.selectors[0]))

    def wait_for_present(self):
        """Wait until the element is present."""
        wait = WebDriverWait(self.driver, self.max_time)
        wait.until(ec.presence_of_element_located(self.selectors[0]))

    @property
    def elem_no_wait(self) -> WebElement:
        """Return the WebElement instance of the element (without wait)."""
        web_elem = self.driver
        for selector in self.selectors:
            web_elem = web_elem.find_element(*selector)
        return web_elem

    @property
    def elem(self) -> WebElement:
        """Return the WebElement instance of the element (with wait)."""
        try:
            self.wait_for_present()
        except TimeoutException:
            pass
        for _ in range(self.max_time * 10):
            try:
                return self.elem_no_wait
            except NoSuchElementException:
                time.sleep(0.1)
        return self.elem_no_wait

    @property
    def elem_clickable(self) -> WebElement:
        """Return the WebElement instance of the element (wait for clickable)."""
        try:
            self.wait_for_click()
        except TimeoutException:
            pass
        for _ in range(self.max_time * 10):
            try:
                return self.elem_no_wait
            except NoSuchElementException:
                time.sleep(0.1)
        return self.elem_no_wait

    @property
    def exist(self) -> bool:
        """To show if the element exists."""
        try:
            el = self.elem_no_wait
            return True
        except NoSuchElementException:
            return False

    @property
    def exist_wait(self) -> bool:
        """To show if the element exists, Add wait."""
        try:
            el = self.elem
            return True
        except NoSuchElementException:
            return False

    @property
    def text(self) -> Optional[str]:
        """Text of the element."""
        return self.elem.text

    def click(self):
        """Click the element."""
        return self.elem_clickable.click()

    def clear(self):
        """Clear the element."""
        return self.elem_clickable.clear()

    def send_keys(self, keys: str, clear: bool = False):
        """Send keys to element.

        :param keys: Keys to send.
        :param clear: Clear before send keys or not. Defaults to False.
        """
        if clear:
            self.elem_clickable.clear()
        return self.elem_clickable.send_keys(keys)

    def csk(self, keys):
        """Clear and send keys to given element."""
        return self.send_keys(keys, True)

    def nn_csk(self, keys: str):
        """Clear and send keys if keys is not None."""
        if keys is not None:
            return self.csk(keys)

    def get_attribute(self, attr):
        """Get attribute of the element."""
        return self.elem.get_attribute(attr)

    def get_property(self, property_text):
        """Get property of the element."""
        return self.elem.get_property(property_text)

    @property
    def value(self):
        """Return text. If text is None or '', return value property (mostly for input element)."""
        return self.text or self.get_property('value')

    def __str__(self):
        try:
            return f'(El \'{self.selectors_xpath}\' at {id(self)})'
        except ValueError:
            return f'(El \'{list(self.selectors)}\' at {id(self)})'

    __repr__ = __str__

    @property
    def is_selected(self):
        """Return if the element is selected."""
        return self.elem_clickable.is_selected()
