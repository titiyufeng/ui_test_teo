# Android 自动化测试框架

基于 pytest 和 uiautomator2 的 Android 自动化测试框架

## 项目结构

```
android_automation/
├── conftest.py                 # pytest配置和fixture
├── pytest.ini                  # pytest配置文件
├── requirements.txt            # 依赖包列表
├── config/                     # 配置文件目录
│   ├── __init__.py
│   └── settings.py            # 配置文件
├── pages/                      # 页面对象目录
│   ├── __init__.py
│   ├── base_page.py            # 基础页面类
│   ├── login_page.py           # 登录页面类
│   └── main_page.py            # 主页面类
├── tests/                      # 测试用例目录
├── utils/                      # 工具类目录
├── reports/                    # 测试报告目录
│   ├── report.html             # HTML测试报告
│   └── screenshots/            # 失败测试截图
└── run_tests.py                # 运行测试脚本
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

### 方法一：使用 pytest 命令直接运行

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_login.py

# 运行特定测试类
pytest tests/test_login.py::TestLogin

# 运行特定测试方法
pytest tests/test_login.py::TestLogin::test_login_success
```

### 方法二：使用运行脚本

```bash
# 运行所有测试并生成报告
python run_tests.py
```

## 自动登录机制

框架内置了自动登录检查机制：
1. 测试开始前自动检查登录状态
2. 如果检测到未登录（页面包含"登录"文案），则自动执行登录流程
3. 如果已登录，则直接进入测试
4. 登录凭据在 `config/settings.py` 中配置

## 测试报告

每次运行测试后，会自动生成 HTML 格式的测试报告，保存在 `reports/report.html` 文件中。

## 失败自动截图

当测试断言失败时，系统会自动截取当前设备屏幕并保存到 `reports/screenshots/` 目录中，文件名格式为 `{test_name}_{timestamp}.png`。

## 日志记录

测试运行期间的日志会输出到控制台，并保存在 `pytest_log/pytest.log` 文件中。