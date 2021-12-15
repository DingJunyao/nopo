from __future__ import annotations

import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from . import El
from .el_parent import ElParent


class Els(ElParent):
    """Like a list of El s, but with more function."""
    def __init__(
            self,
            by: str = None,
            selector_str: str = None,
            selectors: tuple[tuple[str]] = None,
            max_time: int = 10,
            driver: WebDriver = None,
            el: ElParent = None
    ):
        """Init the Els element.

        :param by: How to select the element.
        :param selector_str: Selector text of the element.
        :param selectors: Tuple for multiply selectors (By, selector_str).
                If it's defined, by and selector_str attribute will be dismissed.
        :param max_time: Max time for waiting. Defaults to 10 (s).
        :param driver: Define the driver of the element. Use for normal instance.
        :param el: Transfer El / Els instance to another Els instance. Use for specifying class type.
                If it's determined, by, selector_str, selectors attribute will be dismissed.
                If `el.driver` is not None, driver attribute will be dismissed.
        """
        super().__init__(by, selector_str, selectors, max_time, driver, el)

    def __get__(self, instance, owner) -> Els:
        """To binding the driver from the instance above the element."""
        self.driver = instance.driver
        return self

    def __truediv__(self, other: ElParent) -> Els:
        """Use Els_1 / Els_2 for cascading selectors."""
        if not isinstance(other, ElParent):
            return NotImplemented
        return Els(selectors=self.selectors + other.selectors, max_time=self.max_time, driver=self.driver)

    def __itruediv__(self, other: ElParent) -> Els:
        """Els_1 /= Els_2 is equal to Els_1 = Els_1 / Els_2, but doesn't modify ID."""
        if not isinstance(other, ElParent):
            return NotImplemented
        self.selectors = self.selectors + other.selectors
        return self

    def __len__(self) -> int:
        for _ in range(self.max_time * 4):
            if len(self.driver.find_elements(By.XPATH, self.selectors_xpath)) == 0:
                time.sleep(0.25)
        return len(self.driver.find_elements(By.XPATH, self.selectors_xpath))

    def __getitem__(self, item: slice | int) -> El | list[El]:
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

    def __iter__(self) -> Els:
        self.__order = -1
        return self

    def __next__(self) -> El | list[El]:
        self.__order += 1
        if self.__order >= self.__len__():
            raise StopIteration()
        return self.__getitem__(self.__order)
