Feature: Category-specific Data Visualization

  Scenario: Viewing data for a specific category
    Given the user is on the overview page
    When the user selects "Food" from the "Category" dropdown menu
    Then the system updates the overview to show data for the "Food" category

