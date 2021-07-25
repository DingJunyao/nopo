# nopo

![](./logo.png)

[![PyPI](https://img.shields.io/pypi/v/nopo)](https://pypi.org/project/nopo/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/nopo)

nopo (not only page object) is a package for Page Object Model (POM), a tool based on Selenium that helps you build POM in web test.

Notice: nopo is still in development, so the API is currently unstable.

## Features

- Define and operate an element or elements like using Selenium (but with advanced features)
- Auto wait and find the element(s)
- Cascading selectors support in an element

## Install

```bash
pip install nopo
```

## Usage

### Example

Here shows a simple usage example:

```python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from nopo import El, Els


class GitHubPage:

    def __init__(self, drv):
        self.driver = drv

    # Define like Selenium
    textbox = El(By.XPATH, '//input[@aria-label="Search GitHub"]')
    main_page = El(By.TAG_NAME, 'main')
    user_a = El(By.CLASS_NAME, 'mr-1')
    name = El(By.XPATH, '//span[@itemprop="name"]')

    def search_user(self, name):
        # Operate like Selenium, but with advanced features.
        self.textbox.send_keys(name, clear=True)
        self.textbox.send_keys(Keys.ENTER)
        # Elements define
        # Use El_1 / El_2 to define cascading element(s)
        # Use El(el=El_old) or Els(el=El_old) to turn type
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
```

### Defining

In class which has `driver` attribute to selenium webdriver, you can define it as a class attribute:

```python
example_el = El(by, selector_str)
example_els = Els(by, selector_str)
```

You can also use attribute `driver` to specify a webdriver or use in other occasions:

```python
example_el = El(by, selector_str, driver=driver)
example_els = Els(by, selector_str, driver=driver)
```

### Operating

```python
el.text             # Text of the element.
el.value            # Return text. If text is None or '', return value property (mostly for input element).
el.exist            # To show if the element exists.
el.exist_wait       # To show if the element exists (with wait).
el.is_selected      # Return if the element is selected.
el.selectors_xpath  # Return selector to xpath.
el.elem             # Return the WebElement instance of the element (with wait).
el.elem_clickable   # Return the WebElement instance of the element (wait for clickable).
el.elem_no_wait     # Return the WebElement instance of the element (without wait).

el.click()                                          # Click the element.
el.clear(force=False)                               # Clear the element. Use force=True to ensure the element can be cleared to deal with some situation.
el.send_keys(keys, clear=False, force_clear=False)  # Send keys to element. If clear is True, clear the element before sending. If clear and force are True, clear will be in force mode.
el.csk(keys, force_clear=False)                     # Clear and send keys to element. If force_clear is True, clear will be in force mode.
el.nn_csk(keys, force_clear=False)                  # Clear and send keys if keys is not None. If force_clear is True, clear will be in force mode.
el.get_attribute(attr)                              # Get attribute of the element.
el.get_property(property_text)                      # Get property of the element.
el.wait_for_click()                                 # Wait until the element is clickable.
el.wait_for_present()                               # Wait until the element is present.

El.single_selector_to_xpath(by, selector) # Return single selector to xpath.
```

### Cascading

You can use `/` to cascading selectors:

```python
el1 = El(by1, selector_str1)
el2 = El(by2, selector_str2)
example_el = el1 / el2
```

The type of `example_el` above is same as `el1`.

### Extending

`el` attribute helps you transfer class type, which makes it easy to customize element(s):

```python
class MyEl(El):
    pass

example_el = MyEl(el=el1 / el2)
```

## Build

```bash
python -m build
# or
python3 -m build
```

## Further plan

- More operating functions
- Ready-to-use Element classes for frontend frameworks (like [Ant Design](https://ant.design/) and [Element](https://element-plus.org/))

## License

Apache License Verison 2.0
