Feature: Expense Category Management
  As a user of the MonBud web app
  I want to easily switch between different expense categories
  So that I can efficiently manage and review my expenses categorized by type

  Scenario: Viewing Utilities Expenses
    Given the user is on the "Expenses" tab
    And the user is viewing the "utilities" category
    When the user selects "Transport" from the category dropdown
    Then the expenses list should show only "Transport" expenses

  Scenario: Viewing Food Expenses
    Given the user is on the "Expenses" tab
    And the user is viewing the "Food" category
    When the user selects "utilities" from the category dropdown
    Then the expenses list should show only "utilities" expenses

  Scenario: Viewing All Expense Categories
    Given the user is on the "Expenses" tab
    And the user is viewing the "utilities" category
    When the user selects "All Categories" from the category dropdown
    Then the expenses list should show all categories
