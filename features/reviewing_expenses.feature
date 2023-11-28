Feature: Reviewing Expenses of a Category

  As a user of the MonBud web app
  I want to be able to review expenses of a specific category
  So that I can better understand my spending in that category

  Scenario: Displaying Expenses of a Selected Category
    Given the user is on the "Expenses" tab
    When the user selects the "utilities" category from the "Per category history" dropdown
    Then the system displays the list of expenses under this category
