import pytest
from utils.driver_factory import DriverFactory
from config.settings import APP_PACKAGE, TEST_USERNAME, TEST_PASSWORD
from pages.base_page import BasePage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from utils.feishu_notifier import FeishuNotifier
import os
import time
import logging


# 存储测试结果的全局变量
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "failed_details": []
}


@pytest.fixture(scope="session")
def driver():
    """
    初始化driver的fixture
    """
    driver_instance = DriverFactory.get_driver()
    # 启动应用
    driver_instance.app_start(APP_PACKAGE)
    time.sleep(3)
    yield driver_instance
    # 测试结束后停止应用
    driver_instance.app_stop(APP_PACKAGE)


@pytest.fixture
def base_page(driver):
    """
    提供 BasePage 实例的 fixture
    内部包含driver实例，可直接调用BasePage的方法
    """
    return BasePage(driver)


@pytest.fixture
def main_page(driver):
    """
    提供 MainPage 实例的 fixture
    包含登录状态检查和自动登录功能
    """
    main_page = MainPage(driver)
    
    # 检查登录状态并自动登录（如果需要）
    main_page.perform_login_if_needed(TEST_USERNAME, TEST_PASSWORD)
    # 检查是否有展示发送通知的弹窗，如果有则点击“不允许”
    main_page.handle_notification_request_popup()
    # 检查自选列表是否有完成展示
    main_page.wait_for_watchlist_visible()
    time.sleep(3)
    # 检查是否有展示新股认购弹窗，如果有则关闭新股认购弹窗
    main_page.handle_new_stock_subscription_popup()
    # 检查是否有展示行情恢复弹窗，如果有则点击恢复行情的按钮
    main_page.handle_market_recovery_popup()
    return main_page


@pytest.fixture(autouse=True)
def setup_teardown(driver):
    """
    每个测试用例前后的设置和清理
    """
    # 测试前可以添加前置操作
    driver.app_start(APP_PACKAGE)
    yield
    # 测试后可以添加清理操作
    driver.app_stop(APP_PACKAGE)


def pytest_runtest_makereport(item, call):
    """
    当测试失败时自动截图
    """
    if call.when == "call" and call.excinfo is not None:
        # 获取当前测试的driver实例
        driver_fixture = item.funcargs.get('driver')
        base_page_fixture = item.funcargs.get('base_page')
        main_page_fixture = item.funcargs.get('main_page')
        
        # 优先使用base_page中的driver，否则使用直接传入的driver
        driver = None
        if main_page_fixture is not None:
            driver = main_page_fixture.driver
        elif base_page_fixture is not None:
            driver = base_page_fixture.driver
        elif driver_fixture is not None:
            driver = driver_fixture
            
        if driver is not None:
            # 创建截图保存目录
            screenshot_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # 生成包含测试类名和方法名的截图文件名
            node_parts = item.nodeid.split("::")
            if len(node_parts) >= 3:
                # 格式为: tests/test_file.py::TestClass::test_method
                test_class = node_parts[-2]
                test_method = node_parts[-1]
                screenshot_name = f"{test_class}_{test_method}"
            elif len(node_parts) == 2:
                # 格式为: tests/test_file.py::test_function
                test_class = "function"
                test_method = node_parts[-1]
                screenshot_name = f"{test_class}_{test_method}"
            else:
                # 其他情况使用默认名称
                screenshot_name = item.name
                
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"{screenshot_name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
            
            # 截图并保存
            try:
                driver.screenshot(screenshot_path)
                print(f"\n测试失败截图已保存到: {screenshot_path}")
            except Exception as e:
                print(f"\n截图保存失败: {e}")


def pytest_runtest_logreport(report):
    """
    收集测试结果信息
    """
    if report.when == "call":
        test_results["total"] += 1
        if report.passed:
            test_results["passed"] += 1
        elif report.failed:
            test_results["failed"] += 1
            # 记录失败用例的详细信息
            test_results["failed_details"].append(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束后发送测试结果到飞书群
    """
    # 飞书机器人的webhook地址
    webhook_url = "https://open.larksuite.com/open-apis/bot/v2/hook/99cc5ce3-53bf-4970-a356-8b2ccb49b505"
    
    # 创建飞书通知器实例
    notifier = FeishuNotifier(webhook_url)
    
    # 发送测试结果
    success = notifier.send_test_result(
        total_cases=test_results["total"],
        passed_cases=test_results["passed"],
        failed_cases=test_results["failed"],
        failed_case_details=test_results["failed_details"]
    )
    
    if success:
        print("\n测试结果已成功发送到飞书群")
    else:
        print("\n发送测试结果到飞书群失败")