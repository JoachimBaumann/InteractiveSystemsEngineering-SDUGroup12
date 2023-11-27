from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def before_all(context):
    chrome_options = Options()
    # Uncomment the next line to run Chrome in headless mode
    # chrome_options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=chrome_options)

    # Set the base URL for your application
    context.base_url = "http://127.0.0.1:5000"  # Replace with your application's URL

    # Optional: Set a default implicit wait time (e.g., 5 seconds)
    context.driver.implicitly_wait(5)


def after_all(context):
    try:
        context.driver.quit()
    except Exception as e:
        print(f"Error closing the WebDriver: {e}")
