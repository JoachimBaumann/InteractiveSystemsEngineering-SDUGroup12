from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


@given('the user navigates to the "Categories" section')
def step_given_navigate_to_categories(context):
    # Assuming the driver and the base URL are set up in the environment.py
    context.driver.get(context.base_url + "/categories")


# @when("the user sees a list of their saved categories")
# def step_when_sees_saved_categories(context):
#    WebDriverWait(context.driver, 10).until(
#        EC.visibility_of_element_located((By.CSS_SELECTOR, ".table tbody tr"))
#   )


@when('the user double-clicks on the "1000.0 kr" field for the "Food" category')
def step_when_double_click_food_category(context):
    # This depends on the exact structure of your table and how the double-click is handled
    food_category_row = context.driver.find_element(
        By.XPATH, "//td[contains(text(), 'Food')]/.."
    )
    budget_field = food_category_row.find_element(
        By.XPATH, ".//td[@data-field='budget']"
    )
    ActionChains(context.driver).double_click(budget_field).perform()


@then('the "Delete" button next to the "Food" category changes to "Update"')
def step_then_delete_button_changes_to_update(context):
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "//tr[td[contains(text(), 'Food')]]/td/button"), "Update"
        )
    )
    update_button = context.driver.find_element(
        By.XPATH,
        "//tr[td[contains(text(), 'Food')]]/td/button[contains(text(), 'Update')]",
    )
    assert update_button.is_displayed()


@when('the user edits the budget amount and clicks on the "Update" button')
def step_when_edit_budget_and_click_update(context):
    food_category_row = context.driver.find_element(
        By.XPATH, "//td[contains(text(), 'Food')]/.."
    )
    budget_field = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
            )
        )
    )
    budget_field.clear()
    budget_field.send_keys("1500.0")

    update_button = food_category_row.find_element(
        By.XPATH, ".//button[contains(text(), 'Update')]"
    )
    update_button.click()


@then('the system updates the budget for the "Food" category and confirms the change')
def step_then_system_updates_budget_and_confirms_change(context):
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element(
            (
                By.XPATH,
                "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
            ),
            "1500.0",
        )
    )
    updated_budget_field = context.driver.find_element(
        By.XPATH,
        "//td[contains(text(), 'Food')]/following-sibling::td[@data-field='budget']",
    )
    assert updated_budget_field.text == "1500.0", "Budget not updated as expected."
