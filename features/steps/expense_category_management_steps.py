from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


@given('the user is on the "Expenses" tab')
def step_user_on_expenses_tab(context):
    context.driver.get(context.base_url + "/expenses")


@given('the user is viewing the "{category}" category')
def step_user_viewing_category(context, category):
    select = Select(context.driver.find_element(By.ID, "filter-category-dropdown"))
    select.select_by_visible_text(category)


@when('the user selects "{category}" from the category dropdown')
def step_user_selects_category(context, category):
    select = Select(context.driver.find_element(By.ID, "filter-category-dropdown"))
    select.select_by_visible_text(category)


@then('the expenses list should show only "{category}" expenses')
def step_expenses_list_for_category(context, category):
    expected_row_count = 1
    try:
        WebDriverWait(context.driver, 10).until(
            lambda driver: len(
                [
                    row
                    for row in driver.find_elements(By.XPATH, "//tr/td[2]")
                    if category in row.text
                ]
            )
            >= expected_row_count
        )
    except TimeoutException:
        all_rows = context.driver.find_elements(By.XPATH, "//tr/td[2]")
        print(f"Debug: Rows found: {[row.text for row in all_rows]}")
        raise


@then("the expenses list should show all categories")
def step_expenses_list_shows_all_categories(context):
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr"))
    )
