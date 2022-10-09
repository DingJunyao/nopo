from __future__ import annotations

from cssselect import GenericTranslator
from selenium.webdriver.remote.webdriver import WebDriver

from .by import By


class ElParent:
    """Parent of El and Els."""

    def __init__(
            self,
            by: str = None,
            selector_str: str = None,
            selectors: tuple[tuple[str]] = None,
            max_time: int = 10,
            driver: WebDriver = None,
            el: ElParent = None
    ):
        """Init the ElParent element.

        :param by: How to select the element.
        :param selector_str: Selector text of the element.
        :param selectors: Tuple for multiply selectors (By, selector_str).
                If it's defined, by and selector_str attribute will be dismissed.
        :param max_time: Max time for waiting. Defaults to 10 (s).
        :param driver: Define the driver of the element. Use for normal instance.
        :param el: Transfer ElParent instance to another ElParent instance. Use for specifying class type.
                If it's determined, by, selector_str, selectors attribute will be dismissed.
                If `el.driver` is not None, driver attribute will be dismissed.
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

    @staticmethod
    def single_selector_to_xpath(by: str, selector: str) -> str:
        """Returns single selector to xpath.

        :raise ValueError: if by is wrong
        :raise SelectorSyntaxError: on invalid selectors,
        :raise ExpressionError: on unknown/unsupported selectors, including pseudo-elements.
        """
        if by == By.XPATH or by == By.TAG_NAME:
            return selector
        elif by == By.ID:
            return f'*[@id="{selector}"]'
        elif by == By.CLASS_NAME:
            return f'*[contains(concat(" ",@class," "), " {selector} ")]'
        elif by == By.NAME:
            return f'*[@name="{selector}"]'
        elif by == By.CSS_SELECTOR:
            return GenericTranslator().css_to_xpath(selector)
        elif by == By.LINK_TEXT or by == By.PARTIAL_LINK_TEXT:
            if '"' in selector:
                return_text = 'concat("' + selector.replace('"', '", \'"\', "') + '")'
            else:
                return_text = '"' + selector + '"'
            if by == By.LINK_TEXT:
                return f'a[text()={return_text}]'
            else:
                return f'a[contains(text(), {return_text})]'
        else:
            raise ValueError('By is wrong')

    @property
    def selectors_xpath(self) -> str:
        """Convert selectors to XPath.

        :raise SelectorSyntaxError: on invalid selectors,
        :raise ExpressionError: on unknown/unsupported selectors, including pseudo-elements.
        """
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
