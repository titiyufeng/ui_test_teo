from pages.base_page import BasePage
import time
import logging


class LoginPage(BasePage):
    def login(self, username, password):
        """登录流程"""
        try:
            self.input_text(("xpath", "//android.widget.EditText"), username) ##输入手机号
            self.click_element(("xpath", "//*[contains(@content-desc, '注册')]"))  # 点击登录/注册按钮
            time.sleep(2)
            self.input_text(("xpath", "//android.widget.EditText"), "12312")  ##输入验证码
            self.click_element(("xpath", "//*[contains(@content-desc, '下一步')]"))  # 点击下一步按钮
            time.sleep(2)
            self.input_text(("xpath", "//android.widget.EditText"), password)  ##输入手机号
            self.click_element(("xpath", "//*[@content-desc='登录']"))  # 点击登录按钮
        except Exception as e:
            logging.info(f"登录失败")
            raise "登录失败"
        
        # 等待登录过程完成
        time.sleep(3)