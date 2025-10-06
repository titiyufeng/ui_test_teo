# /Users/vic/teo/code/ui_test/tests/test_va_trade.py
import logging
import time
from config.settings import VA_CODE,US_STOCK_CODE,HK_STOCK_CODE
class TestVaTrade:
    """虚拟货币交易功能测试"""
    def test_va_trade_limit_buy(self, main_page):
        """提交买入限价单，并撤单"""
        logging.info("开始执行买入限价单测试")
        try:
            main_page.swich_account("VA")
            main_page.driver(className="android.widget.ImageView")[0].click()#点击顶部搜索框
            main_page.input_text(("xpath", "//android.widget.EditText"), VA_CODE)#输入搜索内容
            main_page.wait_and_click_element(("xpath", f"//*[@content-desc='{VA_CODE}\nHK\nHashKey']"))#等待搜索结果出现后，并点击
            main_page.wait_for_element_visible(("xpath", "//*[contains(@content-desc,'报价')]"))  # 等待进入个股页后
            main_page.click_element(("xpath", "//*[@content-desc='交易']"))
            time.sleep(0.5)
            main_page.handle_trade_password_input()#输入交易密码
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='最新价']"))
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='买入']"))
            time.sleep(2)
            #获取最新价
            elm_new_price = main_page.find_element(("xpath", "//*[@content-desc='最新价']/following-sibling::*[1]"))
            new_price = float(elm_new_price.info["contentDescription"].split(" ")[0])
            logging.info(f"获取到最新价: {new_price}")

            #计算买入价格
            price  = str(int(new_price*0.8))
            logging.info(f"计算买入价格: {price}")

            #展开价格输入的数字键盘，清除原价格，输入新价格
            main_page.click_element(("xpath", "//android.widget.EditText[@index='10']"))
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='完成']"))
            time.sleep(1)
            #清除原价格
            for i in range(9):
                main_page.click_element(("xpath", "//*[@content-desc='3']/following-sibling::*[1]"))
            # 输入价格
            for num in price:
                main_page.click_element(("xpath",f"//android.widget.Button[@content-desc='{num}']"))
            time.sleep(1)

            #展示数量输入的数字键盘，并输入数量
            main_page.click_element(("xpath", "//*[@content-desc='价格最小单位: 0.01']/following-sibling::*[1]"))
            time.sleep(1)
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='完成']"))
            for key in "0.005":
                main_page.click_element(("xpath", f"//android.widget.Button[@content-desc='{key}']"))
            main_page.click_element(("xpath", "//*[@content-desc='完成']"))

            #提交订单
            main_page.click_element(("xpath", "//*[@content-desc='买入ETH']"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='确认']"))
            time.sleep(1.5)
            logging.info("提交订单成功")

            #撤单
            main_page.click_element(("xpath", "//*[contains(@content-desc,'今日订单')]"))
            time.sleep(1)
            main_page.click_element(("xpath", "//*[contains(@content-desc,'状态')]/following-sibling::*[1]"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='撤单']"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='确认']"))
            time.sleep(3)
            description = main_page.get_description(("xpath", "//*[contains(@content-desc,'HK')]"))
            assert "已撤销" in description, "撤单失败"
            logging.info("撤单成功")

        except Exception as e:
            logging.error(f"买入限价单测试执行失败: {str(e)}", exc_info=True)
            raise

    def test_va_trade_limit_sell(self, main_page):
        """提交卖出限价单，并撤单"""
        logging.info("开始执行卖出限价单测试")
        try:
            main_page.swich_account("VA")
            main_page.driver(className="android.widget.ImageView")[0].click()  # 点击顶部搜索框
            main_page.input_text(("xpath", "//android.widget.EditText"), VA_CODE)  # 输入搜索内容
            main_page.wait_and_click_element(("xpath", f"//*[@content-desc='{VA_CODE}\nHK\nHashKey']"))  # 等待搜索结果出现后，并点击
            main_page.wait_for_element_visible(("xpath", "//*[contains(@content-desc,'报价')]"))  # 等待进入个股页后
            main_page.click_element(("xpath", "//*[@content-desc='交易']"))
            time.sleep(0.5)
            main_page.handle_trade_password_input()  # 输入交易密码
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='最新价']"))
            time.sleep(2)
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='卖出']"))
            # 获取最新价
            elm_new_price = main_page.find_element(("xpath", "//*[@content-desc='最新价']/following-sibling::*[1]"))
            new_price = float(elm_new_price.info["contentDescription"].split(" ")[0])
            logging.info(f"获取到最新价: {new_price}")

            # 计算卖出价格
            price = str(int(new_price * 1.5))
            logging.info(f"计算卖出价格: {price}")

            # 展开价格输入的数字键盘，清除原价格，输入新价格
            main_page.click_element(("xpath", "//android.widget.EditText[@index='10']"))
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='完成']"))
            time.sleep(1)
            # 清除原价格
            for i in range(9):
                main_page.click_element(("xpath", "//*[@content-desc='3']/following-sibling::*[1]"))
            # 输入价格
            for num in price:
                main_page.click_element(("xpath", f"//android.widget.Button[@content-desc='{num}']"))
            time.sleep(1)

            # 展示数量输入的数字键盘，并输入数量
            main_page.click_element(("xpath", "//*[@content-desc='价格最小单位: 0.01']/following-sibling::*[1]"))
            time.sleep(1)
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='完成']"))
            for key in "0.005":
                main_page.click_element(("xpath", f"//android.widget.Button[@content-desc='{key}']"))
            main_page.click_element(("xpath", "//*[@content-desc='完成']"))

            # 提交订单
            main_page.click_element(("xpath", "//*[@content-desc='卖出ETH']"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='确认']"))
            time.sleep(1.5)
            logging.info("提交订单成功")

            # 撤单
            main_page.click_element(("xpath", "//*[contains(@content-desc,'今日订单')]"))
            time.sleep(1)
            main_page.click_element(("xpath", "//*[contains(@content-desc,'状态')]/following-sibling::*[1]"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='撤单']"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='确认']"))
            time.sleep(3)
            description = main_page.get_description(("xpath", "//*[contains(@content-desc,'HK')]"))
            assert "已撤销" in description, "撤单失败"
            logging.info("撤单成功")

        except Exception as e:
            logging.error(f"卖出限价单测试执行失败: {str(e)}", exc_info=True)
            raise
