from utils.driver_factory import DriverFactory
from config.settings import IMPLICIT_WAIT
import logging
from typing import Optional, Any
import uiautomator2 as u2
import time


class BasePage:
    def __init__(self, driver: Optional[u2.Device] = None):
        self.driver: u2.Device = driver or DriverFactory.get_driver()
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    def find_element(self, locator):
        """
        查找元素
        :param locator: 元素定位器，格式为 (by, value) 如: ("xpath", "//android.widget.TextView[@text='交易']")
        :return: UI element
        """
        logging.info(f"查找元素: {locator}")
        by, value = locator
        if by == "xpath":
            return self.driver.xpath(value)
        elif by == "id":
            return self.driver(resourceId=value)
        elif by == "text":
            return self.driver(text=value)
        elif by == "className":
            return self.driver(className=value)
        else:
            # 默认使用 resourceId 查找
            return self.driver(resourceId=value)

    def click_element(self, locator):
        """
        点击元素
        :param locator: 元素定位器
        """
        self.find_element(locator).click()

    def input_text(self, locator, text):
        """
        输入文本
        :param locator: 元素定位器
        :param text: 输入文本
        """
        self.find_element(locator).set_text(text)

    def get_text(self, locator):
        """
        获取元素文本
        :param locator: 元素定位器
        :return: 元素文本
        """
        return self.find_element(locator).info['text']

    def get_description(self, locator):
        """
        获取元素文本
        :param locator: 元素定位器
        :return: 元素文本
        """
        return self.find_element(locator).info['contentDescription']
    def is_element_visible(self, locator):
        """
        判断元素是否可见
        :param locator: 元素定位器
        :return: bool
        """
        return self.find_element(locator).exists

    def wait_for_element_visible(self, locator, timeout=15):
        """
        等待元素可见
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        :return: bool 元素是否可见
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_element_visible(locator):
                logging.info(f"检测到元素 {locator}，继续执行后续操作")
                return True
            time.sleep(1)
        logging.warning(f"等待元素 {locator} 可见超时，未能执行点击操作")
        raise f"等待元素 {locator} 可见超时，未能执行点击操作"

    def wait_and_click_element(self, locator, timeout=15):
        """
        等待元素可见后执行点击操作
        :param locator: 元素定位器
        :param timeout: 超时时间（秒）
        :return: bool 点击是否成功
        """
        if self.wait_for_element_visible(locator, timeout):
            self.click_element(locator)
            logging.info(f"成功点击元素 {locator}")
            return True
        else:
            logging.warning(f"等待元素 {locator} 可见超时，未能执行点击操作")
            raise f"等待元素 {locator} 可见超时，未能执行点击操作"