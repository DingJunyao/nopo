# nopo

![](./logo.png)

[![PyPI](https://img.shields.io/pypi/v/nopo)](https://pypi.org/project/nopo/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/nopo)

nopo （not only page object 的缩写） 是一个关于 Page Object 模型（PO模型，POM）的包，基于 Selenium，帮助你在 Web 测试中构建 POM。

[View README in English](README.md)

[查看开发该模块的历程](https://4ading.com/posts/nopo-development)

## 功能

- 定义、操作一个元素，或所有具有相同属性的元素，方法上类似于 Selenium，不过也扩充了一些功能
- 自动等待、寻找单个元素 / 所有元素
- 在元素中支持层叠的选择器

## 安装

```bash
pip install nopo
```

## 使用方法

### 示例

一个简单的示例：

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from nopo import El, Els, By


class GitHubPage:

    def __init__(self, drv):
        self.driver = drv

    # 像 Selenium 一样定义
    textbox = El(By.XPATH, '//input[@aria-label="Search GitHub"]')
    main_page = El(By.TAG_NAME, 'main')
    user_a = El(By.CLASS_NAME, 'mr-1')
    name = El(By.XPATH, '//span[@itemprop="name"]')

    def search_user(self, name):
        # 像 Selenium 一样操作，不过有更多的功能
        self.textbox.send_keys(name, clear=True)
        self.textbox.send_keys(Keys.ENTER)
        # 元素定义
        # 用 El_1 / El_2 定义层叠的元素
        # 用 El(el=El_old) 或 Els(el=El_old) 改变元素的数据类型
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

### 定义

在有 `driver` 属性，且该属性指向 Selenium WebDriver 实例的类，可以定义为类属性：

```python
example_el = El(by, selector_str)
example_els = Els(by, selector_str)
```
在其他不便使用类属性的场合，或者是想要自定义 WebDriver，可以使用 `driver` 参数：

```python
example_el = El(by, selector_str, driver=driver)
example_els = Els(by, selector_str, driver=driver)
```

### 操作

```python
el.text             # 元素的文本
el.value            # 返回 el.text 的值。如果 el.text 为 None 或 ''，返回 value 属性（多用于 input 元素）
el.exist            # 即刻判断元素是否存在
el.exist_wait       # 判断元素是否存在，支持自动等待
el.is_selected      # 判断元素是否被选择。
el.selectors_xpath  # 返回元素的 XPath 选择器的值
el.elem             # 返回元素的 WebElement 实例，支持自动等待到在 DOM 里出现
el.elem_clickable   # 返回元素的 WebElement 实例，支持自动等待到可点击
el.elem_no_wait     # 即刻返回元素的 WebElement 实例

el.options                  # 针对于 select 标签的元素，返回属于该元素的所有选项
el.all_selected_options     # 针对于 select 标签的元素，返回属于该元素的所有已选选项
el.first_selected_option    # 针对于 select 标签的元素，返回属于该元素的第一个已选选项

el.click()                                          # 单击元素
el.clear(force=False)                               # 清除元素内文本（比如 input 元素）. 设置 force=True 确保元素内文本清除干净，也就是强制模式（在某些场合适用）
el.send_keys(keys, clear=False, force_clear=False)  # 向元素输入按键或文本。如果 clear 为 True，则输入前会清空元素内文本。如果 clear 和 force 均为 True，清除方法进入强制模式
el.csk(keys, force_clear=False)                     # 清空元素内文本，并向元素输入按键或文本。如果 force_clear 为 True，清除方法进入强制模式
el.nn_csk(keys, force_clear=False)                  # 如果keys 非 None，则清空元素内文本，并向元素输入按键或文本。如果 force_clear 为 True，清除方法进入强制模式
el.get_attribute(attr)                              # 获取元素的参数（attribute，偏向于 HTML 层面）
el.get_property(property_text)                      # 获取元素的属性（property，偏向于 JS 层面）
el.wait_for_click()                                 # 等待到元素可点击
el.wait_for_present()                               # 等待到元素出现

el.select_by_value(value)           # 针对于 select 标签的元素，根据给定 value 值选择选项
el.select_by_index(index)           # 针对于 select 标签的元素，根据给定 index 值选择选项
el.select_by_visible_text(text)     # 针对于 select 标签的元素，根据给定显示文本选择选项
el.deselect_all()                   # 针对于 select 标签的元素，取消选择所有内容
el.deselect_by_value(value)         # 针对于 select 标签的元素，根据给定 value 值取消选择选项
el.deselect_by_index(index)         # 针对于 select 标签的元素，根据给定 index 值取消选择选项
el.deselect_by_visible_text(text)   # 针对于 select 标签的元素，根据给定显示文本取消选择选项

el.switch_in()  # 针对于 iframe 标签的元素，切换到该框架

El.single_selector_to_xpath(by, selector) # 将单个选择器转换为 XPath
```

### 层叠

使用 `/` 操作符链接多个元素，得到新元素。新元素的选择器为两者层叠而成:

```python
el1 = El(by1, selector_str1)
el2 = El(by2, selector_str2)
example_el = el1 / el2
```

`example_el` 的数据类型与 `el1` 相同，其选择器为 `el_1` 的选择器下执行 `el2` 的选择器，类似于使用 Selenium 中的：

```python
el1 = driver.find_element.by(by1, selector_str1)
example_el = el1.find_element.by(by2, selector_str2)
```

### 扩展

`el` 参数可用于转换类的类型，便于自定义类：

```python
class MyEl(El):
    pass

example_el = MyEl(el=el1 / el2)
```

## 构建

```bash
pip install -r requirements.txt

python -m build
# 或
python3 -m build
```

## 未来计划

- 添加更多操作功能
- 为前端框架（如 [Ant Design](https://ant.design/) 和 [Element](https://element-plus.org/)）编写开箱即用的元素类

## 协议

Apache 协议 2.0 版
