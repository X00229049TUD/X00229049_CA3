from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from behave import given

@given("the calculator UI is open")
def step_open_calculator(context):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    context.driver = webdriver.Chrome(options=options)
    context.driver.get("http://127.0.0.1:8000")