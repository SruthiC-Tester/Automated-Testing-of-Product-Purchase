import pytest
from pytest_html import extras

def pytest_configure(config):
    config.option.log_cli = True
    config.option.log_file = ".venv/spreecommerce_test.log"
    config.option.log_file_level = "INFO"

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    # Hook to capture screenshot if test fails
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = getattr(item.instance, "driver", None)
        if driver:
            screenshot_name = f"{item.name}_failed.png"
            capture_screenshot(driver, screenshot_name)
            report.extras = getattr(report, "extras", [])
            report.extras.append(extras.image(screenshot_name))

def capture_screenshot(driver, name):
    print(f"Taking screenshot: {name}")
    try:
        driver.get_screenshot_as_file(name)
        print(f"Screenshot saved: {name}")
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")