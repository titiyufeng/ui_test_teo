import uiautomator2 as u2
from config.settings import DEVICE_SERIAL


class DriverFactory:
    @staticmethod
    def get_driver():
        """
        获取uiautomator2驱动实例
        """
        if DEVICE_SERIAL:
            driver = u2.connect(DEVICE_SERIAL)
        else:
            driver = u2.connect()
        return driver
