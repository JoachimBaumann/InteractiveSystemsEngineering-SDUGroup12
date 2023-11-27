Feature: Deleting an Expense
  As a user of the MonBud web app
  I want to be able to delete an expense
  So that I can remove incorrect or unwanted entries

  Scenario: Deleting an Expense from the "Transport" Category
    Given the user is on the "Expenses" page
    And there is an expense in the "Transport" category
    When the user notes the current number of expenses
    And the user clicks the "Delete" button next to the expense in the "Transport" category
    Then the expense should be removed from the list
    And the system should update the relevant data accordingly

