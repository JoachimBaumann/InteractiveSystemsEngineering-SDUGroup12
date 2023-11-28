from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
    try:
        WebDriverWait(context.driver, 10).until(
            lambda driver: any(
                "utilities" in row.text
                for row in driver.find_elements(
                    By.XPATH, "//table[@id='expense-table']/tbody/tr"
                )
            )
        )
    except TimeoutException:
        all_rows = context.driver.find_elements(
            By.XPATH, "//table[@id='expense-table']/tbody/tr"
        )
        print(f"Debug: Rows found: {[row.text for row in all_rows]}")
        assert False, "Timeout waiting for the expenses table to update"
