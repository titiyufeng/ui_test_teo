# /Users/vic/teo/code/ui_test/tests/test_va_trade.py
import logging
import time


class TestVaTrade:
    """虚拟货币交易功能测试"""
    def test_va_trade_limit_buy(self, main_page):
        """提交买入限价单，并撤单"""
        logging.info("开始执行买入限价单测试")
        try:
            main_page.click_element(("xpath", "//*[contains(@content-desc,'股票代码')]"))#点击顶部搜索框
            main_page.input_text(("xpath", "//android.widget.EditText"), "ETH/USD")#输入搜索内容
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='ETH/USD\nHK\nHashKey']"))#等待搜索结果出现后，并点击
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='交易']"))#等待进入个股页后，并点击交易按钮
            if main_page.wait_for_element_visible(("xpath", "//*[@content-desc='完成']")):#判断是否需要输入交易密码，如果需要则正常输入交易密码，如果不需要则继续输入
                #输入交易密码
                time.sleep(1)
                main_page.click_element(("xpath", "//*[@content-desc='1']"))
                main_page.click_element(("xpath", "//*[@content-desc='1']"))
                main_page.click_element(("xpath", "//*[@content-desc='3']"))
                main_page.click_element(("xpath", "//*[@content-desc='5']"))
                main_page.click_element(("xpath", "//*[@content-desc='4']"))
                main_page.click_element(("xpath", "//*[@content-desc='0']"))
            main_page.wait_for_element_visible(("xpath", "//*[@content-desc='买入']"))
            time.sleep(3)
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
            time.sleep(1)
            logging.info("提交订单成功")

            #撤单
            main_page.click_element(("xpath", "//*[contains(@content-desc,'今日订单')]"))
            main_page.click_element(("xpath", "//*[contains(@content-desc,'状态')]/following-sibling::*[1]"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='撤单']"))
            main_page.wait_and_click_element(("xpath", "//*[@content-desc='确认']"))
            logging.info("撤单成功")


        except Exception as e:
            logging.error(f"买入限价单测试执行失败: {str(e)}", exc_info=True)
            raise

    def test_va_trade_limit_sell(self, main_page):
        """提交买出限价单，并撤单"""
        pass
