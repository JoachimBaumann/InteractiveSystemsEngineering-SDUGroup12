from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@given('the user is on the "Expenses" tab')
def step_impl(context):
    # Navigate to the expenses page
    context.driver.get(context.base_url + "/expenses")


@when(
    'the user selects the "utilities" category from the "Per category history" dropdown'
)
def step_impl(context):
    # Wait for the dropdown to be clickable
    dropdown = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "filter-category-dropdown"))
    )
    dropdown.click()

    # Find the "utilities" option
    try:
        utilities_option = WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//select[@id='filter-category-dropdown']/option[normalize-space()='utilities']",
                )
            )
        )
        utilities_option.click()
    except TimeoutException:
        assert False, "Utilities option not found in the dropdown"


@then("the system displays the list of expenses under this category")
def step_impl(context):
    # Wait for the table to update with the filtered results
    try:
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//table[@id='expense-table']/tbody/tr[contains(@data-category-id, 'utilities')]",
                )
            )
        )
    except TimeoutException:
        assert False, "Timeout waiting for the expenses table to update"

    # Additional checks can be added here if needed
