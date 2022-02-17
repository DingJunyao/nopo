from __future__ import annotations

import time
from typing import Optional

from cssselect import ExpressionError, SelectorSyntaxError
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from .el_parent import ElParent


class El(ElParent):
    """Element for each page. You can use El_1 / El_2 for cascading selectors."""

    def __init__(
            self,
            by: str = None,
            selector_str: str = None,
            selectors: tuple[tuple[str]] = None,
            max_time: int = 10,
            driver: WebDriver = None,
            el: ElParent = None
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
                If `el.driver` is not None, driver attribute will be dismissed.
        """
        super().__init__(by, selector_str, selectors, max_time, driver, el)

    def __get__(self, instance, owner) -> El:
        """To binding the driver from the instance above the element."""
        self.driver: WebDriver = instance.driver
        return self

    def __truediv__(self, other: ElParent) -> El:
        """Use El_1 / El_2 for cascading selectors."""
        if not isinstance(other, ElParent):
            return NotImplemented
        return El(selectors=self.selectors + other.selectors, max_time=self.max_time, driver=self.driver)

    def __itruediv__(self, other: ElParent) -> El:
        """El_1 /= El_2 is equal to El_1 = El_1 / El_2, but doesn't modify ID."""
        if not isinstance(other, ElParent):
            return NotImplemented
        self.selectors = self.selectors + other.selectors
        return self

    def wait_for_click(self):
        """Wait until the element is clickable."""
        wait = WebDriverWait(self.driver, self.max_time)
        try:
            xpath = self.selectors_xpath
            wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        except ValueError or SelectorSyntaxError or ExpressionError:
            wait.until(ec.element_to_be_clickable(self.selectors[0]))

    def wait_for_present(self):
        """Wait until the element is present."""
        wait = WebDriverWait(self.driver, self.max_time)
        try:
            xpath = self.selectors_xpath
            wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
        except ValueError or SelectorSyntaxError or ExpressionError:
            wait.until(ec.presence_of_element_located(self.selectors[0]))

    @property
    def elem_no_wait(self) -> WebElement:
        """Returns the WebElement instance of the element (without wait)."""
        web_elem = self.driver
        for selector in self.selectors:
            web_elem = web_elem.find_element(*selector)
        return web_elem

    @property
    def elem(self) -> WebElement:
        """Returns the WebElement instance of the element (with wait)."""
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
        """Returns the WebElement instance of the element (wait for clickable)."""
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
            _ = self.elem_no_wait
            return True
        except NoSuchElementException:
            return False

    @property
    def exist_wait(self) -> bool:
        """To show if the element exists (with wait)."""
        try:
            _ = self.elem
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

    def clear(self, force: bool = False):
        """Clear the element. Use force=True to ensure the element can be cleared to deal with some situation."""
        self.elem_clickable.clear()
        if force:
            if self.elem_clickable.get_property('value'):
                self.driver.execute_script(
                    'document.evaluate(arguments[0],document).iterateNext().value=""',
                    self.selectors_xpath
                )

    def send_keys(self, keys: str, clear: bool = False, force_clear: bool = False):
        """Send keys to element.

        :param keys: Keys to send.
        :param clear: Clear before send keys or not. Defaults to False.
        :param force_clear: Set it to True to ensure the element can be cleared to deal with some situation.
                Invalid if clear=False.
        """
        if clear:
            self.clear(force=force_clear)
        return self.elem_clickable.send_keys(keys)

    def csk(self, keys, force_clear: bool = False):
        """Clear and send keys to given element."""
        return self.send_keys(keys, True, force_clear=force_clear)

    def nn_csk(self, keys: str, force_clear: bool = False):
        """Clear and send keys if keys is not None.
        Use force_clear=True to ensure the element can be cleared to deal with some situation.
        """
        if keys is not None:
            return self.csk(keys, force_clear=force_clear)

    def get_attribute(self, attr):
        """Get attribute of the element."""
        return self.elem.get_attribute(attr)

    def get_property(self, property_text):
        """Get property of the element."""
        return self.elem.get_property(property_text)

    @property
    def value(self):
        """Returns text. If text is None or '', return value property (mostly for input element)."""
        return self.text or self.get_property('value')

    def __str__(self) -> str:
        try:
            return f'(El \'{self.selectors_xpath}\' at {id(self)})'
        except ValueError or SelectorSyntaxError or ExpressionError:
            return f'(El \'{list(self.selectors)}\' at {id(self)})'

    __repr__ = __str__

    @property
    def is_selected(self):
        """Returns if the element is selected."""
        return self.elem_clickable.is_selected()

    # Select methods

    @property
    def options(self):
        """Returns a list of all options belonging to this select tag."""
        from .els import Els
        return Els(el=self / El(By.TAG_NAME, 'option'))

    @property
    def all_selected_options(self):
        """Returns a list of all selected options belonging to this select tag."""
        ret = []
        for opt in self.options:
            if opt.is_selected():
                ret.append(opt)
        return ret

    @property
    def first_selected_option(self):
        """The first selected option in this select tag (or the currently selected option in a normal select)."""
        for opt in self.options:
            if opt.is_selected():
                return opt
        raise NoSuchElementException("No options are selected")

    @property
    def _select_el(self):
        """Returns Select element.

        :raise UnexpectedTagNameException if not support.
        """
        return Select(self.elem_clickable)

    def select_by_value(self, value):
        """Select options by given value argument.

        :param value: Value of the value argument of the option. e.g., 'foo' in <option value="foo">Bar</option>.
        """
        return self._select_el.select_by_value(value)

    def select_by_index(self, index):
        """Select the option at the given index. This is done by examining the "index" attribute of an element, and not
            merely by counting.

        :param index: The option at this index will be selected
        """
        return self._select_el.select_by_index(index)

    def select_by_visible_text(self, text):
        """Select options by visible text.

        :param text: Visible text of the option. e.g., 'Bar' in <option value="foo">Bar</option>
        """
        return self._select_el.select_by_visible_text(text)

    def deselect_all(self):
        """Clear all selected entries. This is only valid when the SELECT supports multiple selections.

        :raise NotImplementedError If the SELECT does not support multiple selections
        """
        return self._select_el.deselect_all()

    def deselect_by_value(self, value):
        """Deselect options by given value argument.

        :param value: Value of the value argument of the option. e.g., 'foo' in <option value="foo">Bar</option>
        """
        return self._select_el.deselect_by_value(value)

    def deselect_by_index(self, index):
        """Deselect the option at the given index. This is done by examining the "index" attribute of an
           element, and not merely by counting.

        :param index: The option at this index will be deselected
        """
        return self._select_el.deselect_by_index(index)

    def deselect_by_visible_text(self, text):
        """Deselect options by visible text.

        :param text: Visible text of the option. e.g., 'Bar' in <option value="foo">Bar</option>
        """
        return self._select_el.deselect_by_visible_text(text)

    # iframe switch in

    def switch_in(self):
        """Switch in the frame. Ensure accessible before calling."""
        return self.driver.switch_to.frame(self.elem)
