from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app import app, db
from app.models import Category


@given('the user is on the "Categories" page')
def step_user_on_categories_page(context):
    context.driver.get(context.base_url + "/categories")
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".table"))
    )


@when('the user enters "{category_name}" in the category name field')
def step_user_enters_category_name(context, category_name):
    name_field = context.driver.find_element(By.ID, "name")
    name_field.send_keys(category_name)


@when('the user enters "{budget}" in the budget field')
def step_user_enters_budget(context, budget):
    budget_field = context.driver.find_element(By.ID, "budget")
    budget_field.send_keys(budget)


@when('the user clicks the "Save" button')
def step_user_clicks_save(context):
    save_button = context.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    save_button.click()


@then('the system saves "{category_name}" with a budget of "{budget}"')
def step_system_saves_category(context, category_name, budget):
    with app.app_context():
        # Query the database for the category
        category = Category.query.filter_by(name=category_name, budget=budget).first()

        # Assert that the category was found
        assert (
            category is not None
        ), f"Category {category_name} with budget {budget} not found in the database"


@then('"{category_name}" is displayed in the categories list')
def step_category_displayed_in_list(context, category_name):
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//td[contains(text(), '{category_name}')]")
        )
    )


@then('a confirmation message "{message}" is displayed')
def step_confirmation_message_displayed(context, message):
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[contains(text(), '{message}')]")
        )
    )
