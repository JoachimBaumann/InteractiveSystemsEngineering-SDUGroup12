from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from behave import given, when, then
import time


@given("the user is on the MonBud login page")
def step_impl(context):
    context.browser = webdriver.Chrome()  # or another browser driver
    context.browser.get("http://localhost:5000")  # Replace with your app's login URL


@when('they click on the "Google" button')
def step_impl(context):
    google_button = context.browser.find_element(By.XPATH, '//button[text()="Google"]')
    google_button.click()


@then("the system redirects the user to the Google login page")
def step_impl(context):
    # This is a complex step as it involves interacting with Google's login page
    # which is protected against automated scripts.
    # For demonstration, we'll just wait and assume redirection.
    time.sleep(1)  # Wait for redirection, this is not reliable for real tests


@given("the user is on the Google login page")
def step_impl(context):
    # This step would require you to be on the Google login page
    # Automating Google login is against Google's policy and is technically challenging
    pass


@when("the user enters their Google credentials and authorizes the MonBud app")
def step_impl(context):
    # Automating this step is not recommended and might not be feasible
    pass


@then("the system logs the user into the MonBud web app")
def step_impl(context):
    # Check if login was successful by looking for elements only present after login
    pass


@then("takes them to the main dashboard or the first-time user setup page")
def step_impl(context):
    # Check for elements specific to the dashboard or setup page
    pass
