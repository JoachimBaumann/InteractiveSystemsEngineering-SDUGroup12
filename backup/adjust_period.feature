Feature: Extend Financial Overview Across Multiple Months

  As a user
  I want to extend the time period on the Overview tab across multiple months
  So that I can view combined financial data for a longer duration

  Background:
    Given the user is logged in
    And is on the "Overview" tab

  Scenario: User extends the time period to cover two months
    Given the "From" date is set to "1/8/2023"
    When the user adjusts the "To" date to "30/9/2023"
    Then the system updates to show combined data for August and September
    And the "Current progress" graph reflects data for both months
    And the "Forecast" graph reflects data for both months