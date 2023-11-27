from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


@given('the user is on the "Expenses" page')
def step_impl(context):
    context.driver.get(context.base_url + "/expenses")


@given('there is an expense in the "Transport" category')
def step_impl(context):
    try:
        context.driver.find_element(By.XPATH, "//tr[td[contains(text(), 'Transport')]]")
    except NoSuchElementException:
        assert False, "No expense found in the Transport category"


@when("the user notes the current number of expenses")
def step_impl(context):
    expenses = context.driver.find_elements(
        By.XPATH, "//table[@id='expense-table']/tbody/tr"
    )
    context.initial_expense_count = len(expenses)


@when(
    'the user clicks the "Delete" button next to the expense in the "Transport" category'
)
def step_impl(context):
    delete_button = context.driver.find_element(
        By.XPATH, "//tr[td[contains(text(), 'Transport')]]//button[@class='delete-btn']"
    )
    delete_button.click()


@then("the expense should be removed from the list")
def step_impl(context):
    WebDriverWait(context.driver, 10).until(
        lambda driver: len(
            driver.find_elements(By.XPATH, "//table[@id='expense-table']/tbody/tr")
        )
        < context.initial_expense_count
    )


@then("the system should update the relevant data accordingly")
def step_impl(context):
    updated_expenses = context.driver.find_elements(
        By.XPATH, "//table[@id='expense-table']/tbody/tr"
    )
    assert (
        len(updated_expenses) == context.initial_expense_count - 1
    ), "The expense count did not decrease as expected."
