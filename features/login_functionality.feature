Feature: Login Functionality

  As a user of MonBud web app
  I want to be able to log in using my preferred provider
  So that I can securely access my budgeting information

  Scenario: Displaying the Login Page with Provider Options
    Given the user opens the MonBud web app
    When they access the login page
    Then the page is displayed with options to "Login with your preferred provider"
    And options for Google and Github are visible
