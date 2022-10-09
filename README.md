# nopo

![](logo.png)

[![PyPI](https://img.shields.io/pypi/v/nopo)](https://pypi.org/project/nopo/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/nopo)

nopo (not only page object) is a package for Page Object Model (POM), a tool based on Selenium that helps you build POM in web test.

[查看中文文档](README_zh.md)

[View the development of it (in Chinese)](https://4ading.com/posts/nopo-development)

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
from selenium.webdriver.common.keys import Keys

from nopo import El, Els, By, Pg


class GitHubPage(Pg):

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

In class which has `driver` attribute to selenium webdriver (e.g., `nopo.Pg` class), you can define it as a class attribute:

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
el.value            # Returns text. If text is None or '', return value property (mostly for input element).
el.exist            # To show if the element exists.
el.exist_wait       # To show if the element exists (with wait).
el.is_selected      # Returns if the element is selected.
el.selectors_xpath  # Returns selector to xpath.
el.elem             # Returns the WebElement instance of the element (with wait).
el.elem_clickable   # Returns the WebElement instance of the element (wait for clickable).
el.elem_no_wait     # Returns the WebElement instance of the element (without wait).

el.options                  # Returns a list of all options belonging to this select tag
el.all_selected_options     # Returns a list of all selected options belonging to this select tag
el.first_selected_option    # Returns the first selected option in this select tag.

el.click()                                          # Click the element.
el.clear(force=False)                               # Clear the element. Use force=True to ensure the element can be cleared to deal with some situation.
el.send_keys(keys, clear=False, force_clear=False)  # Send keys to element. If clear is True, clear the element before sending. If clear and force are True, clear will be in force mode.
el.csk(keys, force_clear=False)                     # Clear and send keys to element. If force_clear is True, clear will be in force mode.
el.nn_csk(keys, force_clear=False)                  # Clear and send keys if keys is not None. If force_clear is True, clear will be in force mode.
el.get_attribute(attr)                              # Get attribute of the element.
el.get_property(property_text)                      # Get property of the element.
el.wait_for_click()                                 # Wait until the element is clickable.
el.wait_for_present()                               # Wait until the element is present.

el.select_by_value(value)           # Select options by given value argument.
el.select_by_index(index)           # Select the option at the given index.
el.select_by_visible_text(text)     # Select options by visible text.
el.deselect_all()                   # Clear all selected entries.
el.deselect_by_value(value)         # Deselect options by given value argument.
el.deselect_by_index(index)         # Deselect the option at the given index.
el.deselect_by_visible_text(text)   # Deselect options by visible text.

el.switch_in()  # Switch in the frame.

El.single_selector_to_xpath(by, selector) # Return single selector to xpath.
```

### Cascading

You can use `/` to cascading selectors:

```python
el1 = El(by1, selector_str1)
el2 = El(by2, selector_str2)
example_el = el1 / el2
```

The type of `example_el` above is same as `el1`, and find element using selector of `el1` and `el2`, like the following code in selenium:

```python
el1 = driver.find_element.by(by1, selector_str1)
example_el = el1.find_element.by(by2, selector_str2)
```

### Extending

`el` attribute helps you transfer class type, which makes it easy to customize element(s):

```python
class MyEl(El):
    pass

example_el = MyEl(el=el1 / el2)
```

## Build

```bash
pip install -r requirements.txt

python -m build
# or
python3 -m build
```

## Further plan

- More operating functions
- Ready-to-use Element classes for frontend frameworks (like [Ant Design](https://ant.design/) and [Element](https://element-plus.org/))

## License

Apache License Version 2.0
