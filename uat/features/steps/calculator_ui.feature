Feature: Calculator web UI

  As a user of the calculator
  I want to perform basic operations through the web interface
  So that I can see the result in my browser

  Scenario: Add two numbers via the UI
    Given I open the calculator page
    When I enter "1" and "2" into the number fields
    And I select the "add" operation
    And I click the calculate button
    Then I should see the result "3.0" on the page
