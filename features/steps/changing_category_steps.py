from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given("the user is on the overview page")
def step_impl(context):
    context.driver.get(context.base_url + "/overview")
    assert WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "category-dropdown"))
    ), "Category dropdown not found on the overview page."


@when('the user selects "{category}" from the "Category" dropdown menu')
def step_impl(context, category):
    dropdown = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "category-dropdown"))
    )
    # Use the `find_elements` method to get all options in the dropdown
    options = dropdown.find_elements(By.TAG_NAME, "option")
    for option in options:
        if option.text == category:
            option.click()
            break


@then('the system updates the overview to show data for the "{category}" category')
def step_impl(context, category):
    # Wait for the budget value to update
    WebDriverWait(context.driver, 10).until(
        lambda driver: driver.find_element(By.ID, "budget").text != "--"
    )

    # Check the budget, expenses, and remainder values
    budget_text = context.driver.find_element(By.ID, "budget").text
    expenses_text = context.driver.find_element(By.ID, "expenses").text
    remainder_text = context.driver.find_element(By.ID, "remainder").text

    # Assuming you have a way to know what the expected values should be, perhaps from a fixture or a database
    expected_budget = "1000kr"
    expected_expenses = "204kr"
    expected_remainder = "796kr"

    assert (
        expected_budget in budget_text
    ), f"Budget does not match expected value. Expected {expected_budget}, got {budget_text}"
    assert (
        expected_expenses in expenses_text
    ), f"Expenses do not match expected value. Expected {expected_expenses}, got {expenses_text}"
    assert (
        expected_remainder in remainder_text
    ), f"Remainder does not match expected value. Expected {expected_remainder}, got {remainder_text}"
