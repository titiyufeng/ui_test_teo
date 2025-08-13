from pages.base_page import BasePage
from pages.login_page import LoginPage
import logging
import time


class MainPage(BasePage):
    """
    执行业务用例前的一些检查
    """
    # 元素定位器
    LOGIN_TEXT = ("xpath", "//*[contains(@content-desc, '注册')]")
    HOME_TITLE = ("xpath", "//android.widget.TextView[@text='首页']")
    NEW_STOCK_SUBSCRIPTION = ("xpath", "//*[@content-desc='今日可认购']")
    NOTIFICATION_REQUEST = ("xpath", "//*[contains(@text, '发送通知')]")
    CLOSE_BUTTON = ("xpath", "//*[@content-desc='今日可认购']/android.widget.ImageView[2]") #新股认购弹窗关闭按钮
    DENY_BUTTON = ("xpath", "//*[contains(@text, '不允许')]")
    
    def is_logged_in(self):
        """
        检查是否已登录
        如果页面包含包含"登录"文案的元素，则说明未登录
        """
        login_element = self.find_element(self.LOGIN_TEXT)
        return not login_element.exists  # 如果找不到包含"登录"的元素，说明已登录
    
    def is_login_page(self):
        """
        检查当前是否在登录页面
        通过检查是否存在包含"登录"文案的元素来判断
        """
        login_element = self.find_element(self.LOGIN_TEXT)
        return login_element.exists
    
    def wait_for_main_page(self, timeout=10):
        """
        等待主页面加载完成
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.is_login_page():
                logging.info("已进入主页面")
                return True
            time.sleep(1)
        logging.warning("等待主页面超时")
        return False
    
    def perform_login_if_needed(self, username, password):
        """
        如果需要登录则执行登录操作
        """
        if self.is_login_page() or not self.is_logged_in():
            logging.info("检测到未登录状态，开始执行登录流程")
            login_page = LoginPage(self.driver)
            login_page.login(username, password)
            # 等待登录完成并跳转到主页面
            self.wait_for_main_page()
            logging.info("登录流程完成")
            return True
        else:
            logging.info("已登录状态，无需执行登录流程")
            return False
            
    def handle_new_stock_subscription_popup(self):
        """
        处理新股认购弹窗
        检查是否有展示"新股认购"的弹窗，如果有，则点击关闭按钮
        :return: bool 是否检测到并关闭了弹窗
        """
        logging.info("检查是否有新股认购弹窗")
        # 检查是否存在新股认购弹窗
        if self.is_element_visible(self.NEW_STOCK_SUBSCRIPTION):
            logging.info("检测到新股认购弹窗，尝试关闭")
            # 尝试点击关闭按钮
            try:
                self.click_element(self.CLOSE_BUTTON)
                logging.info("成功关闭新股认购弹窗")
                return True
            except Exception as e:
                logging.error(f"关闭新股认购弹窗时发生错误: {e}")
                return False
        else:
            logging.info("未检测到新股认购弹窗")
            return False
                
    def handle_notification_request_popup(self):
        """
        处理发送通知权限请求弹窗
        检查是否有展示"发送通知"的弹窗，如果有，则点击"不允许"按钮
        :return: bool 是否检测到并处理了弹窗
        """
        logging.info("检查是否有发送通知权限请求弹窗")
        # 检查是否存在发送通知弹窗
        if self.is_element_visible(self.NOTIFICATION_REQUEST):
            logging.info("检测到发送通知权限请求弹窗，点击不允许按钮")
            # 尝试点击"不允许"按钮
            try:
                self.click_element(self.DENY_BUTTON)
                logging.info("成功点击不允许按钮，关闭通知权限请求")
                return True
            except Exception as e:
                logging.error(f"处理发送通知权限请求时发生错误: {e}")
                return False
        else:
            logging.info("未检测到发送通知权限请求弹窗")
            return False