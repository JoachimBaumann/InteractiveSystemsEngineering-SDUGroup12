Feature: Editing a Category
  Scenario: User can edit a category
    Given the user navigates to the "Categories" section 
    When the user double-clicks on the "1000.0 kr" field for the "Food" category
    Then the "Delete" button next to the "Food" category changes to "Update"
    When the user edits the budget amount and clicks on the "Update" button
    Then the system updates the budget for the "Food" category and confirms the change.

