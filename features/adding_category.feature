Feature: Adding a category
 Scenario: User can add a new category
  Given the user is on the "Categories" page
  When the user enters "NewCategory" in the category name field
  And the user enters "1000" in the budget field
  And the user clicks the "Save" button
  Then the system saves "NewCategory" with a budget of "1000"
  And "NewCategory" is displayed in the categories list
