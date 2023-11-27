from selenium import webdriver
from selenium.webdriver.common.by import By
from behave import given, when, then


@given("the user opens the MonBud web app")
def step_impl(context):
    context.browser = webdriver.Chrome()  # or another browser driver
    context.browser.get("http://localhost:5000")  # Replace with your app's URL


@when("they access the login page")
def step_impl(context):
    # Assuming the login page is the main page
    # If not, navigate to the login page URL
    pass


@then('the page is displayed with options to "Login with your preferred provider"')
def step_impl(context):
    provider_text = context.browser.find_element(By.TAG_NAME, "p").text
    assert "Login with your preferred provider" in provider_text


@then("options for Google and Github are visible")
def step_impl(context):
    buttons = context.browser.find_elements(By.TAG_NAME, "button")
    button_texts = [button.text for button in buttons]
    assert "Google" in button_texts
    assert "Github" in button_texts
