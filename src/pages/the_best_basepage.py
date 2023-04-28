import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


# AL ESTAR DETRÁS DE UN PROXY EMPRESARIAL:
# Para que webdriver_manager no dé error de SSL (Error de certificado autofirmado)
# abrir el archivo C:\Python\Lib\site-packages\webdriver_manager\core\http.py
# comentar la línea 34 con #:
#     # url=url, verify=self._ssl_verify, stream=True, **kwargs)
# y agregar la siguiente a continuación:
#     url=url, verify=False, stream=True, **kwargs)
# TENER EN CUENTA QUE SI SE ACTUALIZA LA LIBRERÍA, HABRÁ QUE VOLVER A HACERLO!!


class BasePage:

    def __init__(self, driver_to_use='chrome' or 'firefox' or 'edge', wait=10, highlight=False, proxy=''):
        if driver_to_use.lower() == 'firefox':
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        elif driver_to_use.lower() == 'edge':
            edge_options = webdriver.EdgeOptions()
            edge_options.use_chromium = True
            self.driver = webdriver.Edge(options=edge_options,
                                         service=EdgeService(EdgeChromiumDriverManager().install()))
        else:
            chrome_options = webdriver.ChromeOptions()
            if proxy != '':
                chrome_options.add_argument('--proxy-server=%s' % proxy)
            chrome_options.add_experimental_option('excludeSwitches', ['disable-logging'])  # para eliminar msg de USB
            self.driver = webdriver.Chrome(options=chrome_options,
                                           service=ChromeService(ChromeDriverManager().install()))
        self.wait = WebDriverWait(self.driver, wait)
        self.actions = ActionChains(self.driver)
        self.highlight = highlight
        self.highlight_script = "arguments[0].style.border='10px ridge #d92356'"

# VALIDADOS
    def navigate_to(self, url):
        self.driver.get(url)

    def close_current_window(self):
        self.sleep(2)
        # close() method closes the current window.
        self.driver.close()

    def close_browser(self):
        time.sleep(2)
        # quit() method quits the driver instance, closing every associated window, which is opened.
        self.driver.quit()

    def find(self, locator):
        # TODO Cuál usar???
        # element = self.wait.until(ec.presence_of_element_located(locator))  # aún no presente
        # element = self.wait.until(ec.visibility_of_element_located(locator))  # presente pero aún no es visible
        element = self.wait.until(ec.element_to_be_clickable(locator))  # presente, visible y aún no es clickeable
        if self.highlight:
            self.driver.execute_script(self.highlight_script, element)
        return element

    def clear_text(self, locator):
        self.find(locator).clear()

    def set_text(self, locator, text_to_write):
        self.clear_text(locator)
        self.find(locator).send_keys(text_to_write)

    def click_element(self, locator):
        self.wait.until(ec.element_to_be_clickable(locator)).click()
        # self.actions.click(self.find(locator))
        # self.find(locator).click()
        """
        Cuál usar??? Según perplexity:
        if the element is not immediately clickable and needs to be waited for, use the first code snippet.
        If the element is immediately clickable, use either the second or third code snippet.
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'myButton'))) => si no, TimeoutException
        """

    def current_url(self):
        return self.driver.current_url

    def handle_popup_window(self, window):
        self.driver.switch_to.window(window)

    def maximize(self):
        self.driver.maximize_window()

    def highlight_web_element(self, element):
        self.driver.execute_script(self.highlight_script, element)

    @staticmethod
    def sleep(sec):
        time.sleep(sec)

# SIN VALIDAR

    def double_click(self, locator):
        # TODO Cuál usar???
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.actions.double_click(element)

    def right_click(self, locator):
        # TODO Cuál usar???
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.actions.context_click(element)

    def click_and_hold(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.actions.click_and_hold(element)

    def release(self, locator):
        element = self.wait.until(ec.element_to_be_clickable(locator))
        self.actions.release(element)

    def get_text(self, locator):
        return self.find(locator).text

    def get_value_from_table(self, locator, row, column):
        cell_need_it = locator+"/table/tbody/tr["+row+"]/td["+column+"]"
        return self.find(cell_need_it).text

    def set_value_on_table(self, locator, row, column, text):
        cell_to_fill = locator + "/table/tbody/tr[" + row + "]/td[" + column + "]"
        self.find(cell_to_fill).sendKeys(text)

    def scroll_down(self, pixels):
        self.driver.execute_script("window.scrollBy(0," + pixels + ")")

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments.scrollIntoView();", element)

    def execute_script(self, js_script):
        # Javascript script
        return self.driver.execute_script(js_script, self)

    def switch_to_iframe(self, iframe):
        self.driver.switch_to.frame(iframe)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_to_parent_frame(self):
        self.driver.switch_to.parent_frame()

    def accept_alert(self):
        try:
            self.wait.until(ec.alert_is_present()).accept()
            # self.driver.switch_to().alert().dismiss()  # freerangetester
        except Exception as err:
            print('No apareció la alerta', err)

    def accept_alert_with_text_input(self, text):
        try:
            alert = self.wait.until(ec.alert_is_present())
            alert.send_keys(text)
            alert.accept()
        except Exception as err:
            print('No apareció la alerta', err)

    def is_enabled(self, locator):
        return self.find(locator).is_enabled()

    def is_displayed(self, locator):
        return self.find(locator).is_displayed()

    def is_selected(self, locator):
        return self.find(locator).is_selected()

    def is_checked(self, locator):
        self.is_selected(locator)

    def go_to_link_text(self, link_text):
        # TODO POR QUÉ USA EL DRIVER DIRECTO??
        self.driver.find_element(By.LINK_TEXT(link_text)).click()

    def get_dropdown_item_count(self, locator):
        select = Select(self.find(locator))
        return len(select.options)

    def get_all_dropdown_elements(self, locator):
        # TODO POR QUÉ USA EL DRIVER DIRECTO??
        return self.driver.find_elements(By.CLASS_NAME(locator))  # List<WebElement>

    def get_all_dropdown_elements_list(self, locator):
        select = Select(self.find(locator))
        list_item = []
        for item in select.options:
            list_item.append(item.text)
        return list_item

    def get_dropdown_selected_item_list(self, locator):
        select = Select(self.find(locator))
        list_item = []
        for item in select.all_selected_options:
            list_item.append(item.text)
        return list_item

    def select_nth_element(self, locator, index):
        # TODO POR QUÉ USA EL DRIVER DIRECTO??
        results = self.driver.find_elements(By.XPATH(locator))  # List<WebElement>
        results[index].click()

    def wait_for_element(self, element):
        self.wait.until(ec.visibility_of_element_located(element))

    def hide_element(self, element):
        self.driver.execute_script("arguments.style.visibility='hidden'", element)

    @staticmethod
    def is_element_displayed(element):
        try:
            return element.is_displayed()
        except Exception as err:
            print("Exception:", err)
            return False

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def switch_to_window(self, window):
        self.driver.switch_to.window(window)

    def select_from_dropdown_by_value(self, locator, value_to_select):
        dropdown = Select(self.find(locator))
        dropdown.select_by_value(value_to_select)

    def select_from_dropdown_by_index(self, locator, value_to_select):
        dropdown = Select(self.find(locator))
        dropdown.select_by_index(value_to_select)

    def select_from_dropdown_by_text(self, locator, value_to_select):
        dropdown = Select(self.find(locator))
        dropdown.select_by_visible_text(value_to_select)

    def verify_item_in_dropdown(self, locator, text):
        select = Select(self.find(locator))
        for item in select.options:
            if text == item.text:
                return True
        return False

    def select_checkbox(self, checkbox):
        self.find(checkbox).click()

    def select_radio_button(self, radio_button):
        self.find(radio_button).click()

    def upload_file(self, locator, file_path):
        self.find(locator).send_keys(file_path)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def drag_and_drop(self, loc_source, loc_target):
        source_element = self.find(loc_source)
        target_element = self.find(loc_target)
        action_chains = ActionChains(self.driver)
        action_chains.drag_and_drop(source_element, target_element).perform()

    def hover_over_element(self, element):
        element_to_hover_over = self.find(element)
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(element_to_hover_over).perform()

    def wait_for_element_to_disappear(self, element):
        self.wait.until_not(ec.visibility_of_element_located(element))

    def wait_for_element_to_be_clickable(self, element):
        self.wait.until(ec.element_to_be_clickable(element))

    def get_title(self, title):
        return self.wait.until(ec.title_is(title))

    def get_attribute(self, attribute_name):
        return self.get_attribute(attribute_name)

    def set_attribute(self, attribute_name, value):
        return self.driver.execute_script("arguments[0].setAttribute(" + attribute_name + "," + value + ")")  # , self)

    def w3c(self):
        return self.w3c

    def invisibility_of_element_located(self, locator):
        # Wait till the element to be invisible
        return self.wait.until(ec.invisibility_of_element_located(locator))

    def visibility_of_element_located(self, locator):
        # Wait till the element to be visible
        return self.wait.until(ec.visibility_of(locator))


"""
Perplexity:
Apologies, it seems like the search results do not provide any additional methods that can be added to the `BasePage` 
class in Selenium. However, there are many other methods that can be added to the `BasePage` class depending on the 
specific needs of your web application. Some examples include:
handling dynamic pop-ups,
handling dynamic forms, 
handling dynamic dropdowns,
handling dynamic tables, 
and more.
The key is to identify the common elements and interactions across your web application and 
create methods in the `BasePage` class to handle them.
This will help to reduce code duplication and make your tests more maintainable.
"""