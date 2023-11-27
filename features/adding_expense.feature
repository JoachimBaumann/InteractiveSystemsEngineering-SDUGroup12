Feature: Adding a New Expense

  As a user of the MonBud web app
  I want to be able to add new expenses
  So that I can keep track of my spending accurately

  Scenario: Successfully Adding an Expense
    Given the user is on the “expenses” page
    When the user inputs all required expense details
    And clicks the "Submit" button
    Then the system adds the expense to the "Per category history" section under the chosen category
