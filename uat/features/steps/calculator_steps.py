from __future__ import annotations

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "http://127.0.0.1:8000"


def _create_driver():
    """
    Create a headless Chrome driver suitable for Azure DevOps ubuntu-latest.
    """
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 720)
    return driver


@given("I open the calculator page")
def step_open_calculator(context):
    context.driver = _create_driver()
    context.driver.get(BASE_URL)
    time.sleep(1)


@when('I enter "{a}" and "{b}" into the number fields')
def step_enter_numbers(context, a, b):
    driver = context.driver
    first_input = driver.find_element(By.NAME, "a")
    second_input = driver.find_element(By.NAME, "b")
    first_input.clear()
    first_input.send_keys(a)
    second_input.clear()
    second_input.send_keys(b)


@when('I select the "{operation}" operation')
def step_select_operation(context, operation):
    driver = context.driver
    select = driver.find_element(By.NAME, "operation")
    driver.execute_script(
        "arguments[0].value = arguments[1];", select, operation
    )


@when("I click the calculate button")
def step_click_calculate(context):
    driver = context.driver
    button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()
    time.sleep(1)


@then('I should see the result "{expected}" on the page')
def step_see_result(context, expected):
    driver = context.driver
    result_elements = driver.find_elements(By.CLASS_NAME, "result")
    assert result_elements, "Result element not found on page"
    text = result_elements[0].text.strip()
    assert expected in text, f"Expected '{expected}' in '{text}'"

    driver.quit()
