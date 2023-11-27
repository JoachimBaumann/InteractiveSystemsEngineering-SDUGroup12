Feature: Login with Preferred Provider

  As a user of the MonBud web app
  I want to be able to log in using my Google account
  So that I can securely and conveniently access my budgeting information

  Scenario: Logging in with Google
    Given the user is on the MonBud login page
    When they click on the "Google" button
    Then the system redirects the user to the Google login page

    Given the user is on the Google login page
    When the user enters their Google credentials and authorizes the MonBud app
    Then the system logs the user into the MonBud web app
    And takes them to the main dashboard or the first-time user setup page