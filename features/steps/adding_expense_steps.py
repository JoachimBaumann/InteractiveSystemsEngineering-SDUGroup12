from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from behave import given, when, then
import time


@given("the user is on the “expenses” page")
def step_impl(context):
    context.browser = webdriver.Chrome()  # or another browser driver
    context.browser.get(
        "http://localhost:5000/expenses"
    )  # Replace with your app's expenses URL


@when("the user inputs all required expense details")
def step_impl(context):
    # Replace the below IDs with the actual IDs from your form
    context.browser.find_element(By.ID, "category-dropdown").send_keys("Transport")
    context.browser.find_element(By.ID, "name").send_keys("Uber")
    context.browser.find_element(By.ID, "amount").send_keys("15")
    context.browser.find_element(By.ID, "currency").send_keys("USD")
    context.browser.find_element(By.ID, "expenseDate").send_keys("2023-03-15")
    context.browser.find_element(
        By.ID, "no"
    ).click()  # Assuming "No" is selected for recurring


@when('clicks the "Submit" button')
def step_impl(context):
    submit_button = context.browser.find_element(By.XPATH, '//input[@value="Submit"]')
    submit_button.click()
    time.sleep(2)  # Wait for the form to submit and page to update


@then(
    'the system adds the expense to the "Per category history" section under the chosen category'
)
def step_impl(context):
    # This step would require checking the "Per category history" section for the new entry
    # Assuming the new entry would be the last row in the table
    rows = context.browser.find_elements(By.CSS_SELECTOR, "#expense-table tbody tr")
    last_row = rows[-1]
    assert (
        "Uber" in last_row.text and "15" in last_row.text and "dollar" in last_row.text
    )
