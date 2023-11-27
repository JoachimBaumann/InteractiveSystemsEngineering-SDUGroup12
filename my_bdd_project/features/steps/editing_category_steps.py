from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


# Define a function to set up the WebDriver before all tests
def before_all(context):
    context.driver = webdriver.Chrome()
    context.driver.get(
        "http://127.0.0.1:5000/"
    )  # Replace with your local development server URL


# Define a function to clean up after all tests
def after_all(context):
    context.driver.quit()


@given('the user navigates to the "Categories" section')
def step_given_navigate_to_categories(context):
    # Already done in 'before_all'
    pass


@given("sees a list of their saved categories")
def step_when_sees_saved_categories(context):
    # Verify that the table of saved categories is displayed
    table = context.driver.find_element(By.CLASS_NAME, "table")
    assert table.is_displayed()


@when('the user double-clicks on the "1000.0 kr" field for the "Food" category')
def step_when_double_click_food_category(context):
    # Locate and double-click the budget amount field for the "Food" category
    cell = context.driver.find_element(
        By.XPATH,
        "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
    )
    cell.click()
    cell.click()  # Double-click


@then('the "Delete" button next to the "Food" category changes to "Update"')
def step_then_delete_button_changes_to_update(context):
    # Verify that the "Delete" button for the "Food" category changes to "Update"
    update_button = context.driver.find_element(
        By.XPATH,
        "//tr[td[contains(text(), 'Food')]]/td/button[contains(text(), 'Update')]",
    )
    assert update_button.is_displayed()


@when('the user edits the budget amount and clicks on the "Update" button')
def step_when_edit_budget_and_click_update(context):
    # Edit the budget amount and click the "Update" button
    cell = context.driver.find_element(
        By.XPATH,
        "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
    )
    cell.clear()
    cell.send_keys("1500.0")

    # Click the "Update" button
    update_button = context.driver.find_element(
        By.XPATH,
        "//tr[td[contains(text(), 'Food')]]/td/button[contains(text(), 'Update')]",
    )
    update_button.click()


@then('the system updates the budget for the "Food" category and confirms the change')
def step_then_system_updates_budget_and_confirms_change(context):
    # Verify that the system updates the budget for the "Food" category
    updated_budget = context.driver.find_element(
        By.XPATH,
        "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
    )
    assert (
        updated_budget.text == "1500.0"
    )  # Check if the budget is updated to the expected value

    # Confirm the change (you may need to check for a confirmation message)


# You should also consider adding appropriate error handling and waiting for elements to load as needed.
