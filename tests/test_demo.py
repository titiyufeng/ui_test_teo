# /Users/vic/teo/code/ui_test/tests/test_va_trade.py
import logging
import time


class TestDemo:
    def test_demo1(self, main_page):
        try:
            main_page.wait_and_click_element(("xpath","//*[contains(@content-desc,'HashKey')]"))
            time.sleep(2)
            assert main_page.is_element_visible(("xpath","//*[contains(@content-desc,'报价')]"))
        except Exception as e:
            logging.error(f"执行失败：{str(e)}", exc_info=True)
            raise

    def test_demo2(self, main_page):
        try:
            main_page.wait_and_click_element(("xpath","//*[contains(@content-desc,'HashKey')]"))
            time.sleep(2)
            assert main_page.is_element_visible(("xpath","//*[contains(@content-desc,'报价2')]"))
        except Exception as e:
            logging.error(f"执行失败：{str(e)}", exc_info=True)
            raise