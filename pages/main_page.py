from pages.base_page import BasePage
from pages.login_page import LoginPage
import logging
import time
from config.settings import TRADE_PASSWORD


class MainPage(BasePage):
    """
    执行业务用例前的一些检查、一些通用业务操作，例如，切换账户、输入交易密码
    """
    # 元素定位器
    LOGIN_TEXT = ("xpath", "//*[contains(@content-desc, '注册')]")
    NEW_STOCK_SUBSCRIPTION = ("xpath", "//*[@content-desc='今日可认购']")
    NOTIFICATION_REQUEST = ("xpath", "//*[contains(@text, '发送通知')]")
    CLOSE_BUTTON = ("xpath", "//*[@content-desc='今日可认购']/android.widget.ImageView[2]") #新股认购弹窗关闭按钮
    DENY_BUTTON = ("xpath", "//*[contains(@text, '不允许')]")
    MARKET_RECOVERY_POPUP = ("xpath", "//*[contains(@content-desc, '行情恢复')]")  # 行情恢复弹窗
    RECOVERY_BUTTON = ("xpath", "//*[contains(@content-desc, '恢复行情')]")  # 恢复行情按钮
    WATCHLIST_ELEMENT_HK = ("xpath", "//*[contains(@content-desc, 'HK')]")  # 自选列表HK元素
    WATCHLIST_ELEMENT_US = ("xpath", "//*[contains(@content-desc, 'US')]")  # 自选列表US元素
    BUY_INPUT = ("xpath", "//*[@content-desc='买入']")  # 下单页买入按钮
    SWITCH_ACCOUNT_BUTTON = ("xpath", "//*[contains(@content-desc,'账户')]")  # 切换账户按钮
    
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
        raise "等待主页面超时"
    
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
                raise f"关闭新股认购弹窗时发生错误: {e}"
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
                raise f"处理发送通知权限请求时发生错误: {e}"
        else:
            logging.info("未检测到发送通知权限请求弹窗")
            return False
            
    def handle_market_recovery_popup(self):
        """
        处理行情恢复弹窗
        检查是否有展示"行情恢复"的弹窗，如果有，则点击"恢复行情"按钮
        :return: bool 是否检测到并处理了弹窗
        """
        logging.info("检查是否有行情恢复弹窗")
        # 检查是否存在行情恢复弹窗
        if self.is_element_visible(self.MARKET_RECOVERY_POPUP):
            logging.info("检测到行情恢复弹窗，点击恢复行情按钮")
            # 尝试点击"恢复行情"按钮
            try:
                self.click_element(self.RECOVERY_BUTTON)
                logging.info("成功点击恢复行情按钮")
                return True
            except Exception as e:
                logging.error(f"处理行情恢复弹窗时发生错误: {e}")
                raise f"处理行情恢复弹窗时发生错误: {e}"
        else:
            logging.info("未检测到行情恢复弹窗")
            return False
            
    def wait_for_watchlist_visible(self, timeout=10):
        """
        等待自选列表展示出来
        检查自选列表是否有展示出来，如果有展示出来，才继续执行后面的代码
        :param timeout: 超时时间（秒）
        :return: bool 自选列表是否可见
        """
        logging.info("检查自选列表是否展示出来")
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 检查是否展示"HK"或"US"文案的元素
            if (self.is_element_visible(self.WATCHLIST_ELEMENT_HK) or 
                self.is_element_visible(self.WATCHLIST_ELEMENT_US)):
                logging.info("自选列表已展示出来（检测到HK或US元素）")
                return True
            time.sleep(1)
        logging.warning(f"等待自选列表展示超时，未能检测到HK或US元素")
        raise "自选列表加载超时"
        
    def handle_trade_password_input(self):
        """
        处理交易密码输入
        判断是否有展示交易密码的输入框，如果有展示，则输入交易密码，输入完成后继续执行后续的代码
        :return: bool 是否检测到并处理了交易密码输入框
        """
        logging.info("检查是否有交易密码输入框展示")
        if not self.is_element_visible(self.BUY_INPUT):  # 判断是否需要输入交易密码，如果需要则正常输入交易密码，如果不需要则继续输入
            time.sleep(1)
            logging.info("检测到交易密码输入框，开始输入交易密码")
            # 输入交易密码
            try:
                for num in TRADE_PASSWORD:
                    self.click_element(("xpath",f"//*[@content-desc='{num}']"))
                logging.info("交易密码输入完成")
                return True
            except Exception as e:
                logging.error(f"输入交易密码时发生错误: {e}")
                raise f"输入交易密码时发生错误: {e}"
        else:
            logging.info("未检测到交易密码输入框")
            return True

    def swich_account(self,account_type):
        """
        切换账户
        :return: bool 是否成功点击切换账户按钮
        """
        logging.info("开始切换账户操作")
        try:
            self.click_element(("xpath","//*[@content-desc='交易']"))
            self.wait_and_click_element(("xpath","//*[contains(@content-desc,'账户')]"))
            if account_type == "VA":
                self.wait_and_click_element(("xpath","//*[contains(@content-desc,'虚拟资产账户')]"))
                logging.info("切换到VA账户成功")
            else:
                self.wait_and_click_element(("xpath","//*[contains(@content-desc,'证券现金账户')]"))
                logging.info("切换到证券账户成功")
            self.click_element(("xpath","//*[@content-desc='胜利']"))
            return True
        except Exception as e:
            logging.error(f"切换账户时发生错误: {e}")
            raise f"切换账户时发生错误: {e}"